#!/usr/bin/env node
/**
 * Portainer DS920+ MCP Server
 * Connects to Portainer REST API on Synology DS920+ NAS (https://djms1.iptime.org:9101).
 * Supports API Token (PORTAINER_API_KEY) or Username/Password (PORTAINER_USERNAME, PORTAINER_PASSWORD).
 */

process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import fs from "fs";
import path from "path";
import os from "os";

function getConfig() {
  let url = process.env.PORTAINER_URL || "";
  let apiKey = process.env.PORTAINER_API_KEY || process.env.PORTAINER_PAT || "";
  let username = process.env.PORTAINER_USERNAME || "";
  let password = process.env.PORTAINER_PASSWORD || "";

  try {
    const configPath = path.join(os.homedir(), ".gemini", "config", "mcp_config.json");
    if (fs.existsSync(configPath)) {
      const config = JSON.parse(fs.readFileSync(configPath, "utf-8"));
      const env = config?.mcpServers?.portainer_ds920?.env || config?.mcpServers?.["portainer-ds920"]?.env || {};
      if (!url && env.PORTAINER_URL) url = env.PORTAINER_URL;
      if (!apiKey && env.PORTAINER_API_KEY) apiKey = env.PORTAINER_API_KEY;
      if (!apiKey && env.PORTAINER_PAT) apiKey = env.PORTAINER_PAT;
      if (!username && env.PORTAINER_USERNAME) username = env.PORTAINER_USERNAME;
      if (!password && env.PORTAINER_PASSWORD) password = env.PORTAINER_PASSWORD;
    }
  } catch (e) {}

  if (!url) url = "https://djms1.iptime.org:9101";
  return {
    url: url.replace(/\/+$/, ""),
    apiKey,
    username,
    password,
  };
}

let cachedJwt = null;

async function getAuthHeaders() {
  const { apiKey, username, password, url } = getConfig();

  if (apiKey) {
    return { "X-API-Key": apiKey };
  }

  if (username && password) {
    if (cachedJwt) {
      return { Authorization: `Bearer ${cachedJwt}` };
    }
    const authRes = await fetch(`${url}/api/auth`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        Username: username,
        Password: password,
      }),
    });
    if (!authRes.ok) {
      const errText = await authRes.text();
      throw new Error(`Portainer login failed (${authRes.status}): ${errText}`);
    }
    const data = await authRes.json();
    cachedJwt = data.jwt;
    return { Authorization: `Bearer ${cachedJwt}` };
  }

  throw new Error(
    "Missing Portainer credentials! Please set PORTAINER_API_KEY (Access Token) or PORTAINER_USERNAME / PORTAINER_PASSWORD in mcp_config.json."
  );
}

async function api(apiPath, options = {}) {
  const { url, apiKey, username } = getConfig();
  let authHeaders = await getAuthHeaders();
  let fullUrl = `${url}/api${apiPath}`;

  let res = await fetch(fullUrl, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...authHeaders,
      ...(options.headers || {}),
    },
  });

  // If JWT expired (401), try re-authenticating once
  if (res.status === 401 && !apiKey && username && cachedJwt) {
    cachedJwt = null;
    authHeaders = await getAuthHeaders();
    res = await fetch(fullUrl, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...authHeaders,
        ...(options.headers || {}),
      },
    });
  }

  const text = await res.text();
  if (!res.ok) {
    throw new Error(`Portainer API error ${res.status}: ${text}`);
  }

  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

// Helper to determine default endpointId
async function getDefaultEndpointId(providedId) {
  if (providedId !== undefined && providedId !== null) {
    return providedId;
  }
  try {
    const endpoints = await api("/endpoints");
    if (Array.isArray(endpoints) && endpoints.length > 0) {
      return endpoints[0].Id;
    }
  } catch {
    // fallback
  }
  return 1;
}

const server = new McpServer({
  name: "portainer-ds920",
  version: "1.0.0",
});

// ── System & Environments ───────────────────────────────────────────────────

server.tool("get_status", "Check Portainer server status and version", {}, async () => {
  const { url } = getConfig();
  try {
    const res = await fetch(`${url}/api/status`);
    const data = await res.json();
    return {
      content: [
        {
          type: "text",
          text: `Portainer Status: Online\nVersion: ${data.Version || "Unknown"}\nInstanceID: ${data.InstanceID || "Unknown"}\nTarget URL: ${url}`,
        },
      ],
    };
  } catch (err) {
    return {
      isError: true,
      content: [{ type: "text", text: `Failed to connect to Portainer at ${url}: ${err.message}` }],
    };
  }
});

