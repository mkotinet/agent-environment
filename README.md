# Agent Environment Sync (AI Agent 통합 형상 동기화 허브)

여러 대의 맥북(MacBook), 노트북, 데스크톱 간에 **동일한 AI Agent 개발 지침(Rules), 에이전트 스킬(Skills), MCP 서버 설정, 커스텀 MCP 소스코드**를 실시간으로 공유하고 원클릭으로 완벽히 복원할 수 있도록 지원하는 공식 중간매개체 레포지토리입니다.

Google Antigravity, Claude Code, OpenAI Codex, Cursor, Gemini CLI 등 다양한 에이전트 런타임 간의 일관된 엔지니어링 환경을 보장합니다.

---

## 📂 레포지토리 구조

```
agent-environment/
├── rules/                           # AI 에이전트 전역 및 워크스페이스 규칙
│   ├── GEMINI.md                    # Antigravity & Gemini CLI 13대 공통 지침
│   ├── AGENTS.md                    # Universal 에이전트 공통 표준 지침
│   ├── ANTIGRAVITY.md               # Google Antigravity 아키텍처 및 계층 가이드
│   └── graphify.md                  # 지식 그래프(Knowledge Graph) 우선 탐색 원칙
├── skills/                          # 에이전트 스킬 관리 및 가이드
│   ├── SKILLS.md                    # 100+ 설치 스킬 종합 가이드 및 워크플로우 맵
│   ├── install-all-skills.sh        # 전역 스킬 원클릭 일괄 설치 스크립트
│   └── installed-skills.json        # 현재 머신에 설치된 전역 스킬 전체 메타데이터
├── mcp/                             # MCP (Model Context Protocol) 연동 및 서버
│   ├── README.md                    # MCP 서버 상세 연동 가이드
│   ├── mcp_config.template.json     # 동적 홈 디렉토리 치환 지원 MCP 마스터 템플릿
│   ├── .env.example                 # MCP 인증 토큰/키 환경변수 템플릿
│   └── servers/                     # 자체 제작 커스텀 MCP 서버 소스코드
│       ├── portainer/               # Synology DS1019+ Portainer REST API 연동 서버
│       └── portainer-ds920/         # Synology DS920+ Portainer (HTTPS) 연동 서버
├── setup.sh                         # 신규 머신 원클릭 환경 복원 스크립트
├── backup.sh                        # 현재 머신 최신 상태 자동 백업 및 GitHub 푸시 스크립트
└── README.md                        # 통합 운영 문서
```

---

## 🎯 13대 공통 운영 및 개발 지침 (Common Guidelines)

본 지침은 Synology NAS 및 관련 모든 애플리케이션 개발, 운영, 배포 시 필수적으로 준수해야 하는 공통 원칙입니다:

1. **양방향 GitHub 형상 동기화 원칙 (Bidirectional Git Sync)**:
   - 시놀로지 NAS(Portainer) 또는 로컬 변경 발생 시 즉시 대상 레포지토리에 커밋/푸시하여 항상 최신 형상 유지 (`git pull --rebase` 선행 충돌 방지).
2. **기술레포트 및 히스토리 필수 반영 원칙 (Documentation Principle)**:
   - 신규 구축, 장애 복구 시 `기술레포트.md` 상세 기록 및 타임라인(`제작히스토리.md`) 상시 갱신.
3. **네트워크 및 도메인 보안 연동 원칙**:
   - 외부 도메인(`danminlove.com`) 연동 시 NPM 역방향 프록시를 통해 HTTPS(443) 와일드카드 SSL 인증서 및 보안 설정 적용.
4. **시간대(KST) 및 일일 갱신 기준 표준화 (Timezone & Midnight Rollover)**:
   - 날짜 비교, 출석, 일일 퀘스트/퀴즈에는 UTC 단순 변환 금지, 한국 표준시(KST, Asia/Seoul) 헬퍼(`getKSTDateString()`) 공통 표준 사용.
5. **모바일 웹앱 라이프사이클 및 백그라운드 복귀 보장 (Mobile Lifecycle)**:
   - 화면 복귀 시 BFCache 이슈 방지를 위해 `visibilitychange`, `pageshow`, `focus` 기반 날짜/세션 전환 감지기 필수 적용.
