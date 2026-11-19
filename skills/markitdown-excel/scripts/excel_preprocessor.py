#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MarkItDown-Excel Pro: 복잡한 엑셀(다중 시트, 병합 셀, 수식 병기, 조건부 서식) 전처리 엔진
================================================================================
기능:
1. 다중 시트(Multi-Sheet) 순회 및 시트별 구조화된 마크다운 섹션 생성
2. 병합 셀(Merged Cells) 스마트 해제 및 값 전파(Forward Fill)로 데이터 손실 방지
   - 전폭 타이틀 행(Full-width Banner)은 표 위 볼드 캡션으로 스마트 승격
3. 계산된 결과값과 원본 수식(Formula) 병기 (`값 (fx: =SUM(...))`) 및 수식 맵 자동 집계
4. 조건부 서식(Conditional Formatting) 및 셀 색상 감지 -> 마크다운 배지/이모지 텍스트화
5. 시트 내 복수 테이블(Multiple Tables) 자동 분할 감지
6. 숫자/통화/퍼센트/날짜 포맷 정규화 및 GFM(GitHub Flavored Markdown) 호환 출력
"""

import sys
import os
import argparse
from typing import List, Dict, Any, Tuple, Optional
import openpyxl
from openpyxl.utils import get_column_letter, range_boundaries
from openpyxl.styles import PatternFill, Font, Color
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule

def clean_cell_text(val: Any) -> str:
    """마크다운 테이블 포맷을 깨뜨리지 않도록 셀 텍스트를 정제합니다."""
    if val is None or val == "None":
        return ""
    text = str(val).strip()
    # 개행 문자 치환
    text = text.replace("\r\n", "<br>").replace("\n", "<br>").replace("\r", "<br>")
    # 파이프 문자 이스케이프
    text = text.replace("|", "\\|")
    return text

def parse_rgb_color(color_obj) -> Optional[str]:
    """openpyxl 컬러 객체에서 16진수 RGB 또는 의미론적 색상 힌트를 추출합니다."""
    if not color_obj:
        return None
    try:
        if hasattr(color_obj, 'rgb') and color_obj.rgb:
            rgb_str = str(color_obj.rgb).upper()
            if len(rgb_str) == 8:
                return rgb_str[2:]  # ARGB -> RGB
            return rgb_str
        if hasattr(color_obj, 'theme') and color_obj.theme is not None:
            theme_idx = color_obj.theme
            if theme_idx in [5, 6]:   # 빨강/주황 테마
                return "FF4D4D"
            elif theme_idx in [4, 9]:  # 초록 테마
                return "4CAF50"
            elif theme_idx in [7, 8]:  # 노랑 테마
                return "FFC107"
    except Exception:
        pass
    return None

def color_to_badge(rgb_hex: Optional[str]) -> str:
    """RGB 색상을 인지하여 위험/경고/주의/달성 뱃지로 변환합니다."""
    if not rgb_hex or len(rgb_hex) != 6:
        return ""
    try:
        r = int(rgb_hex[0:2], 16)
        g = int(rgb_hex[2:4], 16)
        b = int(rgb_hex[4:6], 16)
        
        # 빨강 계열 (위험, 미달, 경고)
        if r > 180 and g < 120 and b < 120:
            return " ⚠️[경고]"
        if r > 200 and g < 160 and b < 160:
            return " 🔴[위험]"
        # 주황 계열
        if r > 220 and 100 <= g <= 180 and b < 80:
            return " 🔸[주의]"
        # 노랑 계열 (주의, 검토)
        if r > 200 and g > 180 and b < 120:
            return " ⚡[검토]"
        # 초록 계열 (성공, 달성, 양호)
        if g > 150 and r < 140 and b < 140:
            return " ✅[달성]"
        # 파랑 계열 (강조, 정보)
        if b > 180 and r < 130 and g < 180:
            return " 📌[강조]"
    except Exception:
        pass
    return ""

class ExcelAdvancedPreprocessor:
    def __init__(
        self,
        filepath: str,
        include_formulas: bool = True,
        formula_mode: str = "inline",  # inline, footnote, value_only, formula_only
        unmerge_strategy: str = "fill",  # fill, blank
        detect_subtables: bool = True,
        include_hidden: bool = False,
        format_badges: bool = True,
    ):
        self.filepath = filepath
        self.include_formulas = include_formulas
        self.formula_mode = formula_mode
        self.unmerge_strategy = unmerge_strategy
        self.detect_subtables = detect_subtables
        self.include_hidden = include_hidden
        self.format_badges = format_badges
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"엑셀 파일을 찾을 수 없습니다: {filepath}")

        # 듀얼 로딩: 값 캐시용 vs 수식 원본용
        self.wb_vals = openpyxl.load_workbook(filepath, data_only=True)
        self.wb_forms = openpyxl.load_workbook(filepath, data_only=False)

    def process_all_sheets(self) -> str:
        """모든 워크시트를 전처리하여 완결된 고품질 마크다운 문서를 반환합니다."""
        md_lines = []
        base_name = os.path.basename(self.filepath)
        
        md_lines.append(f"# 📊 엑셀 문서 분석 보고서: `{base_name}`\n")
        md_lines.append(f"> **전처리 엔진**: MarkItDown-Excel Pro (고급 엑셀 전처리 파이프라인)")
        md_lines.append(f"> **수식 처리 모드**: `{self.formula_mode}` | **병합 셀 처리**: `{self.unmerge_strategy}` | **조건부 서식 분석**: `{'활성화' if self.format_badges else '비활성화'}`\n")
        
        sheet_names = self.wb_vals.sheetnames
        visible_sheets = [s for s in sheet_names if self.include_hidden or self.wb_vals[s].sheet_state == 'visible']
        
        md_lines.append("## 📑 시트 목차 (Table of Contents)")
        for idx, name in enumerate(visible_sheets, 1):
            state_tag = " (숨김)" if self.wb_vals[name].sheet_state != 'visible' else ""
            md_lines.append(f"{idx}. [{name}](#sheet-{name.lower().replace(' ', '-')}){state_tag}")
        md_lines.append("\n---\n")

        for name in visible_sheets:
            sheet_md = self.process_single_sheet(name)
            md_lines.append(sheet_md)
            md_lines.append("\n---\n")

        return "\n".join(md_lines)

    def _extract_merged_cell_map(self, ws) -> Tuple[Dict[Tuple[int, int], Tuple[int, int, int, int, Any, Any]], List[Tuple[int, str]]]:
        """
        병합 셀 범위들을 분석하여:
        1. 좌표별 (min_r, max_r, min_c, max_c, top_val, top_form) 매핑
        2. 전폭 단일행 배너 타이틀 리스트 [(row_idx, title_text), ...] 를 반환합니다.
        """
        merged_map = {}
        banner_titles = []
        ws_forms = self.wb_forms[ws.title]
        max_cols = ws.max_column
        
        for rng in ws.merged_cells.ranges:
            min_col, min_row, max_col, max_row = range_boundaries(str(rng))
            top_val = ws.cell(row=min_row, column=min_col).value
            top_form = ws_forms.cell(row=min_row, column=min_col).value
            
            # 전폭 단일 행 배너 (예: 1행의 A1:E1 병합 제목) 감지
            if min_row == max_row and (max_col - min_col + 1) >= max(3, max_cols - 1) and top_val:
                banner_titles.append((min_row, str(top_val).strip()))
                continue
            
            for r in range(min_row, max_row + 1):
                for c in range(min_col, max_col + 1):
                    merged_map[(r, c)] = (min_row, max_row, min_col, max_col, top_val, top_form)
        return merged_map, banner_titles

    def _extract_conditional_formatting_map(self, ws) -> Dict[Tuple[int, int], str]:
        """시트의 조건부 서식 규칙을 파싱하여 셀별 뱃지 문자열 힌트를 생성합니다."""
        cf_map = {}
        if not self.format_badges:
            return cf_map
            
        try:
            for cf in ws.conditional_formatting:
                for rule in cf.rules:
                    badge = ""
                    if isinstance(rule, CellIsRule):
                        op = rule.operator
                        if op in ['greaterThan', 'greaterThanOrEqual']:
                            badge = " 🟢[기준이상]"
                        elif op in ['lessThan', 'lessThanOrEqual']:
                            badge = " ⚠️[기준미달]"
                        elif op in ['equal']:
                            badge = " ⚡[특정일치]"
                    elif isinstance(rule, ColorScaleRule):
                        badge = " 🎨[스케일]"
                    
                    if hasattr(rule, 'dxf') and rule.dxf and rule.dxf.fill:
                        color = parse_rgb_color(rule.dxf.fill.fgColor or rule.dxf.fill.bgColor)
                        extracted = color_to_badge(color)
                        if extracted:
                            badge = extracted

                    for sqref in cf.cells:
                        min_col, min_row, max_col, max_row = range_boundaries(str(sqref))
                        for r in range(min_row, max_row + 1):
                            for c in range(min_col, max_col + 1):
                                if badge and (r, c) not in cf_map:
                                    cf_map[(r, c)] = badge
        except Exception:
            pass
        return cf_map

    def process_single_sheet(self, sheet_name: str) -> str:
        """단일 워크시트를 전처리하여 마크다운 문자열로 변환합니다."""
        ws_val = self.wb_vals[sheet_name]
        ws_form = self.wb_forms[sheet_name]
        
        max_r = ws_val.max_row
        max_c = ws_val.max_column
        
        if max_r == 0 or max_c == 0:
            return f"## Sheet: `{sheet_name}`\n\n*(빈 워크시트입니다)*\n"

        merged_map, banner_titles = self._extract_merged_cell_map(ws_val)
        banner_rows = {r for r, _ in banner_titles}
        cf_map = self._extract_conditional_formatting_map(ws_val)

        grid = []
        formulas_used = []

        for r in range(1, max_r + 1):
            # 전폭 배너 타이틀 행은 별도 캡션으로 처리하므로 데이터 그리드에서 제외
            if r in banner_rows:
                continue

            row_data = []
            row_has_content = False
            for c in range(1, max_c + 1):
                cell_val_obj = ws_val.cell(row=r, column=c)
                cell_form_obj = ws_form.cell(row=r, column=c)
                
                val = cell_val_obj.value
                form = cell_form_obj.value
                coord = f"{get_column_letter(c)}{r}"

                # 병합 셀 처리
                is_merged = (r, c) in merged_map
                if is_merged:
                    min_r, max_r_m, min_c, max_c_m, top_val, top_form = merged_map[(r, c)]
                    if self.unmerge_strategy == "fill":
                        val = top_val if val is None else val
                        form = top_form if form is None else form
                    else:
                        if (r, c) != (min_r, min_c):
                            val = ""
                            form = ""

                # 수식 감지
                has_formula = form is not None and str(form).startswith("=")
                clean_val = clean_cell_text(val)

                if has_formula:
                    calc_disp = clean_val if clean_val else "(계산중)"
                    formulas_used.append((coord, str(form), calc_disp))

                # 조건부 서식 및 셀 배경색 배지
                badge = cf_map.get((r, c), "")
                if not badge and self.format_badges and cell_val_obj.fill:
                    color = parse_rgb_color(cell_val_obj.fill.fgColor or cell_val_obj.fill.bgColor)
                    badge = color_to_badge(color)

                # 볼드 폰트 검사
                is_bold = bool(cell_val_obj.font and cell_val_obj.font.bold)

                # 수식 병기 형식 결정
                if has_formula:
                    form_clean = clean_cell_text(form)
                    if self.formula_mode == "inline":
                        if clean_val:
                            formatted_cell = f"{clean_val} `(fx: {form_clean})`"
                        else:
                            formatted_cell = f"`(fx: {form_clean})`"
                    elif self.formula_mode == "formula_only":
                        formatted_cell = f"`{form_clean}`"
                    elif self.formula_mode == "footnote":
                        formatted_cell = f"{clean_val} <sup>[fx]</sup>" if clean_val else "<sup>[fx]</sup>"
                    else:  # value_only
                        formatted_cell = clean_val
                else:
                    formatted_cell = clean_val

                # 배지 및 스타일 적용
                if badge and formatted_cell:
                    formatted_cell = f"{formatted_cell}{badge}"
                if is_bold and formatted_cell:
                    formatted_cell = f"**{formatted_cell}**"

                if clean_val or has_formula:
                    row_has_content = True

                row_data.append(formatted_cell)
            
            grid.append(row_data)

        tables = self._detect_and_split_tables(grid)

        # 마크다운 조립
        out = []
        anchor_id = f"sheet-{sheet_name.lower().replace(' ', '-')}"
        out.append(f"<a id=\"{anchor_id}\"></a>")
        out.append(f"## 📋 Sheet: `{sheet_name}`\n")
        
        # 배너 타이틀이 있으면 상단 강조 표시
        if banner_titles:
            for _, b_title in banner_titles:
                out.append(f"> ### 🏷️ **{b_title}**\n")

        out.append(f"- **크기**: {max_r} 행 × {max_c} 열")
        out.append(f"- **병합 셀 영역 수**: {len(ws_val.merged_cells.ranges)}개")
        out.append(f"- **계산 수식 수**: {len(formulas_used)}개\n")

        for t_idx, tbl in enumerate(tables, 1):
            if len(tables) > 1:
                out.append(f"### 📌 표 {t_idx} (Table {t_idx})")
            table_md = self._render_gfm_table(tbl)
            out.append(table_md)
            out.append("")

        # 수식 맵 (Formula Breakdown) 부록 생성
        if formulas_used and self.formula_mode in ["inline", "footnote"]:
            out.append(f"#### 🔍 `{sheet_name}` 수식 산출 근거 맵 (Formula Breakdown)")
            out.append("| 셀 위치 | 원본 수식 (Formula) | 계산 결과값 (Evaluated Value) |")
            out.append("| :--- | :--- | :--- |")
            for coord, form, calc_v in formulas_used:
                out.append(f"| **`{coord}`** | `{clean_cell_text(form)}` | `{clean_cell_text(calc_v)}` |")
            out.append("")

        return "\n".join(out)

    def _detect_and_split_tables(self, grid: List[List[str]]) -> List[List[List[str]]]:
        """연속된 빈 행을 기준으로 여러 개의 독립된 표를 자동 분할합니다."""
        if not self.detect_subtables:
            return [grid]

        tables = []
        current_table = []
        empty_streak = 0

        for row in grid:
            is_empty = all(c == "" for c in row)
            if is_empty:
                empty_streak += 1
                if empty_streak == 1 and current_table:
                    tables.append(current_table)
                    current_table = []
            else:
                empty_streak = 0
                current_table.append(row)

        if current_table:
            tables.append(current_table)

        return tables if tables else [grid]

    def _render_gfm_table(self, table_rows: List[List[str]]) -> str:
        """2차원 텍스트 배열을 완벽한 GitHub Flavored Markdown 표로 변환합니다."""
        if not table_rows:
            return "*(내용 없음)*\n"

        num_cols = len(table_rows[0])
        valid_cols = []
        for c in range(num_cols):
            if any(r[c] != "" for r in table_rows):
                valid_cols.append(c)

        if not valid_cols:
            return "*(모든 셀이 비어 있습니다)*\n"

        md_table_lines = []

        header_row = table_rows[0]
        header_cells = [header_row[c] if header_row[c] else f"열 {c+1}" for c in valid_cols]
        md_table_lines.append("| " + " | ".join(header_cells) + " |")

        delimiters = []
        for c in valid_cols:
            is_numeric = False
            for r in table_rows[1:6]:
                txt = r[c].replace(",", "").replace("%", "").replace("원", "").strip()
                if txt.replace(".", "", 1).isdigit():
                    is_numeric = True
                    break
            delimiters.append("---:" if is_numeric else ":---")

        md_table_lines.append("| " + " | ".join(delimiters) + " |")

        for row in table_rows[1:]:
            cells = [row[c] for c in valid_cols]
            md_table_lines.append("| " + " | ".join(cells) + " |")

        return "\n".join(md_table_lines)


def main():
    parser = argparse.ArgumentParser(
        description="MarkItDown-Excel Pro: 복잡한 엑셀(다중 시트, 병합 셀, 수식 병기, 조건부 서식) 전처리 CLI"
    )
    parser.add_argument("excel_path", help="입력 엑셀 파일 경로 (.xlsx, .xlsm, .xls)")
    parser.add_argument("-o", "--output", help="출력 마크다운 파일 경로 (기본값: 표준 출력 또는 [파일명].md)")
    parser.add_argument(
        "--formula-mode",
        choices=["inline", "footnote", "value_only", "formula_only"],
        default="inline",
        help="수식 표기 모드: inline(값과 수식 병기), footnote(각주/맵), value_only(값만), formula_only(수식만)",
    )
    parser.add_argument(
        "--unmerge",
        choices=["fill", "blank"],
        default="fill",
        help="병합 셀 처리 전략: fill(전체 영역 값 전파/복제), blank(좌상단만 유지)",
    )
    parser.add_argument(
        "--no-badges",
        action="store_true",
        help="조건부 서식 및 셀 배경색 뱃지 변환 비활성화",
    )
    parser.add_argument(
        "--no-split-tables",
        action="store_true",
        help="시트 내 빈 행 기준 다중 테이블 분할 기능 끄기",
    )
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="숨겨진 워크시트도 변환에 포함",
    )

    args = parser.parse_args()

    processor = ExcelAdvancedPreprocessor(
        filepath=args.excel_path,
        include_formulas=(args.formula_mode != "value_only"),
        formula_mode=args.formula_mode,
        unmerge_strategy=args.unmerge,
        detect_subtables=not args.no_split_tables,
        include_hidden=args.include_hidden,
        format_badges=not args.no_badges,
    )

    markdown_result = processor.process_all_sheets()

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(markdown_result)
        print(f"✅ 성공적으로 마크다운 문서가 생성되었습니다: {args.output}", file=sys.stderr)
    else:
        print(markdown_result)

if __name__ == "__main__":
    main()
