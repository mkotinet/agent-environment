# MCP (Model Context Protocol) 서버 구성 및 연동 가이드

본 디렉토리는 AI 에이전트(Google Antigravity, Claude Code, Codex 등)가 외부 인프라 및 API와 소통할 수 있도록 연결하는 MCP 서버 설정과 자체 개발된 커스텀 MCP 서버 소스코드를 관리합니다.

---

## 1. 연동 중인 MCP 서버 목록

| MCP 서버명 | 용도 및 기능 | 구동 방식 | 주요 도구 (Tools) |
| :--- | :--- | :--- | :--- |
| **`github`** | GitHub 레포지토리, 브랜치, 커밋, PR, 이슈 관리 | `@modelcontextprotocol/server-github` (npx) | `create_or_update_file`, `search_repositories`, `list_commits`, `create_pull_request`, `list_issues` 등 |
| **`portainer`** | Synology DS1019+ 도커 컨테이너 및 스택 운영 | 로컬 커스텀 Node.js 서버 (`servers/portainer`) | `list_containers`, `inspect_container`, `start_container`, `stop_container`, `restart_container`, `list_stacks`, `deploy_stack`, `get_container_logs` |
| **`portainer_ds920`** | Synology DS920+ 도커 컨테이너 및 스택 운영 (HTTPS) | 로컬 커스텀 Node.js 서버 (`servers/portainer-ds920`) | `list_containers`, `inspect_container`, `start_container`, `stop_container`, `restart_container`, `list_stacks`, `deploy_stack`, `get_container_logs` |
| **`graphify`** | 지식 그래프(Knowledge Graph) AST 기반 탐색 | `graphify-mcp` 바이너리 | `query_graph`, `get_node`, `get_neighbors`, `shortest_path`, `god_nodes`, `graph_stats` |

---

## 2. 자체 제작 커스텀 MCP 서버 구조 (`servers/`)

- **`servers/portainer/`**:
  - Synology DS1019+ Portainer REST API (`http://djms1.iptime.org:9000`)에 직접 통신합니다.
  - API 토큰(`PORTAINER_API_KEY`) 또는 계정 인증(`PORTAINER_USERNAME`, `PORTAINER_PASSWORD`)을 지원합니다.
- **`servers/portainer-ds920/`**:
  - Synology DS920+ Portainer REST API (`https://djms1.iptime.org:9101`)에 직접 통신합니다.
  - Synology 자체 서명 SSL 인증서 오류 방지를 위해 `NODE_TLS_REJECT_UNAUTHORIZED = "0"`을 내장하고 있습니다.

---

## 3. 원클릭 자동 설치 및 배포

`setup.sh`를 실행하면 자동으로:
1. `servers/portainer` 및 `servers/portainer-ds920` 소스가 `~/.gemini/mcp-servers/`로 복사됩니다.
2. 각 서버 디렉토리에서 `npm install --omit=dev`가 실행되어 의존성이 자동 설치됩니다.
3. `mcp_config.template.json`의 `${HOME}` 경로가 현재 사용자의 실제 홈 디렉토리로 자동 치환되어 `~/.gemini/config/mcp_config.json` 및 `~/.gemini/antigravity/mcp_config.json`으로 배포됩니다.

---

## 4. 인증 정보 설정

`~/.gemini/config/mcp_config.json`을 열어 아래 항목을 입력합니다:

- `GITHUB_PERSONAL_ACCESS_TOKEN`: GitHub Personal Access Token (PAT)
- `PORTAINER_API_KEY`: DS1019+ Portainer Access Token
- `PORTAINER_DS920_API_KEY` (또는 패스워드): DS920+ Portainer 인증 정보
