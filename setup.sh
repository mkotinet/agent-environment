#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================================="
echo "  AI Agent Environment Setup (MacBook & Laptop Portability)"
echo "=========================================================="

# 1. 대상 디렉토리 생성
echo ">> [1/5] 전역 설정 디렉토리 초기화 중..."
mkdir -p "$HOME/.gemini/config"
mkdir -p "$HOME/.gemini/config/skills"
mkdir -p "$HOME/.gemini/antigravity"
mkdir -p "$HOME/.gemini/mcp-servers"
mkdir -p "$HOME/.agents/skills"
mkdir -p "$HOME/Documents/.agents/rules"

# 2. 규칙 파일 복원
echo ">> [2/5] 전역 및 워크스페이스 공통 지침(Rules) 배포 중..."
cp "$SCRIPT_DIR/rules/GEMINI.md" "$HOME/.gemini/config/GEMINI.md"
cp "$SCRIPT_DIR/rules/GEMINI.md" "$HOME/Documents/GEMINI.md" 2>/dev/null || true
cp "$SCRIPT_DIR/rules/AGENTS.md" "$HOME/Documents/AGENTS.md" 2>/dev/null || true
cp "$SCRIPT_DIR/rules/graphify.md" "$HOME/Documents/.agents/rules/graphify.md" 2>/dev/null || true
if [ -f "$SCRIPT_DIR/rules/ANTIGRAVITY.md" ]; then
  cp "$SCRIPT_DIR/rules/ANTIGRAVITY.md" "$HOME/.gemini/config/ANTIGRAVITY.md" 2>/dev/null || true
  cp "$SCRIPT_DIR/rules/ANTIGRAVITY.md" "$HOME/Documents/.agents/rules/ANTIGRAVITY.md" 2>/dev/null || true
fi
if [ -f "$SCRIPT_DIR/skills/SKILLS.md" ]; then
  cp "$SCRIPT_DIR/skills/SKILLS.md" "$HOME/Documents/스킬.md" 2>/dev/null || true
fi

# 3. 자체 제작 커스텀 MCP 서버 배포 및 의존성 설치
echo ">> [3/5] 커스텀 MCP 서버(Portainer, Portainer-DS920) 배포 중..."
if [ -d "$SCRIPT_DIR/mcp/servers/portainer" ]; then
  mkdir -p "$HOME/.gemini/mcp-servers/portainer"
  cp -r "$SCRIPT_DIR/mcp/servers/portainer/"* "$HOME/.gemini/mcp-servers/portainer/"
  if command -v npm &> /dev/null && [ ! -d "$HOME/.gemini/mcp-servers/portainer/node_modules" ]; then
    echo "    Portainer MCP 의존성 패키지 설치 중..."
    (cd "$HOME/.gemini/mcp-servers/portainer" && npm install --omit=dev) || true
  fi
fi

if [ -d "$SCRIPT_DIR/mcp/servers/portainer-ds920" ]; then
  mkdir -p "$HOME/.gemini/mcp-servers/portainer-ds920"
  cp -r "$SCRIPT_DIR/mcp/servers/portainer-ds920/"* "$HOME/.gemini/mcp-servers/portainer-ds920/"
  if command -v npm &> /dev/null && [ ! -d "$HOME/.gemini/mcp-servers/portainer-ds920/node_modules" ]; then
    echo "    Portainer DS920+ MCP 의존성 패키지 설치 중..."
    (cd "$HOME/.gemini/mcp-servers/portainer-ds920" && npm install --omit=dev) || true
  fi
fi

# 3-1. macOS 전용 KakaoTalk MCP 서버 (kakao-mcp) 배포 및 의존성 설정
if [ "$(uname -s)" = "Darwin" ]; then
  echo ">> [3-1/5] macOS 카카오톡 MCP(kakao-mcp) 환경 구성 중..."
  if [ ! -d "$HOME/.gemini/mcp-servers/kakao-mcp" ]; then
    git clone https://github.com/Jaeha0526/kakao-mcp.git "$HOME/.gemini/mcp-servers/kakao-mcp"
  fi
  if command -v uv &> /dev/null; then
    (cd "$HOME/.gemini/mcp-servers/kakao-mcp" && uv sync --quiet) || true
  fi
  if [ ! -f "$HOME/.local/share/kakao-mcp/bin/kakaocli" ] && [ -f "$HOME/.gemini/mcp-servers/kakao-mcp/scripts/install-deps.sh" ]; then
    echo "    kakaocli/kmsg 빌드 중..."
    (cd "$HOME/.gemini/mcp-servers/kakao-mcp" && bash ./scripts/install-deps.sh) || true
  fi
fi

# 4. MCP 서버 설정 템플릿 배포 (동적 홈 디렉토리 치환)
echo ">> [4/5] MCP 서버 설정 검사 및 템플릿 생성 중..."
if [ ! -f "$HOME/.gemini/config/mcp_config.json" ]; then
  sed "s|\${HOME}|$HOME|g" "$SCRIPT_DIR/mcp/mcp_config.template.json" > "$HOME/.gemini/config/mcp_config.json"
  cp "$HOME/.gemini/config/mcp_config.json" "$HOME/.gemini/antigravity/mcp_config.json" 2>/dev/null || true
  echo "    [안내] ~/.gemini/config/mcp_config.json 템플릿이 생성되었습니다."
  echo "    필요한 API 토큰(GitHub PAT, Portainer Key 등)을 입력해 주세요."
else
  echo "    [안내] 기존 ~/.gemini/config/mcp_config.json 파일이 존재하므로 유지합니다."
  cp "$HOME/.gemini/config/mcp_config.json" "$HOME/.gemini/antigravity/mcp_config.json" 2>/dev/null || true
fi

# 5. 전역 에이전트 스킬 일괄 설치
echo ">> [5/5] 필수 에이전트 스킬 설치 중..."
bash "$SCRIPT_DIR/skills/install-all-skills.sh"

echo "=========================================================="
echo "  AI Agent 전역 환경 복원 및 동기화가 성공적으로 완료되었습니다!"
echo "=========================================================="
