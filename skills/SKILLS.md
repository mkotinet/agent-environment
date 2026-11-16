# Google Antigravity & AI Agent 전역 스킬 종합 가이드 (`SKILLS.md`)

본 문서는 Google Antigravity를 비롯한 AI 에이전트 환경에 설치되고 운영 중인 **전역 스킬(Global Skills), 플러그인 스킬(Plugin Skills), 빌트인 스킬(Built-in Skills)**의 전체 카탈로그와 5단계 순차 적용 파이프라인 가이드입니다.

---

## 🚀 핵심 파이프라인: 5단계 스킬 순차 적용 원칙 (Sequential Skill Application)

모든 코드 개발, 기능 구현, 버그 수정, 아키텍처 분석 시 최고 수준의 품질과 최신 웹 표준을 위해 다음 5가지 단계를 **순차적으로** 적용합니다:

```
[1단계: 최신 웹 표준 & 가이던스 우선 검토]
   └── modern-web-guidance-src, modern-web-guidance, baseline-status
        ▼
[2단계: 외부 연동 & 무료 공개 API 생태계 우선 탐색]
   └── public-apis, public-api-lookup (1,400+ API 카탈로그)
        ▼
[3단계: 엔지니어링 표준 & 모범 사례 통합]
   └── vercel-react-best-practices, web-design-guidelines, addyosmani/agent-skills
        ▼
[4단계: 지식 그래프 기반 구조 탐색 및 영향도 분석]
   └── graphify (query_graph, shortest_path, get_node / 작업 후 graphify update .)
        ▼
[5단계: 체계적 프로세스 및 무결성 검증]
   └── superpowers (brainstorming ➔ writing-plans ➔ TDD ➔ verification-before-completion)
```

---

## 📚 스킬 카테고리별 상세 구성

### 1. Google Chrome 최신 웹 표준 및 가이던스 (15종)
*출처: `googlechrome/modern-web-guidance`, `googlechrome/modern-web-guidance-src`*

| 스킬명 | 설명 및 주요 트리거 |
| :--- | :--- |
| **`modern-web-guidance`** | HTML/CSS/클라이언트 JS 작성 전 필수 검토. Popover, Dialog, View Transitions, Container Queries, Scroll-driven Animation, Baseline 호환성 최신 모범 사례 강제. |
| **`baseline-status`** | 웹 기능의 브라우저 지원 현황 및 Baseline(Widely / Newly available) 상태 실시간 확인. |
| **`browser-testing-with-devtools`**| Chrome DevTools MCP를 활용한 실제 브라우저 DOM 검사, 콘솔 에러, 네트워크 트래픽 분석. |
| **`chrome-extensions`** | Manifest V3 기반 크롬 확장 프로그램 개발, 서비스 워커, 팝업, 웹스토어 배포 가이드. |
| **`coherence-auditor`** | 마크다운 문서 일관성, 링크 무결성, 깃 상태 서브에이전트 기반 감사. |
| **`dev-prompt-canary`** | `gd dev` 프롬프트 및 평가 로직 변경 시 격리된 워크트리에서 카나리 재검증. |
| **`grader-replay`** | 평가 채점기(grader.ts) 변경 시 과거 에이전트 솔루션 재실행 및 회귀 검증. |
| **`nightly-eval-investigation`** | GCS 원격 대시보드 야간 평가 실행 로그 분석 및 비정상 태스크 트리아지. |
| **`project-coding-standards`** | Guidance 레포지토리 전용 코딩 스타일 및 PR 리뷰 표준. |
| **`project-discipline-guides`** | Knowledge Mirror 기반 공통 지식 제거 및 discipline 가이드 리팩토링. |
| **`project-evals`** | `expectations.md`, `task.md`, `grader.ts` 품질 평가 파일 작성 가이드. |
| **`project-features`** | `new-feature` 이슈 작성 및 기능 타당성 검토. |
| **`project-guide-validation`** | 가이드 작성 완료 후 기술적 정확성 및 평가 준비도 셀프 검증. |
| **`project-guides`** | `guide.md`, `demo.html` 작성 모범 사례. |
| **`project-maintenance`** | 벤더 의존성, 웹 표준 호환 데이터셋 주기적 유지보수. |
| **`project-use-cases`** | 신규 가이드 작성의 첫 단계인 유스케이스 정의. |

---

### 2. Public APIs 무료 공개 API 카탈로그 (2종)
*출처: `w020316/cautious-broccoli`, `nyldn/public-apis-skill`*