server.tool("list_environments", "List all Portainer environments (endpoints / Docker hosts)", {}, async () => {
  try {
    const envs = await api("/endpoints");
    const formatted = envs.map((e) =>
      `ID: ${e.Id} | Name: ${e.Name} | Type: ${e.Type} | Status: ${e.Status === 1 ? "up" : "down"} | URL: ${e.URL}`
    ).join("\n");
    return { content: [{ type: "text", text: formatted || "No environments found" }] };
  } catch (err) {
    return { isError: true, content: [{ type: "text", text: err.message }] };
  }
});

// ── Stacks (Apps / Docker Compose) ──────────────────────────────────────────

server.tool("list_stacks", "List all deployed stacks (applications) in Portainer", {}, async () => {
  try {
    const stacks = await api("/stacks");
    const formatted = stacks.map((s) =>
      `ID: ${s.Id} | Name: ${s.Name} | Status: ${s.Status === 1 ? "active" : "inactive"} | EndpointId: ${s.EndpointId}`
    ).join("\n");
    return { content: [{ type: "text", text: formatted || "No stacks found" }] };
  } catch (err) {
    return { isError: true, content: [{ type: "text", text: err.message }] };
  }
});

server.tool(
  "inspect_stack",
  "Get detailed metadata about a specific stack",
  { stackId: z.number().describe("Stack ID") },
  async ({ stackId }) => {
    try {
      const stack = await api(`/stacks/${stackId}`);
      return { content: [{ type: "text", text: JSON.stringify(stack, null, 2) }] };
    } catch (err) {
      return { isError: true, content: [{ type: "text", text: err.message }] };
    }
  }
);

server.tool(
  "get_stack_file",
  "Get the docker-compose file content of a stack",
  { stackId: z.number().describe("Stack ID") },
  async ({ stackId }) => {
    try {
      const data = await api(`/stacks/${stackId}/file`);
      return { content: [{ type: "text", text: data.StackFileContent || JSON.stringify(data) }] };
    } catch (err) {
      return { isError: true, content: [{ type: "text", text: err.message }] };
    }
  }
);

server.tool(
  "deploy_stack",
  "Deploy a new Docker Compose stack (app) in Portainer",
  {
    name: z.string().describe("Name of the stack/application"),
    stackFileContent: z.string().describe("docker-compose.yml YAML file content"),
    endpointId: z.number().optional().describe("Portainer environment ID (defaults to primary endpoint, usually 1)"),
    env: z
      .array(
        z.object({
          name: z.string(),
          value: z.string(),
        })
      )
      .optional()
      .describe("Optional environment variables for the stack"),
  },
  async ({ name, stackFileContent, endpointId, env = [] }) => {
    try {
      const targetEndpointId = await getDefaultEndpointId(endpointId);
      const res = await api(`/stacks/create/standalone/string?endpointId=${targetEndpointId}`, {
        method: "POST",
        body: JSON.stringify({
          name,
          stackFileContent,
          env,
        }),
      });
      return {
        content: [
          {
            type: "text",
            text: `Successfully deployed stack '${name}' (ID: ${res.Id || "N/A"}) on endpoint ${targetEndpointId}!\n${JSON.stringify(res, null, 2)}`,
          },
        ],
      };
    } catch (err) {
      return { isError: true, content: [{ type: "text", text: `Failed to deploy stack: ${err.message}` }] };
    }
  }
);

server.tool(
  "update_stack",
  "Update an existing stack's docker-compose content and redeploy",
  {
    stackId: z.number().describe("Stack ID to update"),
    stackFileContent: z.string().describe("Updated docker-compose.yml content"),
    endpointId: z.number().optional().describe("Portainer environment ID (defaults to primary endpoint, usually 1)"),
    env: z
      .array(
        z.object({
          name: z.string(),
          value: z.string(),
        })
      )
      .optional()
      .describe("Optional environment variables"),
    prune: z.boolean().optional().describe("Whether to prune unused containers/services (default: true)"),
  },
  async ({ stackId, stackFileContent, endpointId, env = [], prune = true }) => {
    try {
      const targetEndpointId = await getDefaultEndpointId(endpointId);
      const res = await api(`/stacks/${stackId}?endpointId=${targetEndpointId}`, {
        method: "PUT",
        body: JSON.stringify({
          stackFileContent,
          env,
          prune,
        }),
      });
      return {
        content: [
          {
            type: "text",
            text: `Successfully updated stack ${stackId}!\n${JSON.stringify(res, null, 2)}`,
          },
        ],
      };
    } catch (err) {
      return { isError: true, content: [{ type: "text", text: `Failed to update stack: ${err.message}` }] };
    }
  }
);

