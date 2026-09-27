from dx import *
import json
import pandas as pd

A = "/tmp/claude-1000/-home-krishna-Desktop-Thesis-Hairfall-Thesis/3a0d67b6-c14e-4ab2-95b7-3de697bbdd86/scratchpad/assets/"
P = "/home/krishna/Desktop/Thesis/Hairfall-Thesis/thesis_project/"
R = json.load(open(A + "analysis.json"))
MS, SZ = ["CatBoost", "TabPFN", "TabFM"], ["500", "2000", "Full"]
SZL = {"500": "500", "2000": "2,000", "Full": "17,284"}
CLS = ["Low", "Moderate", "High"]


def M(m, s): return R["models"][f"{m}|{s}"]
def acc(m, s): return 100 * M(m, s)["metrics"]["accuracy"]
def f1(m, s): return M(m, s)["metrics"]["macro_f1"]
def pp(x): return f"{x:.2f}"
def pv(p): return "< 0.0001" if p < 0.0001 else f"{p:.4f}"


def chapter4(t):
    t.chapter_heading(4, "Results and Discussion")
    t.p("This chapter presents the results in the order of the research objectives. Section 4.1 compares the predictive performance of the three models, Section 4.2 shows the "
        "effect of the training size, Section 4.3 explains the predictions with SHAP, and Section 4.4 reports the computational cost and the implementation problems. Section 4.5 "
        "discusses the findings. All values are for the same 4,322 test records unless stated otherwise, and all figures and tables were produced from the saved output of the pipeline steps.")

    # ------------------------------------------------------------------ 4.1
    t.h2("4.1 Predictive performance of the three models")
    t.h3("4.1.1 Overall performance")
    t.p("{tab:perf} gives the performance of the nine model runs on the test partition. With the full training set (17,284 rows) the three models reached almost the same accuracy: "
        f"{pp(acc('CatBoost','Full'))}% for CatBoost, {pp(acc('TabPFN','Full'))}% for TabPFN and {pp(acc('TabFM','Full'))}% for TabFM. The macro-F1 values were "
        f"{f1('CatBoost','Full'):.4f}, {f1('TabPFN','Full'):.4f} and {f1('TabFM','Full'):.4f}, and the ROC-AUC values were {M('CatBoost','Full')['metrics']['roc_auc_ovr']:.4f}, "
        f"{M('TabPFN','Full')['metrics']['roc_auc_ovr']:.4f} and {M('TabFM','Full')['metrics']['roc_auc_ovr']:.4f}. The two foundation models were ahead of CatBoost by "
        f"{acc('TabPFN','Full')-acc('CatBoost','Full'):.2f} and {acc('TabFM','Full')-acc('CatBoost','Full'):.2f} percentage points, and TabPFN and TabFM differed by "
        f"{abs(acc('TabFM','Full')-acc('TabPFN','Full')):.2f} points.")
    rows = []
    for s in SZ:
        for m in MS:
            o = M(m, s); mt = o["metrics"]
            rows.append([SZL[s], m, f"{mt['accuracy']:.4f}", f"{o['macro_p']:.4f}", f"{o['macro_r']:.4f}", f"{mt['macro_f1']:.4f}", f"{mt['weighted_f1']:.4f}", f"{mt['roc_auc_ovr']:.4f}"])
    t.nk("perf")
    t.table("Performance of the three models on the test partition (4,322 records) at each training size", ["Training rows", "Model", "Accuracy", "Macro-precision", "Macro-recall", "Macro-F1", "Weighted F1", "ROC-AUC"],
            rows, [2.1, 2.1, 1.9, 2.3, 2.0, 1.8, 1.8, 1.8], size=9, align=["c", "l", "c", "c", "c", "c", "c", "c"])
    t.p(f"The picture changes when the training data are limited. With 500 rows the accuracy was {pp(acc('CatBoost','500'))}% for CatBoost, {pp(acc('TabPFN','500'))}% for TabPFN and "
        f"{pp(acc('TabFM','500'))}% for TabFM, so both foundation models were about {(acc('TabPFN','500')+acc('TabFM','500'))/2-acc('CatBoost','500'):.1f} points ahead. With 2,000 rows the values were "
        f"{pp(acc('CatBoost','2000'))}%, {pp(acc('TabPFN','2000'))}% and {pp(acc('TabFM','2000'))}%, a lead of about {(acc('TabPFN','2000')+acc('TabFM','2000'))/2-acc('CatBoost','2000'):.1f} points. "
        "The lead of the foundation models therefore shrank as the training size grew and was less than half a point with all the data. Whether these differences are larger than chance is tested in Section 4.1.3.")
    cb = [M("CatBoost", s)["metrics"] for s in SZ]
    t.p("The CatBoost baseline was tuned fairly. {tab:cbparams} gives the combination chosen by cross-validation at each size. Depth 4, the shallowest depth in the grid, was chosen every time, "
        f"and the learning rate was 0.03 for 500 and 2,000 rows and 0.1 for the full data. The cross-validated macro-F1 ({cb[0]['cv_macro_f1']:.4f}, {cb[1]['cv_macro_f1']:.4f} and "
        f"{cb[2]['cv_macro_f1']:.4f}) was close to the macro-F1 on the test partition ({cb[0]['macro_f1']:.4f}, {cb[1]['macro_f1']:.4f} and {cb[2]['macro_f1']:.4f}), which suggests that the "
        "tuning did not overfit the training data and that the test partition gave an honest estimate.")
    t.nk("cbparams")
    t.table("Hyperparameters chosen for CatBoost by cross-validation", ["Training rows", "Depth", "Learning rate", "Iterations", "CV macro-F1", "Test macro-F1"],
            [[SZL[s], str(cb[i]["depth"]), str(cb[i]["learning_rate"]), str(cb[i]["iterations"]), f"{cb[i]['cv_macro_f1']:.4f}", f"{cb[i]['macro_f1']:.4f}"] for i, s in enumerate(SZ)],
            [2.6, 2.0, 2.6, 2.3, 2.8, 2.8], size=10)

    t.h3("4.1.2 Per-class performance and confusion matrices")
    rows = []
    for m in MS:
        o = M(m, "Full")
        for k, c in enumerate(CLS):
            rows.append([m if k == 0 else "", c, f"{o['prec'][k]:.4f}", f"{o['rec'][k]:.4f}", f"{o['f1'][k]:.4f}", f"{o['support'][k]:,}"])
    t.p("{tab:perclass} gives the precision, recall and F1-score of each risk tier for the three models with the full training data. Results for the smaller training sizes are given in Appendix C.")
    t.nk("perclass")
    t.table("Precision, recall and F1-score by risk tier (full training data)", ["Model", "Tier", "Precision", "Recall", "F1-score", "Records"], rows, [2.6, 2.6, 2.6, 2.6, 2.6, 2.4], size=10)
    mod = {m: M(m, "Full")["f1"][1] for m in MS}
    hi = {m: M(m, "Full")["rec"][2] for m in MS}
    t.p(f"All three models classified the Low tier best (F1 between {min(M(m,'Full')['f1'][0] for m in MS):.2f} and {max(M(m,'Full')['f1'][0] for m in MS):.2f}) and the Moderate tier worst "
        f"(F1 between {min(mod.values()):.2f} and {max(mod.values()):.2f}). The High tier had high precision but lower recall (recall between {min(hi.values()):.2f} and {max(hi.values()):.2f}), which means that the models "
        "were cautious about assigning the highest risk and that some High-risk records were placed in the Moderate tier. {fig:cm_full} shows the confusion matrices.")
    t.nk("cm_full")
    t.figure_grid([A + f"cm_{m}_Full.png" for m in MS], "Confusion matrices of the three models with the full training data", cols=2, width_cm=6.6, subcaps=["(a) CatBoost", "(b) TabPFN", "(c) TabFM"])
    e = {m: M(m, "Full") for m in MS}
    t.p(f"The matrices have the same shape for all three models. Almost every error is between neighbouring tiers: of the {e['TabPFN']['errors']} errors of TabPFN, {e['TabPFN']['neighbour_errors']} were Low/Moderate or "
        f"Moderate/High confusions, and only {e['TabPFN']['low_high']} were Low records predicted as High and {e['TabPFN']['high_low']} were High records predicted as Low. {{tab:errors}} gives the same counts for all nine runs. "
        "The extreme confusions were most frequent for CatBoost with 500 rows and almost disappeared with 2,000 rows or more.")
    rows = []
    for s in SZ:
        for m in MS:
            o = M(m, s)
            rows.append([SZL[s], m, str(o["errors"]), str(o["neighbour_errors"]), f"{100*o['neighbour_errors']/o['errors']:.1f}", str(o["low_high"]), str(o["high_low"])])
    t.nk("errors")
    t.table("Errors of each run and their distance from the true tier", ["Training rows", "Model", "Errors", "Between neighbouring tiers", "Neighbouring (%)", "Low predicted High", "High predicted Low"], rows,
            [2.2, 2.2, 1.8, 3.0, 2.3, 2.2, 2.2], size=9)
    t.p("The ordinal-aware measures in {tab:ordinal} lead to the same conclusion. Cohen's kappa was about 0.66 for the three models with the full data, which indicates substantial agreement, and the quadratic weighted kappa "
        f"was about {sum(e[m]['qwk'] for m in MS)/3:.2f} because the few large errors are heavily penalised. In every run at least {100*min(M(m,s)['within1'] for m in MS for s in SZ):.1f}% of the predictions were within one tier of the "
        "true tier, and the mean absolute error was below 0.25 tiers with the full data.")
    rows = []
    for s in SZ:
        for m in MS:
            o = M(m, s)
            rows.append([SZL[s], m, f"{o['kappa']:.4f}", f"{o['qwk']:.4f}", f"{100*o['within1']:.2f}", f"{o['mae']:.4f}"])
    t.nk("ordinal")
    t.table("Ordinal-aware measures for the nine runs", ["Training rows", "Model", "Cohen's kappa", "Quadratic weighted kappa", "Within one tier (%)", "MAE (tiers)"], rows, [2.4, 2.4, 2.5, 3.6, 2.9, 2.2], size=9.5)

    t.h3("4.1.3 Statistical significance")
    mc = pd.read_csv(P + "Step_09_McNemarsTests/mcnemar_results.csv")
    rows = []
    for _, r in mc.iterrows():
        a, b = r["comparison"].split(" vs ")
        first = r["only_CatBoost_correct"] if a == "CatBoost" else r["only_TabPFN_correct"]
        rows.append([SZL[str(r["size"])], f"{a} vs {b}", f"{int(first)}", f"{int(r['only_other_correct'])}", f"{r['chi2']:.2f}", pv(r["p_value"]), "Yes" if r["significant_0.05"] else "No"])
    t.p("McNemar's test compares two models on the records where exactly one of them is correct. {tab:mcnemar} gives the counts b (only the first model correct) and c (only the second model correct), "
        "the test statistic and the p-value for the three pairs of models at each training size.")
    t.nk("mcnemar")
    t.table("Pairwise McNemar's test at each training size (4,322 test records)", ["Training rows", "Comparison", "b: only first correct", "c: only second correct", "χ²", "p-value", "Significant at 0.05"], rows,
            [2.2, 3.7, 2.3, 2.3, 1.5, 2.0, 2.0], size=9, align=["c", "l", "c", "c", "c", "c", "c"])
    t.p("With 500 and with 2,000 training rows, both foundation models were significantly better than CatBoost (p < 0.0001 in all four comparisons). For 500 rows, TabPFN was right and CatBoost wrong on "
        f"{int(mc.iloc[0]['only_other_correct'])} records, and the reverse held on only {int(mc.iloc[0]['only_CatBoost_correct'])}. With the full training data the differences disappeared: "
        f"CatBoost against TabPFN gave p = {mc.iloc[6]['p_value']:.2f} and CatBoost against TabFM gave p = {mc.iloc[7]['p_value']:.2f}, so no advantage of either foundation model over the tuned baseline could be detected. "
        f"TabPFN and TabFM did not differ significantly at any size (p = {mc.iloc[2]['p_value']:.2f}, {mc.iloc[5]['p_value']:.2f} and {mc.iloc[8]['p_value']:.2f}). "
        "Nine tests were run, and a Bonferroni-corrected level of 0.05/9 = 0.0056 leaves the four significant results (all with p < 0.0001) unchanged. A non-significant result does not prove that the models are equivalent, "
        "only that no difference was detected with 4,322 test records.")
    rows = [[SZL[s], m, f"{100*M(m,s)['acc']:.2f}", f"{100*M(m,s)['ci'][0]:.2f} – {100*M(m,s)['ci'][1]:.2f}"] for s in SZ for m in MS]
    t.nk("wilson")
    t.table("Accuracy (%) with 95% Wilson score confidence intervals", ["Training rows", "Model", "Accuracy", "95% confidence interval"], rows, [3.0, 3.0, 3.0, 5.0], size=10)
    t.p("{tab:wilson} shows the uncertainty that comes from the finite test sample. Each interval is about 2.5 points wide. The three intervals with the full data overlap almost completely, "
        "whereas at 500 rows the interval of CatBoost lies far below those of the foundation models. The intervals do not include the variation from other data splits or seeds, which was not measured.")


    ex = R["extra"]
    t.h3("4.1.4 Quality of the predicted probabilities")
    t.p("So far the models were compared by the tier they predict. Each model also returns a probability for every tier, and the quality of these probabilities matters when a risk estimate is shown to a person. "
        "{tab:probq} gives the log loss (the mean negative logarithm of the probability given to the true tier, lower is better), the Brier score (the mean squared distance between the probability vector and the true tier, "
        "lower is better) and the mean confidence (the average of the highest probability), which can be compared with the accuracy.")
    rows = []
    for s in SZ:
        for m in MS:
            o = ex["prob"][f"{m}|{s}"]
            rows.append([SZL[s], m, f"{o['logloss']:.4f}", f"{o['brier']:.4f}", f"{o['mean_conf']:.4f}", f"{o['acc']:.4f}"])
    t.nk("probq")
    t.table("Log loss, Brier score and mean confidence of the nine runs", ["Training rows", "Model", "Log loss", "Brier score", "Mean confidence", "Accuracy"], rows, [2.4, 2.4, 2.4, 2.6, 3.2, 2.4], size=9.5)
    pf, cb5, cbF = ex["prob"]["TabPFN|500"], ex["prob"]["CatBoost|500"], ex["prob"]["CatBoost|Full"]
    t.p(f"With the full data the two foundation models gave slightly better probabilities than CatBoost (log loss {ex['prob']['TabPFN|Full']['logloss']:.4f} for TabPFN and {ex['prob']['TabFM|Full']['logloss']:.4f} for TabFM, against "
        f"{cbF['logloss']:.4f} for CatBoost). The gap was large with 500 rows: the log loss of CatBoost was {cb5['logloss']:.4f} against {pf['logloss']:.4f} for TabPFN, and its Brier score was {cb5['brier']:.4f} against {pf['brier']:.4f}. "
        f"A model trained on 500 rows was also under-confident (mean confidence {cb5['mean_conf']:.3f} for an accuracy of {cb5['acc']:.3f}), whereas TabPFN with 500 rows had a mean confidence of {pf['mean_conf']:.3f} for an accuracy of {pf['acc']:.3f}, "
        "which is close. Better probabilities are an advantage of the foundation models when a numerical risk and not only a tier is reported, and this advantage, like the one in accuracy, shrinks with more data. "
        "No calibration method was applied to any model, and the probabilities were stored with four decimals, which is enough for these measures.")

    t.h3("4.1.5 Overlap of the errors of the three models")
    t.p("The differences between the models are small compared with the number of errors that they share. {tab:overlap} counts, for each training size, the test records that were classified correctly by all three models, by exactly two, by exactly one and by none.")
    rows = []
    for s in SZ:
        o = ex["overlap"][s]
        rows.append([SZL[s], f"{o['all3']:,}", f"{o['two']:,}", f"{o['one']:,}", f"{o['none']:,}", f"{100*o['none']/o['n']:.1f}"])
    t.nk("overlap")
    t.table("Number of test records classified correctly by all, two, one or none of the three models", ["Training rows", "All three correct", "Exactly two correct", "Exactly one correct", "None correct", "None correct (%)"], rows, [2.4, 2.8, 3.0, 3.0, 2.4, 2.8], size=9.5)
    o5, oF = ex["overlap"]["500"], ex["overlap"]["Full"]
    sh = {m: 100 * oF["none"] / R["models"][f"{m}|Full"]["errors"] for m in MS}
    t.p(f"With 500 rows, {o5['two'] + o5['one']:,} test records ({100*(o5['two']+o5['one'])/o5['n']:.1f}%) were classified correctly by some models and not by others, and with the full data only {oF['two'] + oF['one']:,} records ({100*(oF['two']+oF['one'])/oF['n']:.1f}%). "
        f"With the full data, {oF['none']:,} records ({100*oF['none']/oF['n']:.1f}%) were misclassified by all three models, which is {sh['CatBoost']:.0f}% of the errors of CatBoost, {sh['TabPFN']:.0f}% of those of TabPFN and {sh['TabFM']:.0f}% of those of TabFM. "
        "The models therefore make mostly the same mistakes, and the more data they have, the more alike their mistakes are. This points to a limit set by the data themselves, such as records close to a tier boundary or noise in the data, and not by "
        "the choice of model, which is the reason why three very different methods end at almost the same accuracy.")

    t.h3("4.1.6 Performance in subgroups")
    t.p("The accuracy of the models was also checked in subgroups of the test partition ({tab:subgroup}). The gender \"Other\" could not be examined because none of its 12 records fell in the test partition, and age was grouped into three bands.")
    rows = []
    for s in ("500", "Full"):
        for m in MS:
            g, ag = ex["gender"][f"{m}|{s}"], ex["age"][f"{m}|{s}"]
            rows.append([SZL[s], m, f"{100*g['Female'][0]:.2f}", f"{100*g['Male'][0]:.2f}", f"{100*ag['20-29'][0]:.2f}", f"{100*ag['30-39'][0]:.2f}", f"{100*ag['40-55'][0]:.2f}"])
    gn, an = ex["gender"]["CatBoost|Full"], ex["age"]["CatBoost|Full"]
    t.nk("subgroup")
    t.table("Accuracy (%) in subgroups of the test partition", ["Training rows", "Model", f"Female (n = {gn['Female'][1]:,})", f"Male (n = {gn['Male'][1]:,})", f"Age 20–29 (n = {an['20-29'][1]:,})", f"Age 30–39 (n = {an['30-39'][1]:,})", f"Age 40–55 (n = {an['40-55'][1]:,})"], rows,
            [2.1, 2.1, 2.5, 2.4, 2.6, 2.6, 2.6], size=9)
    fem = all(ex["gender"][f"{m}|{s}"]["Female"][0] >= ex["gender"][f"{m}|{s}"]["Male"][0] for m in MS for s in ("500", "Full"))
    dec = all(ex["age"][f"{m}|{s}"]["20-29"][0] >= ex["age"][f"{m}|{s}"]["30-39"][0] >= ex["age"][f"{m}|{s}"]["40-55"][0] for m in MS for s in ("Full",))
    spread = max(abs(ex["gender"][f"{m}|Full"]["Female"][0] - ex["gender"][f"{m}|Full"]["Male"][0]) for m in MS) * 100
    aspread = max(max(v[0] for v in ex["age"][f"{m}|Full"].values()) - min(v[0] for v in ex["age"][f"{m}|Full"].values()) for m in MS) * 100
    t.p(f"With the full data the accuracy differed by at most {spread:.1f} points between women and men and by at most {aspread:.1f} points between the age bands. "
        + ("Accuracy was a little higher for women than for men in every run, and " if fem else "The direction of the gender difference was not the same in every run, and ")
        + ("it fell slightly from the youngest to the oldest band in all three models with the full data. " if dec else "the age bands did not show the same order in all three models. ")
        + "These differences are small and were not tested, because the subgroups are small and the dataset came from a single company, so they should be read as a check that no group was served much worse and not as evidence about fairness in real patients.")

    # ------------------------------------------------------------------ 4.2
    t.h2("4.2 Effect of training context size")
    t.p("{tab:accsize} and {fig:scaling} show how the performance changed with the number of training rows. CatBoost gained a great deal from more data, whereas the two foundation models gained little.")
    rows = []
    for m in MS:
        rows.append([m] + [f"{acc(m,s):.2f}" for s in SZ] + [f"+{acc(m,'Full')-acc(m,'500'):.2f}"] + [f"{f1(m,s):.4f}" for s in SZ] + [f"+{f1(m,'Full')-f1(m,'500'):.4f}"])
    t.nk("accsize")
    t.table("Accuracy (%) and macro-F1 by training size", ["Model", "Acc. 500", "Acc. 2,000", "Acc. Full", "Change (points)", "F1 500", "F1 2,000", "F1 Full", "Change"], rows,
            [2.0, 1.6, 1.8, 1.6, 2.0, 1.6, 1.8, 1.6, 1.6], size=9)
    t.nk("scaling")
    t.figure(A + "scaling.png", "Accuracy, macro-F1 and ROC-AUC of the three models against the number of training rows (logarithmic axis)", 15.5)
    gcb, gpf, gfm = acc("CatBoost", "Full") - acc("CatBoost", "500"), acc("TabPFN", "Full") - acc("TabPFN", "500"), acc("TabFM", "Full") - acc("TabFM", "500")
    t.p(f"From 500 rows to the full training data, the accuracy of CatBoost rose by {gcb:.2f} percentage points, whereas TabPFN rose by {gpf:.2f} and TabFM by {gfm:.2f} points. "
        f"CatBoost therefore depended about {gcb/((gpf+gfm)/2):.0f} times more on the amount of data. The steps were also uneven: from 500 to 2,000 rows CatBoost gained {acc('CatBoost','2000')-acc('CatBoost','500'):.2f} points "
        f"and from 2,000 rows to the full data a further {acc('CatBoost','Full')-acc('CatBoost','2000'):.2f} points, while the foundation models gained about {(acc('TabPFN','2000')-acc('TabPFN','500')+acc('TabFM','2000')-acc('TabFM','500'))/2:.1f} and "
        f"{(acc('TabPFN','Full')-acc('TabPFN','2000')+acc('TabFM','Full')-acc('TabFM','2000'))/2:.1f} points.")
    t.p(f"Two comparisons show how efficiently each model used its data. First, the foundation models with 500 rows ({pp(acc('TabPFN','500'))}% and {pp(acc('TabFM','500'))}%) were more accurate than CatBoost with 2,000 rows "
        f"({pp(acc('CatBoost','2000'))}%), so they reached a given accuracy with a quarter of the rows or less. Second, CatBoost needed all 17,284 rows to reach the accuracy ({pp(acc('CatBoost','Full'))}%) that TabPFN "
        f"({pp(acc('TabPFN','2000'))}%) and TabFM ({pp(acc('TabFM','2000'))}%) had with 2,000 rows, which is 8.6 times more data. Because two independently developed foundation models behaved in the same way, the behaviour does not seem to be "
        "specific to one design, although only one dataset was tested. The accuracy of the foundation models flattened at about 78.6% to 78.7%, so more context gave little further gain on this dataset.")
    t.p("The ranking of TabPFN and TabFM with each other was not reliable at any size: TabFM was slightly higher at 2,000 and full rows and TabPFN slightly higher at 500 rows, and none of the differences "
        "was significant (Section 4.1.3).")


    ex = R["extra"]
    rows = []
    for m in MS:
        for k, c in enumerate(CLS):
            v = [M(m, sz)["f1"][k] for sz in SZ]
            rows.append([m if k == 0 else "", c] + [f"{x:.4f}" for x in v] + [f"+{v[2]-v[0]:.4f}"])
    t.p("The per-tier F1-scores in {tab:tierf1} show where the gain from more data came from.")
    t.nk("tierf1")
    t.table("F1-score by risk tier and training size", ["Model", "Tier", "500 rows", "2,000 rows", "17,284 rows", "Change 500 to Full"], rows, [2.6, 2.6, 2.6, 2.6, 2.8, 3.0], size=10)
    gains = {m: max(range(3), key=lambda k: M(m, "Full")["f1"][k] - M(m, "500")["f1"][k]) for m in MS}
    t.p(f"For CatBoost the largest gain was in the {CLS[gains['CatBoost']]} tier (F1 from {M('CatBoost','500')['f1'][gains['CatBoost']]:.3f} to {M('CatBoost','Full')['f1'][gains['CatBoost']]:.3f}), "
        f"whereas TabPFN and TabFM gained most in the {CLS[gains['TabPFN']]} and {CLS[gains['TabFM']]} tiers ({M('TabPFN','Full')['f1'][gains['TabPFN']]-M('TabPFN','500')['f1'][gains['TabPFN']]:+.3f} and "
        f"{M('TabFM','Full')['f1'][gains['TabFM']]-M('TabFM','500')['f1'][gains['TabFM']]:+.3f}). With 500 rows the recall of the High tier was only {M('CatBoost','500')['rec'][2]:.2f} for CatBoost against {M('TabPFN','500')['rec'][2]:.2f} for TabPFN "
        f"and {M('TabFM','500')['rec'][2]:.2f} for TabFM, and the recall of the Moderate tier was {M('CatBoost','500')['rec'][1]:.2f} against {M('TabPFN','500')['rec'][1]:.2f} and {M('TabFM','500')['rec'][1]:.2f}. "
        "A tuned model with few rows therefore missed many patients of the middle and upper tiers, which is the clinically important failure, and the foundation models missed far fewer.")

    # ------------------------------------------------------------------ 4.3
    t.h2("4.3 Explainability of the predictions")
    t.h3("4.3.1 Relationship between the features and the risk tier in the data")
    t.p("Before the model explanations are read, {tab:means} and {tab:flags} show what the data themselves say. The continuous features are ordered by the absolute value of the Spearman correlation with the risk tier, "
        "and the mean of each feature in each tier is given.")
    order = sorted(R["by_tier"], key=lambda k: -abs(R["spearman"][k]))
    rows = [[k, f"{R['by_tier'][k][0]:.2f}", f"{R['by_tier'][k][1]:.2f}", f"{R['by_tier'][k][2]:.2f}", f"{R['spearman'][k]:+.2f}"] for k in order]
    t.nk("means")
    t.table("Mean of the continuous predictors by risk tier and Spearman correlation with the tier", ["Predictor", "Low", "Moderate", "High", "Spearman ρ"], rows, [5.0, 2.4, 2.6, 2.4, 2.6], size=10, align=["l", "c", "c", "c", "c"])
    forder = sorted(R["flags"], key=lambda k: -abs(R["spearman"][k]))
    rows = [[k, f"{100*R['flags'][k][0]:.1f}", f"{100*R['flags'][k][1]:.1f}", f"{100*R['flags'][k][2]:.1f}", f"{R['spearman'][k]:+.2f}"] for k in forder]
    t.nk("flags")
    t.table("Share of records (%) with each binary flag, by risk tier", ["Flag", "Low", "Moderate", "High", "Spearman ρ"], rows, [5.0, 2.4, 2.6, 2.4, 2.6], size=10, align=["l", "c", "c", "c", "c"])
    sp = R["spearman"]
    t.p(f"The strongest single relationships were with stress_level (ρ = {sp['stress_level']:+.2f}, higher in higher tiers), iron (ρ = {sp['iron']:+.2f}), total_protein (ρ = {sp['total_protein']:+.2f}), vitamin_d "
        f"(ρ = {sp['vitamin_d']:+.2f}), alt_liver (ρ = {sp['alt_liver']:+.2f}) and calcium (ρ = {sp['calcium']:+.2f}). Iron, protein, vitamin D and calcium fall from the Low to the High tier, and stress and "
        "the liver enzyme ALT rise. Every binary flag was more common in higher tiers. These correlations are moderate, so no single feature separates the tiers, which agrees with the argument in Section 1.1.")

    t.h3("4.3.2 Global feature importance")
    t.p("{fig:bar_cb} to {fig:bar_fm} show the global importance of the features of the three models with the full training data, measured as the mean absolute SHAP value averaged over the three classes. The values are on "
        "different scales, because CatBoost was explained with exact tree values on 1,000 records and the foundation models with kernel estimates on 30 and 20 records, so the models are compared by rank and not by the size of the bars.")
    for m, key in zip(MS, ("bar_cb", "bar_pf", "bar_fm")):
        t.nk(key)
        t.figure(A + f"bar_{m}_Full.png", f"{m} global feature importance (SHAP), full training data", 9.5)
    top = {k: v["features"] for k, v in R["shap"].items()}
    rows = []
    for k in range(10):
        rows.append([str(k + 1)] + [top[f"{m}|Full"][k] for m in MS])
    t.nk("top10")
    t.table("Ten most important features with the full training data, by mean absolute SHAP value", ["Rank", "CatBoost", "TabPFN", "TabFM"], rows, [2.0, 4.4, 4.4, 4.4], size=10, align=["c", "l", "l", "l"])
    base6 = set(top["CatBoost|Full"][:6])
    assert all(set(top[f"{m}|Full"][:6]) == base6 for m in MS)
    t.p(f"The same six features occupied the first six places in all three models with the full data, in a slightly different order: {', '.join(sorted(base6))}. The seventh place was "
        f"{top['CatBoost|Full'][6]} for CatBoost and TabFM and {top['TabPFN|Full'][6]} for TabPFN, in which {top['CatBoost|Full'][6]} was eighth. Iron and stress_level were the two most important features in every model, and "
        "the demographic, hair-condition and binary features contributed less individually. {tab:top5} shows that this holds at the smaller training sizes as well: iron and stress_level are the first two features in all nine analyses.")
    rows = []
    for m in MS:
        for s in SZ:
            rows.append([m, SZL[s], ", ".join(top[f"{m}|{s}"][:5])])
    t.nk("top5")
    t.table("Five most important features in each of the nine SHAP analyses", ["Model", "Training rows", "Top five features (in order)"], rows, [2.4, 2.6, 10.5], size=9.5, align=["l", "c", "l"])
    same6 = [k for k, v in top.items() if set(v[:6]) == base6]
    odd = [k for k in top if k not in same6]
    assert len(same6) == 8 and odd == ["TabFM|2000"], odd
    t.p(f"The set of the six leading features was the same in {len(same6)} of the nine analyses. The exception was TabFM with 2,000 rows, in which the yes/no feature stress took the fifth place and vitamin_d moved down to seventh. "
        "The two features that always led were iron and stress_level; in CatBoost with 500 and 2,000 rows stress_level was first and iron second, and in the other seven analyses the order was reversed.")

    t.h3("4.3.3 Direction of the effects")
    t.p("The beeswarm plots in {fig:bee_cb} to {fig:bee_fm} show the direction of each effect for the High risk class. Each dot is one explained record, its position on the horizontal axis is the contribution of the feature to the "
        "High-risk output (right means towards High risk), and its colour is the value of the feature (red is high, blue is low).")
    for m, key in zip(MS, ("bee_cb", "bee_pf", "bee_fm")):
        t.nk(key)
        t.figure(A + f"bee_{m}_Full.png", f"{m} SHAP beeswarm plot for the High risk class, full training data", 10.5)
    t.p("The direction was the same in all three models. Low iron values (blue dots on the right) and high stress_level values (red dots on the right) pushed the prediction towards High risk. Higher total_protein, "
        "vitamin_d, calcium and manganese values (red dots on the left) pushed it away from High risk, and higher alt_liver values pushed it towards High risk. The yes/no features (chronic_illness, anemia, stress, "
        "late_night_sleep, sleep_disturbance, chemical_use and family_hair_fall_history) formed two clusters, with the value 1 always on the side of higher risk. Older age also pushed towards High risk. These directions match "
        "the signs of the correlations in {tab:means} and {tab:flags}.")

    t.h3("4.3.4 Differences between the rankings")
    fe = R["shap"]["CatBoost|Full"]["features"]
    rc = R["shap_rank_corr"]
    t.nk("rankcorr")
    t.table("Spearman rank correlation of the SHAP feature rankings of the three models (full training data)", ["", "CatBoost", "TabPFN", "TabFM"], [
        ["CatBoost", "1.000", f"{rc['CatBoost|Full~TabPFN|Full']:.3f}", f"{rc['CatBoost|Full~TabFM|Full']:.3f}"],
        ["TabPFN", f"{rc['CatBoost|Full~TabPFN|Full']:.3f}", "1.000", f"{rc['TabPFN|Full~TabFM|Full']:.3f}"],
        ["TabFM", f"{rc['CatBoost|Full~TabFM|Full']:.3f}", f"{rc['TabPFN|Full~TabFM|Full']:.3f}", "1.000"]], [3.0, 3.4, 3.4, 3.4], size=10)
    t.p(f"The rankings of all 20 features agreed closely between the models (Spearman correlation {min(rc['CatBoost|Full~TabPFN|Full'], rc['CatBoost|Full~TabFM|Full'], rc['TabPFN|Full~TabFM|Full']):.2f} to "
        f"{max(rc['CatBoost|Full~TabPFN|Full'], rc['CatBoost|Full~TabFM|Full'], rc['TabPFN|Full~TabFM|Full']):.2f}, {{tab:rankcorr}}). The differences are in the middle of the ranking, where the importance values are close together "
        "and, for the foundation models, are based on only 20 or 30 records. For example, the feature stress appeared among the five leading features of TabFM with 2,000 rows only, and manganese and body_water_content "
        "changed places between models. Such changes should not be interpreted. Only the shared set of leading features and the direction of their effects are reliable, which is why the conclusions in Chapter 5 rest on them.")
    t.p("This finding must be read together with the data. The dataset is a single company dataset (Section 3.7). Agreement between the models and with the "
        "correlations in Section 4.3.1 shows that all three models recovered the relationships built into the dataset. It is not new clinical evidence about hair loss, and it cannot be assumed to hold in real patients.")

    # ------------------------------------------------------------------ 4.4
    t.h2("4.4 Computational cost and implementation limitations")
    t.h3("4.4.1 Run time")
    t.p("{tab:timing} gives the time to fit or set up each model and to predict the 4,322 test records, as recorded in the runs on the Kaggle GPU (CatBoost on the CPU). {fig:timings} shows the sum of the two on a logarithmic axis.")
    rows = []
    for s in SZ:
        for m in MS:
            mt = M(m, s)["metrics"]
            pr = "not measured*" if (m == "TabFM" and s == "500") else f"{mt['predict_seconds']:,.1f}"
            per = "-" if (m == "TabFM" and s == "500") else f"{1000*mt['predict_seconds']/4322:.1f}"
            rows.append([SZL[s], m, f"{mt['fit_seconds']:,.1f}", pr, per])
    t.nk("timing")
    t.table("Fit and prediction time of the nine runs (seconds)", ["Training rows", "Model", "Fit or context set-up (s)", "Prediction of 4,322 records (s)", "Per record (ms)"], rows, [2.4, 2.4, 3.6, 4.3, 2.6], size=9.5,
            note="* The TabFM run with 500 rows was resumed from a saved checkpoint, so the prediction time was not measured. Fit time for the foundation models includes loading the model weights.")
    t.nk("timings")
    t.figure(A + "timings_new.png", "Fit and prediction time of the three models at each training size (logarithmic axis). The hatched bar has no prediction time (resumed run).", 13.5)
    tp, tf = M("TabPFN", "Full")["metrics"]["predict_seconds"], M("TabFM", "Full")["metrics"]["predict_seconds"]
    t.p(f"CatBoost was by far the cheapest: fitting took {M('CatBoost','500')['metrics']['fit_seconds']:.1f} to {M('CatBoost','Full')['metrics']['fit_seconds']:.1f} seconds and predicting the test records took less than a second. "
        "The whole CatBoost step, including the grid search with cross-validation, took between 158 and 358 seconds. The foundation models have almost no fitting cost, because they only store the rows, but their prediction "
        f"cost grows with the size of the context. TabPFN needed {M('TabPFN','500')['metrics']['predict_seconds']:.1f} s, {M('TabPFN','2000')['metrics']['predict_seconds']:.1f} s and {tp:,.1f} s for 500, 2,000 and 17,284 rows, an increase of "
        f"{tp/M('TabPFN','500')['metrics']['predict_seconds']:.0f} times for 34.6 times more rows. TabFM needed {M('TabFM','2000')['metrics']['predict_seconds']:.1f} s with 2,000 rows and {tf:,.1f} s (about 51 minutes) with the full data, "
        f"which is {tf/tp:.1f} times the time of TabPFN, and about {1000*tf/4322:.0f} ms per record against {1000*tp/4322:.0f} ms for TabPFN. Predicting the test records with TabFM took roughly {tf/M('CatBoost','Full')['metrics']['fit_seconds']:.0f} times as long as fitting CatBoost on the same data.")
    sh = {k: json.load(open(P + f"Step_{k}/shap_summary.json")) for k in ("08a_CatBoost_SHAP_500", "08b_CatBoost_SHAP_2000", "08c_CatBoost_SHAP_Full", "08d_TabPFN_SHAP_500", "08e_TabPFN_SHAP_2000",
                                                                       "08f_TabPFN_SHAP_Full", "08g_TabFM_SHAP_500", "08h_TabFM_SHAP_2000", "08i_TabFM_SHAP_Full")}
    rows = []
    for k, v in sh.items():
        rows.append([v["model"], SZL[v["size"]], v["explainer"], str(v["rows_explained"]), f"{v['seconds']:,.1f}", f"{v['seconds']/v['rows_explained']:,.2f}"])
    t.p("Explaining the models was much more expensive than predicting with them ({tab:shaptime}). TreeExplainer took a fraction of a second for 1,000 records of CatBoost. Kernel SHAP needed 100 samples for each explained record, "
        f"and with the full context each explained record took {sh['08f_TabPFN_SHAP_Full']['seconds']/30:.0f} seconds for TabPFN and {sh['08i_TabFM_SHAP_Full']['seconds']/20:.0f} seconds for TabFM. This is why only 30 and 20 records could be explained for the foundation models.")
    t.nk("shaptime")
    t.table("Time of the SHAP analyses", ["Model", "Training rows", "Explainer", "Records explained", "Time (s)", "Time per record (s)"], rows, [2.4, 2.3, 3.4, 2.6, 2.4, 2.6], size=9.5)

    t.h3("4.4.2 Software problems and workarounds")
    t.p("The runs exposed practical problems. They are recorded here because they affect anyone who plans to repeat the study, and because they are usually left out of benchmark reports.")
    t.bullets([
        "**Memory.** TabFM with the full 17,284-row context could not be run on the local computer with 16 GB of RAM and no GPU: the kernel ran out of memory and stopped, and the first 200 records took 3,240 seconds "
        "(16 seconds per record), which projects to about 19 hours for the test partition. It was therefore run on the Kaggle GPU. Even there, the default attention implementation exceeded the memory of the T4, so the attention was evaluated "
        "in chunks of 1,024 queries, the column chunk size was set to 4, and the prediction batch size was halved automatically after any out-of-memory error. These settings change the memory use only.",
        "**Dependencies.** The TabFM package required a different array library that conflicted with the notebook image, so that library was removed and the PyTorch backend was used.",
        "**Single-row input.** TabPFN and TabFM failed on a single query row. The SHAP wrapper pads a one-row query with a copy and keeps the first prediction.",
        "**Long runs and interruptions.** Predictions were saved in batches, so that runs of many hours could resume after an interruption. A resumed run has no valid prediction time, which is the case for TabFM with 500 rows.",
        "**Licence and downloads.** TabPFN needs a licence token, and the TabFM weights are large (about 6.5 GB) and have to be downloaded once.",
        "**Bookkeeping.** In the Lab, a run that was stopped by hand was at one point stored as successful. A check was added so that a stopped run is stored as an error, and the affected result was restored from the saved files."], numbered=False)
    t.p("These problems come mainly from the recency and the size of the foundation models and not from the modelling approach. CatBoost ran without any of them.")

    # ------------------------------------------------------------------ 4.5
    t.h2("4.5 Discussion")
    t.h3("4.5.1 Plausibility of the findings")
    t.p("A ceiling of about 78% to 79% accuracy for all three models, whatever their design, suggests that the limit is set by the data and not by the models. The Moderate tier, which lies between the other two, was "
        "the hardest for every model, and almost all errors were between neighbouring tiers. This is the pattern expected when a continuous risk is cut into three ordered tiers: records close to a boundary are easily placed "
        "on the wrong side, whereas confusing Low with High is almost never seen. The agreement of the three models in their leading features and in the direction of their effects, and its agreement with the correlations in the data, "
        "shows that the models learned the same relationships. Because the dataset came from a single company, this agreement shows what the models can recover from such data and is not clinical evidence.")
    t.h3("4.5.2 Comparison with similar studies")
    t.p("The hair loss studies reviewed in Section 2.1 used different data, targets and metrics, so their accuracies cannot be compared with the values here. What can be compared is the behaviour of the models. "
        "The finding that a foundation model beats a tuned tree ensemble on small data agrees with the report of Hollmann et al. [20] for datasets of up to 10,000 samples, and the finding that the gap closes at 17,284 rows "
        "is consistent with that report being limited to smaller tables. The zero-shot competitiveness of TabFM reported by its authors [9] and by the independent evaluation [10] is confirmed here at every size, but no advantage over "
        "TabPFN or over a tuned CatBoost with the full data was found. The result of Patel et al. [4], that Random Forest outperformed CatBoost, cannot be compared with this study, which did not evaluate Random Forest. "
        "The conclusion of Sai et al. [3] that an ensemble method beat individual classifiers is in line with the strength of the boosted ensemble at large sizes. The tree-versus-deep-learning results of [17] and [18] "
        "are matched by the strength of CatBoost with all the data, and the advantage of pretrained models with little data adds a case where the balance favours the neural approach.")
    t.h3("4.5.3 Implications and cautions")
    t.p("Four implications follow, each with a caution. First, where labelled data are limited (a few thousand rows or fewer), a zero-shot foundation model such as TabPFN is a reasonable first choice, since it reached the "
        "accuracy of a tuned CatBoost without tuning and lost far less accuracy when the data were reduced. The caution is that this advantage was measured on one company dataset. Second, with plenty of data the tuned "
        "gradient-boosted model is as accurate and thousands of times cheaper to run, so the extra cost of a foundation model is hard to justify. Third, the cost of the foundation models grows with the context and their explanation with Kernel SHAP is "
        "very expensive, which limits where they can be used. Fourth, explanations by SHAP could be produced for all three models and agreed with each other, but they describe the models and not causes.")
    t.p("A practical point that is not visible in the accuracy is deployment. A fitted CatBoost model is a small file that predicts in milliseconds without the training data and without a GPU. TabPFN and TabFM need the training rows "
        "at prediction time, TabFM needs a large weight file (about 6.5 GB), and both needed a GPU to predict the test records in a reasonable time with the full context. For a tool that gives a risk to one person at a time, "
        "as in a clinic, this favours CatBoost unless the training data are very few.")
    t.h3("4.5.4 Relation of the results to the research questions")
    t.bullets([
        "**Research Question 1.** With the full data no significant difference between CatBoost, TabPFN and TabFM was found (p between 0.23 and 0.90). With 500 and 2,000 rows both foundation models were significantly more accurate than CatBoost.",
        "**Research Question 2.** CatBoost gained 8.8 accuracy points from 500 rows to the full data, whereas TabPFN and TabFM gained 1.7 and 1.8. The foundation models used limited data far more efficiently.",
        "**Research Question 3.** Iron and stress_level were the two leading features in every analysis, with total_protein, alt_liver, vitamin_d and calcium completing the first six places in eight of the nine analyses, and with the same direction of effect in all three models and in agreement with the correlations in the data.",
        "**Research Question 4.** CatBoost took seconds. TabPFN took about 5 minutes and TabFM about 51 minutes to predict the test records with the full context on a T4 GPU, and TabFM could not be run on a 16 GB CPU computer. Kernel SHAP for the foundation models took up to 2.4 hours for 20 records."], numbered=False)

    t.h3("4.5.5 Threats to the validity of the findings")
    mcf = pd.read_csv(P + "Step_09_McNemarsTests/mcnemar_results.csv")
    disc = int(mcf.iloc[6]["only_CatBoost_correct"] + mcf.iloc[6]["only_other_correct"])
    need = 1 + 1.96 * disc ** 0.5
    t.p("Four kinds of threat limit how far the findings can be trusted, and they are listed here so that the conclusions of Chapter 5 are read with them in mind.")
    t.p("**Construct validity.** The target is a three-tier label in a company dataset and not a clinical diagnosis, so accuracy measures agreement with the labels built into the data and not with true hair loss. "
        "The tiers are cut from a continuous risk, so labels near a boundary are partly arbitrary, which the large share of errors made by all three models (Section 4.1.5) illustrates.")
    t.p("**Internal validity.** The models were compared on the same records and the same split, the test partition was not used for tuning or stopping, and the baseline was tuned. The CatBoost grid was small, "
        "the foundation models were used with default settings, the cloud runs did not fix the versions of TabPFN and SHAP, and TabFM was run in a memory-saving configuration. Reruns of the same step differed in the third decimal place "
        "(Section 3.10), so differences of a few tenths of a point between models cannot be interpreted, and all differences with the full training data are of that size.")
    t.p("**External validity.** There was one dataset, from a single company, with adults aged 20 to 55 and 20 mostly numeric predictors. The size of the advantage of the foundation models, the point at which CatBoost catches up and the "
        "rank of the features may all depend on the number and type of the features, on the class balance and on how the labels were built. The results cannot be assumed for real patients or for other tabular problems.")
    t.p(f"**Conclusion validity.** There was one split and one seed. McNemar's test on 4,322 records has limited power for small differences: between CatBoost and TabPFN with the full data only {disc} records were classified "
        f"correctly by one model and not by the other, so a difference of about {need:.0f} records ({100*need/4322:.1f} accuracy points) would have been needed to reach significance. A non-significant result at full size therefore means that no difference "
        "larger than about this size was found, and it does not show that the models are equal. Nine tests were run without correction in the main analysis, although the conclusions do not change under a Bonferroni correction (Section 4.1.3), "
        "and the Wilson intervals show an uncertainty of about 1.3 points in each accuracy value.")
