#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== [Agent Sync] 로컬 지침/스킬 최신 상태 백업 및 GitHub 푸시 시작 ==="

# 1. 규칙 파일 동기화
echo ">> [1/4] 규칙 파일 동기화 중..."
cp "$HOME/.gemini/config/GEMINI.md" "$SCRIPT_DIR/rules/GEMINI.md" 2>/dev/null || true
cp "$HOME/Documents/AGENTS.md" "$SCRIPT_DIR/rules/AGENTS.md" 2>/dev/null || true
cp "$HOME/Documents/.agents/rules/graphify.md" "$SCRIPT_DIR/rules/graphify.md" 2>/dev/null || true

# 2. 설치된 스킬 목록 JSON 덤프
echo ">> [2/4] 전역 설치 스킬 목록 갱신 중..."
npx skills ls -g --json > "$SCRIPT_DIR/skills/installed-skills.json" 2>/dev/null || true

# 3. Git 변경점 확인 및 커밋/푸시
echo ">> [3/4] Git 변경 상태 확인 중..."
cd "$SCRIPT_DIR"

if [ -n "$(git status --porcelain)" ]; then
  git add .
  COMMIT_MSG="chore(sync): agent rules, skills, and configuration update ($(date '+%Y-%m-%d %H:%M:%S'))"
  git commit -m "$COMMIT_MSG"
  echo ">> [4/4] GitHub 원격 레포지토리(origin main)로 푸시 중..."
  git push origin main
  echo "=== [Agent Sync] 성공적으로 GitHub에 형상 동기화가 완료되었습니다! ==="
else
  echo ">> [4/4] 변경된 파일이 없어 푸시를 건너뜁니다."
  echo "=== [Agent Sync] 이미 최신 상태입니다. ==="
fi