6. **순수 실제 회원 기반 데이터 무결성 원칙 (No Mock Data in Production)**:
   - 리더보드/랭킹 등 서비스 핵심 화면에 하드코딩된 더미 가상 유저 잔존 금지, 영구 DB 기반 실시간 API 연동.
7. **보안 감사 로깅 및 관리자 인가 제어 (Audit Logging & RBAC)**:
   - 로그인/회원가입/중요 작업 이력을 클라이언트 IP, User-Agent, KST 일시와 함께 감사 로그에 안전하게 기록 및 관리자 권한 이중 보호.
8. **퀴즈/평가 선택지 동적 무작위화 원칙 (Dynamic Choice Randomization)**:
   - 1번 정답 편향 방지를 위해 출제 시 Fisher-Yates 알고리즘으로 동적 셔플 및 정답 인덱스 자동 재매핑.
9. **모바일 영구 로그인 세션 및 탄력적 인증 유지 원칙 (Persistent Auth Session)**:
   - 일시적 통신 지연이나 일시 5xx 에러로 인한 세션 삭제 방지, 오직 401 Unauthorized 수신 시에만 토큰 파기.
10. **게이미피케이션 상태 동기화 및 랭킹 분리 무결성 원칙 (Gamification & Dual-Ranking Integrity)**:
    - 방패, 찬스 아이템, 스트릭 상태의 영속성 보장 및 과목별 독립 랭킹/지표 분리 집계.
11. **Graphify 지식 그래프 연동 원칙 (Knowledge Graph Architecture)**:
    - 코드베이스 질의 시 `graphify query` / MCP 우선 질의 및 코드 변경 후 `graphify update .` 실행.
12. **코드 개발 및 분석 시 스킬 순차 적용 원칙 (Sequential Skill Application)**:
    - 6단계 핵심 스킬 파이프라인 순차 적용.