| 스킬명 | 설명 및 주요 트리거 |
| :--- | :--- |
| **`public-apis`** | 외부 연동 요구 시 무작정 유료/임의 API를 사용하지 않고 1,400+ 카탈로그에서 최적의 무료 API 탐색 (지도, 날씨, 금융, AI, 소셜, Mock 등). |
| **`public-api-lookup`** | 카테고리, 인증 방식(무인증/API키/OAuth), HTTPS, CORS 지원 여부별 API 상세 검색. |

---

### 3. Addy Osmani 시니어 엔지니어링 스킬 (25종)
*출처: `addyosmani/agent-skills`*

| 스킬명 | 설명 및 주요 역할 |
| :--- | :--- |
| **`api-and-interface-design`** | REST, GraphQL, 모듈 간 타입 계약 및 안정적인 인터페이스 설계. |
| **`ci-cd-and-automation`** | CI/CD 파이프라인 자동화, 품질 게이트, 배포 전략 구축. |
| **`code-review-and-quality`** | 다축(정확성, 보안, 성능, 가독성 등) 심층 코드 리뷰. |
| **`code-simplification`** | 동작 변경 없는 명확한 리팩터링 및 불필요한 복잡성/중첩 제거. |
| **`constraint-driven-development`**| `CONSTRAINTS.md`에 프로젝트 품질 기준을 계약으로 명문화하고 조용한 기준 완화 방지. |
| **`context-engineering`** | 에이전트 세션 컨텍스트 및 규칙 파일 최적화. |
| **`debugging-and-error-recovery`** | 체계적 근본 원인 분석(RCA) 및 복구 가이드. |
| **`deprecation-and-migration`** | 시스템, API, DB 무중단 마이그레이션(Expand/Contract) 및 안전한 폐기. |
| **`documentation-and-adrs`** | 아키텍처 결정 레코드(ADR) 작성 및 문서-코드 간 괴리(Drift) 감지. |
| **`doubt-driven-development`** | 핵심 보안/아키텍처 결정 전 신선한 컨텍스트에서의 적대적 검증(Adversarial Review). |
| **`frontend-ui-engineering`** | 프로덕션 수준의 반응형, 접근성(WCAG) 준수 UI 엔지니어링. |
| **`git-workflow-and-versioning`** | 원자적 커밋, 충돌 해결, 브랜칭, 시맨틱 버저닝, 체인지로그. |
| **`idea-refine`** | 확산적/수렴적 사고를 통한 아이디어 정제 및 가정 검증. |
| **`incremental-implementation`** | 얇고 독립적으로 검증 가능한 슬라이스 단위 점진적 구현. |
| **`interview-me`** | 사용자가 진정으로 원하는 요구사항을 도출하기 위한 심층 인터뷰. |
| **`observability-and-instrumentation`**| 로깅, 메트릭, 분산 트레이싱, 알림 등 프로덕션 관측성 확보. |
| **`performance-optimization`** | 프론트/백엔드/DB/Core Web Vitals 전방위 성능 최적화. |
| **`planning-and-task-breakdown`** | 명세 기반의 실행 가능한 단위 태스크 분할 및 우선순위 지정. |
| **`security-and-hardening`** | OWASP Top 10, 입력값 검증, 세션 보안, 공급망 종속성 감사. |
| **`shipping-and-launch`** | 프로덕션 출시 체크리스트, 모니터링, 롤백 전략. |
| **`source-driven-development`** | 공식 문서 원본에 근거한 정확하고 최신 패턴 중심의 개발. |
| **`spec-driven-development`** | 코드 작성 전 요구사항 명세서(PRD) 및 역량 맵 작성. |
| **`test-driven-development`** | Red-Green-Refactor 루프 기반 테스트 주도 개발. |
| **`using-agent-skills`** | 현재 작업에 최적화된 엔지니어링 스킬 자동 식별 및 호출. |
| **`writing-guidelines`** | 기술 문서 보이스앤톤 및 스타일 가이드 준수 검사. |

---

### 4. Vercel 엔지니어링 & 프론트엔드 최적화 (10종)
*출처: `vercel-labs/skills`, `vercel-labs/agent-skills`*

