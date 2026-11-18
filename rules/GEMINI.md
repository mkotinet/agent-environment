# 공통 운영 및 개발 지침 (Common Guidelines)

본 지침은 Synology NAS 및 관련 모든 애플리케이션 개발, 운영, 배포 작업 시 필수적으로 준수해야 하는 공통 원칙입니다.

---

## 1. 양방향 GitHub 형상 동기화 원칙 (Bidirectional Git Sync)
* **실시간 / 상시 동기화**:
  * 시놀로지(Synology NAS Portainer) 또는 로컬에서 앱 설정, 소스 코드, Docker Compose 설정, NPM 라우팅 등이 변경되었을 경우, 변경된 모든 코드는 즉시 대상 GitHub 레포지토리에 커밋 및 푸시하여 양방향 최신 상태를 유지합니다.
  * 신규 추가되거나 변경된 도커 컨테이너는 반드시 `docker-compose.yml` 및 관련 설정 파일 형태로 해당 레포지토리에 빠짐없이 버전 관리합니다.
* **충돌 방지 및 안전 동기화**:
  * 서버 자동 백업 스크립트나 동기화 배치 구동 시, 원격 변경사항을 안전하게 병합하기 위해 `git pull --rebase`를 선행한 후 푸시하여 `fetch first` 충돌을 방지합니다.
* **민감정보 보호**:
  * GitHub 푸시 시 API 시크릿, 개인 액세스 토큰(PAT), 비밀번호 등 민감 정보가 소스에 하드코딩되지 않도록 주의합니다.

---

## 2. 기술레포트 및 히스토리 필수 반영 원칙 (Documentation Principle)
* **기술레포트 (`기술레포트.md`) 상시 작성**:
  * 앱 신규 구축, 장애 복구, 인프라 고도화, SSL/HTTPS 연동, 네트워크 설정 등 주요 변경 시 아키텍처, 장애 원인(RCA), 해결 절차, 엔드포인트 검증 결과를 `기술레포트.md`에 상세히 기록합니다.
* **제작히스토리 (`제작히스토리.md` / `히스토리.md`) 타임라인 기록**:
  * 작업 일시, 단계별 수행 타임라인, 생성 및 수정된 산출물 목록을 지속적으로 업데이트하여 유지보수 추적성을 확보합니다.
* **코드 개선 및 변경 후 문서 깃허브 필수 동기화**:
  * 모든 코드 개선 및 기능 변경 작업 완료 후에는 `기술레포트.md`와 `제작히스토리.md`(`히스토리.md`)를 반드시 업데이트하고, 소스 코드와 함께 대상 GitHub 레포지토리에 빠짐없이 커밋 및 푸시하여 영구 버전 관리합니다.

---

## 3. 네트워크 및 도메인 보안 연동 원칙
* **HTTPS & Cloudflare 표준화**:
  * 외부 도메인(`danminlove.com`) 연동 시 NPM 역방향 프록시를 통해 HTTPS(443 포트) 및 와일드카드 SSL 인증서를 적용하고, WebSocket 및 Block Exploits 보안 설정을 기본 활성화합니다.

---

## 4. 시간대(KST) 및 일일 갱신 기준 표준화 (Timezone & Midnight Rollover)
* **한국 표준시(KST, Asia/Seoul) 일관 적용**:
  * 날짜 비교, 출석 체크, 일일 퀘스트/퀴즈 생성, 랭킹 리셋 등 일일(Daily) 갱신 로직에는 단순 `toISOString().split('T')[0]`(UTC 기준) 사용을 엄격히 금지합니다. (새벽 00:00~08:59 시간대 날짜 오류 방지)
  * 클라이언트와 서버 모두 `Intl.DateTimeFormat` 등을 활용한 한국 표준시 기준 날짜 헬퍼(`getKSTDateString()`)를 공통 표준으로 적용합니다.

---

## 5. 모바일 웹앱 라이프사이클 및 백그라운드 복귀 보장 (Mobile Lifecycle)
* **모바일 백그라운드 복귀 및 BFCache 대응**:
  * 모바일 브라우저(Safari, Chrome 등)에서 창을 닫지 않고 화면을 껐다가 다음 날 다시 열 경우, 페이지 새로고침 없이 이전 메모리 상태가 유지되는 문제를 방지합니다.
  * `visibilitychange`, `pageshow`, `focus` 이벤트 및 주기적 타이머 기반의 **날짜/세션 감지기(`checkDateTransition`)**를 필수 구현하여, 자정이 지난 후 복귀 시 출석 캘린더 요일 이동, 일일 진행도 초기화, 최신 콘텐츠 갱신이 자동 수행되도록 합니다.

