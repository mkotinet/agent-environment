---
name: markitdown-excel
description: "마크다운잇(MarkItDown) 범용 문서 변환과 복잡한 엑셀(다중 시트, 병합 셀 스마트 해제 및 값 전파, 계산값/수식 동시 병기, 조건부 서식 및 셀 색상 뱃지화, 다중 테이블 자동 분할) 전처리가 모두 내장된 올인원 마크다운 변환 스킬"
---

# MarkItDown-Excel Pro (고급 엑셀 전처리 & 범용 마크다운 변환 스킬)

Microsoft의 **MarkItDown** 엔진과 **고급 엑셀 전처리 파이프라인(Excel Advanced Preprocessor)**을 결합한 올인원 커스텀 스킬입니다.  
일반적인 마크다운 변환 도구가 해결하지 못하는 엑셀의 복잡한 실무 서식(다중 시트 누락, 병합 셀 왜곡, 수식 증발, 조건부 서식 소실 등)을 완벽하게 전처리하여 분석용 AI 에이전트 및 LLM이 데이터 손실 없이 읽을 수 있는 최적의 GFM(GitHub Flavored Markdown) 규격으로 변환합니다.

---

## 🎯 주요 기능 및 해결 문제

| 기능 구분 | 기존 일반 변환기 (Pandas / 기본 MarkItDown) | MarkItDown-Excel Pro |
| :--- | :--- | :--- |
| **다중 시트 (Multi-Sheet)** | 첫 시트만 변환하거나 시트 간 구조 유실 | 모든 워크시트 자동 탐색, 목차(TOC) 및 섹션별 완전 구조화 |
| **병합 셀 (Merged Cells)** | 좌상단 셀만 값 유지, 나머지 행/열은 `NaN`/공백 발생으로 표 왜곡 | **Smart Unmerge & Fill**: 병합된 영역 전체에 계층 값 자동 전파(Forward Fill)하여 데이터 레코드 정합성 100% 보장 |
| **수식 처리 (Formulas)** | 수식 원본이 사라지고 계산값만 남거나, 반대로 수식만 남음 | **Dual-Pass Extraction**: 계산된 최종 결과값과 원본 수식 동시 병기 (`1,250,000 (fx: =SUM(C2:C10))`) + 시트별 수식 산출 근거 맵 제공 |
| **조건부 서식 (Conditional Formatting)** | 시각적 강조 및 색상 정보가 완전히 소실됨 | 배경색/글꼴/조건부 룰(기준초과/미달 등) 감지 -> `⚠️[경고]`, `🔴[위험]`, `✅[달성]`, `⚡[검토]`, `📌[강조]` 텍스트 뱃지 자동 변환 |
| **시트 내 다중 표 (Multi-Tables)** | 빈 행으로 나뉜 여러 표가 하나의 거대한 깨진 표로 합쳐짐 | 빈 행 streak 기반 **스마트 서브테이블 분할 감지** 및 개별 GFM 표 렌더링 |
| **타 문서 호환성 (All Documents)** | 엑셀만 지원 | Microsoft MarkItDown 공식 엔진 내장으로 PDF, Word(DOCX), PowerPoint(PPTX), HTML, 텍스트 파일도 원클릭 변환 |

---

## 🚀 사용법 (CLI)

### 1. 기본 실행 (엑셀 파일)
```bash
# 엑셀 파일을 마크다운 파일로 변환
python3 ~/.agents/skills/markitdown-excel/scripts/markitdown_converter.py input.xlsx -o output.md

# 또는 글로벌 단축 CLI 명령어 사용
markitdown-excel input.xlsx -o output.md
```

