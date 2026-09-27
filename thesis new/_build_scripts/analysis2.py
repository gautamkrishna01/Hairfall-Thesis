import json, glob
import numpy as np, pandas as pd
from sklearn.metrics import log_loss
P = "/home/krishna/Desktop/Thesis/Hairfall-Thesis/thesis_project/"
A = "/tmp/claude-1000/-home-krishna-Desktop-Thesis-Hairfall-Thesis/3a0d67b6-c14e-4ab2-95b7-3de697bbdd86/scratchpad/assets/"
R = json.load(open(A + "analysis.json"))
MODELS = {"CatBoost": "Step_05", "TabPFN": "Step_06", "TabFM": "Step_07"}; SIZES = {"500": "a", "2000": "b", "Full": "c"}
test = pd.read_csv(P + "Step_04_TrainTestSplit/test.csv")
pred = {}
for m, pre in MODELS.items():
    for s, l in SIZES.items():
        d = glob.glob(f"{P}{pre}{l}_{m}_{s}")[0]
        pr = pd.read_csv(d + "/predictions.csv").sort_values("row").reset_index(drop=True)
        assert (pr.row.values == test.index.values).all() and (pr.y_true.values == test.hair_fall.values).all()
        pred[(m, s)] = pr
ex = {"prob": {}, "overlap": {}, "gender": {}, "age": {}}
for (m, s), pr in pred.items():
    P3 = pr[["p_Low", "p_Moderate", "p_High"]].values; y = pr.y_true.values
    ll = log_loss(y, P3, labels=[0, 1, 2]); br = float(((P3 - np.eye(3)[y]) ** 2).sum(1).mean())
    conf = P3.max(1); corr = (pr.y_pred.values == y)
    ex["prob"][f"{m}|{s}"] = dict(logloss=float(ll), brier=br, mean_conf=float(conf.mean()), acc=float(corr.mean()))
for s in SIZES:
    ok = np.stack([(pred[(m, s)].y_pred.values == pred[(m, s)].y_true.values) for m in MODELS])
    k = ok.sum(0)
    ex["overlap"][s] = dict(all3=int((k == 3).sum()), two=int((k == 2).sum()), one=int((k == 1).sum()), none=int((k == 0).sum()), n=int(len(k)))
g = test.gender.values; age = test.age.values
bands = {"20-29": (age <= 29), "30-39": (age >= 30) & (age <= 39), "40-55": (age >= 40)}
for m in MODELS:
    for s in ("500", "Full"):
        pr = pred[(m, s)]; corr = (pr.y_pred.values == pr.y_true.values)
        ex["gender"][f"{m}|{s}"] = {"Female": [float(corr[g == 0].mean()), int((g == 0).sum())], "Male": [float(corr[g == 1].mean()), int((g == 1).sum())], "Other": [float(corr[g == 2].mean()) if (g == 2).any() else None, int((g == 2).sum())]}
        ex["age"][f"{m}|{s}"] = {b: [float(corr[mask].mean()), int(mask.sum())] for b, mask in bands.items()}
R["extra"] = ex
json.dump(R, open(A + "analysis.json", "w"), indent=1)
for s in SIZES: print(s, ex["overlap"][s])
for k in ("CatBoost|Full", "TabPFN|Full", "TabFM|Full", "CatBoost|500", "TabPFN|500"): print(k, {a: round(b, 4) for a, b in ex["prob"][k].items()})
print(ex["gender"]["CatBoost|Full"], ex["age"]["TabPFN|Full"])
