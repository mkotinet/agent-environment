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

## 3. 네트워크 및 도메인 보안 연동 및 공인 SSL 무장애 표준화 원칙 (NPM Reverse Proxy & Zero-Warning SSL)
* **신규 앱 개발 완료 직후 시놀로지 1019+ MCP 연계 NPM 서브도메인 원스톱 자동 등록 의무화**:
  * 신규 앱/서비스 개발 및 포테이너 스택 배포가 완료되면, 사용자가 수동으로 NPM 웹 UI에 들어가 설정하지 않도록 **시놀로지 DS1019+ Portainer Docker Exec API를 연동하여 NPM 컨테이너 내부에서 서브도메인(`*.danminlove.com`) 등록 및 공인 Let's Encrypt 정식 SSL 발급, Nginx 리로드까지 원스톱으로 즉시 자동 완결**합니다.
* **자체 서명(Self-signed) 인증서 단독 연결 원천 금지**:
  * `*.danminlove.com` 자체 서명 와일드카드 인증서만 연결할 경우, Cloudflare를 거치지 않는 직접 접속이나 특정 모바일 브라우저(Safari, Chrome 등)에서 "연결이 비공개로 설정되어 있지 않습니다 (`NET::ERR_CERT_AUTHORITY_INVALID`)" 보안 경고가 발생하므로 이를 단독으로 남겨두지 않습니다.
