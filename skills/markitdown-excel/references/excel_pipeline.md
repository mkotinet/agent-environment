# MarkItDown-Excel Pro 전처리 파이프라인 명세서

## 1. 개요
MarkItDown-Excel Pro는 비정형 엑셀 파일(XLSX, XLSM, XLS)을 AI 에이전트 및 LLM이 데이터 유실 없이 완벽히 해석할 수 있는 GitHub Flavored Markdown(GFM) 규격으로 변환하는 전처리 엔진입니다.

## 2. 세부 파이프라인 사양

### (1) 듀얼 패스 로딩 (Dual-Pass Loading)
- **Pass 1 (Cached Value Pass)**: `openpyxl.load_workbook(filepath, data_only=True)`
  - Excel 프로세스가 직전에 계산하여 캐시해 둔 최종 표시 문자열/숫자를 추출합니다.
- **Pass 2 (Raw Formula Pass)**: `openpyxl.load_workbook(filepath, data_only=False)`
  - `=SUM(A1:A10)`, `=IF(C2>100, ...)` 등 산출식 원본을 추출합니다.
- **합성 원칙**:
  - `inline` 모드: `{계산값} (fx: {수식})`
  - `footnote` 모드: `{계산값} <sup>[fx]</sup>` (표 하단 Formula Breakdown 맵과 연결)

### (2) 병합 셀 스마트 해제 및 값 전파 (Smart Unmerge & Fill)
- 엑셀의 `ws.merged_cells.ranges`를 파싱하여 병합 경계 `(min_r, max_r, min_c, max_c)`를 획득합니다.
- **전폭 단일 행 배너 (Full-width Banner)**:
  - 행의 열 폭 대부분을 차지하는 1행/2행 제목 셀(`A1:E1` 등)은 표 컬럼으로 쪼개지 않고, 표 상단의 `> ### 🏷️ 제목` 마크다운 블록쿼트로 승격합니다.
- **데이터 병합 셀 (Row/Column Merged Cells)**:
  - `unmerge=fill`: 좌상단 셀의 값과 수식을 병합된 전체 하위 행과 우측 열로 복제(Forward Fill)하여 각 행이 완전한 레코드 무결성을 유지합니다.

### (3) 조건부 서식 및 셀 스타일 텍스트화 (Styling to Markdown Badges)
- `ws.conditional_formatting`의 룰(`CellIsRule`, `ColorScaleRule`) 및 셀 직접 채우기 색상(`cell.fill.fgColor`)의 16진수 ARGB 값을 분석합니다.
- 색상 및 연산자에 대응되는 의미론적 배지를 부착합니다:
  - 빨강 계열 (R > 180, G < 120, B < 120): ` ⚠️[경고]`
  - 진한 빨강 계열 (R > 200, G < 160, B < 160): ` 🔴[위험]`
  - 주황 계열 (R > 220, 100 <= G <= 180): ` 🔸[주의]`
  - 노랑 계열 (R > 200, G > 180, B < 120): ` ⚡[검토]`
  - 초록 계열 (G > 150, R < 140, B < 140): ` ✅[달성]`
  - 파랑 계열 (B > 180, R < 130): ` 📌[강조]`
- 굵은 글꼴(`cell.font.bold`): `**값**` 볼드 적용.

### (4) 서브 테이블 자동 분할 (Sub-table Detection)
- 하나의 워크시트 안에 여러 개의 표가 빈 행(Empty Rows streak)으로 구분되어 있을 경우, 이를 개별 GFM 표(`### 📌 표 1`, `### 📌 표 2`)로 분할하여 표 레이아웃이 깨지지 않도록 정돈합니다.