### 2. 수식 표기 옵션 (`--formula-mode`)
```bash
# 기본값: 인라인 병기 (값과 수식을 동시에 표기: "15,000 (fx: =SUM(B2:B10))")
markitdown-excel report.xlsx --formula-mode inline -o report.md

# 각주 모드: 표 안에는 값과 [fx] 표기, 하단 수식 맵에서 상세 분해
markitdown-excel report.xlsx --formula-mode footnote -o report.md

# 값 전용 모드 (수식 제외하고 순수 데이터만 추출)
markitdown-excel report.xlsx --formula-mode value_only -o report.md

# 수식 전용 모드 (감사 및 엑셀 로직 디버깅용)
markitdown-excel report.xlsx --formula-mode formula_only -o report.md
```

### 3. 병합 셀 처리 옵션 (`--unmerge`)
```bash
# 기본값: fill (병합된 모든 하위/우측 셀에 부모 값을 복제하여 완벽한 테이블 행 구조 생성)
markitdown-excel complex.xlsx --unmerge fill -o result.md

# blank (좌상단 셀에만 값을 두고 병합 영역 나머지는 빈칸 유지)
markitdown-excel complex.xlsx --unmerge blank -o result.md
```

### 4. 기타 상세 옵션
```bash
# 숨김 시트도 모두 포함하여 변환
markitdown-excel data.xlsx --include-hidden -o full_data.md

# 조건부 서식 뱃지 태그 제외 (순수 텍스트만)
markitdown-excel data.xlsx --no-badges -o plain.md

# PDF, Word(DOCX), PowerPoint(PPTX) 등 비 엑셀 파일 변환
markitdown-excel presentation.pptx -o presentation.md
markitdown-excel proposal.docx -o proposal.md
markitdown-excel paper.pdf -o paper.md
```

---

## 🛠️ 내부 아키텍처 및 파이프라인

1. **Dual-Pass OpenPyXL Engine**:
   - `wb_val = load_workbook(data_only=True)`: Excel 계산 엔진이 산출한 최종 수치/문자열 캐시 획득
   - `wb_form = load_workbook(data_only=False)`: `=SUM(...)`, `=IF(...)`, `=VLOOKUP(...)` 등 원본 수식 획득
2. **Merged Cells Graph Mapping**:
   - `ws.merged_cells.ranges`를 파싱하여 (min_row, max_row, min_col, max_col) 경계를 추적.
   - Forward-fill 알고리즘으로 하위/측면 데이터에 컨텍스트를 주입하여 Markdown 표의 열 어긋남 방지.
3. **Conditional Formatting Scanner**:
   - `ws.conditional_formatting`의 `CellIsRule`, `ColorScaleRule` 및 셀 직접 스타일(`cell.fill`, `cell.font`)의 ARGB 16진수 색상을 분석.
   - 위험/경고/주의/달성 뱃지로 변환하여 LLM 프롬프트에 뉘앙스를 전달.
4. **GFM Serializer & Cleaner**:
   - 개행(`<br>`), 파이프(`\|`), 숫자 우측 정렬, 빈 행 정리 등 정밀한 GFM 마크다운 생성.

---

## 💡 에이전트 실행 지침 (Instructions for AI Agents)

사용자가 다음과 같은 작업을 요청할 때 이 스킬을 호출하십시오:
1. **"엑셀 파일을 마크다운으로 바꿔줘", "xlsx 읽어서 분석해줘"**  
   -> 단순 파이썬 판다스로 읽지 말고 `markitdown-excel <파일명> -o <출력경로>`를 실행하여 수식과 병합 셀이 온전히 보존된 마크다운을 생성한 뒤 분석을 진행하세요.
2. **"이 엑셀에 들어있는 수식이나 계산 근거를 확인해줘"**  
   -> `--formula-mode inline` 또는 `--formula-mode footnote`로 변환하여 하단에 생성되는 **수식 산출 근거 맵(Formula Breakdown)**을 확인하세요.
3. **"조건부 서식이나 강조된 항목 위주로 요약해줘"**  
   -> 변환된 마크다운 내 `⚠️[경고]`, `🔴[위험]`, `✅[달성]` 태그를 검색하여 즉시 이상치 및 핵심 KPI 항목을 요약하세요.
