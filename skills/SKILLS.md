# Google Antigravity & AI Agent 전역 스킬 및 MCP 종합 가이드 (`SKILLS.md`)

본 문서는 Google Antigravity를 비롯한 AI 에이전트 환경에 연동된 **전체 5개 MCP 서버**와 **202개 에이전트 스킬**의 전체 카탈로그 및 8단계 순차 적용 파이프라인 종합 레퍼런스입니다.

---

## 🚀 핵심 파이프라인: 8단계 스킬 순차 적용 원칙 (Sequential Skill Application)

모든 코드 개발, 기능 구현, 버그 수정, 리팩토링, 아키텍처 분석 시 최고 수준의 품질과 최신 웹 표준, 영속적 맥락 보존, 최적화된 프레임워크 아키텍처 및 결함 없는 간결한 코드를 달성하기 위해 다음 8가지 단계를 **순차적으로** 적용합니다:

```
[1단계: LLM 코딩 행동 강령 최우선 준수]
   └── karpathy-guidelines (Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven)
        ▼
[2단계: 지속 기억 컨텍스트 회상 및 교훈 반영]
   └── agentmemory (memory-discipline, recall, remember, lesson, commit-context)
        ▼
[3단계: 최신 웹 표준 & 가이던스 우선 검토]
   └── modern-web-guidance-src, modern-web-guidance, baseline-status
        ▼
[4단계: 외부 연동 & 무료 공개 API 생태계 우선 탐색]
   └── public-apis, public-api-lookup (1,400+ API 카탈로그)
        ▼
[5단계: Vercel 프레임워크 & UI/UX 최적화 필수 적용]
   └── vercel-react-best-practices, vercel-composition-patterns, impeccable, web-design-guidelines, vercel-optimize
        ▼
[6단계: 시니어 풀스택 엔지니어링 표준 통합]
   └── addyosmani/agent-skills (api-and-interface-design, security-and-hardening, performance, TDD)
        ▼
[7단계: 지식 그래프 기반 구조 탐색 및 영향도 분석]
   └── graphify (query_graph, shortest_path, get_node / 작업 후 graphify update .)
        ▼
[8단계: 체계적 프로세스 및 무결성 검증]
   └── superpowers (brainstorming ➔ writing-plans ➔ TDD ➔ verification-before-completion)
```

---

## 🔌 1. 연동 중인 MCP (Model Context Protocol) 서버 (5종)

| MCP 서버명 | 대상 시스템 및 패키지 | 핵심 기능 및 주요 도구 요약 |
| :--- | :--- | :--- |
| **`github`** | `@modelcontextprotocol/server-github` | **GitHub 원격 형상 및 협업 자동화**<br>• 레포지토리/브랜치 생성 및 관리<br>• 파일 읽기/수정/푸시 및 커밋 이력 추적<br>• 이슈(Issue) 및 풀 리퀘스트(PR) 생성, 리뷰, 병합<br>• 코드 및 파일 검색 |
| **`portainer`** | `Synology DS1019+ NAS`<br>(`http://djms1.iptime.org:9000`) | **DS1019+ NAS 도커 컨테이너 및 스택 생명주기 관리**<br>• 컨테이너 목록/상태/로그 조회, 시작/정지/재시작/삭제<br>• Docker Compose 스택(Stack) 배포, 파일 조회, 업데이트<br>• 도커 이미지 풀링, 볼륨 및 네트워크 리소스 제어 |
| **`portainer_ds920`** | `Synology DS920+ NAS`<br>(`https://djms1.iptime.org:9101`) | **DS920+ NAS 도커 컨테이너 및 스택 보안(HTTPS) 관리**<br>• DS920+ 원격 환경의 컨테이너 상태 모니터링 및 제어<br>• 독립 Docker Compose 스택 배포, 수정, 무중단 재배포<br>• 볼륨 데이터 및 격리 브리지 네트워크 관리 |
| **`graphify`** | `graphify-mcp` (AST 기반 지식 그래프) | **코드베이스 아키텍처 및 의존성 관계 분석**<br>• `query_graph`: 자연어 질문 기반 관련 서브그래프 우선 검색<br>• `shortest_path`: 두 모듈/파일 간 의존성 연결 경로 추적<br>• `get_node` / `get_neighbors`: 핵심 엔티티 세부정보 및 인접 구조 분석<br>• `god_nodes`: 고위험 고결합도 모듈 식별 및 리팩터링 대상 추천<br>• `get_pr_impact`: 변경사항이 전체 시스템에 미치는 영향도 예측 |
| **`kakao`** | `kakao-mcp` (macOS 카카오톡 연동) | **macOS 로컬 카카오톡 안전 조회 및 메시징**<br>• 카카오톡 Mac 앱 로컬 암호화 SQLite(SQLCipher) 직접 읽기<br>• 메시지를 읽어도 **'읽음(1 사라짐)' 표시가 남지 않는** 무흔적 조회<br>• `kakao_list_chats` (대화방 목록), `kakao_read_messages` (메시지 읽기)<br>• `kakao_search` (키워드 검색), `kakao_get_attachment` (사진/파일 다운로드)<br>• 2단계 승인 게이트(`prepare_send` ➔ `confirm_send`) 기반 안전 메시지 전송 |

