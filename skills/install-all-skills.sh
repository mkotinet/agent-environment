#!/usr/bin/env bash
set -e

echo "=== [Agent Skills] 전역 스킬 일괄 설치 및 동기화 시작 ==="

# 1. Google Chrome 최신 웹 표준 스킬
echo ">> [1/5] googlechrome/modern-web-guidance 설치 중..."
npx skills add googlechrome/modern-web-guidance -g -y --all

echo ">> [2/5] googlechrome/modern-web-guidance-src 설치 중..."
npx skills add googlechrome/modern-web-guidance-src -g -y --all

# 2. Vercel & Addy Osmani 엔지니어링 스킬
echo ">> [3/5] vercel-labs/agent-skills 설치 중..."
npx skills add vercel-labs/agent-skills -g -y --all

echo ">> [4/5] addyosmani/agent-skills 설치 중..."
npx skills add addyosmani/agent-skills -g -y --all

# 3. Public APIs 스킬
echo ">> [5/5] public-apis 스킬 설치 중..."
npx skills add w020316/cautious-broccoli --skill public-apis -g -y
npx skills add nyldn/public-apis-skill -g -y --all

echo "=== [Agent Skills] 전역 스킬 설치 완료! ==="
npx skills ls -g
