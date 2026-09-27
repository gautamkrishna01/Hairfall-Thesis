import json, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Liberation Serif"
A = "/tmp/claude-1000/-home-krishna-Desktop-Thesis-Hairfall-Thesis/3a0d67b6-c14e-4ab2-95b7-3de697bbdd86/scratchpad/assets/"
R = json.load(open(A + "analysis.json"))["models"]
cols = {"CatBoost": "#e6a23c", "TabPFN": "#2f6fd6", "TabFM": "#2ea44f"}
fig, ax = plt.subplots(figsize=(7.4, 3.9))
w = 0.26
for i, m in enumerate(cols):
    vals = [R[f"{m}|{s}"]["metrics"]["fit_seconds"] + R[f"{m}|{s}"]["metrics"]["predict_seconds"] for s in ("500", "2000", "Full")]
    xs = np.arange(3) + (i - 1) * w
    bars = ax.bar(xs, vals, w, color=cols[m], label=m, edgecolor="black", linewidth=0.6)
    for x, v in zip(xs, vals):
        ax.text(x, v * 1.12, f"{v:,.0f}" if v >= 10 else f"{v:.1f}", ha="center", fontsize=8)
    if m == "TabFM":
        bars[0].set_hatch("///"); ax.text(xs[0], vals[0] * 2.2, "*", ha="center", fontsize=12)
ax.set_yscale("log"); ax.set_ylim(0.5, 2e4)
ax.set_xticks(range(3)); ax.set_xticklabels(["500", "2,000", "Full (17,284)"]); ax.set_xlabel("training / context rows"); ax.set_ylabel("fit + predict time (s, log scale)")
ax.set_title("Fit and prediction time on the 4,322 test records"); ax.legend(frameon=False, ncol=3, loc="upper left"); ax.grid(axis="y", alpha=0.3)
fig.tight_layout(); fig.savefig(A + "timings_new.png", dpi=200)
print("ok")
