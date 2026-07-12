#######################################################################
# Author: Lehlohonolo Adolf Matobakele  
# Email: lehlohonolo.matobakele@gov.ls
# Contacxt: 00266 62320704
#######################################################################
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Iterable

from pdf2docx import Converter


class ConversionError(RuntimeError):
    """Raised when document conversion fails."""


def _ensure_file(path: Path, expected_suffixes: Iterable[str]) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    suffixes = {suffix.lower() for suffix in expected_suffixes}
    if path.suffix.lower() not in suffixes:
        allowed = ", ".join(sorted(suffixes))
        raise ValueError(f"Unsupported file type '{path.suffix}'. Expected: {allowed}")


def _default_output(input_path: Path, suffix: str) -> Path:
    return input_path.with_suffix(suffix)


def pdf_to_docx(
    input_pdf: str | Path,
    output_docx: str | Path | None = None,
    *,
    start: int | None = None,
    end: int | None = None,
    pages: list[int] | None = None,
    password: str | None = None,
) -> Path:
    """
    Convert a PDF file to DOCX.

    start, end, and pages are zero-based because pdf2docx uses zero-based page indexes.
    """
    input_path = Path(input_pdf).expanduser().resolve()
    _ensure_file(input_path, [".pdf"])

    output_path = (
        Path(output_docx).expanduser().resolve()
        if output_docx
        else _default_output(input_path, ".docx")
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    converter = Converter(str(input_path), password=password) if password else Converter(str(input_path))
    try:
        converter.convert(str(output_path), start=start, end=end, pages=pages)
    finally:
        converter.close()

    if not output_path.exists():
        raise ConversionError(f"PDF to DOCX conversion failed: {output_path} was not created")

    return output_path


def _find_libreoffice(explicit_path: str | Path | None = None) -> str:
    if explicit_path:
        explicit = Path(explicit_path).expanduser()
        if explicit.exists():
            return str(explicit)
        raise FileNotFoundError(f"LibreOffice executable not found at: {explicit}")

    for command in ("libreoffice", "soffice", "soffice.com"):
        found = shutil.which(command)
        if found:
            return found

    raise FileNotFoundError(
        "LibreOffice was not found. Install LibreOffice and make sure 'libreoffice' "
        "or 'soffice' is available in your PATH."
    )


def docx_to_pdf(
    input_docx: str | Path,
    output_pdf: str | Path | None = None,
    *,
    libreoffice_path: str | Path | None = None,
    timeout: int = 120,
) -> Path:
    """Convert a DOCX file to PDF using LibreOffice in headless mode."""
    input_path = Path(input_docx).expanduser().resolve()
    _ensure_file(input_path, [".doc", ".docx"])

    output_path = (
        Path(output_pdf).expanduser().resolve()
        if output_pdf
        else _default_output(input_path, ".pdf")
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    libreoffice = _find_libreoffice(libreoffice_path)

    command = [
        libreoffice,
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        str(output_path.parent),
        str(input_path),
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=timeout,
        check=False,
    )

    if result.returncode != 0:
        raise ConversionError(
            "Word to PDF conversion failed.\n"
            f"Command: {' '.join(command)}\n"
            f"STDOUT: {result.stdout}\n"
            f"STDERR: {result.stderr}"
        )

    generated_pdf = output_path.parent / f"{input_path.stem}.pdf"
    if not generated_pdf.exists():
        raise ConversionError(
            "LibreOffice finished but the expected PDF was not created.\n"
            f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        )

    if generated_pdf != output_path:
        if output_path.exists():
            output_path.unlink()
        generated_pdf.rename(output_path)

    return output_path