| 스킬명 | 설명 및 주요 역할 |
| :--- | :--- |
| **`deploy-to-vercel`** | Vercel 프로젝트 생성, 프리뷰 및 프로덕션 배포. |
| **`find-skills`** | 새로운 기능에 필요한 에이전트 스킬 발견 및 안내. |
| **`impeccable`** | 프로덕션 수준의 정교한 UX/UI 디자인, 타이포그래피, 모션, DESIGN.md 토큰 관리. |
| **`vercel-cli-with-tokens`** | 토큰 기반 Vercel CLI 인증 및 환경 변수 관리. |
| **`vercel-composition-patterns`**| React 19 컴포넌트 합성, Compound 컴포넌트, Context 아키텍처. |
| **`vercel-optimize`** | 서버리스 함수 호출, 빌드 시간, Fast Data Transfer, 캐싱 비용 최적화. |
| **`vercel-react-best-practices`**| Vercel 공식 성능 가이드(서버 컴포넌트, 번들 최적화, 데이터 페칭). |
| **`vercel-react-native-skills`** | React Native & Expo 모바일 성능 최적화 및 네이티브 모듈. |
| **`vercel-react-view-transitions`**| React `<ViewTransition>` 기반 자연스러운 화면 전환 애니메이션. |
| **`web-design-guidelines`** | Web Interface Guidelines(WIG) 기반 UI/UX 준수 감사. |

---

### 5. Superpowers 엔지니어링 프레임워크 (15종)
*출처: `antigravity-plugins-partners/plugin/superpowers`*

| 단계 (Phase) | 스킬명 | 역할 및 핵심 규칙 |
| :--- | :--- | :--- |
| **진입점** | **`using-superpowers`** | 대화 시작 시 적절한 엔지니어링 스킬 자동 활성화. |
| **기획** | **`brainstorming`** | 사용자 요구사항 심층 분석 및 2~3개 대안 수립, 스펙 작성. |
| **계획** | **`writing-plans`** | 2~5분 단위의 최소 실행 태스크로 세분화된 계획서 작성. |
| **구현** | **`test-driven-development`** | 실패 테스트(Red) 우선 작성 후 최소 구현(Green) 및 리팩터링. |
| **실행** | **`executing-plans`** | 계획서 순서를 엄격히 준수하며 인라인 단계별 구현. |
| **위임** | **`subagent-driven-development`**| 독립 태스크를 서브에이전트에 할당하여 컨텍스트 보호. |
| **병렬** | **`dispatching-parallel-agents`**| 상호 의존성 없는 태스크를 다중 에이전트로 병렬 분산 처리. |
| **디버깅** | **`systematic-debugging`** | 4단계 디버깅(재현 ➔ RCA ➔ 최소수정 ➔ 회귀방지 테스트). |
| **검증** | **`verification-before-completion`**| 완료 주장 전 빌드/테스트 성공 로그 등 실제 증거 필수 제시. |
| **리뷰** | **`requesting-code-review`** | 작업 산출물에 대한 셀프 리뷰 및 피드백 요청. |
| **피드백** | **`receiving-code-review`** | 기술적 타당성을 엄격히 검증하여 안전하게 피드백 수용. |
| **마무리** | **`finishing-a-development-branch`**| 브랜치 정리 및 통합/머지 전략 확정. |
| **격리** | **`using-git-worktrees`** | Git Worktree를 통한 깨끗한 독립 작업 환경 유지. |
| **제작** | **`writing-skills`** | 새로운 에이전트 스킬 올바른 표준 형식으로 작성. |
| **진단** | **`diagnosing-superpowers`** | 이상 동작 발생 시 세션 로그 및 트레이스 진단. |

---

### 6. Google Workspace & Gmail 연동 (45종)
*출처: `antigravity-plugins-official/plugin/gmail`, `mkotinet/Google-Workspace-CLI-`*

- **공식 Gmail 플러그인 (`gmail`)**: 메일 검색, 읽기, 답장, 라벨링, 이모지 반응 등.
- **Google Workspace CLI 스킬군 (`gws-*`)**:
  - 핵심 서비스: `gws-drive`, `gws-gmail`, `gws-calendar`, `gws-sheets`, `gws-docs`, `gws-slides`, `gws-forms`, `gws-chat`, `gws-keep`, `gws-meet`, `gws-tasks`, `gws-people`, `gws-script`, `gws-admin-reports`, `gws-events`.
  - 업무 자동화 레시피 (Recipes): `recipe-meeting-prep`, `recipe-standup-report`, `recipe-weekly-digest`, `recipe-backup-sheet-as-csv`, `recipe-bulk-download-folder` 등 20여 종.
  - 역할별 페르소나 (Personas): `persona-exec-assistant`, `persona-project-manager`, `persona-team-lead`, `persona-researcher`, `persona-it-admin` 등 10여 종.