---

## 📚 2. 전체 에이전트 스킬 카탈로그 (총 202종)

### 1. 코딩 행동 강령 (Karpathy Guidelines, 1종)
*출처: `szkocot/andrej-karpathy-skills` (`karpathy-guidelines`)*

| 스킬명 | 설명 및 주요 역할 |
| :--- | :--- |
| **`karpathy-guidelines`** | 코딩 전 사전 사고(Think Before Coding), 요청하지 않은 과잉 설계 차단(Simplicity First), 무관한 코드 수정을 금지하는 외과수술식 패치(Surgical Changes), 검증 가능한 테스트 루프(Goal-Driven Execution) 강제. |

---

### 2. 지속 기억 및 메모리 규율 (AgentMemory, 17종)
*출처: `rohitg00/agentmemory`*

| 스킬명 | 설명 및 주요 역할 |
| :--- | :--- |
| **`memory-discipline`** | 작업 전 사전 회상(`recall`), 결정 순간 즉시 기록(`remember`), 사용자 교정 시 교훈 학습(`lesson`)의 메모리 수명주기 루프 총괄. |
| **`remember`** | 핵심 통찰, 아키텍처 결정, 문제 해결법을 2~5개 개념 태그 및 파일 경로와 함께 장기 메모리에 저장. |
| **`recall`** | 과거 프로젝트의 결정 사항, 기술 제약, 트러블슈팅 이력을 하이브리드 검색(BM25+벡터+지식그래프)으로 조회. |
| **`lesson`** | 사용자의 교정 및 피드백을 향후 동일 실수 방지를 위한 확신도 기반 행동 규칙으로 승격 학습. |
| **`recap`** | 최근 N개 세션의 작업 히스토리와 주요 관측치를 일자별/프로젝트별로 요약 브리핑. |
| **`commit-context`** | 특정 파일, 함수, 코드 라인이 어느 에이전트 세션의 맥락에서 커밋되었는지 역추적. |
| **`commit-history`** | 에이전트 세션과 연결된 최근 깃 커밋 이력 및 작업 맥락 목록 제공. |
| **`handoff`** | 현재 세션의 진행 상황과 미해결 질문을 다음 세션으로 안전하게 인수인계. |
| **`session-history`** | 과거 작업 세션 타임라인을 구조화된 로그로 복기 및 조회. |
| **`forget`** | 사용자의 명시적 확인 하에 구버전이 되거나 불필요해진 영구 메모리를 안전하게 선별 삭제. |
| **`agentmemory-agents`** | 호스트 코딩 에이전트(Antigravity, Claude Code, Cursor 등)와의 연결 어댑터 및 스코프 관리. |
| **`agentmemory-architecture`** | AgentMemory 내부 스토리지 엔진, 임베딩, 포트, 뷰어 아키텍처 기술 레퍼런스. |
| **`agentmemory-config`** | 메모리 데몬 포트, 환경 변수, 인증, 기능 플래그 설정 및 진단. |
| **`agentmemory-hooks`** | 세션 수명주기 전반에서 관측 데이터를 수동 개입 없이 자동 수집하는 훅 관리. |
| **`agentmemory-mcp-tools`** | AgentMemory MCP 도구 목록 및 파라미터 규격 안내. |
| **`agentmemory-rest-api`** | MCP를 지원하지 않는 환경을 위한 AgentMemory HTTP REST API 연동 가이드. |
| **`write-agentmemory-skill`** | 일관된 표준 형식의 메모리 확장 스킬을 제작하기 위한 가이드라인. |

---

### 3. 최신 웹 표준 및 Chrome 가이던스 (Google Chrome, 16종)
*출처: `googlechrome/modern-web-guidance`, `googlechrome/modern-web-guidance-src`*