---

## 6. 순수 실제 회원 기반 데이터 무결성 원칙 (No Mock Data in Production)
* **운영 환경 더미/가상 데이터 잔존 금지**:
  * 랭킹, 사용자 통계, 리더보드 등 서비스 핵심 화면에 하드코딩된 가상 더미 유저나 클라이언트 목(Mock) 데이터를 일절 남기지 않습니다.
  * 모든 통계와 순위는 서버 영구 저장소(DB)의 실제 회원 데이터를 기반으로 실시간 REST API를 통해 집계 및 제공합니다.

---

## 7. 보안 감사 로깅 및 관리자 인가 제어 (Audit Logging & RBAC)
* **이용 기록 감사 추적성 확보**:
  * 로그인(성공/실패), 회원가입, 세션 갱신, 중요 작업 완료 이력은 클라이언트 IP(프록시 헤더 고려), User-Agent, 작업 일시(KST)와 함께 서버 감사 로그(최대 건수 자동 로테이션)에 안전하게 기록합니다.
* **관리자 전용 기능 보호**:
  * 전체 회원 감사 로그, 시스템 관리 등 민감 관리자 엔드포인트 및 UI는 사이트 대표 계정(예: `단민러브`) 등 인가된 특정 권한에 의해서만 접근할 수 있도록 이중 보호합니다.

---

## 8. 퀴즈/평가 선택지 동적 무작위화 원칙 (Dynamic Choice Randomization)
* **정답 위치 편향 원천 차단**:
  * 문제은행 데이터베이스 관리 시 편의상 1번(Index 0)에 정답이 주로 배치되더라도, 사용자 출제 시에는 반드시 Fisher-Yates 알고리즘 등을 통해 선택지 순서를 동적으로 셔플하고 정답 인덱스(`answerIndex`)를 자동 재매핑합니다.
  * 연속 문제 풀이 시 특정 번호로 정답이 고정 노출되는 UX 결함을 방지하고, 정답 텍스트 무결성을 100% 유지합니다.

---

## 9. 모바일 영구 로그인 세션 및 탄력적 인증 유지 원칙 (Persistent Auth Session)
* **네트워크 지연 및 일시 에러 시 세션 보호**:
  * 모바일 화면을 켠 직후의 일시적 통신 지연(오프라인), 서버 일시 5xx 에러 등으로 인해 로컬스토리지 토큰이 섣불리 삭제(로그아웃)되지 않도록 보호합니다.
  * 토큰 파기는 오직 서버로부터 명시적인 `401 Unauthorized`를 수신했을 때만 수행하며, 그 외에는 캐시된 인증 정보를 유지하고 `online` 이벤트 시 조용히 백그라운드 재동기화를 수행합니다.
* **서버 저장소 영속성 보장**:
  * 도커 컨테이너의 영구 데이터 볼륨(`/app/data`)을 서버 코드 레벨에서 우선 감지하여, 컨테이너 재시작 및 재배포 시에도 세션 토큰과 유저 정보가 유실되지 않도록 보장합니다.

---

## 10. 게이미피케이션 상태 동기화 및 랭킹 분리 무결성 원칙 (Gamification & Dual-Ranking Integrity)
* **게임 상태 및 아이템 영속성 보장**:
  * 방패(Shield), 찬스 아이템(50:50, 하트, 부스터), 연속 만점 스트릭 등 게이미피케이션 상태는 브라우저 새로고침이나 모바일 앱 복귀 시에도 유실되지 않도록 로컬스토리지 및 서버 계정과 유기적으로 동기화합니다.
* **과목별 독립 랭킹 및 지표 분리**:
  * 서비스 내 학습 과목(예: 국어 맞춤법 vs 한자·고사성어)이 다변화될 경우, 도달 최고 라운드(`maxRound`), 일간 점수, 누적 포인트를 과목별로 엄격히 분리 집계하여 특정 과목 쏠림 현상을 방지하고 다양한 동기부여 경로를 제공합니다.

---

