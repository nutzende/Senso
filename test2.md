#!/usr/bin/env python3
"""
bmp2ssd1306.py — Convert BMP(s) to Python arrays of 0b... for SSD1306 OLED
Requirements: Pillow (install with `pip install pillow`)
Usage:
    python bmp2ssd1306.py input.bmp
    python bmp2ssd1306.py ./badges_dir
Outputs: one .py file per BMP inside ./converted
"""

import sys
from pathlib import Path
from PIL import Image

def convert_bmp(infile: Path, outdir: Path):
    name = infile.stem
    outfile = outdir / f"{name}.py"

    img = Image.open(infile).convert("1")  # force 1-bit
    w, h = img.size
    pixels = img.load()

    rows = []
    for y in range(h):
        row_bits = ""
        for x in range(w):
            bit = 0 if pixels[x, y] == 0 else 1
            row_bits += str(bit)
            if len(row_bits) == 8:
                rows.append("0b" + row_bits)
                row_bits = ""
        if row_bits:  # pad last byte if width not multiple of 8
            row_bits = row_bits.ljust(8, "0")
            rows.append("0b" + row_bits)

    with open(outfile, "w") as f:
        f.write(f"{name} = [\n")
        for r in rows:
            f.write(f"    {r},\n")
        f.write("]\n")
        f.write(f"{name}_width = {w}\n")
        f.write(f"{name}_height = {h}\n")

    print(f"Converted: {outfile}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python bmp2ssd1306.py input.bmp | input_directory