* **시놀로지 1019+ Portainer Exec 기반 NPM 서브도메인 & 공인 SSL 자동화 5대 절차**:
  1. **NPM 컨테이너 Exec 연동**:
     DS1019+ Portainer(Endpoint ID: `3`)의 NPM 컨테이너(`7665696692b3`, `/npm`)를 대상으로 Docker Exec API(`http://djms1.iptime.org:9000/api/endpoints/3/docker/containers/7665696692b3/exec`) 채널을 확보합니다.
  2. **공인 Certbot 정식 발급 자동화**:
     NPM 컨테이너 내부에서 Webroot 기반 HTTP-01 챌린지를 무인 실행하여 정식 인증서를 즉시 발급받습니다:
     `certbot certonly --webroot -w /data/letsencrypt-acme-challenge --cert-name <앱이름>_official --email minkim@danminlove.com --agree-tos --no-eff-email --non-interactive -d <도메인>`
  3. **Custom SSL 키체인 배치 및 SQLite DB 자동 등록**:
     발급된 인증서를 `/data/custom_ssl/npm-<CertID>/{fullchain.pem, privkey.pem}`으로 배치하고, `/data/database.sqlite`의 `certificate` 테이블에 자동 등록(Max ID + 1)합니다.
  4. **Proxy Host DB 등록 및 Nginx 가상호스트 생성**:
     `/data/database.sqlite`의 `proxy_host` 테이블에 등록(도메인, 포워딩 호스트 IP/포트, `certificate_id`, `ssl_forced: 1`, `http2_support: 1`, `allow_websocket_upgrade: 1`, `block_exploits: 1`)하고, `/data/nginx/proxy_host/<HostID>.conf` 가상호스트 설정 파일을 표준 생성한 후 `nginx -t && nginx -s reload`로 무중단 적용합니다.
  5. **엄격한 공인 SSL 체인 검증 의무화**:
     작업 완료 보고 전 반드시 `curl -v https://<도메인>/` (보안 무시 `-k` 옵션 엄격히 배제) 명령어로 `SSL certificate verify ok` 및 공인 CA(ISRG / Let's Encrypt) 서명을 최종 증거 기반으로 검증한 후 사용자에게 인도합니다.

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
코드 개발, 수정, 점검, 리팩토링, 기능 구현 및 아키텍처 분석 시 다음 9단계 핵심 파이프라인을 **순차적으로** 적용하여 최고 수준의 품질과 최신 웹 표준, 영속적 맥락 보존, 최적화된 프레임워크 아키텍처 및 결함 없는 간결한 코드를 달성합니다:

0. **0단계: `트러블슈팅.md` (개인 커스텀 오류 검증·해결 기술노트 최우선 사전 검토)**
   * **Pre-Review Before Action (작업 착수 전 오류 자산 최우선 검토)**: 코드 작성, 버그 수정, 리팩토링, 기능 구현 및 배포 검토 착수 전, 대상 프로젝트의 `트러블슈팅.md`(`오류해결노트.md`)를 **반드시 가장 먼저 읽고 검토**합니다.
   * **Gotcha & Failure Pattern Inoculation (실패 패턴 사전 면역)**: 과거 해당 앱이나 유사 환경에서 발생했던 런타임 오류, 이벤트 버블링/터치 충돌, 전역 함수 누락(ReferenceError), DOM ID 불일치(TypeError), 인라인 이스케이프 파싱 오류, PWA 캐시 고착화 등의 선례를 사전에 숙지하여 동일한 실수를 0%로 원천 차단하고 검증된 해결 패턴을 즉각 적용합니다.
   * **Live Update of Troubleshooting Asset (해결 즉시 자산 갱신)**: 새로운 오류를 규명하고 검증을 마쳤을 경우, 즉시 `트러블슈팅.md`에 증상, RCA, 해결 기술, 검증 결과를 추가하여 지식 자산을 상시 최신화합니다.

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

5. **5단계: `vercel-framework-and-ui` (Vercel 프레임워크 & UI/UX 최적화 필수 적용)**
   * **React/Next.js 성능 최적화 (`vercel-react-best-practices`)**: 불필요한 클라이언트 사이드 렌더링을 지양하고 서버 컴포넌트(RSC)를 우선 활용하며, 워터폴(Waterfall) 데이터 페칭 제거 및 JS 번들 크기를 최소화합니다.
   * **컴포넌트 합성 아키텍처 (`vercel-composition-patterns`)**: 단일 컴포넌트 내 무분별한 불리언 Prop 증식(Prop Proliferation)을 엄격히 방지하고, Compound Components 및 Context 분할을 통해 유지보수성과 확장성을 확보합니다.
   * **프로덕션 수준 UI/UX 디자인 시스템 (`impeccable`, `web-design-guidelines`)**: 아마추어 AI 생성물 특유의 엉성한 디자인을 원천 배제하고, 타이포그래피 위계, 접근성(WCAG 2.1 AA+ 대비), 정교한 간격/여백, 일관된 디자인 토큰(`DESIGN.md`)을 준수합니다.
   * **자연스러운 뷰 트랜지션 (`vercel-react-view-transitions`)**: React `<ViewTransition>` 및 CSS View Transition을 적용하여 페이지/컴포넌트 전환 시 부드러운 네이티브 앱 수준의 인터랙션을 구현합니다.
   * **서버리스 런타임 & 비용 최적화 (`vercel-optimize`)**: 불필요한 서버리스 함수 호출 및 빌드 시간을 줄이고, 엣지 캐싱 및 Fast Data Transfer 비용을 최적화합니다.
   * **모바일/PC 반응형 듀얼 최적화 & 뷰포트 공간 극대화 (`frontend-ui-engineering`, 원칙 19 연동)**: 상단 메뉴바 접기/1행 요약바 전환, 100vw × 100vh Zen 몰입형 전체화면, PC 와이드 스크린 반응형 그리드 & 단축키, 모바일 상세 필터 자동 접힘 및 사이드 패널의 슬라이드업 바텀 시트 전환을 필수로 구현합니다.

6. **6단계: `agent-skills` (Addy Osmani 시니어 풀스택 엔지니어링 표준)**
   * `api-and-interface-design`: 모듈 경계 간 견고한 타입 계약과 안정적인 REST/GraphQL API를 설계합니다.
   * `frontend-ui-engineering` & `code-review-and-quality`: 반응형 레이아웃 및 다축 심층 코드 리뷰를 수행합니다.
   * `security-and-hardening` & `performance-optimization`: OWASP 보안 규칙, 입력값 검증, DB 쿼리 최적화 및 Core Web Vitals를 강화합니다.

7. **7단계: `graphify` (지식 그래프 기반 탐색 및 영향도 분석)**
   * 변경 전: `query_graph`, `shortest_path`, `get_node` 등을 통해 의존성 및 결합도(God nodes)를 파악합니다.
   * 변경 후: 반드시 `graphify update .`를 실행하여 지식 그래프를 최신 상태로 유지합니다.

8. **8단계: `super-powers` (체계적 프로세스 및 무결성 검증)**
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

---

## 14. 오피스·문서 첨부파일 마크다운 변환 및 토큰 최적화 원칙 (Office & PDF Token Optimization via MarkItDown-Excel)
* **비정형 문서 첨부 시 선제적 마크다운 변환 의무화**:
  * 사용자가 Excel(`.xlsx`, `.xlsm`, `.xls`, `.csv`), Word(`.docx`), PowerPoint(`.pptx`), PDF(`.pdf`), HTML 등 오피스 및 비정형 문서를 첨부하거나 분석을 요청할 경우, 대용량 바이너리나 원시 텍스트를 컨텍스트에 그대로 읽어 토큰을 낭비하지 않습니다.
  * 반드시 선제적으로 `markitdown-excel <파일명> -o <출력경로.md>` CLI 도구(또는 `markitdown-excel` 스킬)를 가동하여 정제된 GFM(GitHub Flavored Markdown) 규격으로 변환한 후 필요한 부분만 정밀하게 읽고 분석함으로써 **컨텍스트 토큰을 극대화하여 절감**합니다.
* **복잡한 엑셀(Excel) 4대 전처리 필수 준수**:
  * 엑셀 파일 분석 시에는 단순 텍스트 추출이나 판다스(Pandas) 단독 읽기를 지양하고, `markitdown-excel`의 전처리 파이프라인을 필수로 거칩니다:
    1. **다중 시트(Multi-Sheet)**: 시트 누락 없이 전 시트를 목차(TOC)와 앵커 섹션으로 구조화하여 탐색.
    2. **병합 셀 해제 및 값 전파(Smart Unmerge & Fill)**: 병합된 행/열에 부모 값을 자동 전파하여 레코드 무결성을 유지하고, 전폭 타이틀 행은 표 상단 캡션으로 승격.
    3. **수식 및 계산값 동시 병기**: 표 내 인라인 병기(`값 (fx: =SUM(...))`) 또는 각주 모드(`--formula-mode footnote`)를 활용하여 계산 결과와 산출 근거(Formula Breakdown 맵)를 투명하게 보존.
    4. **조건부 서식 및 셀 색상 텍스트화**: 셀 배경색과 조건부 서식 룰을 분석하여 `⚠️[경고]`, `🔴[위험]`, `✅[달성]`, `⚡[검토]`, `📌[강조]` 텍스트 뱃지로 변환함으로써 시각적 상태 정보를 텍스트화하여 컨텍스트에 반영.

---

## 15. 모바일 웹앱 PWA(Progressive Web App) 표준화 및 원스톱 설치·알림 의무화 원칙 (Mobile PWA Standard & Zero-Friction Install/Notification)
모든 신규 웹 애플리케이션 및 모바일 웹 서비스 구축 시, 사용자가 네이티브 앱과 동일한 사용 경험을 누릴 수 있도록 다음 5대 PWA 핵심 요소를 필수적으로 기본 탑재합니다:

* **1) 무캐시 Web App Manifest (`manifest.json`) & 아이콘 표준화**:
  * `id`: `/?pwa=1`, `start_url`: `/?pwa=1`, `display: "standalone"`, `orientation: "portrait"`을 명시하여 독립 앱 창으로 구동되도록 합니다.
  * 모바일 브라우저 캐시로 인한 설치 지연/구버전 고착을 방지하기 위해 백엔드 서빙 시 `Cache-Control: no-cache, no-store, must-revalidate` 헤더를 필수 지정합니다.
  * 고해상도 규격 아이콘(192x192, 512x512, apple-touch-icon 180x180)을 빠짐없이 배치하고 HTML 헤더에 `<link rel="manifest" href="/manifest.json">`, `<meta name="mobile-web-app-capable" content="yes">`, `<meta name="apple-mobile-web-app-capable" content="yes">`, `<meta name="theme-color">`를 기본 등록합니다.