| 스킬명 | 설명 및 주요 역할 |
| :--- | :--- |
| **`modern-web-guidance`** | HTML/CSS/JS 작업 전 필수 검토. Popover, Dialog, View Transitions, Container Queries 등 최신 웹 API 권장 패턴 검색 및 적용. |
| **`baseline-status`** | 웹 기술 및 API의 크로스 브라우저 지원 현황 및 Baseline 상태(Widely / Newly available) 실시간 확인. |
| **`browser-testing-with-devtools`** | Chrome DevTools MCP를 연동하여 실제 브라우저 DOM 검사, 콘솔 오류 추적, 네트워크 요청 검증. |
| **`chrome-extensions`** | Manifest V3 기반 크롬 확장 프로그램 개발, 서비스 워커, 사이드 패널, 웹스토어 배포 가이드. |
| **`coherence-auditor`** | 마크다운 문서 일관성, 깨진 링크, 깃 상태를 전용 서브에이전트로 자동 감사. |
| **`dev-prompt-canary`** | 프롬프트 및 평가 로직 변경 시 격리된 워크트리에서 카나리 재검증 수행. |
| **`grader-replay`** | 평가 채점기(`grader.ts`) 수정 시 저장된 과거 솔루션을 재실행하여 전/후 회귀 검증. |
| **`nightly-eval-investigation`** | GCS 원격 대시보드 야간 평가 실행 로그 분석 및 비정상 태스크 트리아지. |
| **`project-coding-standards`** | Guidance 레포지토리 전용 아키텍처 규칙 및 PR 리뷰 표준. |
| **`project-discipline-guides`** | Knowledge Mirror 기반 공통 지식 필터링 및 discipline 가이드 리팩토링. |
| **`project-evals`** | `expectations.md`, `task.md`, `grader.ts` 품질 평가 파일 작성 가이드. |
| **`project-features`** | 신규 웹 기능 이슈 등록 및 브라우저 출시 가이던스 필요 여부 심사. |
| **`project-guide-validation`** | 작성된 가이드 문서의 기술적 정확성 및 테스트 준비도 셀프 검증. |
| **`project-guides`** | `guide.md`, `demo.html` 작성 모범 사례. |
| **`project-maintenance`** | 벤더 의존성, 웹 표준 호환 데이터셋 주기적 유지보수. |
| **`project-use-cases`** | 신규 가이드 작성의 첫 단계인 유스케이스 정의 가이드. |

---

### 4. Public APIs 무료 공개 API 카탈로그 (2종)
*출처: `w020316/cautious-broccoli`, `nyldn/public-apis-skill`*

| 스킬명 | 설명 및 주요 역할 |
| :--- | :--- |
| **`public-apis`** | 외부 연동 필요 시 유료/사설 API 도입 전에 50+ 카테고리 1,400+ 무료 공개 API 카탈로그 우선 조회. |
| **`public-api-lookup`** | 카테고리, 인증 방식(무인증/API키/OAuth), HTTPS, CORS 지원 여부별 세부 필터링 검색. |

---

### 5. Addy Osmani 시니어 엔지니어링 스킬 (25종)
*출처: `addyosmani/agent-skills`*