server.tool(
  "delete_stack",
  "Delete a stack from Portainer",
  {
    stackId: z.number().describe("Stack ID"),
    endpointId: z.number().optional().describe("Portainer environment ID (defaults to primary endpoint, usually 1)"),
  },
  async ({ stackId, endpointId }) => {
    try {
      const targetEndpointId = await getDefaultEndpointId(endpointId);
      await api(`/stacks/${stackId}?endpointId=${targetEndpointId}`, { method: "DELETE" });
      return { content: [{ type: "text", text: `Stack ${stackId} deleted successfully.` }] };
    } catch (err) {
      return { isError: true, content: [{ type: "text", text: `Failed to delete stack: ${err.message}` }] };
    }
  }
);

// ── Containers ──────────────────────────────────────────────────────────────

server.tool(
  "list_containers",
  "List containers in a Portainer environment",
  {
    endpointId: z.number().optional().describe("Portainer environment ID (default 1)"),
    all: z.boolean().optional().describe("Include stopped containers (default: true)"),
  },
  async ({ endpointId, all = true }) => {
    try {
      const targetEndpointId = await getDefaultEndpointId(endpointId);
      const containers = await api(`/endpoints/${targetEndpointId}/docker/containers/json?all=${all}`);
      const formatted = containers.map((c) =>
        `ID: ${c.Id.slice(0, 12)} | Names: ${(c.Names || []).join(", ")} | Image: ${c.Image} | State: ${c.State} | Status: ${c.Status}`
      ).join("\n");
      return { content: [{ type: "text", text: formatted || "No containers found" }] };
    } catch (err) {
      return { isError: true, content: [{ type: "text", text: err.message }] };
    }
  }
);

server.tool(
  "inspect_container",
  "Get detailed information about a container",
  {
    containerId: z.string().describe("Container ID or name"),
    endpointId: z.number().optional().describe("Portainer environment ID (default 1)"),
  },
  async ({ containerId, endpointId }) => {
    try {
      const targetEndpointId = await getDefaultEndpointId(endpointId);
      const data = await api(`/endpoints/${targetEndpointId}/docker/containers/${containerId}/json`);
      return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
    } catch (err) {
      return { isError: true, content: [{ type: "text", text: err.message }] };
    }
  }
);

server.tool(
  "get_container_logs",
  "Fetch logs from a container",
  {
    containerId: z.string().describe("Container ID or name"),
    endpointId: z.number().optional().describe("Portainer environment ID (default 1)"),
    tail: z.number().optional().describe("Number of lines from the end (default 100)"),
    timestamps: z.boolean().optional().describe("Include timestamps (default false)"),
  },
  async ({ containerId, endpointId, tail = 100, timestamps = false }) => {
    try {
      const targetEndpointId = await getDefaultEndpointId(endpointId);
      const params = new URLSearchParams({
        stdout: "1",
        stderr: "1",
        tail: String(tail),
        timestamps: String(timestamps),
      });
      const logs = await api(`/endpoints/${targetEndpointId}/docker/containers/${containerId}/logs?${params}`);
      return { content: [{ type: "text", text: String(logs) || "No logs returned." }] };
    } catch (err) {
      return { isError: true, content: [{ type: "text", text: err.message }] };
    }
  }
);

server.tool(
  "start_container",
  "Start a stopped container",
  {
    containerId: z.string().describe("Container ID or name"),
    endpointId: z.number().optional().describe("Portainer environment ID (default 1)"),
  },
  async ({ containerId, endpointId }) => {
    try {
      const targetEndpointId = await getDefaultEndpointId(endpointId);
      await api(`/endpoints/${targetEndpointId}/docker/containers/${containerId}/start`, { method: "POST" });
      return { content: [{ type: "text", text: `Container ${containerId} started successfully.` }] };
    } catch (err) {
      return { isError: true, content: [{ type: "text", text: err.message }] };
    }
  }
);

server.tool(
  "stop_container",
  "Stop a running container",
  {
    containerId: z.string().describe("Container ID or name"),
    endpointId: z.number().optional().describe("Portainer environment ID (default 1)"),
  },
  async ({ containerId, endpointId }) => {
    try {
      const targetEndpointId = await getDefaultEndpointId(endpointId);
      await api(`/endpoints/${targetEndpointId}/docker/containers/${containerId}/stop`, { method: "POST" });
      return { content: [{ type: "text", text: `Container ${containerId} stopped successfully.` }] };
    } catch (err) {
      return { isError: true, content: [{ type: "text", text: err.message }] };
    }
  }
);

