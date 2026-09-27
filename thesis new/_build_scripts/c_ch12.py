import json, re
from dx import *
from eqs import EQ

S = "/tmp/claude-1000/-home-krishna-Desktop-Thesis-Hairfall-Thesis/3a0d67b6-c14e-4ab2-95b7-3de697bbdd86/scratchpad/"
RUNIN = ["Scope of the study.", "Limitations of the study.", "Clinicians and dermatology practitioners.", "Individuals at risk of hair loss.",
         "Machine learning researchers and practitioners working with tabular data.", "Future researchers."]

SCOPE = ("**Scope of the study.** The study is limited to three-tier (Low, Moderate, High) hair fall risk classification from structured "
         "tabular clinical and lifestyle data. The dataset has 21,606 records, taken from a company dataset."
         " Three models are compared: CatBoost, TabPFN and TabFM. Each is trained on, or supplied as context with, "
         "500, 2,000 and all 17,284 training records, and each is evaluated on the same held-out test partition of 4,322 records with accuracy, "
         "macro-averaged precision, recall and F1-score, ROC-AUC (area under the receiver operating characteristic curve) and McNemar's test. "
         "The predictions of every model at every training size are explained with SHAP (Shapley Additive Explanations).")
LIMITS = ("**Limitations of the study.** The dataset came from a single company and was not drawn from a clinical registry, so the results show model capability "
          "on this data and are not a validated diagnostic tool. All results come from one train/test split and one random seed. The SHAP analysis "
          "of the two foundation models used a small sample of test records (30 for TabPFN and 20 for TabFM) because each explanation needs "
          "thousands of model calls. Scalp images, free-text records and other hair or scalp conditions are outside the scope of the study.")


def _items(text):
    parts = re.split(r"(?<=[\.\?\)])\s+(?=\d\.\s+[A-Z])", text)
    return [re.sub(r"^\d+\.\s+", "", x) for x in parts]


def _emit(t, blocks, start, edits=None, skip=(), after=None):
    edits, after = edits or {}, after or {}
    pending = []

    def flush():
        nonlocal pending
        if pending:
            t.bullets(pending, numbered=True)
            pending = []

    for i in range(start, len(blocks)):
        b = blocks[i]
        if i in skip:
            if i in after:
                flush(); after[i](t)
            continue
        x = edits.get(i, b["x"])
        if b["t"] == "h":
            flush(); t.h2(x)
        elif re.match(r"^\d\.\s+[A-Z]", x) and i not in edits:
            pending += _items(x)
        else:
            flush()
            if x in ("General objective", "Specific objectives"):
                t.h4(x)
            else:
                for r in RUNIN:
                    if x.startswith(r):
                        x = "**" + r + "**" + x[len(r):]
                        break
                t.p(x)
        if i in after:
            flush(); after[i](t)
    flush()


def chapter1(t):
    b = json.load(open(S + "blocks_16_21.json"))
    t.chapter_heading(1, "Introduction")
    _emit(t, b, 1, edits={2: SCOPE, 3: LIMITS})


def table21(t):
    t.table("Summary of related studies on hair loss prediction", ["Ref.", "Focus", "Approach", "Main finding", "Limitation relevant to this study"], [
        ["[1]", "Multi-class hair loss severity", "Explainable decision-support system", "Transformations must be kept inside cross-validation folds", "Does not compare foundation models"],
        ["[2]", "Alopecia Areata", "Machine learning diagnostic model", "Improved prediction for one condition", "Single condition, not multi-factorial risk"],
        ["[3]", "Hair fall prediction", "Individual classifiers vs. an ensemble", "Ensemble outperformed all individual classifiers", "Classical models only"],
        ["[4]", "Hair fall prediction", "Random Forest with hereditary, hormonal, medical and nutritional factors", "Random Forest outperformed XGBoost, CatBoost and LightGBM", "Conflicts with [3]; result specific to their dataset"],
        ["[5]", "Hair loss from genetic and scalp data", "Classifiers vs. neural networks", "Neural networks captured richer interactions", "Lower interpretability"],
        ["[6]", "Healthy hair vs. Alopecia Areata", "Image features with SVM and KNN", "SVM 91.4%, KNN 88.9% accuracy", "Image-based and binary; not tabular risk tiers"],
        ["[12]", "Hair loss severity from survey data", "Survey-based clinical and lifestyle features", "Used ROC-AUC and macro-F1 for class imbalance", "Not compared with foundation models"]],
        [1.1, 3.0, 3.6, 4.0, 3.8], size=9.5, align=["c", "l", "l", "l", "l"])


def table22(t):
    t.table("Model families relevant to this study", ["Model family", "Representative studies", "Strengths", "Known limitations", "Role in this study"], [
        ["Random Forest and other classical classifiers", "[13], [3], [4]", "Robust, little tuning", "Ranking versus boosting varies by dataset", "Not evaluated (context only)"],
        ["Gradient-boosted trees", "[14], [15], [16], [7]", "Strong on tabular data; tuned baseline", "Needs tuning; needs enough training data", "CatBoost, tuned baseline"],
        ["Neural networks", "[5], [17], [18]", "Can capture complex interactions", "Often no better than trees on tabular data; harder to interpret", "Not evaluated (context only)"],
        ["Tabular foundation models", "[8], [20], [9], [10]", "No tuning; strong with small data", "Cost grows with context; TabFM evidence provisional", "TabPFN and TabFM, zero-shot"],
        ["Post-hoc explanation", "[21], [11], [22]", "Model-agnostic feature attribution", "Kernel estimation is costly for large-context models", "SHAP for all three models"]],
        [3.0, 2.6, 3.2, 3.6, 3.1], size=9.5, align=["l", "c", "l", "l", "l"])


def chapter2(t):
    b = json.load(open(S + "blocks_22_31.json"))
    t.chapter_heading(2, "Literature Review")
    edits = {36: b[36]["x"].replace("All three are used in Chapter 4.", "The bar plot and the beeswarm plot are used in Chapter 4.")}
    after = {7: table21, 13: lambda t: (t.equation(EQ[1], 1), t.equation(EQ[2], 2)), 23: lambda t: t.equation(EQ[3], 3),
             32: lambda t: t.equation(EQ[4], 4), 33: lambda t: t.equation(EQ[5], 5), 44: table22}
    _emit(t, b, 1, edits=edits, skip={8, 14, 15, 24, 34, 45}, after=after)