| 스킬명 | 설명 및 주요 역할 |
| :--- | :--- |
| **`api-and-interface-design`** | REST, GraphQL, 모듈 간 인터페이스 경계 및 견고한 타입 계약 설계. |
| **`ci-cd-and-automation`** | CI/CD 파이프라인 자동화, 품질 게이트 및 무중단 배포 전략 수립. |
| **`code-review-and-quality`** | 정확성, 보안, 가독성, 성능 등 다축 심층 코드 리뷰 수행. |
| **`code-simplification`** | 동작 변경 없이 불필요한 복잡성과 중첩 코드를 단순화하는 리팩터링. |
| **`constraint-driven-development`** | `CONSTRAINTS.md`에 품질 기준을 명문화하여 조용한 기준 완화 방지. |
| **`context-engineering`** | 에이전트 세션의 컨텍스트 품질을 최적화하고 규칙 파일 구조 개선. |
| **`debugging-and-error-recovery`** | 체계적 근본 원인 분석(RCA)을 통한 원인 규명 및 최소 수정 가이드. |
| **`deprecation-and-migration`** | 레거시 시스템 및 DB 무중단 마이그레이션(Expand/Contract)과 안전한 폐기. |
| **`documentation-and-adrs`** | 아키텍처 결정 레코드(ADR) 작성 및 코드-문서 간 괴리(Drift) 방지. |
| **`doubt-driven-development`** | 보안 및 고위험 결정 전 신선한 컨텍스트에서의 적대적 교차 검증(Adversarial Review). |
| **`frontend-ui-engineering`** | 프로덕션 수준의 반응형, 접근성(WCAG) 준수 UI 엔지니어링. |
| **`git-workflow-and-versioning`** | 원자적 커밋 분할, 충돌 해결, 브랜칭, 시맨틱 버저닝, 체인지로그 관리. |
| **`idea-refine`** | 확산적/수렴적 사고를 통한 아이디어 구체화 및 숨은 가정 검증. |
| **`incremental-implementation`** | 변경사항을 얇고 독립적으로 검증 가능한 슬라이스 단위로 점진 구현. |
| **`interview-me`** | 모호한 요구사항 이면의 실제 사용자 의도를 파악하기 위한 심층 인터뷰. |
| **`observability-and-instrumentation`** | 로깅, 메트릭, 분산 트레이싱, 장애 알림 등 프로덕션 관측성 확보. |
| **`performance-optimization`** | 프론트/백엔드/DB/Core Web Vitals 전방위 병목 제거 및 성능 최적화. |
| **`planning-and-task-breakdown`** | 명세 기반으로 구현 가능한 순차 단위 태스크 분할 및 일정 추정. |
| **`security-and-hardening`** | OWASP Top 10, 입력값 검증, 세션 보안, 공급망 종속성 감사. |
| **`shipping-and-launch`** | 프로덕션 출시 전 체크리스트 점검, 모니터링 및 롤백 전략 수립. |
| **`source-driven-development`** | 공식 기술 문서를 근거로 한 최신의 정확한 코드 패턴 작성. |
| **`spec-driven-development`** | 코드 작성 전 요구사항 명세서(PRD) 및 기능 맵 수립. |
| **`test-driven-development`** | Red-Green-Refactor 루프 기반 실패 테스트 우선 작성 개발. |
| **`using-agent-skills`** | 현재 작업에 가장 적합한 엔지니어링 스킬을 자동 탐색하고 호출. |
| **`writing-guidelines`** | 기술 문서의 보이스앤톤, 명확성, 스타일 가이드라인 준수 검사. |

---

### 6. Vercel 프레임워크 & UI 최적화 (10종)
*출처: `vercel-labs/skills`, `vercel-labs/agent-skills`*

| 스킬명 | 설명 및 주요 역할 |
| :--- | :--- |
| **`deploy-to-vercel`** | Vercel 프로젝트 생성, 토큰 기반 프리뷰 및 프로덕션 배포. |
| **`find-skills`** | 사용자가 필요한 새로운 에이전트 스킬 발견 및 설치 안내. |
| **`impeccable`** | 정교한 타이포그래피, 컬러, 모션, 여백, DESIGN.md 토큰을 적용한 고품질 UI/UX 디자인 및 폴리싱. |
| **`vercel-cli-with-tokens`** | 대화형 로그인 없이 접근 토큰을 활용한 Vercel CLI 및 환경 변수 자동화. |
| **`vercel-composition-patterns`** | React 19 컴포넌트 합성, Compound 컴포넌트, Context 아키텍처. |
| **`vercel-optimize`** | 서버리스 함수 호출, 빌드 시간, Fast Data Transfer, 캐싱 비용 최적화. |
| **`vercel-react-best-practices`** | React/Next.js 공식 성능 가이드(서버 컴포넌트, 번들 최적화, 워터폴 제거). |
| **`vercel-react-native-skills`** | React Native & Expo 모바일 성능 최적화 및 리스트 가상화. |
| **`vercel-react-view-transitions`** | React `<ViewTransition>` 기반 부드러운 화면 전환 애니메이션 구현. |
| **`web-design-guidelines`** | Web Interface Guidelines(WIG) 기반 UI 접근성 및 인터랙션 감사. |

---

### 7. Superpowers 엔지니어링 프레임워크 (14종)
*출처: `antigravity-plugins-partners/plugin/superpowers`*

