import json, glob, os, math
import numpy as np, pandas as pd
from scipy.stats import spearmanr
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support, cohen_kappa_score

P = "/home/krishna/Desktop/Thesis/Hairfall-Thesis/thesis_project/"
A = "/tmp/claude-1000/-home-krishna-Desktop-Thesis-Hairfall-Thesis/3a0d67b6-c14e-4ab2-95b7-3de697bbdd86/scratchpad/assets/"
MODELS = {"CatBoost": "Step_05", "TabPFN": "Step_06", "TabFM": "Step_07"}
SIZES = {"500": "a", "2000": "b", "Full": "c"}
out = {"models": {}}

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h

for m, pre in MODELS.items():
    for s, l in SIZES.items():
        d = glob.glob(f"{P}{pre}{l}_{m}_{s}")[0]
        pr = pd.read_csv(d + "/predictions.csv"); met = json.load(open(d + "/metrics.json"))
        y, yp = pr.y_true.values, pr.y_pred.values
        cm = confusion_matrix(y, yp)
        p_, r_, f_, sup = precision_recall_fscore_support(y, yp, labels=[0, 1, 2], zero_division=0)
        n = len(y); k = int((y == yp).sum()); lo, hi = wilson(k, n)
        nb = int(cm[0,1]+cm[1,0]+cm[1,2]+cm[2,1]); err = int(n - k)
        out["models"][f"{m}|{s}"] = dict(
            metrics=met, cm=cm.tolist(), prec=p_.tolist(), rec=r_.tolist(), f1=f_.tolist(), support=sup.tolist(),
            macro_p=float(p_.mean()), macro_r=float(r_.mean()), macro_f1=float(f_.mean()), acc=k / n, correct=k, n=n,
            ci=[lo, hi], kappa=float(cohen_kappa_score(y, yp)), qwk=float(cohen_kappa_score(y, yp, weights="quadratic")),
            within1=float((np.abs(y - yp) <= 1).mean()), mae=float(np.abs(y - yp).mean()),
            neighbour_errors=nb, errors=err, low_high=int(cm[0,2]), high_low=int(cm[2,0]),
            mod_recall=float(r_[1]), high_recall=float(r_[2]), low_recall=float(r_[0]))

# data descriptives
df = pd.read_csv(P + "data/data.csv")
cont = ["age","total_protein","calcium","iron","vitamin_d","alt_liver","manganese","body_water_content","stress_level","total_keratine","hair_texture"]
out["desc"] = {c: dict(mean=float(df[c].mean()), sd=float(df[c].std()), min=float(df[c].min()), max=float(df[c].max())) for c in cont}
out["by_tier"] = {c: [float(df[df.hair_fall == t][c].mean()) for t in (0, 1, 2)] for c in cont}
flags = ["family_hair_fall_history","chronic_illness","late_night_sleep","sleep_disturbance","water_reason","chemical_use","anemia","stress"]
out["flags"] = {c: [float(df[df.hair_fall == t][c].mean()) for t in (0, 1, 2)] for c in flags}
out["spearman"] = {c: float(spearmanr(df[c], df.hair_fall)[0]) for c in cont + flags}
out["gender"] = df.gender.value_counts().to_dict(); out["classes"] = df.hair_fall.value_counts().sort_index().tolist()
out["n"] = len(df)

# SHAP tables
shap = {}
for f in sorted(glob.glob(P + "Step_08*/shap_importance.csv")):
    tag = os.path.basename(os.path.dirname(f)).split("_", 2)[2]   # CatBoost_SHAP_500 etc
    m, _, s = tag.split("_")
    t = pd.read_csv(f); shap[f"{m}|{s}"] = dict(features=t.feature.tolist(), imp=t.mean_abs_all.round(4).tolist(),
                                               high=t.mean_abs_High.round(4).tolist(), low=t.mean_abs_Low.round(4).tolist(), mod=t.mean_abs_Moderate.round(4).tolist())
out["shap"] = shap
feats = shap["CatBoost|Full"]["features"]
def rank(key): return {f: i + 1 for i, f in enumerate(shap[key]["features"])}
keys = list(shap)
rc = {}
for a in keys:
    for b in keys:
        ra, rb = rank(a), rank(b); rc[f"{a}~{b}"] = float(spearmanr([ra[f] for f in feats], [rb[f] for f in feats])[0])
out["shap_rank_corr"] = rc
out["top7_overlap"] = {k: sorted(set(shap[k]["features"][:7])) for k in keys}
json.dump(out, open(A + "analysis.json", "w"), indent=1)
print("ok", len(out["models"]), "models,", len(shap), "shap sets")
for k in ("CatBoost|Full","TabPFN|Full","TabFM|Full"):
    o = out["models"][k]; print(k, round(o["acc"],4), o["ci"], "kappa",round(o["kappa"],3),"qwk",round(o["qwk"],3),"within1",round(o["within1"],4),"nb",o["neighbour_errors"],"/",o["errors"], "LH",o["low_high"],"HL",o["high_low"])
print("spearman top:", sorted(out["spearman"].items(), key=lambda x:-abs(x[1]))[:6])
print("rank corr Full:", round(rc["CatBoost|Full~TabPFN|Full"],3), round(rc["CatBoost|Full~TabFM|Full"],3), round(rc["TabPFN|Full~TabFM|Full"],3))
print("top7 all identical?", len({tuple(v) for v in out["top7_overlap"].values()}))