* **2) 네트워크 우선(Network-First) 서비스 워커 (`sw.js`) 기본 배포**:
  * 오프라인 또는 불안정한 통신 환경에서도 최소한의 앱 쉘(Shell)이 정상 표시되도록 캐시 전략(Network-First with Cache Fallback)을 수립합니다.
  * 새 버전 배포 시 브라우저가 신속하게 새 리소스를 내려받을 수 있도록 서비스 워커 생명주기(`skipWaiting()`, `clients.claim()`) 및 버전별 캐시 자동 정리 로직을 내장합니다.
  * 서비스 워커 스코프 헤더(`Service-Worker-Allowed: /`)를 보장합니다.
* **3) `beforeinstallprompt` 최우선 캡처 & 원클릭 설치 배너/버튼 필수 제공**:
  * 스크립트 로드 최상단에서 `window.addEventListener('beforeinstallprompt')`를 선제적으로 바인딩하여 브라우저의 기본 설치 이벤트가 유실되지 않도록 캡처합니다.
  * 웹앱 상단에 눈에 띄는 **고정 설치 유도 배너(`[📱 홈 화면에 바로가기 앱 추가하기 📥]`)** 및 헤더 설치 버튼을 기본 배치하여, 터치 한 번으로 설치 팝업(`deferredPrompt.prompt()`)이 즉시 호출되도록 구현합니다.