| 스킬명 | 설명 및 주요 역할 |
| :--- | :--- |
| **`using-superpowers`** | 대화 시작 시 워크플로우에 맞는 Superpowers 스킬 자동 탐색 및 활성화. |
| **`brainstorming`** | 신규 기능 착수 전 2~3가지 대안을 탐색하고 사용자 합의를 도출하는 기획. |
| **`writing-plans`** | 2~5분 단위의 최소 실행 단위로 세분화된 단계별 구현 계획서 작성. |
| **`executing-plans`** | 수립된 계획서의 순서를 엄격히 준수하며 인라인 단계별 구현. |
| **`subagent-driven-development`** | 독립 태스크를 서브에이전트에 할당하여 메인 컨텍스트를 보호하며 작업. |
| **`dispatching-parallel-agents`** | 상호 의존성 없는 2개 이상의 독립 작업을 다중 에이전트로 병렬 처리. |
| **`systematic-debugging`** | 4단계 체계적 디버깅 (재현 ➔ RCA ➔ 최소 수정 ➔ 회귀 방지 검증). |
| **`verification-before-completion`** | 완료를 주장하기 전 빌드 성공/테스트 통과 로그 등 실제 증거 필수 검증. |
| **`requesting-code-review`** | 구현 완료 후 검증 기준 충족 여부를 확인하고 피드백 요청. |
| **`receiving-code-review`** | 코드 리뷰 피드백 수신 시 기술적 타당성을 엄격히 검증하여 안전하게 반영. |
| **`finishing-a-development-branch`** | 모든 테스트 통과 후 브랜치 병합 및 정리 전략 수립. |
| **`using-git-worktrees`** | Git Worktree를 활용하여 현재 워크스페이스와 격리된 작업 환경 구성. |
| **`writing-skills`** | 표준 규격에 부합하는 새로운 에이전트 스킬 작성 및 검증. |
| **`diagnosing-superpowers`** | 에이전트 실행 실패 또는 비정상 동작 시 세션 로그 진단. |

---

### 8. 한국어 AI 텍스트 자연화 (Humanize & im-not-ai, 6종)
*출처: `epoko77-ai/im-not-ai`*

| 스킬명 | 설명 및 주요 역할 |
| :--- | :--- |
| **`humanize-korean`** | 10대 카테고리 85개 AI 티 패턴을 전수 탐지하여 자연스러운 한국어 문체와 리듬으로 전면 윤문. |
| **`humanize-kr`** | 한국어 AI 티 제거기 빠른 실행 트리거. |
| **`humanize-scan`** | 상위 6대 지표로 원본 글의 AI 티 점수를 신속 측정하고 샘플 교정문 제공. |
| **`im-not-ai`** | AI 탐지기 바이패스 및 자연스러운 한국어 문체 변환. |
| **`humanize`** | 기본 한국어 텍스트 휴머나이징 진입점. |
| **`humanize-redo`** | 기존 윤문 결과에 대해 톤과 문체를 재조정하여 다시 작성. |

---

### 9. 지식 그래프 아키텍처 (Graphify, 1종)
*출처: `graphifyy`*

| 스킬명 | 설명 및 주요 역할 |
| :--- | :--- |
| **`graphify`** | 코드베이스 및 아키텍처 질의 시 지식 그래프(`graphify-out/`)를 우선 검색하고 변경 후 그래프를 갱신하는 스킬. |

---

### 10. Google Antigravity 빌트인 전용 스킬 (14종)
*출처: `~/.gemini/antigravity/builtin/skills/`*

| 스킬명 | 설명 및 주요 역할 |
| :--- | :--- |
| **`antigravity_guide`** | Antigravity 2.0 종합 가이드, CLI(`agy`), 단축키, 설정 맵 제공. |
| **`agy-customizations`** | 커스터마이징 로딩 우선순위, 스킬/규칙/MCP/사이드카 구조 안내. |
| **`automation`** | 주기적/스케줄링 백그라운드 자동화 작업 설계 (`/automation`). |
| **`generative_ui`** | 대화창 내에 동적 대화형 인터랙티브 HTML 위젯 렌더링. |
| **`run-workflow`** | Python 스크립트 기반 다중 에이전트 동적 오케스트레이션 파이프라인. |
| **`native_swarm`** | 공유 메시지 보드 기반의 멀티 에이전트 병렬 협동 작업 오케스트레이션. |
| **`swarm_monitor`** | 멀티 에이전트 스웜 협업이 정체(Stall)되었을 때 자동 감지 및 조율. |
| **`swarm_narrator`** | 스웜 내 에이전트 간의 진행 상황과 결론을 사용자에게 브리핑. |
| **`plugin`** | Antigravity 플러그인 설치, 활성화, 패키징 및 관리 (`/plugin`). |
| **`migrate-agent-settings`** | Claude Code, Codex, Cursor 설정을 Antigravity 플러그인으로 마이그레이션. |
| **`migrate-workflows`** | 구버전 워크플로우를 모던 스킬 구조로 자동 변환. |
| **`ui-plugin-navigation`** | 사이드 패널의 UI 플러그인 바로가기 렌더링. |
| **`mcp-app-development`** | 신규 MCP 애플리케이션 및 도구 개발 가이드. |
| **`permissioned-github`** | 권한 제어 기반의 보안 GitHub 작업 프로토콜. |

