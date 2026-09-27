import shutil, glob, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams["font.family"] = "Liberation Serif"
P = "/home/krishna/Desktop/Thesis/Hairfall-Thesis/thesis_project/"
A = "/tmp/claude-1000/-home-krishna-Desktop-Thesis-Hairfall-Thesis/3a0d67b6-c14e-4ab2-95b7-3de697bbdd86/scratchpad/assets/"

# copy Lab figures under stable names
M = {"CatBoost": "Step_05", "TabPFN": "Step_06", "TabFM": "Step_07"}
S = {"500": "a", "2000": "b", "Full": "c"}
for m, pre in M.items():
    for s, l in S.items():
        d = glob.glob(f"{P}{pre}{l}_{m}_{s}")[0]
        shutil.copy(d + "/confusion_matrix.png", f"{A}cm_{m}_{s}.png")
SH = {"CatBoost": ("08a", "08b", "08c"), "TabPFN": ("08d", "08e", "08f"), "TabFM": ("08g", "08h", "08i")}
for m, ids in SH.items():
    for s, i in zip(("500", "2000", "Full"), ids):
        d = glob.glob(f"{P}Step_{i}_*")[0]
        shutil.copy(d + "/shap_beeswarm_high.png", f"{A}bee_{m}_{s}.png")
        shutil.copy(d + "/shap_global_importance.png", f"{A}bar_{m}_{s}.png")
shutil.copy(P + "Step_10_FinalResults/scaling_curves.png", A + "scaling.png")
shutil.copy(P + "Step_10_FinalResults/timings.png", A + "timings.png")
shutil.copy(P + "Step_02_LoadData/class_distribution.png", A + "class_dist.png")
shutil.copy(P + "Step_03_CleanEncode/range_check.png", A + "range_check.png")

# block diagram
fig, ax = plt.subplots(figsize=(9.2, 6.6)); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
def box(x, y, w, h, text, fc="#f2f2f2", fs=9.5, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2", fc=fc, ec="black", lw=1))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, fontweight="bold" if bold else "normal", linespacing=1.25)
def arrow(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=12, lw=1.1, color="black"))
box(20, 88, 60, 9, "Company dataset [27]\n(biochemical, lifestyle and heredity features)")
box(20, 73, 60, 9, "Dataset used: 21,606 records, 23 columns\n(20 predictors, 3 risk tiers)", "#dfe9f7")
box(20, 58, 60, 9, "Validation and cleaning (Steps 2-3)\nreference ranges, drop id / full_name, encode gender", "#f2f2f2")
box(20, 42, 60, 11, "Stratified 80/20 split, seed 42 (Step 4)\ntrain 17,284 | test 4,322 (same for every model)\ntraining sizes used by each model: 500, 2,000, Full", "#dfe9f7")
box(3, 28, 30, 10, "CatBoost (Step 5)\nGrid search + 5-fold CV\n(tuned baseline)", "#fde9c8")
box(35, 28, 30, 10, "TabPFN (Step 6)\nzero-shot, training rows\nas context", "#d9efdc")
box(67, 28, 30, 10, "TabFM (Step 7)\nzero-shot, training rows\nas context", "#d9efdc")
box(3, 6, 30, 13, "Evaluation on the 4,322 test records\naccuracy, macro-P/R/F1, ROC-AUC,\nkappa, Wilson intervals", "#dfe9f7", fs=9)
box(35, 6, 30, 13, "SHAP explanations (Step 8)\nTreeExplainer / KernelExplainer\nglobal bars, beeswarm (High)", "#dfe9f7", fs=9)
box(67, 6, 30, 13, "Comparison (Steps 9-10)\nMcNemar's test per size,\nscaling curves, run times", "#dfe9f7", fs=9)
arrow(50, 88, 50, 82.3)
arrow(50, 73, 50, 66.7); arrow(50, 58, 50, 53.3)
arrow(50, 42, 18, 38.3); arrow(50, 42, 50, 38.3); arrow(50, 42, 82, 38.3)
for x in (18, 50, 82): arrow(x, 28, x, 19.3)
fig.savefig(A + "method.png", dpi=200, bbox_inches="tight"); print("figs ok", len(glob.glob(A + "*.png")))
