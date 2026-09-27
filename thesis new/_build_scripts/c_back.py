import glob
import json
import re
import pandas as pd
from dx import *

S = "/tmp/claude-1000/-home-krishna-Desktop-Thesis-Hairfall-Thesis/3a0d67b6-c14e-4ab2-95b7-3de697bbdd86/scratchpad/"
A = S + "assets/"
P = "/home/krishna/Desktop/Thesis/Hairfall-Thesis/thesis_project/"
B = "/home/krishna/Desktop/Thesis/Hairfall-Thesis/backend/"
R = json.load(open(A + "analysis.json"))
MS, SZ = ["CatBoost", "TabPFN", "TabFM"], ["500", "2000", "Full"]
SZL = {"500": "500", "2000": "2,000", "Full": "17,284"}


def references(t):
    t.unnumbered_heading("REFERENCES", level=0)
    pages = open(S + "thesis_lay.txt").read().split("\f")
    txt = "\n".join(pages[71:74])
    txt = re.sub(r"\n\s*\d{2}\s*\n", "\n", txt)
    txt = txt.replace("REFERENCES", "")
    entries = re.split(r"\n\s*(?=\[\d+\]\s)", "\n" + txt.strip())
    n = 0
    for e in entries:
        e = re.sub(r"\s+", " ", e.replace("-\n", "-")).strip()
        if not e.startswith("["):
            continue
        n += 1
        para = t.doc.add_paragraph()
        pf = para.paragraph_format
        pf.alignment = L; pf.line_spacing = 1.15; pf.space_after = Pt(6)
        pf.left_indent = Cm(1.2); pf.first_line_indent = Cm(-1.2)
        pf.tab_stops.add_tab_stop(Cm(1.2), WD_TAB_ALIGNMENT.LEFT)
        m = re.match(r"(\[\d+\])\s+(.*)", e)
        t._runs(para, f"{m.group(1)}\t{m.group(2)}", size=12)
    assert n == 31, n


def _code(t, title, path, size=7.5):
    t.h4(title)
    t.code(open(path).read(), size)


def appendix_a(t):
    t.appendix_heading("A", "Source Code")
    t.p("This appendix gives the code of every step of the pipeline. Each step is a short Python script that is run in the Hairfall Lab (Section 3.8.9) after the shared module of Section A.1 is loaded. "
        "The scripts read the result files of the earlier steps from their step folders, and write their own results (metrics, predictions, figures, tables) to the folder of their step. The code is "
        "listed as it is stored in the project (folder backend/steps). A step is identified by its number: Steps 1 to 4 prepare the data, Steps 5 to 7 fit or run the three models at the three training "
        "sizes (a, b and c stand for 500, 2,000 and Full), Step 8 explains the models with SHAP, and Steps 9 and 10 compare the results.", align=J)
    t.h4("A.1 Shared helper module (lab.py)")
    t.code(open(B + "workspace/lab.py").read())
    files = sorted(glob.glob(B + "steps/Step_*.py"))
    for k, f in enumerate(files, 2):
        first = open(f).read().splitlines()[0].lstrip("# ").strip()
        t.h4(f"A.{k} {first}")
        t.code(open(f).read())
    k = len(files) + 2
    t.h4(f"A.{k} Memory and reliability settings added in the Kaggle runs")
    t.p("The steps run on Kaggle are packaged in notebook files (folder backend/kaggle). Each file embeds the module lab.py and the step code above without change, and adds the following block for the "
        "foundation models. It splits the prediction into batches that are halved after a GPU out-of-memory error, evaluates the attention in chunks and reduces the column chunk size of TabFM. These "
        "settings change the memory use and not the computation.", align=J)
    src = open(B + "kaggle/Step_07c_TabFM_Full_kaggle.py").read()
    i = src.index("def _chunk_predict(cls, chunk):")
    j = src.index("import builtins")
    t.code(src[i:j])


def appendix_b(t):
    t.appendix_heading("B", "Additional Figures")
    t.p("This appendix gives the figures that were not needed in the main text: the confusion matrices, the global SHAP importance plots and the SHAP beeswarm plots for the training sizes of 500 and "
        "2,000 rows, and two figures that describe the data.", align=J)
    for s, n in (("500", "500"), ("2000", "2,000")):
        t.figure_grid([A + f"cm_{m}_{s}.png" for m in MS], f"Confusion matrices with {n} training rows", cols=2, width_cm=6.6, subcaps=[f"({c}) {m}" for c, m in zip("abc", MS)])
    for s, n in (("500", "500"), ("2000", "2,000")):
        t.figure_grid([A + f"bar_{m}_{s}.png" for m in MS], f"Global feature importance (SHAP) with {n} training rows", cols=2, width_cm=7.4, subcaps=[f"({c}) {m}" for c, m in zip("abc", MS)])
    for s, n in (("500", "500"), ("2000", "2,000")):
        t.figure_grid([A + f"bee_{m}_{s}.png" for m in MS], f"SHAP beeswarm plots for the High risk class with {n} training rows", cols=2, width_cm=7.4, subcaps=[f"({c}) {m}" for c, m in zip("abc", MS)])
    t.figure(A + "class_dist.png", "Class distribution of the hair fall risk tiers in the dataset", 9.0)
    t.figure(A + "range_check.png", "Share of records outside the clinical reference range, by biomarker", 10.0)


