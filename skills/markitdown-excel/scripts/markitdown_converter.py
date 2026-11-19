#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MarkItDown-Excel Pro 통합 변환기
==============================
- 엑셀 파일 (.xlsx, .xlsm, .xls): 다중 시트, 병합 셀 해제, 수식 병기, 조건부 서식 전처리 엔진 가동
- 기타 파일 (.pdf, .docx, .pptx, .html, .txt 등): Microsoft MarkItDown 공식 엔진 가동
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

# 동일 디렉토리의 excel_preprocessor 모듈 로드
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from excel_preprocessor import ExcelAdvancedPreprocessor

EXCEL_EXTENSIONS = {".xlsx", ".xlsm", ".xltx", ".xltm"}

def find_markitdown_bin() -> str:
    """시스템에 설치된 markitdown 실행 경로를 탐색합니다."""
    candidates = [
        os.path.expanduser("~/.local/bin/markitdown"),
        "/usr/local/bin/markitdown",
        "/opt/homebrew/bin/markitdown"
    ]
    for c in candidates:
        if os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    return "markitdown"

def convert_document(
    input_path: str,
    output_path: str = None,
    formula_mode: str = "inline",
    unmerge: str = "fill",
    badges: bool = True,
    split_tables: bool = True,
    include_hidden: bool = False
) -> str:
    ext = Path(input_path).suffix.lower()

    if ext in EXCEL_EXTENSIONS:
        # 고급 엑셀 전처리 파이프라인 가동
        processor = ExcelAdvancedPreprocessor(
            filepath=input_path,
            include_formulas=(formula_mode != "value_only"),
            formula_mode=formula_mode,
            unmerge_strategy=unmerge,
            detect_subtables=split_tables,
            include_hidden=include_hidden,
            format_badges=badges
        )
        md_text = processor.process_all_sheets()
    else:
        # Microsoft MarkItDown 엔진 가동
        md_bin = find_markitdown_bin()
        cmd = [md_bin, input_path]
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            md_text = res.stdout
        except (subprocess.CalledProcessError, FileNotFoundError):
            # uv run 대체 시도
            try:
                res = subprocess.run(
                    ["uv", "run", "--with", "markitdown", "markitdown", input_path],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True
                )
                md_text = res.stdout
            except Exception as e:
                raise RuntimeError(f"MarkItDown 실행 실패: {e}")

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_text)
        print(f"✅ 변환 완료: {output_path}", file=sys.stderr)
    return md_text

def main():
    parser = argparse.ArgumentParser(
        description="MarkItDown-Excel Pro: 범용 문서 마크다운 변환 및 고급 엑셀 전처리 통합 CLI"
    )
    parser.add_argument("input_file", help="변환할 입력 파일 (.xlsx, .docx, .pdf, .pptx, .html 등)")
    parser.add_argument("-o", "--output", help="출력 마크다운 파일 (.md). 지정하지 않으면 표준 출력")
    parser.add_argument(
        "--formula-mode",
        choices=["inline", "footnote", "value_only", "formula_only"],
        default="inline",
        help="[엑셀 전용] 수식 표기: inline(값+수식 병기), footnote(각주/맵), value_only(값만), formula_only(수식만)"
    )
    parser.add_argument(
        "--unmerge",
        choices=["fill", "blank"],
        default="fill",
        help="[엑셀 전용] 병합 셀 해제 방식: fill(값 전파 채우기), blank(빈칸)"
    )
    parser.add_argument(
        "--no-badges",
        action="store_true",
        help="[엑셀 전용] 조건부 서식/셀 색상 배지 끄기"
    )
    parser.add_argument(
        "--no-split-tables",
        action="store_true",
        help="[엑셀 전용] 시트 내 복수 테이블 분할 끄기"
    )
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="[엑셀 전용] 숨김 시트 포함"
    )

    args = parser.parse_args()
    md = convert_document(
        input_path=args.input_file,
        output_path=args.output,
        formula_mode=args.formula_mode,
        unmerge=args.unmerge,
        badges=not args.no_badges,
        split_tables=not args.no_split_tables,
        include_hidden=args.include_hidden
    )
    if not args.output:
        print(md)

if __name__ == "__main__":
    main()
