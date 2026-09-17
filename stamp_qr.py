#!/usr/bin/env python3.13
"""Stamp a QR code (bottom-right) onto finalized resume PDFs -> *_print.pdf (offline/线下版).

Usage: python3.13 stamp_qr.py <pdf> [<pdf> ...]
"""
import io
import os
import sys
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

QR_PNG = "/Users/louis/PycharmProjects/offer-call/homepage/qrcode.png"
URL = "https://louisultra.github.io/"
SIZE_MM = 12  # 34pt: fits the bottom margin strip without touching body text

def stamp(src):
    reader = PdfReader(src)
    w = float(reader.pages[0].mediabox.width)
    h = float(reader.pages[0].mediabox.height)
    size = SIZE_MM * 72 / 25.4
    x = w - 35 - size   # right margin zone (right edge ~w-35..w)
    y = 1.0             # bottom margin strip, below the 36pt body area
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(w, h))
    c.drawImage(ImageReader(QR_PNG), x, y, size, size, mask="auto")
    # caption to the LEFT of the code, inside the bottom margin strip
    c.setFont("Helvetica", 6.0)
    c.setFillColorRGB(0.40, 0.40, 0.40)
    c.drawRightString(x - 5, y + size / 2 - 2, "扫码看成果主页")
    c.drawRightString(x - 5, y + size / 2 - 9, "louisultra.github.io")
    c.save()
    buf.seek(0)
    overlay = PdfReader(buf)
    writer = PdfWriter()
    for page in reader.pages:
        page.merge_page(overlay.pages[0])
        writer.add_page(page)
    root, _ = os.path.splitext(src)
    dst = root + "_print.pdf"
    with open(dst, "wb") as f:
        writer.write(f)
    return dst

if __name__ == "__main__":
    failed = []
    for p in sys.argv[1:]:
        try:
            print(stamp(p))
        except Exception as e:
            failed.append((p, str(e)))
            print(f"FAILED: {p}: {e}", file=sys.stderr)
    if failed:
        sys.exit(1)
