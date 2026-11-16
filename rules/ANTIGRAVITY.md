# Google Antigravity 운영 및 커스터마이징 지침 (Antigravity Architecture & Guidelines)

본 문서는 Google Antigravity 환경에서 지침(Rules), 스킬(Skills), MCP 서버(Model Context Protocol), 플러그인(Plugins)의 로딩 계층 구조와 운영 원칙을 정의합니다.

---

## 1. 지침(Rules) 로딩 계층 및 우선순위

Antigravity는 세션 시작 시 다음 순서에 따라 지침을 탐색하고 시스템 프롬프트 및 사용자 규칙(`user_rules`)으로 주입합니다:

1. **전역 시스템 지침 (Global Rules)**:
   - `~/.gemini/config/GEMINI.md`: Antigravity 및 Gemini CLI 전역 운영 표준
   - 주입 형태: `<RULE[user_global]>` 태그로 세션 최우선 적용
2. **워크스페이스 공통 지침 (Workspace Rules)**:
   - `<Workspace>/AGENTS.md`: 다양한 AI 에이전트(Codex, Claude Code, Cursor, Copilot 등) 호환 표준
   - `<Workspace>/GEMINI.md`: 워크스페이스 전용 상세 지침
   - `<Workspace>/.agents/rules/*.md`: 개별 도구 및 모듈별 세부 규칙 (예: `graphify.md`)

---

## 2. 스킬(Skills) 아키텍처 및 로딩 순서

Antigravity는 다계층 스킬 디렉토리를 지원하여 전역, 플러그인, 빌트인 스킬을 유기적으로 결합합니다:

1. **빌트인 스킬 (Built-in Skills)**:
   - 위치: `~/.gemini/antigravity/builtin/skills/`
   - 핵심 스킬:
     - `antigravity-guide`: Antigravity 사용법, 슬래시 커맨드, CLI 가이드
     - `agy-customizations`: 커스터마이징 시스템 및 로딩 우선순위 레퍼런스
     - `automation`: 예약된 백그라운드 자동화 작업 설계
     - `generative_ui`: 리치 인터랙티브 HTML 위젯 렌더링
     - `run-workflow`: 멀티 에이전트 오케스트레이션 워크플로우
     - `swarm` / `swarm_monitor`: 병렬 멀티 에이전트 협업 스웜
     - `plugin`: 플러그인 관리 및 제작 가이드
2. **플러그인 스킬 (Plugin Skills)**:
   - 위치: `~/.gemini/config/plugins/<plugin-id>/skills/`
   - 관리 플러그인:
     - `superpowers`: TDD, 체계적 디버깅, 스펙 주도 개발 14종 스킬
     - `gmail`: 공식 Gmail 관리 CLI 및 스킬
     - `google-workspace-cli`: Google Workspace(드라이브, 시트, 문서, 캘린더 등) 44종 스킬 및 레시피
3. **전역 에이전트 스킬 (Global Skills)**:
   - 위치: `~/.gemini/config/skills/` 및 `~/.agents/skills/`
   - 설치 소스: `addyosmani/agent-skills`, `googlechrome/modern-web-guidance`, `vercel-labs/agent-skills`, `public-apis` 등 50여 개
4. **특화 및 로컬 스킬**:
   - `humanize-korean` / `im-not-ai`: AI 생성 한국어 텍스트의 85개 기계적 패턴 윤문
   - `graphify`: 지식 그래프 기반 AST 탐색 및 영향도 분석

---

## 3. MCP (Model Context Protocol) 연동 구조

Antigravity는 외부 툴 및 인프라 연동을 위해 MCP 서버를 지연 로딩(Lazy loading) 및 즉시 로딩(Eager loading) 방식으로 구동합니다:

* **설정 파일 위치**:
  - 마스터 설정: `~/.gemini/config/mcp_config.json`
  - 런타임 미러: `~/.gemini/antigravity/mcp_config.json`
* **주요 MCP 서버 구성**:
  1. `github`: `@modelcontextprotocol/server-github` (GitHub 레포지토리, 이슈, PR, 파일 동기화)
  2. `portainer`: Synology DS1019+ Portainer REST API 연동 (도커 컨테이너, 스택, 이미지, 볼륨 관리)
  3. `portainer_ds920`: Synology DS920+ Portainer REST API 연동 (HTTPS 자체 서명 인증서 자동 우회)
  4. `graphify`: `graphify-mcp` (지식 그래프 쿼리, 노드 탐색, 최단 경로, God Node 분석)

---

## 4. 핵심 5단계 스킬 순차 적용 파이프라인 (Sequential Skill Application)

모든 코드 개발, 기능 구현, 버그 수정, 아키텍처 분석 시 반드시 아래 5단계를 순차적으로 거칩니다:

```
[1단계: 최신 웹 표준 & 가이던스 우선 검토]
   └── modern-web-guidance-src, modern-web-guidance, baseline-status
        ▼
[2단계: 외부 연동 & 무료 공개 API 카탈로그 우선 탐색]
   └── public-apis, public-api-lookup (1,400+ API 생태계)
        ▼
[3단계: 엔지니어링 표준 & 모범 사례 통합]
   └── vercel-react-best-practices, web-design-guidelines, addyosmani/agent-skills
        ▼
[4단계: 지식 그래프 기반 구조 탐색 및 영향도 분석]
   └── graphify (query_graph, shortest_path, get_node / 작업 후 graphify update .)
        ▼
[5단계: 체계적 프로세스 및 무결성 검증]
   └── superpowers (brainstorming -> writing-plans -> TDD -> verification-before-completion)
```

---

## 5. 멀티 디바이스 환경 동기화 원칙 (Portability & Sync)

1. **상시 동기화**:
   - 지침, 스킬, MCP 설정 변경 시 [agent-environment](https://github.com/mkotinet/agent-environment) 레포지토리에 즉시 커밋 및 푸시합니다.
2. **원클릭 복원**:
   - 신규 머신에서 `bash setup.sh` 단 한 번의 실행으로 동일한 에이전트 환경을 복원합니다.
3. **시크릿 보안 분리**:
   - 실제 토큰과 비밀번호는 `mcp_config.json`에만 보관하고, 저장소에는 `mcp_config.template.json` 및 `.env.example`로 추상화하여 안전하게 관리합니다.