* **4) 안드로이드/iOS 브라우저별 설치 분기 가이드 완비 (`modalPwaGuide`)**:
  * **구글 크롬(Android)**: 상단 배너 또는 주소창 우측 [설치 📥] 버튼으로 100% 독립 WebAPK 즉시 설치 지원.
  * **삼성인터넷**: `[더보기]` ➔ `[현재 페이지 추가]` 시 단순 `[홈 화면]`(단순 북마크)이 아닌 **`👉 [앱 (App)]`**을 선택해야 네이티브 WebAPK로 등록됨을 팝업으로 명확히 안내.
  * **네이버 웨일**: 브라우저 자체 정책상 독립 앱(WebAPK)이 아닌 웨일 뱃지 북마크로 저장되므로, 독립 창 구동 및 실시간 알림을 원할 경우 크롬 또는 삼성인터넷 사용 권장 안내 제공.
  * **아이폰(iOS Safari)**: 하단 `[공유 ⎋]` ➔ `[홈 화면에 추가 ➕]` 3초 가이드 팝업 지원.
* **5) 시스템 웹 알림(Web Notification & Push) 연동 기반 구축**:
  * 중요한 공지, 가족/채팅 메시지, 긴급 알림, 일일 퀘스트/리셋 등의 이벤트를 앱이 닫힌 상태에서도 수신할 수 있도록 `Notification.requestPermission()` 권한 요청 UI(`[🔔 알림 켜기]`)를 기본 제공합니다.
  * 권한 획득 시 서비스 워커 `showNotification` 또는 브라우저 `new Notification`을 통해 안드로이드 상단 시스템 알림바(소리/진동) 배너로 실시간 팝업되도록 설계합니다.

---

## 16. 실시간 버전 감지·자동 캐시 갱신 및 업데이트 릴리스 보고 원칙 (Live Version Rollover & What's New Release Modal)
모든 웹 애플리케이션 및 모바일 웹 서비스는 배포 후 사용자가 브라우저 구버전 캐시에 머무르는 현상을 방지하고 최신 개선 사항을 즉시 체감할 수 있도록 **하루퀴즈 표준 4단계 릴리스 파이프라인(버전 메타데이터 서빙 ➔ 실시간 버전 비교 ➔ 무한루프 방지 캐시 소거 및 강제 갱신 ➔ 업데이트 보고 모달 자동 표출)**을 필수로 기본 구현합니다:

* **1) 버전 메타데이터 규격화 및 무캐시 서빙 (`version.json` & `/api/version`)**:
  * 프로젝트 루트에 `version.json`을 배치하고 `{ "version": "X.Y.Z", "build": "YYYYMMDD_HHMM", "name": "앱명칭", "releaseNotes": "업데이트 요약", "features": [{ "icon": "...", "title": "...", "desc": "..." }] }` 메타데이터 규격을 항시 유지합니다.
  * 백엔드 API(`/api/version`, `/version.json`)는 모바일 및 프록시 캐시를 차단하기 위해 `Cache-Control: no-cache, no-store, must-revalidate` 헤더로 응답합니다.
  * HTML 헤더에 `<meta name="app-version" content="X.Y.Z">` 및 번들 스크립트 쿼리스트링(`app.js?v=X.Y.Z`)을 주입하여 클라이언트가 자신의 버전을 정확히 인지하도록 합니다.