## 11. Graphify 지식 그래프 연동 원칙 (Knowledge Graph Architecture)
* **코드베이스 및 아키텍처 질의 시 지식 그래프 우선 참조**:
  * 프로젝트 내 `graphify-out/graph.json`이 존재하는 경우, 맹목적인 `grep`이나 대량 파일 탐색 전에 `graphify query "<질문>"`(CLI) 또는 `query_graph`(MCP), 관계 파악을 위한 `graphify path "<A>" "<B>"` / `shortest_path`, 핵심 개념 분석을 위한 `graphify explain "<개념>"` / `get_node`를 우선적으로 활용합니다.
  * `graphify-out/wiki/index.md`가 존재하면 원시 코드 파일을 직접 읽기 전에 위키 구조를 우선 탐색합니다.
  * `graphify-out/GRAPH_REPORT.md`는 전체적인 시스템 아키텍처 조망 및 주요 고위험 결합도(God nodes) 확인 시 참조합니다.
  * 세션 내에서 파일 생성/수정 등 코드베이스 변경 작업이 발생한 후에는 `graphify update .`를 실행하여 AST 기반 최신 그래프 상태를 유지합니다.
  * 신규 프로젝트 또는 지식 그래프가 없는 경우 `/graphify .` 명령어로 손쉽게 그래프를 생성합니다.

---

## 12. 코드 개발 및 분석 시 스킬 순차 적용 원칙 (Sequential Skill Application)
코드 개발, 수정, 점검, 리팩토링, 기능 구현 및 아키텍처 분석 시 다음 7가지 핵심 스킬 파이프라인을 **순차적으로** 적용하여 최고 수준의 품질과 최신 웹 표준, 영속적 맥락 보존 및 결함 없는 간결한 코드를 달성합니다:

1. **1단계: `karpathy-guidelines` (LLM 코딩 원칙 및 행동 강령 최우선 준수)**
   * **Think Before Coding (코딩 전 심층 사고)**: 암묵적 가정(Assumption)을 엄격히 배제하고 명시화하며, 모호한 요구사항이나 다중 해석이 존재할 경우 혼자 넘겨짚지 않고 질문합니다. 단순한 대안이 있다면 먼저 제시하고 트레이드오프를 투명하게 공개합니다.
   * **Simplicity First (단순함 우선 / 과잉 설계 원천 차단)**: 요청하지 않은 추상화(단일 사용 함수/클래스 분리 등), 미래 대비용 확장성(Speculative generality), 불필요한 설정 추가를 엄격히 금지합니다. 50줄로 해결할 수 있는 문제를 200줄로 늘리지 않으며, 오늘 당장 요구된 최소한의 간결한 코드만 작성합니다.
   * **Surgical Changes (외과수술식 정밀 수정)**: 버그 수정 및 기능 추가 시 요청과 무관한 주변 코드 포맷, 주석, 타입, 레거시 코드를 임의로 리팩터링("Drive-by refactoring")하지 않습니다. 오직 자신의 작업으로 인해 발생한 고아 코드(미사용 import/변수)만 정리하며, 모든 수정 라인은 반드시 사용자의 요구사항에 직접 연결되어야 합니다.
   * **Goal-Driven Execution (목표 지향적 검증)**: "알아서 잘 동작하게 만들기" 같은 모호한 실행을 지양하고, 검증 가능한 명확한 완료 조건(성공 기준)과 단계별 계획을 수립한 후 재현 테스트 및 자동화 검증 루프를 통해 증거 기반으로 완료합니다.

2. **2단계: `agentmemory` (지속 기억 기반 컨텍스트 회상 및 교훈 반영)**
   * **Recall Before Work (작업 전 기억 회상)**: 코드 작성이나 디버깅 착수 전, 과거 유사 작업의 의사결정, 프로젝트 고유 제약사항, 해결된 Gotcha, 과거 사용자 교정 교훈(`lesson`)을 사전 회상(`recall`, `memory-discipline`)하여 동일 실수를 반복하지 않습니다.
   * **Save at Decision Points (결정 순간 즉시 기록)**: 아키텍처 결정이 내려지거나 난해한 버그의 원인이 규명된 즉시, 이유(Reason)와 파일 경로, 구체적 개념 태그와 함께 영구 메모리에 기록(`remember`)합니다. 세션 종료 후 일괄 저장은 맥락과 이유가 유실되므로 금지합니다.
   * **Learn from Corrections (피드백의 교훈 승격)**: 사용자가 접근법이나 코드를 교정했을 경우 단순 사실이 아닌 향후 행동 지침인 교훈(`lesson`)으로 저장하여 다음 유사 작업 시 최우선 반영합니다.

