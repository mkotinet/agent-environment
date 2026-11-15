# Agent Environment Sync (AI Agent 통합 형상 동기화 허브)

여러 대의 맥북(MacBook), 노트북, 데스크톱 간에 **동일한 AI Agent 개발 지침(Rules), 에이전트 스킬(Skills), MCP 서버 설정**을 실시간으로 공유하고 원클릭으로 완벽히 복원할 수 있도록 지원하는 공식 중간매개체 레포지토리입니다.

---

## 🎯 주요 동기화 대상

1. **에이전트 지침 (Rules)**:
   - `rules/GEMINI.md`: Antigravity / Gemini CLI 전역 운영 및 개발 지침
   - `rules/AGENTS.md`: Universal 에이전트(Codex, Claude Code, Cursor, Copilot 등) 공통 지침
   - `rules/graphify.md`: 지식 그래프(Knowledge Graph) 우선 탐색 원칙
2. **에이전트 스킬 (Skills)**:
   - `modern-web-guidance` & `modern-web-guidance-src` (Google Chrome 최신 웹 표준)
   - `public-apis` & `public-api-lookup` (1,400+ 무료 공개 API 카탈로그)
   - `vercel-labs/agent-skills` (React/Next.js 성능 최적화, 웹 디자인 가이드)
   - `addyosmani/agent-skills` (Addy Osmani의 프론트엔드/테스트/보안/성능 25종 스킬)
   - `graphify`, `super-powers`, `humanize-korean` 등
3. **MCP 서버 연동 (MCP Servers)**:
   - GitHub, Portainer, Graphify 등 MCP 구성 템플릿 (`mcp/mcp_config.template.json`)

---

## 🚀 다른 맥북 / 노트북에서 원클릭 환경 복원 (Setup)

새로운 머신에서 아래 명령어 단 한 줄을 실행하면 즉시 현재 환경과 100% 동일하게 모든 지침과 스킬이 자동 설치 및 세팅됩니다.

```bash
git clone https://github.com/mkotinet/agent-environment.git
cd agent-environment
bash setup.sh
```

> **참고**: `setup.sh` 실행 시:
> 1. `~/.gemini/config/GEMINI.md` 및 `~/Documents/AGENTS.md`에 지침이 자동 배포됩니다.
> 2. `npx skills`를 통해 50여 개 전역 스킬이 자동 설치됩니다.
> 3. `~/.gemini/config/mcp_config.json` 템플릿이 배치됩니다. (필요한 개인 토큰 입력)

---

## 🔄 현재 기기에서 변경사항 발생 시 자동 백업 & 푸시 (Backup)

현재 작업 머신에서 새로운 지침을 추가하거나, 신규 스킬을 설치하거나, 설정을 변경한 경우 아래 스크립트를 실행하면 즉시 이 레포지토리에 반영 및 GitHub 푸시가 완료됩니다.

```bash
cd /Users/kotinet/Documents/GIT/agent-environment
bash backup.sh
```

---

## 📋 핵심 운영 지침 (Sequential Skill Application)

코드 개발, 수정, 점검, 리팩토링, 기능 구현 및 아키텍처 분석 시 5단계 파이프라인을 **순차적으로** 적용합니다:

1. **1단계: `modern-web-guidance-src` (최신 웹 표준 & 가이던스 우선 검토)**
2. **2단계: `public-apis` (외부 연동 및 무료 공개 API 생태계 우선 탐색)**
3. **3단계: `agent-skills` (엔지니어링 표준 및 모범 사례 통합)**
4. **4단계: `graphify` (지식 그래프 기반 탐색 및 영향도 분석)**
5. **5단계: `super-powers` (체계적 프로세스 및 무결성 검증)**