* **2) 시작 및 백그라운드 복귀 시 실시간 버전 감지 (`checkAppVersionUpdate`)**:
  * 앱 최초 진입 시(`DOMContentLoaded` 후 1~1.5초 딜레이) 및 모바일 백그라운드 복귀(`visibilitychange`, `pageshow`, `focus`) 시 `fetch('/api/version?_t=' + Date.now(), { cache: 'no-store' })`를 호출하여 서버 최신 버전을 비동기 조회합니다.
  * 세맨틱 버저닝(`isServerVersionNewer`)을 통해 서버 버전이 클라이언트 버전보다 높을 경우 즉각적인 업데이트 절차에 돌입합니다.
* **3) 무한 루프 방지(Loop Guard) & 브라우저 캐시 소거 후 강제 갱신 (`forcePageReload`)**:
  * 브라우저 캐시 고착으로 인한 무한 새로고침 핑퐁을 원천 방지하기 위해 `sessionStorage`에 `auto_reload_to_<serverVersion>` 플래그와 타임스탬프를 기록하여 60초 내 중복 재시도를 차단합니다.
  * 갱신 직전 토스트 안내(`🚀 새 버전(vX.Y.Z)으로 업데이트되었습니다. 최신 화면으로 새로고침합니다...`)를 표출합니다.
  * `caches.keys()` 순회 및 `caches.delete()`로 브라우저 CacheStorage를 소거하고, 캐시 버스팅 파라미터(`_v=X.Y.Z&_t=Date.now()`)를 붙여 `window.location.replace()`로 새 화면을 즉시 로드합니다.
* **4) 갱신 직후 '새로운 기능 / 업데이트 보고창'(`modalWhatsNew`) 자동 팝업**:
  * 강제 갱신 완료 후 앱 홈 화면 로드 시(`checkWhatsNewPopup`, 0.6초 딜레이) `localStorage`의 `dismissed_update_version`을 확인합니다.
  * 현재 버전과 일치하지 않는 경우(즉, 이번 업데이트 후 처음 화면을 연 경우), **업데이트 보고창 모달(`#modalWhatsNew`)**을 화면 중앙에 자동으로 띄웁니다.
  * 보고창에는 **새 버전 뱃지(`vX.Y.Z`), 릴리스 일시, 릴리스 노트 요약문, 핵심 변경 기능 카드 목록**을 시각적으로 일목요연하게 렌더링합니다.
  * 사용자가 `[확인하고 계속하기]` 또는 닫기를 누르면 `localStorage.setItem('dismissed_update_version', currentVersion)`을 영구 저장하여 이후 재접속 시에는 팝업되지 않도록 제어합니다.

---

## 17. 모바일 팝업·바텀시트 하단 잘림 방지 및 뷰포트 반응형 보장 원칙 (Mobile Zero-Cut Modal & Viewport Responsive Standard)
모든 웹 애플리케이션 및 모바일 웹 서비스는 다양한 모바일 기기(스마트폰, 폴더블폰, 태블릿)의 화면 해상도, 브라우저 상·하단 툴바(주소창/네비게이션 바), 가상 키보드 팝업 시 팝업 및 바텀시트 하단의 주요 조작 버튼(확인, 저장, 취소, 즐겨찾기 등)이 화면 밖으로 잘리거나 가려지는 현상을 원천 방지하기 위해 다음 **5대 모바일 뷰포트 대응 표준**을 필수로 기본 구현합니다:

* **1) 동적 뷰포트 단위(`dvh`) 및 안전 영역(`safe-area-inset-bottom`) 필수 지정**:
  * 모바일 브라우저 주소창 및 툴바의 유동적 높이 변화를 정확히 반영하기 위해 기존 단순 `vh` 대신 **`max-height: 90dvh;` (또는 `92dvh`)**를 모달(`.modal-content`) 및 바텀시트(`.detail-sheet`)에 의무 적용합니다 (구형 브라우저 폴백용 `max-height: 90vh;` 병기).
  * 홈 인디케이터 바 및 노치 영역과의 겹침을 방지하기 위해 컨테이너 하단 패딩에 `padding-bottom: calc(20px + env(safe-area-inset-bottom, 16px));`를 반드시 지정합니다.
* **2) 독립 내부 스크롤 보장 (`overflow-y: auto`)**:
  * 화면 높이가 500~600px 이하인 작은 기기(갤럭시 폴드 커버 화면 등)에서도 모든 콘텐츠를 빠짐없이 탐색할 수 있도록 모달 본문과 카드 컨테이너에 `overflow-y: auto;` 및 `-webkit-overflow-scrolling: touch;`를 기본 부여합니다.