3. **3단계: `modern-web-guidance-src` (최신 웹 표준 & 가이던스 우선 검토)**
   * 최신 HTML/CSS/JS 기능(Popover, Dialog, View Transitions, Container Queries, Scroll-driven Animation, Baseline 호환성 등) 구현 시 낡은 레거시 패턴 대신 최신 표준 가이던스를 검색(`npx modern-web-guidance search`) 및 적용합니다.
   * 브라우저 호환성 및 Baseline 상태를 `baseline-status` 등을 통해 사전 검증합니다.

4. **4단계: `public-apis` (외부 연동 및 무료 공개 API 생태계 우선 탐색)**
   * 외부 서비스 연동, Mock/테스트 데이터, 인증(OAuth/BaaS), 결제, 지도/LBS, 날씨, AI/ML, 소셜, 미디어 처리 등 서드파티 기능이 요구되는 경우, 임의의 유료 서비스나 불완전한 ad-hoc API를 도입하기 전에 `public-apis` 카탈로그(1,400+ API) 및 `public-api-lookup` 스킬을 우선 조회합니다.
   * 인증 방식(무인증/apiKey/OAuth), HTTPS 및 CORS 지원 여부를 사전 확인하여 프론트엔드/백엔드 아키텍처에 가장 적합하고 안정적인 무료 공개 API를 선제적으로 매핑 및 통합합니다.

5. **5단계: `agent-skills` (엔지니어링 표준 및 모범 사례 통합)**
   * `vercel-react-best-practices`, `web-design-guidelines`, `vercel-composition-patterns` 등 프레임워크 최적화 규칙을 준수합니다.
   * `frontend-ui-engineering`, `code-review-and-quality`, `security-and-hardening`, `performance-optimization` 등 Addy Osmani 엔지니어링 스킬을 통해 아키텍처와 코드를 고도화합니다.

6. **6단계: `graphify` (지식 그래프 기반 탐색 및 영향도 분석)**
   * 변경 전: `query_graph`, `shortest_path`, `get_node` 등을 통해 의존성 및 결합도(God nodes)를 파악합니다.
   * 변경 후: 반드시 `graphify update .`를 실행하여 지식 그래프를 최신 상태로 유지합니다.

7. **7단계: `super-powers` (체계적 프로세스 및 무결성 검증)**
   * `brainstorming` 및 `writing-plans`로 선계획을 수립하고, `systematic-debugging` 및 `test-driven-development`로 구현합니다.
   * 최종 완료 전 `verification-before-completion`을 필수로 수행하여 실제 테스트 및 런타임 결과 증거를 확인한 후 작업을 마무리합니다.

---

## 13. 중간매개체 레포지토리 기반 멀티 디바이스 형상 동기화 원칙 (Multi-Device Agent Environment Sync)
* **환경 동기화 전용 레포지토리 상시 최신화 (`mkotinet/agent-environment`)**:
  * 전역 지침(Rules), 설치된 에이전트 스킬(Skills), MCP 서버 설정(`mcp_config.json`)이 신규 추가되거나 변경될 경우, 즉시 중간매개체 GitHub 레포지토리([agent-environment](https://github.com/mkotinet/agent-environment))에 동기화 커밋 및 푸시하여 항상 최신 상태를 유지합니다.
* **다른 노트북 및 맥북 간 완벽한 이식성(Portability) 보장**:
  * 신규 또는 다른 맥북/노트북 환경에서 `git clone` 후 `bash setup.sh` 단 한 줄의 명령어로 지침, 스킬, MCP 환경이 100% 동일하게 복원 및 동기화될 수 있도록 레포지토리 내 자동화 스크립트와 템플릿을 철저히 유지관리합니다.
* **민감 정보 보호 및 템플릿 분리 원칙**:
  * GitHub 푸시 시 개인 액세스 토큰(PAT), 비밀번호, 외부 서비스 API 키 등 시크릿 정보는 `mcp_config.template.json` 및 `.env` 템플릿으로 추상화하여 민감정보가 외부에 노출되지 않도록 엄격히 보호합니다.
