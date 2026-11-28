"""topdf.py — make a PDF next to each Word file.

Usage:  python3 topdf.py "<file>.docx" ["<another>.docx" ...]

On a Mac it uses Microsoft Word. Otherwise, or if Word fails, it uses LibreOffice
(soffice, found on the PATH or in its usual install folder). If neither works it
says so: open the .docx in Word and choose File › Save As › PDF.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

SOFFICE_PLACES = ["/Applications/LibreOffice.app/Contents/MacOS/soffice",
                  r"C:\Program Files\LibreOffice\program\soffice.exe",
                  r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"]


def with_word(docx: Path, pdf: Path) -> bool:
    if sys.platform != "darwin":
        return False
    script = f'''
tell application "Microsoft Word"
    set d to open file name (POSIX file "{docx}" as text)
    save as d file name (POSIX file "{pdf}" as text) file format format PDF
    close d saving no
end tell'''
    try:
        subprocess.run(["osascript", "-e", script], check=True, capture_output=True, text=True, timeout=180)
        return pdf.exists()
    except Exception:
        return False


def with_libreoffice(docx: Path) -> bool:
    exe = shutil.which("soffice") or next((p for p in SOFFICE_PLACES if os.path.exists(p)), None)
    if not exe:
        return False
    try:
        subprocess.run([exe, "--headless", "--convert-to", "pdf", "--outdir", str(docx.parent), str(docx)],
                       check=True, capture_output=True, timeout=180)
        return docx.with_suffix(".pdf").exists()
    except Exception:
        return False


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    failed = False
    for arg in sys.argv[1:]:
        docx = Path(arg).expanduser().resolve()
        if not docx.is_file():
            print(f"NOT FOUND: {docx}"); failed = True; continue
        pdf = docx.with_suffix(".pdf")
        if with_word(docx, pdf) or with_libreoffice(docx):
            print("saved", pdf)
        else:
            print(f"PDF NOT MADE for {docx.name}: open it in Word and choose File › Save As › PDF."); failed = True
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