* **3) 하단 핵심 액션 버튼 영역 스티키 고정 (`position: sticky; bottom: 0`)**:
  * 콘텐츠나 입력 폼이 세로로 길어지더라도 사용자가 스크롤을 끝까지 내리지 않고 즉시 액션을 취할 수 있도록, 하단 버튼 영역(`.modal-actions`, `.selected-card-actions`)에 `position: sticky; bottom: 0; background: inherit; z-index: 10;`을 적용하여 화면 하단에 상시 고정 노출합니다.
* **4) 인터랙티브 핀/항목 선택 시 자동 부드러운 스크롤 (`scrollIntoView`)**:
  * 지도 위 핀(마커)을 꽂거나 목록 카드를 선택하여 하단에 상세 정보 카드 및 조작 버튼이 렌더링될 때, 사용자가 수동으로 스크롤하지 않아도 되도록 `setTimeout(() => card.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 100);`를 의무 호출하여 하단 버튼이 100% 즉시 시야에 확보되도록 구현합니다.
* **5) 팝업/시트 내 지도 캔버스 반응형 가변 높이 (`clamp`)**:
  * 팝업이나 바텀시트 내부에 지도 뷰(Kakao Map, Leaflet 등)가 포함될 경우, 고정 픽셀(예: `height: 350px`) 사용을 엄격히 금지하고, 뷰포트 높이에 맞게 유연하게 축소·확대되는 **`height: clamp(180px, 30dvh, 260px);`**를 적용하여 지도가 세로 화면 전체를 독점하고 하단 조작부를 화면 밖으로 밀어내는 UX 결함을 원천 차단합니다.

---

## 18. 오류 검증 기술자산 전용 마크다운(`트러블슈팅.md`) 누적 저장 및 개발·수정 시 최우선 사전 검토 원칙 (Custom Troubleshooting Knowledge Base & Pre-Review Standard)
모든 애플리케이션 개발, 버그 패치, 기능 수정, 배포 및 코드 검토 작업 시, 오류를 검증하고 해결한 모든 기술적 내용과 실전 노하우를 체계적으로 자산화하고 다음 개발 시 재발을 원천 차단하기 위해 다음 **4대 오류 기술자산 운영 표준**을 필수 준수합니다:

* **1) 오류 해결 기술 전용 마크다운(`트러블슈팅.md`) 독립 저장 의무화**:
  * 개발 및 운영 과정에서 발생한 모든 버그의 원인 분석(RCA), 코드 수정 내역, 검증 절차는 일반 보고서에 묻히지 않도록 프로젝트 루트의 **`트러블슈팅.md` (또는 `오류해결노트.md`)**에 독립된 기술 문서로 빠짐없이 누적 기록합니다.
  * **5대 필수 기록 표준 템플릿**:
    ① **결함 증상 (Symptom)**: 사용자가 겪은 오류 현상, 모바일/데스크톱 환경, 재현 경로, 에러 메시지.
    ② **근본 원인 분석 (RCA - Root Cause Analysis)**: 코드 문법, 런타임 예외, DOM 구조 불일치, 비동기 레이스 컨디션, 모바일 터치 이벤트 버블링, 캐시 라이프사이클 등 기술적 실원인 규명.
    ③ **해결 기술 및 아키텍처 패턴 (Fix & Solution Pattern)**: 실제 적용된 코드 수정 라인, 방어 가드, 전역 안전 바인딩, 재발 방지 패턴.
    ④ **무결성 검증 절차 및 결과 (Verification Evidence)**: 문법 검사(`node -c`, `py_compile`), 단위/통합 테스트, 실서버 cURL 및 브라우저 엔드포인트 검증 증거.
    ⑤ **향후 주의사항 및 체크리스트 (Gotcha Checklist)**: 다음 유사 기능 구현 또는 수정 시 반드시 점검해야 할 핵심 팁.
