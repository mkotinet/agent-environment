# 공통 운영 및 개발 지침 (Common Guidelines)

본 지침은 Synology NAS 및 관련 모든 애플리케이션 개발, 운영, 배포 작업 시 필수적으로 준수해야 하는 공통 원칙입니다.

---

## 1. 양방향 GitHub 형상 동기화 원칙 (Bidirectional Git Sync)
* **실시간 / 상시 동기화**:
  * 시놀로지(Synology NAS Portainer) 또는 로컬에서 앱 설정, 소스 코드, Docker Compose 설정, NPM 라우팅 등이 변경되었을 경우, 변경된 모든 코드는 즉시 대상 GitHub 레포지토리에 커밋 및 푸시하여 양방향 최신 상태를 유지합니다.
  * 신규 추가되거나 변경된 도커 컨테이너는 반드시 `docker-compose.yml` 및 관련 설정 파일 형태로 해당 레포지토리에 빠짐없이 버전 관리합니다.
* **민감정보 보호**:
  * GitHub 푸시 시 API 시크릿, 개인 액세스 토큰(PAT), 비밀번호 등 민감 정보가 소스에 하드코딩되지 않도록 주의합니다.

---

## 2. 기술레포트 및 히스토리 필수 반영 원칙 (Documentation Principle)
* **기술레포트 (`기술레포트.md`) 상시 작성**:
  * 앱 신규 구축, 장애 복구, 인프라 고도화, SSL/HTTPS 연동, 네트워크 설정 등 주요 변경 시 아키텍처, 장애 원인(RCA), 해결 절차, 엔드포인트 검증 결과를 `기술레포트.md`에 상세히 기록합니다.
* **제작히스토리 (`제작히스토리.md` / `히스토리.md`) 타임라인 기록**:
  * 작업 일시, 단계별 수행 타임라인, 생성 및 수정된 산출물 목록을 지속적으로 업데이트하여 유지보수 추적성을 확보합니다.

---

## 3. 네트워크 및 도메인 보안 연동 원칙
* **HTTPS & Cloudflare 표준화**:
  * 외부 도메인(`danminlove.com`) 연동 시 NPM 역방향 프록시를 통해 HTTPS(443 포트) 및 와일드카드 SSL 인증서를 적용하고, WebSocket 및 Block Exploits 보안 설정을 기본 활성화합니다.

---

## 4. Graphify 지식 그래프 연동 원칙 (Knowledge Graph Architecture)
* **코드베이스 및 아키텍처 질의 시 지식 그래프 우선 참조**:
  * 프로젝트 내 `graphify-out/graph.json`이 존재하는 경우, 맹목적인 `grep`이나 대량 파일 탐색 전에 `graphify query "<질문>"`(CLI) 또는 `query_graph`(MCP), 관계 파악을 위한 `graphify path "<A>" "<B>"` / `shortest_path`, 핵심 개념 분석을 위한 `graphify explain "<개념>"` / `get_node`를 우선적으로 활용합니다.
  * `graphify-out/wiki/index.md`가 존재하면 원시 코드 파일을 직접 읽기 전에 위키 구조를 우선 탐색합니다.
  * `graphify-out/GRAPH_REPORT.md`는 전체적인 시스템 아키텍처 조망 및 주요 고위험 결합도(God nodes) 확인 시 참조합니다.
  * 세션 내에서 파일 생성/수정 등 코드베이스 변경 작업이 발생한 후에는 `graphify update .`를 실행하여 AST 기반 최신 그래프 상태를 유지합니다.
  * 신규 프로젝트 또는 지식 그래프가 없는 경우 `/graphify .` 명령어로 손쉽게 그래프를 생성합니다.

---

## 5. 코드 개발 및 분석 시 스킬 순차 적용 원칙 (Sequential Skill Application)
코드 개발, 수정, 점검, 리팩토링, 기능 구현 및 아키텍처 분석 시 다음 5가지 핵심 스킬 파이프라인을 **순차적으로** 적용하여 최고 수준의 품질과 최신 웹 표준을 달성합니다:

1. **1단계: `modern-web-guidance-src` (최신 웹 표준 & 가이던스 우선 검토)**
   * 최신 HTML/CSS/JS 기능(Popover, Dialog, View Transitions, Container Queries, Scroll-driven Animation, Baseline 호환성 등) 구현 시 낡은 레거시 패턴 대신 최신 표준 가이던스를 검색(`npx modern-web-guidance search`) 및 적용합니다.
   * 브라우저 호환성 및 Baseline 상태를 `baseline-status` 등을 통해 사전 검증합니다.

2. **2단계: `public-apis` (외부 연동 및 무료 공개 API 생태계 우선 탐색)**
   * 외부 서비스 연동, Mock/테스트 데이터, 인증(OAuth/BaaS), 결제, 지도/LBS, 날씨, AI/ML, 소셜, 미디어 처리 등 서드파티 기능이 요구되는 경우, 임의의 유료 서비스나 불완전한 ad-hoc API를 도입하기 전에 `public-apis` 카탈로그(1,400+ API) 및 `public-api-lookup` 스킬을 우선 조회합니다.
   * 인증 방식(무인증/apiKey/OAuth), HTTPS 및 CORS 지원 여부를 사전 확인하여 프론트엔드/백엔드 아키텍처에 가장 적합하고 안정적인 무료 공개 API를 선제적으로 매핑 및 통합합니다.

3. **3단계: `agent-skills` (엔지니어링 표준 및 모범 사례 통합)**
   * `vercel-react-best-practices`, `web-design-guidelines`, `vercel-composition-patterns` 등 프레임워크 최적화 규칙을 준수합니다.
   * `frontend-ui-engineering`, `code-review-and-quality`, `security-and-hardening`, `performance-optimization` 등 Addy Osmani 엔지니어링 스킬을 통해 아키텍처와 코드를 고도화합니다.

4. **4단계: `graphify` (지식 그래프 기반 탐색 및 영향도 분석)**
   * 변경 전: `query_graph`, `shortest_path`, `get_node` 등을 통해 의존성 및 결합도(God nodes)를 파악합니다.
   * 변경 후: 반드시 `graphify update .`를 실행하여 지식 그래프를 최신 상태로 유지합니다.

5. **5단계: `super-powers` (체계적 프로세스 및 무결성 검증)**
   * `brainstorming` 및 `writing-plans`로 선계획을 수립하고, `systematic-debugging` 및 `test-driven-development`로 구현합니다.
   * 최종 완료 전 `verification-before-completion`을 필수로 수행하여 실제 테스트 및 런타임 결과 증거를 확인한 후 작업을 마무리합니다.

---

## 6. 중간매개체 레포지토리 기반 멀티 디바이스 형상 동기화 원칙 (Multi-Device Agent Environment Sync)
* **환경 동기화 전용 레포지토리 상시 최신화 (`mkotinet/agent-environment`)**:
  * 전역 지침(Rules), 설치된 에이전트 스킬(Skills), MCP 서버 설정(`mcp_config.json`)이 신규 추가되거나 변경될 경우, 즉시 중간매개체 GitHub 레포지토리([agent-environment](https://github.com/mkotinet/agent-environment))에 동기화 커밋 및 푸시하여 항상 최신 상태를 유지합니다.
* **다른 노트북 및 맥북 간 완벽한 이식성(Portability) 보장**:
  * 신규 또는 다른 맥북/노트북 환경에서 `git clone` 후 `bash setup.sh` 단 한 줄의 명령어로 지침, 스킬, MCP 환경이 100% 동일하게 복원 및 동기화될 수 있도록 레포지토리 내 자동화 스크립트와 템플릿을 철저히 유지관리합니다.
* **민감 정보 보호 및 템플릿 분리 원칙**:
  * GitHub 푸시 시 개인 액세스 토큰(PAT), 비밀번호, 외부 서비스 API 키 등 시크릿 정보는 `mcp_config.template.json` 및 `.env` 템플릿으로 추상화하여 민감정보가 외부에 노출되지 않도록 엄격히 보호합니다.
