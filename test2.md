@echo off
REM bmp2ssd1306.bat — Convert BMP(s) to Python arrays of 0b... for SSD1306
REM Requirements: Python 3 + Pillow (install with: pip install pillow)

setlocal enabledelayedexpansion

if "%~1"=="" (
    echo Usage: bmp2ssd1306.bat input.bmp ^| input_directory
    exit /b 1
)

set INPUT=%~1
set OUTDIR=converted

if not exist "%OUTDIR%" (
    mkdir "%OUTDIR%"
)

REM Check if input is a directory or file
if exist "%INPUT%\*" (
    REM Directory mode
    for %%F in ("%INPUT%\*.bmp") do (
        call :process "%%~fF"
    )
    for %%F in ("%INPUT%\*.BMP") do (
        call :process "%%~fF"
    )
) else (
    REM Single file mode
    if not exist "%INPUT%" (
        echo Error: input file not found: %INPUT%
        exit /b 1
    )
    call :process "%INPUT%"
)

echo Done. Output in %OUTDIR%
exit /b 0

:process
set FILE=%~1
set NAME=%~n1
set OUTFILE=%OUTDIR%\%NAME%.py

echo Converting %FILE% ...

python - <<PYCODE %FILE% %OUTFILE% %NAME%
import sys
from PIL import Image

infile, outfile, varname = sys.argv[1:4]

img = Image.open(infile).convert("1")
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
    if row_bits:
        row_bits = row_bits.ljust(8, "0")
        rows.append("0b" + row_bits)

with open(outfile, "w") as f:
    f.write(f"{varname} = [\n")
    for r in rows:
        f.write(f"    {r},\n")
    f.write("]\n")
    f.write(f"{varname}_width = {w}\n")
    f.write(f"{varname}_height = {h}\n")
PYCODE

echo Converted: %OUTFILE%
exit /b 0