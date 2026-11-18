#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "  [Agent Skills] 전역 에이전트 스킬 일괄 설치 및 동기화"
echo "=========================================================="

if ! command -v npx &> /dev/null; then
  echo "[오류] npx 명령어를 찾을 수 없습니다. Node.js를 먼저 설치해 주세요."
  exit 1
fi

# 1. Karpathy Guidelines (안드레이 카파시 코딩 행동 강령)
echo ">> [1/8] Karpathy Guidelines (안드레이 카파시 코딩 행동 강령) 설치 중..."
npx skills add szkocot/andrej-karpathy-skills --skill karpathy-guidelines -g -y || true

# 2. AgentMemory (지속 기억 및 메모리 규율 스킬 17종)
echo ">> [2/8] AgentMemory (장기 지속 기억 및 메모리 규율 17종) 설치 중..."
npx skills add rohitg00/agentmemory -g -y --all || true

# 3. Google Chrome 최신 웹 표준 및 가이던스 스킬
echo ">> [3/8] Google Chrome 최신 웹 표준 스킬 설치 중..."
npx skills add googlechrome/modern-web-guidance -g -y --all || true
npx skills add googlechrome/modern-web-guidance-src -g -y --all || true

# 4. Vercel 프레임워크 & UI 스킬
echo ">> [4/8] Vercel 엔지니어링 및 UI 스킬 설치 중..."
npx skills add vercel-labs/skills -g -y --all || true
npx skills add vercel-labs/agent-skills -g -y --all || true

# 5. Addy Osmani 시니어 엔지니어링 스킬 (25종)
echo ">> [5/8] Addy Osmani 엔지니어링 스킬 설치 중..."
npx skills add addyosmani/agent-skills -g -y --all || true

# 6. Public APIs (1,400+ 무료 공개 API 카탈로그)
echo ">> [6/8] Public APIs 카탈로그 스킬 설치 중..."
npx skills add w020316/cautious-broccoli --skill public-apis -g -y || true
npx skills add nyldn/public-apis-skill -g -y --all || true

# 7. Korean AI Humanizer (im-not-ai / humanize-korean)
echo ">> [7/8] 한국어 AI 티 제거기 (im-not-ai) 점검 중..."
if [ ! -d "$HOME/.gemini/im-not-ai" ]; then
  echo "    epoko77-ai/im-not-ai 복제 및 설치 진행..."
  git clone https://github.com/epoko77-ai/im-not-ai.git "$HOME/.gemini/im-not-ai" 2>/dev/null || true
  if [ -f "$HOME/.gemini/im-not-ai/install.sh" ]; then
    bash "$HOME/.gemini/im-not-ai/install.sh" || true
  fi
else
  echo "    이미 ~/.gemini/im-not-ai 가 존재합니다."
fi

# 8. Graphify 지식 그래프 도구
echo ">> [8/8] Graphify 지식 그래프 도구 점검 중..."
if ! command -v graphify &> /dev/null; then
  if command -v uv &> /dev/null; then
    echo "    uv tool install graphifyy 실행..."
    uv tool install graphifyy || true
  elif command -v pip3 &> /dev/null; then
    echo "    pip3 install graphifyy 실행..."
    pip3 install graphifyy || true
  fi
fi

echo "=========================================================="
echo "  [Agent Skills] 전역 스킬 설치 완료! 현재 설치 목록:"
echo "=========================================================="
npx skills ls -g
