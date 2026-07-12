#######################################################################
# Author: Lehlohonolo Adolf Matobakele  
# Email: lehlohonolo.matobakele@gov.ls
# Contacxt: 00266 62320704
#######################################################################
from __future__ import annotations

import argparse
from pathlib import Path

from .converter import docx_to_pdf, pdf_to_docx


def _parse_pages(value: str | None) -> list[int] | None:
    """Parse one-based comma-separated page numbers into zero-based indexes."""
    if not value:
        return None

    pages: list[int] = []
    for item in value.split(","):
        item = item.strip()
        if not item:
            continue
        page = int(item)
        if page < 1:
            raise argparse.ArgumentTypeError("Pages must start from 1")
        pages.append(page - 1)

    return pages or None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pdf-word-converter",
        description="Convert PDF to Word and Word to PDF from the command line.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    pdf_parser = subparsers.add_parser("pdf-to-word", help="Convert PDF to DOCX")
    pdf_parser.add_argument("input", help="Input PDF file")
    pdf_parser.add_argument("output", nargs="?", help="Output DOCX file")
    pdf_parser.add_argument("--start", type=int, help="First page to convert, one-based")
    pdf_parser.add_argument("--end", type=int, help="Last page to convert, one-based and inclusive")
    pdf_parser.add_argument("--pages", type=_parse_pages, help="Specific pages, for example: 1,3,5")
    pdf_parser.add_argument("--password", help="PDF password, only when required")

    word_parser = subparsers.add_parser("word-to-pdf", help="Convert DOC/DOCX to PDF")
    word_parser.add_argument("input", help="Input DOC or DOCX file")
    word_parser.add_argument("output", nargs="?", help="Output PDF file")
    word_parser.add_argument("--libreoffice-path", help="Custom path to LibreOffice/soffice executable")
    word_parser.add_argument("--timeout", type=int, default=120, help="Conversion timeout in seconds")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "pdf-to-word":
        if args.pages and (args.start or args.end):
            parser.error("Use either --pages or --start/--end, not both.")

        start = args.start - 1 if args.start else None
        end = args.end if args.end else None

        output = pdf_to_docx(
            args.input,
            args.output,
            start=start,
            end=end,
            pages=args.pages,
            password=args.password,
        )
        print(f"Created Word file: {Path(output)}")
        return

    if args.command == "word-to-pdf":
        output = docx_to_pdf(
            args.input,
            args.output,
            libreoffice_path=args.libreoffice_path,
            timeout=args.timeout,
        )
        print(f"Created PDF file: {Path(output)}")
        return


if __name__ == "__main__":
    main()
