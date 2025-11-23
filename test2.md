#!/usr/bin/env python3
"""
Convert a single BMP file or every BMP in a folder to a MicroPython
bitmap definition that can be used with an SSD1306 OLED on ESP‑32.

Output format (example):
    my_image = [
        0b10101010,
        0b11001100,
        ...
    ]
"""

import os
import struct
import sys
from pathlib import Path

# ----------------------------------------------------------------------
# Helper: read a 1‑bit BMP and return a list of rows, each row as a list of 0/1
# ----------------------------------------------------------------------
def read_bmp_1bit(path: Path):
    with path.open("rb") as f:
        # ---- BMP header -------------------------------------------------
        header = f.read(14)
        if header[:2] != b"BM":
            raise ValueError("Not a BMP file")
        # skip file size, reserved fields, offset to pixel data
        _, _, offset = struct.unpack("<IHHI", header + f.read(4))

        # ---- DIB header (BITMAPINFOHEADER) -------------------------------
        dib = f.read(40)
        (
            width,
            height,
            planes,
            bpp,
            compression,
            img_size,
            xppm,
            yppm,
            clr_used,
            clr_important,
        ) = struct.unpack("<iiHHIIIIII", dib)

        if bpp != 1:
            raise ValueError("Only 1‑bit (black‑white) BMPs are supported")
        if compression != 0:
            raise ValueError("Compressed BMPs are not supported")

        # ---- Color table (2 entries) ------------------------------------
        # BMP stores colors as BGR0; we only need to know which index is white.
        # Usually index 0 = black, 1 = white, but we check to be safe.
        palette = [f.read(4) for _ in range(2)]
        white_index = 1 if palette[1][:3] == b"\xff\xff\xff" else 0

        # ---- Pixel data -------------------------------------------------
        # BMP rows are padded to a 4‑byte boundary.
        row_bytes = (width + 7) // 8
        padded_row = (row_bytes + 3) & ~3  # round up to multiple of 4

        f.seek(offset)
        rows = []
        for _ in range(abs(height)):
            raw = f.read(padded_row)[:row_bytes]
            bits = []
            for byte in raw:
                for i in range(8):
                    if len(bits) >= width:
                        break
                    # most‑significant bit first
                    bit = (byte >> (7 - i)) & 1
                    # map BMP palette index to 0/1 (0 = black, 1 = white)
                    bits.append(bit if white_index == 1 else 1 - bit)
            rows.append(bits)

        # BMP stores rows bottom‑up unless height is negative
        if height > 0:
            rows.reverse()
        return rows


# ----------------------------------------------------------------------
# Convert rows → list of binary literals (as strings)
# ----------------------------------------------------------------------
def rows_to_literal(rows):
    literals = []
    for row in rows:
        # pack bits into an integer
        value = 0
        for bit in row:
            value = (value << 1) | bit
        # format as binary literal with minimal width
        literals.append(f"0b{value:0{len(row)}b}")
    return literals


# ----------------------------------------------------------------------
# Main conversion routine
# ----------------------------------------------------------------------
def convert_file(bmp_path: Path, out_dir: Path):
    rows = read_bmp_1bit(bmp_path)
    literals = rows_to_literal(rows)

    var_name = bmp_path.stem.replace("-", "_")
    out_path = out_dir / f"{var_name}.txt"

    with out_path.open("w") as out:
        out.write(f"{var_name} = [\n")
        for lit in literals:
            out.write(f"    {lit},\n")
        out.write("]\n")
    print(f"✔ {bmp_path.name} → {out_path.name}")


# ----------------------------------------------------------------------
# CLI handling
# ----------------------------------------------------------------------
def main():
    if len(sys.argv) != 3:
        print(
            "Usage: python bmp2mpy.py <input_path> <output_folder>\n"
            "  <input_path>  : BMP file or directory containing BMPs\n"
            "  <output_folder>: where .txt files will be written"
        )
        sys.exit(1)

    input_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)

    if input_path.is_file():
        convert_file(input_path, out_dir)
    elif input_path.is_dir():
        for bmp_file in input_path.rglob("*.bmp"):
            convert_file(bmp_file, out_dir)
    else:
        print("Error: input path does not exist.")
        sys.exit(1)


if __name__ == "__main__":
    main()