* **2) 코드 개발·수정·검토 착수 전 개인 커스텀 마크다운 1순위 조회 의무화 (Pre-Review Standard)**:
  * 에이전트는 사용자의 개발/수정/점검 요청을 수신했을 때, 소스 코드를 열람하거나 수정을 시작하기 전에 **반드시 대상 프로젝트의 `트러블슈팅.md`를 최우선으로 먼저 읽고 검토(Mandatory Pre-read)**합니다.
  * 이전에 겪었던 오류 패턴과 기술적 제약사항을 머리에 장착한 상태에서 설계를 수립함으로써, 과거의 실수를 단 1회도 반복하지 않는 무결점 코딩을 보장합니다.
  * 프로젝트에 아직 `트러블슈팅.md`가 존재하지 않는 신규 프로젝트인 경우, 첫 번째 트러블슈팅 또는 기능 검증 완료 즉시 해당 파일을 신규 생성하여 자산화를 개시합니다.
* **3) 공통/전역 오류 패턴의 크로스 프로젝트 확산 및 전파**:
  * 특정 앱(예: `family-care`, `daily-quiz`, `nas-dashboard` 등)에서 발견된 치명적 오류 기법(예: 모바일 터치 이벤트의 캔버스 관통 방지, PWA 캐시 즉각 무효화, 전역 이벤트 핸들러 안전 바인딩 등)은 다른 앱 개발 시에도 공통 체크리스트로 적극 교차 적용합니다.
* **4) Git 양방향 실시간 동기화 및 영구 버전 관리 (Rule 1, 2 연동)**:
  * 새로 추가되거나 보강된 `트러블슈팅.md`는 소스 코드 및 `기술레포트.md`, `제작히스토리.md`와 함께 대상 GitHub 레포지토리에 즉시 커밋 및 푸시하여 영구 보존하며, 멀티 디바이스 환경 동기화 레포지토리([agent-environment](https://github.com/mkotinet/agent-environment))에도 상시 최신 상태를 유지합니다.

---

## 19. 모바일/PC(데스크톱) 반응형 듀얼 최적화 및 뷰포트 공간 극대화 코드 구현 원칙 (Mobile & PC Dual Optimization & Viewport Maximization Standard)
모든 웹 애플리케이션 및 뷰어, 대시보드, 인터랙티브 서비스 개발 시, 모바일의 협소한 세로 화면과 PC의 광활한 가로 와이드 화면의 특성을 모두 극대화하여 최상의 사용자 경험을 제공할 수 있도록 다음 **6대 모바일/PC 듀얼 최적화 코드 구현 표준**을 필수로 기본 구현합니다:

* **1) 상단 메뉴바 접기/펼치기 및 1행 미니멀 요약바 표준화 (Collapsible Topbar & Compact Summary Bar)**:
  * 복잡한 다행(Multi-row) 검색창, 필터 칩 빌더, 카테고리 선택자, 툴바 등은 모바일/PC 모두에서 본문 작업 영역(장표, 캔버스, 그리드, 리스트)의 세로 높이를 30~50% 이상 잠식하지 않도록 **상단바 접기/펼치기 토글(`#btnToggleTopbar`, 단축키 `Alt+H`)**을 의무 구현합니다.
  * 접혔을 때는 높이 40px 내외의 슬림한 **1행 미니멀 요약 바(`#collapsedSummary`)**로 축소 전환되고, 현재 검색어/필터 상태 뱃지(`#collapsedQueryBadge`)와 원클릭 `검색창 열기/펼치기` 버튼(`#btnQuickExpand`)을 상시 노출하여 작업 맥락(Context)을 완벽히 보존합니다.
  * 접힘/펼침 상태는 `localStorage`(`app_topbar_collapsed`)에 영속화하여 브라우저 새로고침이나 재접속 시에도 사용자가 설정한 최적 뷰포트 배치를 유지합니다.
* **2) 100vw × 100vh Zen 몰입형 전체화면 모드 (Immersive Fullscreen / Zen Mode)**:
  * 장표, 도면, 차트, 데이터 테이블, 코드/문서 뷰어 등 정밀 검토 및 몰입이 필요한 핵심 화면에는 브라우저 표준 Fullscreen API와 CSS `body.zen-fullscreen`을 연동한 **무방해 전체화면 모드(`#btnFullscreen`, `#btnStageFullscreen`, 단축키 `Alt+F`)**를 기본 탑재합니다.
  * Zen 모드 활성화 시 상단 헤더, 좌측 사이드바, 우측 인스펙터/속성창 등 모든 부가 UI를 일제히 `display: none !important;`로 숨기고, 주 작업 영역(캔버스/그리드)을 **`100vw × 100vh`**로 화면 전체에 꽉 채웁니다.
  * 화면 우측 상단에 반투명 블러 백드롭의 **플로팅 복귀 버튼(`#btnExitFullscreen`, `⤢ 전체창 닫기 (ESC)`)**을 상시 플로팅 배치하고, 키보드 `ESC` 키 리스너를 바인딩하여 0.1초 만에 안전하게 일반 화면으로 복귀할 수 있도록 보장합니다.