def appendix_c(t):
    t.appendix_heading("C", "Result Tables from the Experiments")
    fr = pd.read_csv(P + "Step_10_FinalResults/final_results.csv")
    rows = [[r.model, "17,284" if str(r["size"]) == "Full" else f"{int(r['size']):,}", f"{r.accuracy:.4f}", f"{r.macro_f1:.4f}", f"{r.weighted_f1:.4f}", f"{r.roc_auc_ovr:.4f}", f"{r.fit_seconds:,.1f}", f"{r.predict_seconds:,.1f}"]
            for _, r in fr.iterrows()]
    t.table("Results of all model runs (final_results.csv from Step 10)", ["Model", "Training rows", "Accuracy", "Macro-F1", "Weighted F1", "ROC-AUC", "Fit (s)", "Predict (s)"], rows,
            [2.2, 2.2, 2.0, 2.0, 2.2, 2.0, 1.8, 2.3], size=9.5, align=["l", "c", "c", "c", "c", "c", "c", "c"],
            note="Rows for a run resumed from a checkpoint (TabFM, 500 rows) show a prediction time of 0.")
    for s, d in (("500", "05a_CatBoost_500"), ("2000", "05b_CatBoost_2000"), ("Full", "05c_CatBoost_Full")):
        g = pd.read_csv(P + f"Step_{d}/grid_search.csv")
        rows = [[str(int(r.depth)), str(r.learning_rate), f"{r.cv_macro_f1:.4f}", f"{r.cv_std:.4f}", str(int(r.iterations))] for _, r in g.iterrows()]
        t.table(f"CatBoost grid search with {SZL[s]} training rows (5-fold cross-validation, sorted by macro-F1)", ["Depth", "Learning rate", "CV macro-F1", "CV standard deviation", "Iterations"], rows, [2.2, 3.0, 3.0, 3.6, 2.6], size=10)
    rows = []
    for s in ("500", "2000"):
        for m in MS:
            o = R["models"][f"{m}|{s}"]
            for k, c in enumerate(["Low", "Moderate", "High"]):
                rows.append([SZL[s] if (m == "CatBoost" and k == 0) else "", m if k == 0 else "", c, f"{o['prec'][k]:.4f}", f"{o['rec'][k]:.4f}", f"{o['f1'][k]:.4f}"])
    t.table("Precision, recall and F1-score by risk tier with 500 and 2,000 training rows", ["Training rows", "Model", "Tier", "Precision", "Recall", "F1-score"], rows, [2.4, 2.6, 2.6, 2.6, 2.6, 2.6], size=9.5)
    feats = R["shap"]["CatBoost|Full"]["features"]
    imp = {m: dict(zip(R["shap"][f"{m}|Full"]["features"], R["shap"][f"{m}|Full"]["imp"])) for m in MS}
    rows = [[f, f"{imp['CatBoost'][f]:.4f}", f"{imp['TabPFN'][f]:.4f}", f"{imp['TabFM'][f]:.4f}"] for f in feats]
    t.table("Mean absolute SHAP value of every feature with the full training data (average over the three classes)", ["Feature", "CatBoost", "TabPFN", "TabFM"], rows, [5.4, 3.3, 3.3, 3.3], size=9.5,
            note="The values are not comparable between the columns (Section 4.3.2). Features are listed in the order of the CatBoost ranking.")
    rows = []
    for k in ("08a_CatBoost_SHAP_500", "08b_CatBoost_SHAP_2000", "08c_CatBoost_SHAP_Full", "08d_TabPFN_SHAP_500", "08e_TabPFN_SHAP_2000", "08f_TabPFN_SHAP_Full", "08g_TabFM_SHAP_500", "08h_TabFM_SHAP_2000", "08i_TabFM_SHAP_Full"):
        v = json.load(open(P + f"Step_{k}/shap_summary.json"))
        rows.append([v["model"], SZL[v["size"]], v["explainer"], str(v["rows_explained"]), str(v.get("nsamples", "-")), str(v.get("background", "-")), f"{v['seconds']:,.1f}"])
    t.table("Settings and run time of the nine SHAP analyses", ["Model", "Training rows", "Explainer", "Records explained", "Samples per record", "Background centres", "Time (s)"], rows,
            [2.2, 2.2, 3.3, 2.3, 2.3, 2.3, 1.8], size=9)


def appendix_d(t):
    t.appendix_heading("D", "Dataset Description and Sample Records")
    df = pd.read_csv(P + "data/data.csv")
    t.p(f"The dataset (data.csv) has {len(df):,} records and {df.shape[1]} columns. The columns id and full_name were removed before modelling, and hair_fall is the target. The 20 predictors are listed in Table 3.2. "
        "Table D.1 shows the first three records of the dataset without the name column, with one column per record.", align=J)
    cols = [c for c in df.columns if c != "full_name"]
    rows = [[c] + [str(df.iloc[i][c]) for i in range(3)] for c in cols]
    t.table("First three records of the dataset (full_name omitted; one column per record)", ["Column", "Record 1", "Record 2", "Record 3"], rows, [5.4, 3.3, 3.3, 3.3], size=9.5)