13. **중간매개체 레포지토리 기반 멀티 디바이스 형상 동기화 원칙 (Multi-Device Agent Environment Sync)**:
    - 환경 동기화 전용 레포지토리([agent-environment](https://github.com/mkotinet/agent-environment)) 상시 최신화 및 원클릭 복원 보장.

---

## ⚡ 6단계 스킬 순차 적용 파이프라인 (Sequential Skill Application)

모든 코드 작업 시 6개 핵심 스킬을 순차적으로 적용합니다:

```
1단계: karpathy-guidelines   --> LLM 코딩 행동 강령 최우선 준수 (Think Before Coding, Simplicity, Surgical, Goal-Driven)
   ▼
2단계: modern-web-guidance-src  --> 최신 웹 표준 & 가이던스 우선 검토 (Baseline 검증)
   ▼
3단계: public-apis              --> 외부 연동 & 1,400+ 무료 공개 API 생태계 우선 탐색
   ▼
4단계: agent-skills             --> Vercel & Addy Osmani 엔지니어링 표준/모범 사례 통합
   ▼
5단계: graphify                 --> 지식 그래프 기반 구조 탐색 및 영향도 분석
   ▼
6단계: super-powers             --> 브레인스토밍 -> 계획 -> TDD -> 증거 기반 완료 검증
```

---

## 🧩 설치된 스킬 카탈로그 요약

자세한 설명 및 워크플로우는 [`skills/SKILLS.md`](skills/SKILLS.md)를 참고하세요.

| 카테고리 | 스킬 수 | 대표 스킬 |
| :--- | :---: | :--- |
| **코딩 행동 강령 (Karpathy Guidelines)** | 1종 | `karpathy-guidelines` (Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven) |
| **최신 웹 표준 (Google Chrome)** | 15종 | `modern-web-guidance`, `baseline-status`, `browser-testing-with-devtools`, `chrome-extensions` 등 |
| **무료 공개 API 카탈로그** | 2종 | `public-apis`, `public-api-lookup` (1,400+ API) |
| **Addy Osmani 엔지니어링** | 25종 | `api-and-interface-design`, `ci-cd-and-automation`, `code-review-and-quality`, `security-and-hardening`, `test-driven-development` 등 |
| **Vercel 프레임워크 & UI** | 10종 | `deploy-to-vercel`, `impeccable`, `vercel-composition-patterns`, `vercel-react-best-practices`, `web-design-guidelines` 등 |
| **Superpowers 엔지니어링** | 15종 | `using-superpowers`, `brainstorming`, `writing-plans`, `systematic-debugging`, `verification-before-completion` 등 |
| **Google Workspace & Gmail** | 45종 | `gmail`, `gws-drive`, `gws-gmail`, `gws-calendar`, `gws-sheets`, 업무 자동화 레시피 20여 종 등 |
| **한국어 AI 텍스트 자연화** | 4종 | `humanize-korean`, `humanize-kr`, `humanize-scan`, `im-not-ai` |
| **지식 그래프 아키텍처** | 1종 | `graphify` (AST 기반 코드베이스 지식 그래프 질의 및 분석) |
| **Antigravity 빌트인 전용** | 11종 | `antigravity-guide`, `agy-customizations`, `automation`, `generative_ui`, `run-workflow`, `swarm` 등 |

---

## 🔌 MCP (Model Context Protocol) 연동 서버

자세한 설정 방법은 [`mcp/README.md`](mcp/README.md)를 참고하세요.

1. **`github`**: GitHub 공식 MCP (`@modelcontextprotocol/server-github`)
2. **`portainer`**: Synology DS1019+ Portainer REST API 연동 커스텀 서버 (`mcp/servers/portainer`)
3. **`portainer_ds920`**: Synology DS920+ Portainer REST API (HTTPS) 연동 커스텀 서버 (`mcp/servers/portainer-ds920`)
4. **`graphify`**: 지식 그래프 AST 탐색 MCP (`graphify-mcp`)

---

## 🚀 다른 맥북 / 노트북에서 원클릭 환경 복원 (Setup)

새로운 머신에서 아래 명령어 단 한 줄을 실행하면 즉시 현재 환경과 100% 동일하게 모든 지침, 스킬, 커스텀 MCP 서버가 자동 설치 및 구성됩니다.

```bash
git clone https://github.com/mkotinet/agent-environment.git
cd agent-environment
bash setup.sh
```

> **`setup.sh` 동작 과정**:
> 1. `~/.gemini/config/GEMINI.md`, `~/Documents/GEMINI.md`, `~/Documents/AGENTS.md`에 최신 13대 지침 자동 배포
> 2. `mcp/servers/`의 커스텀 Portainer MCP 서버를 `~/.gemini/mcp-servers/`에 배포하고 의존성 패키지 자동 설치
> 3. macOS 환경 감지 시 `kakao-mcp` (카카오톡 로컬 연동 MCP) 복제 및 의존성 환경(`kakaocli`, `kmsg`, Python 패키지) 자동 복원
> 4. 현재 사용자의 `$HOME` 디렉토리를 자동 감지하여 `~/.gemini/config/mcp_config.json` 템플릿 생성
> 5. `npx skills`를 통해 50여 개 전역 스킬 및 `im-not-ai`, `graphify` 일괄 설치

---

## 🔄 현재 머신에서 변경사항 발생 시 자동 백업 & 푸시 (Backup)

현재 작업 머신에서 새로운 지침을 추가하거나, 신규 스킬을 설치하거나, MCP 설정을 수정한 경우 아래 스크립트를 실행하면 즉시 이 레포지토리에 반영 및 GitHub 푸시가 완료됩니다.

```bash
cd /Users/kotinet/Documents/GIT/agent-environment
bash backup.sh
```

---

## 🔐 보안 및 민감정보 보호 원칙

- GitHub 원격 레포지토리에 푸시할 때 실제 API 시크릿, 개인 액세스 토큰(PAT), 비밀번호 등은 절대로 커밋되지 않습니다.
- MCP 인증 정보는 `mcp/mcp_config.template.json` 및 `mcp/.env.example`을 통해서만 공유되며, 실제 값은 로컬 머신의 `~/.gemini/config/mcp_config.json`에만 안전하게 보관됩니다.
