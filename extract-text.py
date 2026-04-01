#!/usr/bin/env python3
"""Extract plain text from PDF, EPUB, and MHTML files."""
from __future__ import annotations

import os
import sys
from email import policy
from email.parser import BytesParser

try:
    import fitz  # type: ignore
except Exception:
    fitz = None

try:
    import ebooklib  # type: ignore
    from ebooklib import epub  # type: ignore
except Exception:
    ebooklib = None
    epub = None

try:
    from bs4 import BeautifulSoup  # type: ignore
except Exception:
    BeautifulSoup = None


def normalize_quotes(text: str) -> str:
    replacements = {
        "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"',
        "\u2014": "—", "\u2013": "-",
        "\u2026": "...", "\u00a0": " ",
    }
    for smart, plain in replacements.items():
        text = text.replace(smart, plain)
    return text


def extract_text_from_pdf(pdf_path: str) -> str:
    if fitz is None:
        raise RuntimeError("PyMuPDF is not installed")
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text("text") + "\n"
    return normalize_quotes(text)


def extract_text_from_epub(epub_path: str) -> str:
    if epub is None or ebooklib is None or BeautifulSoup is None:
        raise RuntimeError("ebooklib and beautifulsoup4 are required")
    text = ""
    book = epub.read_epub(epub_path)
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), "html.parser")
            text += soup.get_text() + "\n"
    return normalize_quotes(text)


def extract_text_from_mhtml(mhtml_path: str) -> str:
    if BeautifulSoup is None:
        raise RuntimeError("beautifulsoup4 is required")
    text_parts = []
    with open(mhtml_path, "rb") as handle:
        msg = BytesParser(policy=policy.default).parse(handle)

    def decode_part(part) -> str:
        charset = part.get_content_charset() or "utf-8"
        payload = part.get_payload(decode=True) or b""
        return payload.decode(charset, errors="replace")

    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype == "text/html":
                html = decode_part(part)
                soup = BeautifulSoup(html, "html.parser")
                text_parts.append(soup.get_text(separator="\n", strip=True))
            elif ctype == "text/plain":
                text_parts.append(decode_part(part))
    else:
        content = decode_part(msg)
        if msg.get_content_type() == "text/html":
            soup = BeautifulSoup(content, "html.parser")
            text_parts.append(soup.get_text(separator="\n", strip=True))
        else:
            text_parts.append(content)
    return normalize_quotes("\n\n".join(text_parts))


def save_text(text: str, original_path: str) -> None:
    output_file = os.path.splitext(original_path)[0] + ".txt"
    with open(output_file, "w", encoding="utf-8") as handle:
        handle.write(text)
    print(f"[ok] {output_file}")


def process_file(file_path: str) -> None:
    if not os.path.isfile(file_path):
        print(f"[missing] {file_path}")
        return
    lower = file_path.lower()
    try:
        if lower.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif lower.endswith(".epub"):
            text = extract_text_from_epub(file_path)
        elif lower.endswith((".mhtml", ".mht")):
            text = extract_text_from_mhtml(file_path)
        else:
            print(f"[skip] unsupported file: {file_path}")
            return
    except Exception as exc:
        print(f"[error] {file_path}: {exc}")
        return

    if text.strip():
        save_text(text, file_path)
    else:
        print(f"[empty] {file_path}")


def process_directory(directory: str) -> None:
    for filename in os.listdir(directory):
        if filename.lower().endswith((".pdf", ".epub", ".mhtml", ".mht")):
            process_file(os.path.join(directory, filename))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            process_file(arg)
    else:
        process_directory(os.getcwd())
