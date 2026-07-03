# PDF Word Converter

A simple Python command-line tool that converts:

- PDF to Word `.docx`
- Word `.doc` / `.docx` to PDF

## How it works

PDF to Word uses the `pdf2docx` Python library.

Word to PDF uses LibreOffice in headless mode, which makes it practical on Windows, Linux, and macOS when LibreOffice is installed.

## Requirements

- Python 3.10+
- LibreOffice installed for Word to PDF conversion

### Install LibreOffice

On Debian, Ubuntu, or Kali Linux:

```bash
sudo apt update
sudo apt install libreoffice
```

On Windows or macOS, install LibreOffice from the official LibreOffice website, then make sure `soffice` or `libreoffice` is available in your system PATH.

## Installation

```bash
git clone https://github.com/JanVanYaku/pdf-word-converter.git
cd pdf-word-converter
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Usage

### Convert PDF to Word

```bash
python main.py pdf-to-word input.pdf output.docx
```

Convert only selected pages:

```bash
python main.py pdf-to-word input.pdf output.docx --pages 1,3,5
```

Convert a page range:

```bash
python main.py pdf-to-word input.pdf output.docx --start 2 --end 5
```

### Convert Word to PDF

```bash
python main.py word-to-pdf input.docx output.pdf
```

Use a custom LibreOffice path:

```bash
python main.py word-to-pdf input.docx output.pdf --libreoffice-path "/usr/bin/libreoffice"
```

## Notes

- PDF to Word conversion is not always perfect because PDF is a fixed-layout format.
- Scanned PDFs are images. They need OCR first before clean text conversion can work.
- Word to PDF quality depends on LibreOffice fonts and document compatibility.

## Project structure

```text
pdf-word-converter/
├── doc_converter/
│   ├── __init__.py
│   ├── cli.py
│   └── converter.py
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── LICENSE
```

## License

MIT License.
