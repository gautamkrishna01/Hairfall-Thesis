import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dx import *
import c_front as F
import c_ch12 as C12
import c_ch3 as C3
import c_ch4 as C4
import c_ch5 as C5
import c_back as CB
import dx

S = "/tmp/claude-1000/-home-krishna-Desktop-Thesis-Hairfall-Thesis/3a0d67b6-c14e-4ab2-95b7-3de697bbdd86/scratchpad/"
OUTDIR = "/home/krishna/Desktop/Thesis/Hairfall-Thesis/thesis new/"
NAME = "Hairfall_Thesis_New"
TAIL = [(0, "Table of Contents", "Table of Contents"), (0, "List of Tables", "List of Tables"), (0, "List of Figures", "List of Figures"), (0, "List of Appendices", "List of Appendices")]


def roman(n):
    vals = [(10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]
    out = ""
    for v, s in vals:
        while n >= v:
            out += s; n -= v
    return out


def build(path, entries=None, captions=None, appendices=None, pages=None):
    pages = pages or {}
    t = Thesis()
    F.cover(t)
    t.new_section(fmt="lowerRoman", start=1, footer=True, first_page_blank=True)
    F.title_page(t)
    t.page_break()
    F.declaration(t); F.recommendation(t); F.certificate(t); F.acknowledgements(t); F.abbreviations(t); F.units(t)
    F.abstract(t, C5.ABSTRACT, C5.KEYWORDS)
    if entries is not None:
        t.toc_page("Table of Contents", entries, pages)
        t.list_page("List of Tables", captions["Table"], pages, "Table")
        t.list_page("List of Figures", captions["Fig."], pages, "Fig.")
        t.list_page("List of Appendices", appendices, pages, "App")
    t.new_section(fmt="decimal", start=1, footer=True)
    C12.chapter1(t); C12.chapter2(t); C3.chapter3(t); C4.chapter4(t); C5.chapter5(t)
    CB.references(t)
    CB.appendix_a(t); CB.appendix_b(t); CB.appendix_c(t); CB.appendix_d(t)
    t.save(path)
    return t


def to_pdf(docx):
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", os.path.dirname(docx), docx], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=900)
    return docx[:-5] + ".pdf"


def page_texts(pdf):
    return subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout.split("\f")


def detect(pdf, entries, captions, appendices):
    pg = page_texts(pdf)
    lines = [[l.strip() for l in p.splitlines()] for p in pg]
    main = next(i for i, ls in enumerate(lines) if "CHAPTER 1" in ls and i > 8)
    pages, ptr, missing = {}, 2, []
    front = [e for e in entries if e[2] in [x[2] for x in entries[:entries.index(next(e2 for e2 in entries if e2[2] == "CHAPTER 1"))]]]
    for lvl, text, key in entries:
        is_front = (lvl == 0 and not key.startswith(("CHAPTER", "APPENDIX", "REFERENCES")))
        lo, hi = (2, main) if is_front else (max(ptr, main), len(pg))
        want = text if not key.startswith("CHAPTER") and not key.startswith("APPENDIX") else key
        found = next((i for i in range(lo, hi) if want in lines[i]), None)
        if found is None:
            missing.append(key); continue
        pages[("toc", key)] = roman(found) if is_front else str(found - main + 1)
        if not is_front:
            ptr = found
        else:
            pages[("toc", key)] = roman(found)          # cover = pdf page 0 (unnumbered), title page = i
    def label(i): return str(i - main + 1)
    for kind, items in (("Table", captions["Table"]), ("Fig.", captions["Fig."])):
        for num, _ in items:
            rx = re.compile(r"^" + re.escape(num) + r":")
            found = next((i for i in range(main, len(pg)) if any(rx.match(l) for l in lines[i])), None)
            if found is None:
                missing.append(num)
            else:
                pages[(kind, num)] = label(found)
    for num, title in appendices:
        letter = num.split()[1].rstrip(":")
        found = next((i for i in range(main, len(pg)) if f"APPENDIX {letter}" in lines[i]), None)
        pages[("App", num)] = label(found) if found is not None else ""
    return pages, main, missing


if __name__ == "__main__":
    os.makedirs(OUTDIR, exist_ok=True)
    draft = S + "draft0.docx"
    t0 = build(draft)
    dx.LABELS.update(t0.labels)
    t0 = build(draft)
    dx.LABELS.update(t0.labels)
    toc = t0.toc
    first_main = next(i for i, e in enumerate(toc) if e[2] == "CHAPTER 1")
    entries = toc[:first_main] + TAIL + toc[first_main:]
    captions, appendices = t0.captions, t0.appendices
    print("entries", len(entries), "tables", len(captions["Table"]), "figures", len(captions["Fig."]), "appendices", len(appendices))
    pages = {}
    docx = OUTDIR + NAME + ".docx"
    for it in range(3):
        tt = build(docx, entries, captions, appendices, pages)
        dx.LABELS.update(tt.labels)
        pdf = to_pdf(docx)
        newpages, main, missing = detect(pdf, entries, captions, appendices)
        print(f"pass {it + 1}: main body starts at pdf page {main + 1}; missing: {missing}; changed: {sum(1 for k in newpages if pages.get(k) != newpages[k])}")
        if newpages == pages:
            break
        pages = newpages
    print("done", pdf)
