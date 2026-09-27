"""Import step runs made on Kaggle so they appear in the UI, Postgres, MinIO and thesis_project/.

Usage (from backend/, with the lab's venv):
    .venv/bin/python import_kaggle_run.py ~/Downloads/Step_07c_TabFM_Full.zip
    .venv/bin/python import_kaggle_run.py ~/Downloads/some_folder/        # one sub-folder per step
    .venv/bin/python import_kaggle_run.py --sync [~/Documents] [--force]
        # import the newest Step_*.zip per step from a folder (default ~/Documents); steps whose
        # newest zip is already imported are skipped, so it is safe to run on every start
A step folder holds output.txt plus its result files (metrics.json / shap_summary.json, csv, png ...).
The run is stored with the step's local code (backend/steps/), so it can be re-run here; the Kaggle
version of the code stays in backend/kaggle/.
"""
import json
import mimetypes
import re
import zipfile
import shutil
import sys
import tempfile
from pathlib import Path

from app import project, store


def import_step(step: str, src: Path):
    if step not in project.step_ids():
        raise SystemExit(f"unknown step {step}")
    text = (src / "output.txt").read_text()
    took = re.search(r"\n?\[finished OK \| time: ([\d.]+)s\]\n?", text)  # wall time written by the Kaggle file
    seconds = float(took.group(1)) if took else None
    if took:
        text = text.replace(took.group(0), "")
    code = (project.STEPS_DIR / f"{step}.py").read_text()

    with store.pg() as c:
        rid = c.execute("INSERT INTO runs (step, code, status, started_at, finished_at, seconds, source) "
                        "VALUES (%s,%s,'ok', now(), now(), %s, 'kaggle') RETURNING id", (step, code, seconds)).fetchone()[0]

    outputs = [{"type": "stream", "name": "stdout", "text": text}]
    files, n = [], 0
    for p in sorted(src.iterdir()):
        if p.name in ("code.py", "output.txt") or not p.is_file():
            continue
        key = f"runs/{rid}/files/{p.name}"
        store.put_file(key, str(p))
        files.append({"key": key, "name": p.name, "type": mimetypes.guess_type(p.name)[0] or "application/octet-stream"})
        if p.suffix == ".png":
            n += 1
            store.put_file(f"runs/{rid}/image_{n}.png", str(p))
            outputs.append({"type": "image", "key": f"runs/{rid}/image_{n}.png"})

    with store.pg() as c:
        c.execute("UPDATE runs SET outputs=%s, files=%s WHERE id=%s", (store.dumps(outputs), store.dumps(files), rid))
    project.export_run(step, rid, code, outputs, files, seconds or 0)
    print(f"Imported {step} as run #{rid} -> thesis_project/{step}/")


def _clean_log(text: str) -> str:
    return re.sub(r"\n?\[finished OK \| time: [\d.]+s\]\n?", "", text)


def sync(folder: Path, force: bool = False):
    """Import the newest zip of every step found in `folder` (Kaggle downloads, e.g. ~/Documents)."""
    newest = {}  # step -> newest zip
    for z in folder.glob("Step_*.zip"):
        try:
            with zipfile.ZipFile(z) as zf:
                step = next(n.split("/")[0] for n in zf.namelist() if n.endswith("/output.txt"))
        except (zipfile.BadZipFile, StopIteration):
            continue
        if step not in newest or z.stat().st_mtime > newest[step].stat().st_mtime:
            newest[step] = z
    if not newest:
        print(f"no Step_*.zip files in {folder}")
        return
    todo = 0
    for step in sorted(newest):
        if step not in project.step_ids():
            print(f"skip {newest[step].name}: unknown step {step}")
            continue
        with zipfile.ZipFile(newest[step]) as zf:
            new_text = _clean_log(zf.read(f"{step}/output.txt").decode())
        with store.pg() as c:
            row = c.execute("SELECT outputs FROM runs WHERE step=%s AND source='kaggle' ORDER BY id DESC LIMIT 1",
                            (step,)).fetchone()
        old = row[0] if row else None
        old = json.loads(old) if isinstance(old, str) else old
        if not force and old and old[0].get("text") == new_text:
            continue
        tmp = Path(tempfile.mkdtemp())
        shutil.unpack_archive(newest[step], tmp)
        import_step(step, tmp / step)
        shutil.rmtree(tmp, ignore_errors=True)
        todo += 1
    print(f"Sync done: {todo} step(s) imported, {len(newest) - todo} already up to date ({folder})")


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    store.init()
    if sys.argv[1] == "--sync":
        args = [a for a in sys.argv[2:] if a != "--force"]
        sync(Path(args[0] if args else "~/Documents").expanduser(), "--force" in sys.argv)
        return
    src = Path(sys.argv[1]).expanduser()
    if src.suffix == ".zip":
        tmp = Path(tempfile.mkdtemp())
        shutil.unpack_archive(src, tmp)
        src = tmp
    if (src / "output.txt").exists():
        import_step(src.name, src)
    else:
        dirs = [d for d in sorted(src.glob("Step_*")) if d.is_dir() and (d / "output.txt").exists()]
        if not dirs:
            raise SystemExit(f"no step folders with output.txt in {src}")
        for d in dirs:
            import_step(d.name, d)


if __name__ == "__main__":
    main()