server.tool(
  "restart_container",
  "Restart a container",
  {
    containerId: z.string().describe("Container ID or name"),
    endpointId: z.number().optional().describe("Portainer environment ID (default 1)"),
  },
  async ({ containerId, endpointId }) => {
    try {
      const targetEndpointId = await getDefaultEndpointId(endpointId);
      await api(`/endpoints/${targetEndpointId}/docker/containers/${containerId}/restart`, { method: "POST" });
      return { content: [{ type: "text", text: `Container ${containerId} restarted successfully.` }] };
    } catch (err) {
      return { isError: true, content: [{ type: "text", text: err.message }] };
    }
  }
);

server.tool(
  "delete_container",
  "Remove a container from Docker",
  {
    containerId: z.string().describe("Container ID or name"),
    endpointId: z.number().optional().describe("Portainer environment ID (default 1)"),
    force: z.boolean().optional().describe("Force removal even if running (default true)"),
  },
  async ({ containerId, endpointId, force = true }) => {
    try {
      const targetEndpointId = await getDefaultEndpointId(endpointId);
      await api(`/endpoints/${targetEndpointId}/docker/containers/${containerId}?force=${force}`, { method: "DELETE" });
      return { content: [{ type: "text", text: `Container ${containerId} removed successfully.` }] };
    } catch (err) {
      return { isError: true, content: [{ type: "text", text: err.message }] };
    }
  }
);

// ── Images, Networks & Volumes ──────────────────────────────────────────────

server.tool(
  "pull_image",
  "Pull a Docker image from a registry",
  {
    image: z.string().describe("Docker image name (e.g. nginx:latest, node:20-alpine)"),
    endpointId: z.number().optional().describe("Portainer environment ID (default 1)"),
  },
  async ({ image, endpointId }) => {
    try {
      const targetEndpointId = await getDefaultEndpointId(endpointId);
      const res = await api(`/endpoints/${targetEndpointId}/docker/images/create?fromImage=${encodeURIComponent(image)}`, {
        method: "POST",
      });
      return { content: [{ type: "text", text: `Successfully requested pull for image '${image}'. Output:\n${typeof res === "string" ? res : JSON.stringify(res)}` }] };
    } catch (err) {
      return { isError: true, content: [{ type: "text", text: `Failed to pull image: ${err.message}` }] };
    }
  }
);

server.tool(
  "list_images",
  "List Docker images in an environment",
  { endpointId: z.number().optional().describe("Portainer environment ID (default 1)") },
  async ({ endpointId }) => {
    try {
      const targetEndpointId = await getDefaultEndpointId(endpointId);
      const images = await api(`/endpoints/${targetEndpointId}/docker/images/json`);
      const formatted = images.map((img) =>
        `ID: ${(img.Id || "").slice(7, 19)} | Tags: ${(img.RepoTags || ["<none>"]).join(", ")} | Size: ${(
          (img.Size || 0) /
          1024 /
          1024
        ).toFixed(1)}MB`
      ).join("\n");
      return { content: [{ type: "text", text: formatted || "No images found" }] };
    } catch (err) {
      return { isError: true, content: [{ type: "text", text: err.message }] };
    }
  }
);

server.tool(
  "list_networks",
  "List Docker networks in an environment",
  { endpointId: z.number().optional().describe("Portainer environment ID (default 1)") },
  async ({ endpointId }) => {
    try {
      const targetEndpointId = await getDefaultEndpointId(endpointId);
      const networks = await api(`/endpoints/${targetEndpointId}/docker/networks`);
      const items = Array.isArray(networks) ? networks : Object.values(networks);
      const formatted = items.map((n) =>
        `ID: ${(n.Id || "").slice(0, 12)} | Name: ${n.Name} | Driver: ${n.Driver} | Scope: ${n.Scope}`
      ).join("\n");
      return { content: [{ type: "text", text: formatted || "No networks found" }] };
    } catch (err) {
      return { isError: true, content: [{ type: "text", text: err.message }] };
    }
  }
);

server.tool(
  "list_volumes",
  "List Docker volumes in an environment",
  { endpointId: z.number().optional().describe("Portainer environment ID (default 1)") },
  async ({ endpointId }) => {
    try {
      const targetEndpointId = await getDefaultEndpointId(endpointId);
      const data = await api(`/endpoints/${targetEndpointId}/docker/volumes`);
      const vols = data.Volumes || [];
      const formatted = vols.map((v) =>
        `Name: ${v.Name} | Driver: ${v.Driver} | Mountpoint: ${v.Mountpoint}`
      ).join("\n");
      return { content: [{ type: "text", text: formatted || "No volumes found" }] };
    } catch (err) {
      return { isError: true, content: [{ type: "text", text: err.message }] };
    }
  }
);

// ── Start MCP Stdio Transport ───────────────────────────────────────────────

const transport = new StdioServerTransport();
await server.connect(transport);