---

### 7. 한국어 AI 텍스트 자연화 (Humanize Korean & im-not-ai)
*출처: `epoko77-ai/im-not-ai`*

| 스킬명 | 설명 및 주요 역할 |
| :--- | :--- |
| **`humanize-korean`** | 사실·주장·수치는 보존하고, 번역투·기계적 병렬·상투적 관용구·피동태 등 10대 카테고리 85개 AI 티 패턴을 탐지하여 자연스러운 한국어로 전면 윤문. |
| **`humanize-kr`** | 빠른 한국어 윤문 실행 트리거. |
| **`humanize-scan`** | 원본 텍스트의 AI 티 지수를 6대 지표로 신속 측정하고 샘플 교정 결과 제공. |
| **`im-not-ai`** | AI 탐지기 바이패스 및 매끄러운 한글 문체 변환. |

---

### 8. 지식 그래프 아키텍처 (Graphify)
*출처: `graphifyy`*

| 스킬 / 명령어 | 설명 및 주요 역할 |
| :--- | :--- |
| **`graphify query "<질문>"`** | 코드베이스 및 아키텍처 질의 시 관련 서브그래프 우선 검색 (MCP: `query_graph`). |
| **`graphify path "<A>" "<B>"`** | 두 모듈/파일 간 의존성 경로 추적 (MCP: `shortest_path`). |
| **`graphify explain "<개념>"`** | 핵심 엔티티의 인접 노드 및 역할 분석 (MCP: `get_node`). |
| **`graphify update .`** | 코드 수정 후 지식 그래프 최신 상태 갱신 (AST 기반, 비용 없음). |

---

### 9. Google Antigravity 빌트인 전용 스킬 (11종)
*출처: `~/.gemini/antigravity/builtin/skills/`*

| 스킬명 | 설명 및 주요 역할 |
| :--- | :--- |
| **`antigravity-guide`** | Antigravity 2.0 종합 가이드, CLI (`agy`), 단축키, 설정 맵. |
| **`agy-customizations`** | 커스터마이징 시스템, 로딩 우선순위, 스킬/규칙/MCP/사이드카 구조. |
| **`automation`** | 정기적/스케줄링 백그라운드 자동화 작업 설계 (`/automation`). |
| **`generative_ui`** | 채팅창 내 실시간 대화형 인터랙티브 HTML 위젯 렌더링. |
| **`run-workflow`** | Python 스크립트 기반 다중 에이전트 동적 오케스트레이션 파이프라인. |
| **`swarm` / `swarm_monitor`** | 메시지 보드 기반의 멀티 에이전트 병렬 스웜 협동 작업. |
| **`plugin`** | Antigravity 플러그인 설치, 활성화, 패키징 및 제작. |
| **`migrate-agent-settings`** | Claude Code, Codex, Cursor 등 타 에이전트 설정을 Antigravity 플러그인으로 마이그레이션. |
| **`migrate-workflows`** | 레거시 워크플로우를 모던 스킬로 자동 변환. |
| **`ui-plugin-navigation`** | 사이드 패널의 UI 플러그인 바로가기 렌더링. |

---

## 🛠️ 작업 상황별 권장 스킬 워크플로우

| 작업 시나리오 | 최적의 권장 스킬 순서 |
| :--- | :--- |
| **신규 웹 UI / 기능 개발** | `modern-web-guidance` ➔ `brainstorming` ➔ `public-apis` ➔ `writing-plans` ➔ `test-driven-development` ➔ `verification-before-completion` |
| **에러 해결 및 버그 수정** | `graphify query` ➔ `systematic-debugging` ➔ 최소 패치 ➔ 회귀 테스트 ➔ `verification-before-completion` |
| **외부 서드파티 연동** | `public-api-lookup` ➔ `api-and-interface-design` ➔ `security-and-hardening` ➔ TDD |
| **성능 최적화 및 비용 절감** | `performance-optimization` ➔ `vercel-optimize` ➔ `vercel-react-best-practices` |
| **대규모 리팩터링 / 마이그레이션** | `query_graph` ➔ `writing-plans` ➔ `subagent-driven-development` ➔ `code-simplification` ➔ `verification-before-completion` |
| **AI 생성 문서/글 다듬기** | `humanize-scan` ➔ `humanize-korean` (또는 `humanize-kr`) |
| **작업 완료 및 PR 제출** | `verification-before-completion` ➔ `code-review-and-quality` ➔ `requesting-code-review` ➔ `finishing-a-development-branch` |