---

### 11. Google Workspace & Gmail 연동 스킬군 (총 96종)
*출처: `antigravity-plugins-official/plugin/gmail`, `mkotinet/Google-Workspace-CLI-`*

#### ① 공식 Gmail 플러그인 (1종)
| 스킬명 | 설명 및 주요 역할 |
| :--- | :--- |
| **`gmail`** | Gmail 메시지 검색, 읽기, 답장, 전달, 임시저장, 라벨 관리, 이모지 반응 등 CLI 연동. |

#### ② GWS 핵심 서비스 CLI 스킬 (`gws-*`, 43종)
| 스킬명 | 설명 및 주요 역할 |
| :--- | :--- |
| **`gws-shared`** | GWS CLI 공통 인증, 글로벌 플래그, 출력 형식 패턴 가이드. |
| **`gws-gmail`** | Gmail 발송, 읽기, 관리 통합 인터페이스. |
| **`gws-gmail-read`** | 특정 이메일 메시지 본문 및 헤더 추출. |
| **`gws-gmail-send`** | 수신자에게 이메일 발송. |
| **`gws-gmail-reply`** | 이메일 답장 (자동 스레딩 지원). |
| **`gws-gmail-reply-all`** | 이메일 전체 답장 (자동 스레딩 지원). |
| **`gws-gmail-forward`** | 이메일 메시지 전달. |
| **`gws-gmail-triage`** | 안읽은 메일 요약 (발신자, 제목, 일시). |
| **`gws-gmail-watch`** | 실시간 신규 이메일 수신 스트리밍(NDJSON). |
| **`gws-drive`** | Google Drive 파일, 폴더, 공유 드라이브 관리. |
| **`gws-drive-upload`** | 자동 메타데이터 파일 업로드. |
| **`gws-calendar`** | Google Calendar 캘린더 및 이벤트 관리. |
| **`gws-calendar-agenda`** | 전체 캘린더의 다가오는 일정 목록 요약. |
| **`gws-calendar-insert`** | 캘린더에 신규 이벤트 등록. |
| **`gws-sheets`** | Google Sheets 스프레드시트 읽기 및 쓰기. |
| **`gws-sheets-read`** | 스프레드시트의 셀/범위 데이터 읽기. |
| **`gws-sheets-append`** | 스프레드시트에 행 데이터 추가. |
| **`gws-docs`** | Google Docs 문서 읽기 및 작성. |
| **`gws-docs-write`** | Docs 문서에 텍스트 내용 추가. |
| **`gws-slides`** | Google Slides 프레젠테이션 읽기 및 편집. |
| **`gws-forms`** | Google Forms 설문지 읽기 및 작성. |
| **`gws-chat`** | Google Chat 스페이스 및 메시지 관리. |
| **`gws-chat-send`** | Chat 스페이스에 메시지 발송. |
| **`gws-keep`** | Google Keep 메모 및 체크리스트 관리. |
| **`gws-meet`** | Google Meet 회의 공간 생성 및 관리. |
| **`gws-tasks`** | Google Tasks 할일 목록 및 작업 관리. |
| **`gws-people`** | Google Contacts 주소록 및 프로필 관리. |
| **`gws-script`** | Google Apps Script 프로젝트 관리. |
| **`gws-script-push`** | 로컬 파일을 Apps Script 프로젝트에 업로드. |
| **`gws-admin-reports`** | Google Workspace Admin SDK 감사 로그 및 사용량 보고서. |
| **`gws-classroom`** | Google Classroom 코스, 수강생 및 과제 관리. |
| **`gws-events`** | Workspace 이벤트 구독 관리. |
| **`gws-events-subscribe`** | Workspace 이벤트를 실시간 NDJSON으로 구독. |
| **`gws-events-renew`** | 만료 예정인 Workspace 이벤트 구독 갱신. |
| **`gws-modelarmor`** | Google Model Armor 기반 사용자 입력 안전 필터링. |
| **`gws-modelarmor-create-template`** | Model Armor 보안 템플릿 생성. |
| **`gws-modelarmor-sanitize-prompt`** | 사용자 프롬프트 안전 검사 및 새니타이징. |
| **`gws-modelarmor-sanitize-response`**| 모델 응답 안전 검사 및 새니타이징. |
| **`gws-workflow`** | 크로스 서비스 생산성 복합 워크플로우. |
| **`gws-workflow-meeting-prep`** | 다음 회의 안건, 참석자, 관련 문서 사전 준비. |
| **`gws-workflow-standup-report`** | 오늘 일정 + 열린 할일을 스탠드업 요약으로 정리. |
| **`gws-workflow-weekly-digest`** | 이번 주 회의 + 안읽은 메일 주간 브리핑. |
| **`gws-workflow-email-to-task`** | Gmail 메시지를 Google Tasks 할일로 자동 변환. |
| **`gws-workflow-file-announce`** | Google Drive 파일을 Chat 스페이스에 자동 공지. |

