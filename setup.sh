#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================================="
echo "  AI Agent Environment Setup (MacBook & Laptop Portability)"
echo "=========================================================="

# 1. 대상 디렉토리 생성
echo ">> [1/4] 전역 설정 디렉토리 초기화 중..."
mkdir -p "$HOME/.gemini/config"
mkdir -p "$HOME/.gemini/config/skills"
mkdir -p "$HOME/.agents/skills"
mkdir -p "$HOME/Documents/.agents/rules"

# 2. 규칙 파일 복원
echo ">> [2/4] 전역 및 워크스페이스 공통 지침(Rules) 배포 중..."
cp "$SCRIPT_DIR/rules/GEMINI.md" "$HOME/.gemini/config/GEMINI.md"
cp "$SCRIPT_DIR/rules/AGENTS.md" "$HOME/Documents/AGENTS.md" 2>/dev/null || true
cp "$SCRIPT_DIR/rules/GEMINI.md" "$HOME/Documents/GEMINI.md" 2>/dev/null || true
cp "$SCRIPT_DIR/rules/graphify.md" "$HOME/Documents/.agents/rules/graphify.md" 2>/dev/null || true

# 3. 전역 에이전트 스킬 일괄 설치
echo ">> [3/4] 필수 에이전트 스킬 설치 중..."
bash "$SCRIPT_DIR/skills/install-all-skills.sh"

# 4. MCP 서버 설정 템플릿 배포
echo ">> [4/4] MCP 서버 설정 검사 중..."
if [ ! -f "$HOME/.gemini/config/mcp_config.json" ]; then
  cp "$SCRIPT_DIR/mcp/mcp_config.template.json" "$HOME/.gemini/config/mcp_config.json"
  echo "    [안내] ~/.gemini/config/mcp_config.json 템플릿이 생성되었습니다."
  echo "    필요한 API 토큰(GitHub PAT, Portainer Key 등)을 입력해 주세요."
else
  echo "    [안내] 기존 ~/.gemini/config/mcp_config.json 파일이 존재하므로 유지합니다."
fi

echo "=========================================================="
echo "  AI Agent 전역 환경 복원 및 동기화가 성공적으로 완료되었습니다!"
echo "=========================================================="
