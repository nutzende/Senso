#!/usr/bin/env bash
# bmp2ssd1306.sh — Convert BMP(s) to Python arrays of 0b... for SSD1306
# Requirements: ImageMagick + Python3
# Usage:
#   ./bmp2ssd1306.sh input.bmp
#   ./bmp2ssd1306.sh ./badges_dir

set -euo pipefail

INPUT="$1"
OUTDIR="./converted"
mkdir -p "$OUTDIR"

process_file() {
  local infile="$1"
  local base="$(basename "$infile")"
  local name="${base%.*}"
  local outfile="$OUTDIR/${name}.py"

  # Use Python to read BMP and emit binary literals
  python3 <<'PYCODE' "$infile" "$outfile" "$name"
import sys
from PIL import Image

infile, outfile, varname = sys.argv[1:4]

# Open BMP
img = Image.open(infile).convert("1")  # ensure 1-bit
w, h = img.size
pixels = img.load()

rows = []
for y in range(h):
    row_bits = ""
    for x in range(w):
        bit = 0 if pixels[x, y] == 0 else 1
        row_bits += str(bit)
        # group into bytes
        if len(row_bits) == 8:
            rows.append("0b" + row_bits)
            row_bits = ""
    if row_bits:  # pad last byte if width not multiple of 8
        row_bits = row_bits.ljust(8, "0")
        rows.append("0b" + row_bits)

with open(outfile, "w") as f:
    f.write(f"{varname} = [\n")
    for r in rows:
        f.write(f"    {r},\n")
    f.write("]\n")
    f.write(f"# Resolution: {w}x{h}\n")
PYCODE

  echo "Converted: $outfile"
}

if [[ -d "$INPUT" ]]; then
  shopt -s nullglob
  for f in "$INPUT"/*.bmp "$INPUT""/*.BMP"; do
    [[ -f "$f" ]] && process_file "$f"
  done
else
  process_file "$INPUT"
fi

echo "Done. Output in: $OUTDIR"