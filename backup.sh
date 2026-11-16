#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== [Agent Sync] 로컬 지침/스킬/MCP 최신 상태 백업 및 GitHub 푸시 시작 ==="

# 1. 규칙 및 지침 파일 동기화
echo ">> [1/5] 규칙 및 지침 파일 동기화 중..."
cp "$HOME/Documents/GEMINI.md" "$SCRIPT_DIR/rules/GEMINI.md" 2>/dev/null || true
cp "$HOME/Documents/GEMINI.md" "$HOME/.gemini/config/GEMINI.md" 2>/dev/null || true
cp "$HOME/Documents/AGENTS.md" "$SCRIPT_DIR/rules/AGENTS.md" 2>/dev/null || true
cp "$HOME/Documents/.agents/rules/graphify.md" "$SCRIPT_DIR/rules/graphify.md" 2>/dev/null || true
if [ -f "$HOME/Documents/스킬.md" ]; then
  cp "$HOME/Documents/스킬.md" "$SCRIPT_DIR/skills/SKILLS.md" 2>/dev/null || true
fi

# 2. 커스텀 MCP 서버 소스 백업
echo ">> [2/5] 커스텀 MCP 서버 소스코드 동기화 중..."
if [ -d "$HOME/.gemini/mcp-servers/portainer" ]; then
  mkdir -p "$SCRIPT_DIR/mcp/servers/portainer"
  cp "$HOME/.gemini/mcp-servers/portainer/index.js" "$SCRIPT_DIR/mcp/servers/portainer/" 2>/dev/null || true
  cp "$HOME/.gemini/mcp-servers/portainer/package.json" "$SCRIPT_DIR/mcp/servers/portainer/" 2>/dev/null || true
  cp "$HOME/.gemini/mcp-servers/portainer/package-lock.json" "$SCRIPT_DIR/mcp/servers/portainer/" 2>/dev/null || true
fi

if [ -d "$HOME/.gemini/mcp-servers/portainer-ds920" ]; then
  mkdir -p "$SCRIPT_DIR/mcp/servers/portainer-ds920"
  cp "$HOME/.gemini/mcp-servers/portainer-ds920/index.js" "$SCRIPT_DIR/mcp/servers/portainer-ds920/" 2>/dev/null || true
  cp "$HOME/.gemini/mcp-servers/portainer-ds920/package.json" "$SCRIPT_DIR/mcp/servers/portainer-ds920/" 2>/dev/null || true
  cp "$HOME/.gemini/mcp-servers/portainer-ds920/package-lock.json" "$SCRIPT_DIR/mcp/servers/portainer-ds920/" 2>/dev/null || true
fi

# 3. 설치된 스킬 목록 JSON 덤프
echo ">> [3/5] 전역 설치 스킬 목록 갱신 중..."
npx skills ls -g --json > "$SCRIPT_DIR/skills/installed-skills.json" 2>/dev/null || true

# 4. Git 변경점 확인 및 커밋/푸시
echo ">> [4/5] Git 변경 상태 확인 중..."
cd "$SCRIPT_DIR"

if [ -n "$(git status --porcelain)" ]; then
  git add .
  COMMIT_MSG="chore(sync): update agent rules, comprehensive skills guide, and mcp servers ($(date '+%Y-%m-%d %H:%M:%S'))"
  git commit -m "$COMMIT_MSG"
  echo ">> [5/5] GitHub 원격 레포지토리(origin main)로 푸시 중..."
  git push origin main
  echo "=== [Agent Sync] 성공적으로 GitHub에 형상 동기화가 완료되었습니다! ==="
else
  echo ">> [5/5] 변경된 파일이 없어 푸시를 건너뜁니다."
  echo "=== [Agent Sync] 이미 최신 상태입니다. ==="
fi