#### ③ 역할별 전문 페르소나 (`persona-*`, 10종)
| 스킬명 | 설명 및 주요 역할 |
| :--- | :--- |
| **`persona-exec-assistant`** | 경영진 비서: 일정, 받은편지함 및 대외 커뮤니케이션 총괄. |
| **`persona-project-manager`** | 프로젝트 매니저: 일정, 회의 조율, 작업 트래킹 및 문서 공유. |
| **`persona-team-lead`** | 팀 리더: 스탠드업 운영, 작업 분배, 팀 커뮤니케이션. |
| **`persona-researcher`** | 연구원: 참고자료 정리, 연구 노트 수집, 협업 공유. |
| **`persona-it-admin`** | IT 관리자: 보안 모니터링, 감사 로그 점검, Workspace 설정. |
| **`persona-hr-coordinator`** | 인사 담당: 온보딩 프로세스, 공지 배포, 사내 인사 안내. |
| **`persona-content-creator`** | 콘텐츠 크리에이터: 콘텐츠 기획, 제작 및 Workspace 배포. |
| **`persona-customer-support`** | 고객 지원: 지원 티켓 추적, 응대, 장애 이슈 에스컬레이션. |
| **`persona-event-coordinator`** | 이벤트 기획자: 행사 일정, 초대장 발송, 물류/자료 준비. |
| **`persona-sales-ops`** | 영업 관리: 파이프라인 관리, 통화 기록, 고객 후속 조치. |

#### ④ 업무 자동화 레시피 (`recipe-*`, 42종)
| 스킬명 | 설명 및 주요 역할 |
| :--- | :--- |
| **`recipe-batch-invite-to-event`** | 기존 캘린더 일정에 참석자 대량 초대 및 알림. |
| **`recipe-block-focus-time`** | 캘린더에 반복 집중 근무(Focus Time) 블록 생성. |
| **`recipe-create-events-from-sheet`**| 스프레드시트 행 데이터를 읽어 캘린더 이벤트로 일괄 등록. |
| **`recipe-create-meet-space`** | Meet 회의 공간 생성 및 참여 링크 공유. |
| **`recipe-find-free-time`** | 다중 참석자의 빈 시간대를 찾아 회의 슬롯 추천. |
| **`recipe-plan-weekly-schedule`** | 주간 캘린더의 빈 시간을 분석하여 계획 일정 자동 배치. |
| **`recipe-post-mortem-setup`** | 사후 검토 Docs 생성, Calendar 리뷰 예약, Chat 알림. |
| **`recipe-reschedule-meeting`** | 회의 일정 시간 이동 및 전 참석자 자동 알림. |
| **`recipe-review-meet-participants`**| Meet 회의 실제 참석자 및 체류 시간 분석. |
| **`recipe-schedule-recurring-event`**| 반복 캘린더 일정 생성 및 참석자 초대. |
| **`recipe-share-event-materials`** | 캘린더 일정 참석자 전원에게 Drive 참고 파일 공유. |
| **`recipe-create-gmail-filter`** | 조건에 맞는 메일 자동 라벨링/보관 필터 생성. |
| **`recipe-create-vacation-responder`**| 휴가 부재중 자동응답기 설정. |
| **`recipe-draft-email-from-doc`** | Docs 문서 내용을 읽어 Gmail 메일 초안 작성. |
| **`recipe-forward-labeled-emails`** | 특정 라벨 메일을 지정 주소로 자동 전달. |
| **`recipe-label-and-archive-emails`**| 일치하는 메일에 라벨 부여 및 받은편지함 보관. |
| **`recipe-save-email-attachments`** | 메일 첨부파일을 지정 Drive 폴더로 자동 저장. |
| **`recipe-save-email-to-doc`** | 메일 본문을 Docs 문서로 저장하여 아카이빙. |
| **`recipe-send-team-announcement`** | Gmail 메일과 Chat 스페이스에 동시 팀 공지 발송. |
| **`recipe-bulk-download-folder`** | Drive 폴더 내 모든 파일을 로컬로 일괄 다운로드. |
| **`recipe-create-doc-from-template`**| Docs 템플릿 복사 후 내용 채워 협업자에게 공유. |
| **`recipe-create-presentation`** | 신규 Slides 발표자료 생성 및 초기 슬라이드 구성. |
| **`recipe-create-shared-drive`** | Google 공유 드라이브 생성 및 권한별 멤버 추가. |
| **`recipe-email-drive-link`** | Drive 파일 권한 부여 및 링크 이메일 안내. |
| **`recipe-find-large-files`** | 드라이브 용량을 많이 차지하는 대용량 파일 탐색. |
| **`recipe-organize-drive-folder`** | 폴더 구조를 자동 생성하고 파일들을 제자리로 정리. |
| **`recipe-share-doc-and-notify`** | Docs 문서 편집 권한 공유 및 이메일 링크 알림. |
| **`recipe-share-folder-with-team`** | Drive 폴더 전체를 팀원 목록에 일괄 공유. |
| **`recipe-watch-drive-changes`** | Drive 파일/폴더의 변경 알림 구독. |
| **`recipe-backup-sheet-as-csv`** | Sheets 스프레드시트를 로컬 CSV 파일로 백업. |
| **`recipe-collect-form-responses`**| Forms 설문 응답 수집 및 결과 검토. |
| **`recipe-compare-sheet-tabs`** | 시트 내 2개 탭 데이터를 비교하여 차이점 추출. |
| **`recipe-copy-sheet-for-new-month`**| 템플릿 탭을 새 달 추적용 탭으로 복제. |
| **`recipe-create-expense-tracker`** | 지출 추적용 스프레드시트 템플릿 자동 구성. |
| **`recipe-generate-report-from-sheet`**| 시트 데이터를 읽어 양식화된 Docs 보고서 생성. |
| **`recipe-log-deal-update`** | 영업 현황 스프레드시트에 딜 업데이트 행 추가. |
| **`recipe-sync-contacts-to-sheet`** | Google Contacts 주소록을 스프레드시트로 내보내기. |
| **`recipe-create-classroom-course`**| Classroom 신규 수업 개설 및 학생 초대. |
| **`recipe-create-feedback-form`** | 피드백 설문지 생성 및 Gmail로 공유. |
| **`recipe-create-task-list`** | Tasks 신규 할일 목록 생성 및 초기 작업 등록. |
| **`recipe-review-overdue-tasks`** | 마감 기한이 지난 지연 할일 목록 탐색. |