* **3) PC(데스크톱) 와이드 뷰포트 및 사이드바/인스펙터 독립 제어 & 단축키 (PC Wide-Screen Ergonomics)**:
  * **사이드바/패널 독립 토글**: 좌측 탐색 사이드바(`#btnToggleSidebar`, `[` 단축키), 우측 상세/텍스트 인스펙터(`]` 단축키)를 각각 독립적으로 접거나 펼칠 수 있도록 하여 가로 캔버스 폭을 360px 이상 추가 확보할 수 있도록 구현합니다.
  * **와이드 스크린 그리드 반응형 (CSS Grid Dynamic Breakpoints)**: 1200px 이상(4~5열, `minmax(240px, 1fr)`), 1600px 이상(5~6열, `minmax(260px, 1fr)`) 등 데스크톱 대형 모니터의 해상도를 낭비 없이 100% 활용하도록 유연한 반응형 그리드 미디어 쿼리를 기본 탑재합니다.
  * **생산성 키보드 단축키 (Keyboard Shortcuts)**: `Alt+H`(상단바 접기), `Alt+F`(전체화면), `[`(좌측 사이드바), `]`(우측 인스펙터), `ESC`(전체화면 해제 / 모달 닫기) 등 마우스 이동 없이 양손 키보드만으로 신속히 조작할 수 있는 전역 `keydown` 이벤트 핸들러를 필수로 구성합니다.
* **4) 모바일 전용 레이아웃 분할 및 자동 필터 아코디언 (Mobile Compact Accordion & Auto-Fold)**:
  * 좁은 세로 모바일 화면에서는 다수의 검색 필터, 권별 선택지, 정렬 옵션을 **'상세 필터' 아코디언(`#topbarCollapsibleFilters`, `#btnToggleFilters`)**으로 묶어 기본 접힘 상태로 로드하여, 첫 화면 진입 시 즉시 핵심 검색창과 콘텐츠 장표에 집중하도록 합니다.
  * 모바일 환경에서 검색 버튼 터치 또는 엔터 입력 시, 모바일 가상 키보드가 닫힘과 동시에 필터 아코디언을 자동으로 축소 접기(`runSearch() ➔ updateFiltersState(true)`)하여 사용자가 수동 스크롤을 하지 않고도 검색 결과 목록을 화면 최상단에서 즉각 확인할 수 있도록 자동화합니다.
* **5) 모바일 사이드 패널의 슬라이드업 바텀 시트 전환 (Mobile Slide-up Bottom Sheet)**:
  * 데스크톱에서 좌/우 분할 창(Split View)으로 표시되는 상세 인스펙터, 메타데이터 정보창, OCR 텍스트 뷰 등을 모바일에서는 화면을 영구 잠식하는 가로 분할 대신 **하단 슬라이드업 바텀 시트(`@keyframes slideUpSheet`, `max-height: 55dvh;`, `position: fixed; bottom: 0;`)**로 동적 전환합니다.
  * 캔버스나 장표 영역을 항상 시야에 확보하고, 필요할 때만 바텀 시트를 끌어올려 상세 텍스트나 조작부를 확인할 수 있도록 하여 터치 스크롤 간섭을 배제합니다.
* **6) 터치 친화적 타깃 크기 및 동적 뷰포트 보장 (Touch Targets & Dynamic Viewport Height)**:
  * 모바일 인터랙션 요소(버튼, 탭, 체크박스 등)는 최소 **44px × 44px** 이상의 터치 타깃(`min-height: 44px; min-width: 44px;`)과 충분한 간격을 확보하여 터치 오작동을 방지합니다.
  * 모바일 브라우저의 가변 주소창 및 하단 툴바에 대응하기 위해 단순 `vh` 대신 **`100dvh` / `calc(100dvh - 120px)`**와 `env(safe-area-inset-*)` 환경 변수를 필수 지정합니다.