---

## 🛠️ 작업 상황별 권장 스킬 워크플로우

| 작업 시나리오 | 최적의 권장 스킬 순서 |
| :--- | :--- |
| **신규 웹 UI / 기능 개발** | `karpathy-guidelines` (사전 사고 & 단순함) ➔ `agentmemory` (기억 회상) ➔ `modern-web-guidance` ➔ `brainstorming` ➔ `public-apis` ➔ `vercel-composition-patterns` & `impeccable` ➔ `writing-plans` ➔ `test-driven-development` ➔ `remember` (결정 기록) ➔ `verification-before-completion` |
| **에러 해결 및 버그 수정** | `karpathy-guidelines` (외과수술식 수정) ➔ `agentmemory` (Gotcha 회상) ➔ `graphify query` ➔ `systematic-debugging` ➔ 최소 패치 ➔ `remember` (해결 원인 기록) ➔ `verification-before-completion` |
| **외부 서드파티 연동** | `karpathy-guidelines` ➔ `agentmemory` ➔ `public-api-lookup` ➔ `api-and-interface-design` ➔ `security-and-hardening` ➔ TDD ➔ `remember` |
| **성능 최적화 및 비용 절감** | `karpathy-guidelines` ➔ `agentmemory` ➔ `performance-optimization` ➔ `vercel-optimize` ➔ `vercel-react-best-practices` |
| **대규모 리팩터링 / 마이그레이션** | `karpathy-guidelines` ➔ `agentmemory` ➔ `query_graph` ➔ `writing-plans` ➔ `subagent-driven-development` ➔ `code-simplification` ➔ `commit-context` ➔ `verification-before-completion` |
| **사용자 교정 및 피드백 수신** | `lesson` (행동 교훈 영구 저장) ➔ `memory-discipline` ➔ 다음 작업 시 자동 적용 |
| **AI 생성 문서/글 다듬기** | `humanize-scan` ➔ `humanize-korean` (또는 `humanize-kr`) |
| **작업 완료 및 PR 제출** | `verification-before-completion` ➔ `code-review-and-quality` ➔ `handoff` / `commit-context` ➔ `requesting-code-review` ➔ `finishing-a-development-branch` |
