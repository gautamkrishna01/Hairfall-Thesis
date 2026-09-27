from dx import *
import json

A = "/tmp/claude-1000/-home-krishna-Desktop-Thesis-Hairfall-Thesis/3a0d67b6-c14e-4ab2-95b7-3de697bbdd86/scratchpad/assets/"
R = json.load(open(A + "analysis.json"))


def a(m, s): return 100 * R["models"][f"{m}|{s}"]["metrics"]["accuracy"]
def f(m, s): return R["models"][f"{m}|{s}"]["metrics"]["macro_f1"]


ABSTRACT = [
    "Hair loss is influenced by many factors acting together, and no single measurement predicts it reliably. Earlier prediction studies used classical classifiers, reached conflicting "
    "conclusions about the best model, and did not test tabular foundation models. This study benchmarked a tuned gradient-boosted model, CatBoost, against two zero-shot tabular "
    "foundation models, TabPFN and TabFM, for classifying hair fall risk into three tiers (Low, Moderate and High) from structured clinical and lifestyle data, and explained all three models with SHAP.",
    "The dataset had 21,606 records with 20 predictors, taken from a company dataset. A stratified 80/20 split gave 17,284 training "
    "and 4,322 test records. Each model was run with 500, 2,000 and all 17,284 training rows and scored on the same test records. CatBoost was tuned by grid search with five-fold "
    "cross-validation, while TabPFN and TabFM received the training rows as context without tuning. The models were compared using accuracy, macro-averaged precision, recall and F1-score, "
    "ROC-AUC and McNemar's test.",
    f"With all training rows, accuracy was {a('CatBoost','Full'):.2f}% for CatBoost, {a('TabPFN','Full'):.2f}% for TabPFN and {a('TabFM','Full'):.2f}% for TabFM, and no pair of models "
    f"differed significantly. With 500 rows the accuracies were {a('CatBoost','500'):.2f}%, {a('TabPFN','500'):.2f}% and {a('TabFM','500'):.2f}%, and with 2,000 rows {a('CatBoost','2000'):.2f}%, "
    f"{a('TabPFN','2000'):.2f}% and {a('TabFM','2000'):.2f}%; at these sizes both foundation models were significantly better than CatBoost (p < 0.0001). Almost all errors were between "
    "neighbouring tiers, and the Moderate tier was classified least well. SHAP showed that iron and stress level were the two most influential features in all nine analyses, with the same "
    "direction of effect in every model, reflecting relationships built into the dataset, not new clinical evidence. On a GPU, predicting the test records took 290 seconds for TabPFN "
    "and 3,082 seconds for TabFM with the full context, whereas CatBoost was fitted in 3.3 seconds.",
    "Zero-shot foundation models matched a tuned gradient-boosted model when all data were used, clearly outperformed it when data were limited, and could be explained with SHAP, but at a much "
    "higher computing cost. Because the results come from one company dataset and one data split, testing on real clinical data is recommended.",
]
KEYWORDS = "hair fall risk, tabular foundation models, CatBoost, TabPFN, TabFM, SHAP, explainable machine learning"


def chapter5(t):
    t.chapter_heading(5, "Conclusion and Recommendations")
    t.h2("5.1 Conclusion")
    t.p("This study set out to benchmark CatBoost, TabPFN and TabFM for explainable, multi-tier (Low, Moderate, High) hair fall risk stratification from structured clinical and lifestyle data. "
        "It was motivated by three gaps identified in Section 1.2: the evidence on the best model for hair fall data was inconsistent, tabular foundation models had not been tested on this problem, "
        "and complex models were hard to interpret. The four research questions of Section 1.3 are answered below, using the results of Chapter 4.")
    t.p(f"**Predictive performance (Research Question 1).** With all 17,284 training rows the three models reached close results on the 4,322-record test partition. Accuracy was {a('CatBoost','Full'):.2f}% for "
        f"CatBoost, {a('TabPFN','Full'):.2f}% for TabPFN and {a('TabFM','Full'):.2f}% for TabFM, and macro-F1 was {f('CatBoost','Full'):.4f}, {f('TabPFN','Full'):.4f} and {f('TabFM','Full'):.4f}. McNemar's test found no "
        "significant difference between any pair of models at the 0.05 level (p between 0.23 and 0.90). On this dataset, therefore, no advantage of the foundation models over a tuned gradient-boosted model was "
        "detected when all the data were used. This does not prove that the models are equivalent. With 500 and with 2,000 training rows, however, both foundation models were significantly more accurate "
        "than CatBoost (p < 0.0001). Almost every error, for every model, was between neighbouring tiers, and the Moderate tier was the hardest to classify.")
    t.p(f"**Effect of training size (Research Question 2).** From 500 rows to the full training data, the accuracy of CatBoost rose by {a('CatBoost','Full')-a('CatBoost','500'):.2f} points, whereas that of TabPFN rose by "
        f"{a('TabPFN','Full')-a('TabPFN','500'):.2f} and that of TabFM by {a('TabFM','Full')-a('TabFM','500'):.2f} points. CatBoost needed all 17,284 rows to reach the accuracy that the foundation models had with 2,000 rows, "
        "and the foundation models with 500 rows were more accurate than CatBoost with 2,000 rows. The tuned gradient-boosted model therefore depended most on the amount of training data. Because two "
        "independently developed foundation models behaved in the same way, the behaviour does not seem to be specific to one design, although only one dataset was tested. The ranking of TabFM and TabPFN with each "
        "other was not reliable at any size.")
    t.p("**Explainability (Research Question 3).** SHAP explanations were produced for all three models at all three training sizes. Iron and stress_level were the two most influential features in every one of the "
        "nine analyses, and total_protein, alt_liver, vitamin_d and calcium completed the first six places in eight of them. The direction of the effects was the same in all three models: higher stress_level and "
        "alt_liver values and the presence of the yes/no risk factors raised the predicted High risk contribution, and higher iron, total_protein, vitamin_d, calcium and manganese values lowered it. This agrees with "
        "the correlations measured in the data and with the relationships used to build the dataset, so it shows that the models recovered those relationships. It is not new clinical evidence.")
    t.p("**Computational cost and implementation (Research Question 4).** CatBoost was fitted in a few seconds and its predictions were immediate. With the full context on a T4 GPU, TabPFN needed about 5 minutes and TabFM "
        "about 51 minutes to predict the test records, and TabFM could not be run at all on a computer with 16 GB of RAM and no GPU. Explaining the foundation models with Kernel SHAP took up to 54 minutes for "
        "30 records (TabPFN) and 2.4 hours for 20 records (TabFM). The runs also exposed memory limits, package conflicts and single-row failures that needed workarounds. These problems came from the size and "
        "recency of the software and not from the modelling approaches.")
    t.p("In summary, on this dataset a tuned gradient-boosted model and two zero-shot foundation models gave comparable accuracy when all the data were available, the foundation models were much more efficient when "
        "data were limited, and all three could be explained with SHAP, but the foundation models cost far more to run and to explain. This meets the general objective of the study, within the limits described in Section 5.2.")
    t.p("The problem stated in Section 1.2 was that the evidence on the best model for hair fall data was inconsistent, that tabular foundation models had not been tested on it, and that complex models were hard to "
        "interpret. The general objective of Section 1.4 was to benchmark the three models for explainable multi-tier hair fall risk stratification, and each of the four specific objectives was met by the analyses in "
        "Sections 4.1 to 4.4. The comparison was made on one dataset, so the conclusions describe the behaviour of the models on this dataset and should not be generalised beyond it.")
    t.p("The contribution of the study can be stated in four points. It is a benchmark of two independently developed tabular foundation models against a tuned gradient-boosted model on multi-tier hair fall risk "
        "classification, a comparison that the reviewed literature did not contain (Section 2.8). It compares the three models at three matched training sizes on the complete test partition, and shows how the "
        "comparison changes from limited to full data. It applies one explanation method to three different architectures at every size and checks the explanations against the relationships measured in the data "
        "(Section 4.3). It also documents the run time and the software problems met with a recently released model, which may help others who plan to use it.")

    t.h2("5.2 Limitations of the study")
    t.p("The conclusions must be read with the following limitations.")
    t.bullets([
        "The dataset came from a single company (Section 3.7). It was not drawn from a clinical registry, so the results show how the models perform on this dataset and are not the validation of a diagnostic tool.",
        "All results come from one train/test split with one random seed. Confidence intervals were given only for accuracy ({tab:wilson}) and describe the uncertainty from the finite test sample, not the variation between splits or seeds. Reruns of the same step differed in the third decimal place (Section 3.10).",
        "The SHAP analyses of TabPFN and TabFM used only 30 and 20 test records and small background samples, so their attributions are less certain than CatBoost's exact values on 1,000 records. Only the leading features and the direction of their effects were interpreted. Patient-level (waterfall) explanations were not produced.",
        "CatBoost ran on a CPU and the foundation models on a GPU, so the run times are not comparable across model families in absolute terms, and they come from shared cloud hardware. The prediction time of TabFM with 500 rows was not measured because the run was resumed from a checkpoint.",
        "The versions of TabPFN and SHAP were not fixed in the cloud runs, and TabFM was evaluated in the memory-saving configuration described in Section 3.8.4.",
        "The CatBoost grid was small (nine combinations), and TabPFN and TabFM were used with default settings, so a more thorough tuning of any of the three models could change the ranking.",
        "The Moderate tier was the hardest to classify in all three models. The study offered an explanation based on the ordered structure of the target but did not test an ordinal model."], numbered=True)

    t.h2("5.3 Recommendations")
    t.p("**Recommendations for practice.** These follow from the findings and apply to structured data of a similar kind.")
    t.bullets([
        "Where labelled data are limited (a few thousand rows or fewer), a zero-shot tabular foundation model such as TabPFN is a reasonable first choice, since it reached or exceeded the accuracy of the tuned CatBoost without tuning and lost much less accuracy when the training data were reduced.",
        "Where a large training set is available, a tuned gradient-boosted model such as CatBoost is a sound choice, since with all the data it could not be told apart from the foundation models and it costs seconds instead of minutes or hours.",
        "The running time and memory of TabFM and TabPFN should be measured at the intended context size and on the intended hardware before an evaluation is planned, because their cost grew steeply with the context.",
        "Feature-level explanations such as SHAP should accompany any risk prediction, and in this study they were available for all three models. Any use in a health setting should be as decision support and only after validation on real clinical data."], numbered=True)
    t.p("**Recommendations for further research.** These address the limitations above.")
    t.bullets([
        "Repeat the experiment with repeated cross-validation or several random splits and seeds, and report confidence intervals for the differences between the models, to find out how reliable the small differences at full size are.",
        "Compute SHAP values for the foundation models on more test records and with larger backgrounds, and add patient-level explanations, so that the feature order can be compared more closely.",
        "Tune TabPFN and TabFM options and use a larger CatBoost search space, to test whether the ranking at full size changes.",
        "Compare ordinal-aware models with the multi-class approach, to see whether they improve the classification of the Moderate tier.",
        "Validate the framework on real clinical hair loss data when ethically cleared data become available.",
        "Study ensembles of the three models, and distillation of the foundation models into lightweight models, since TabPFN and TabFM need their training data at prediction time.",
        "Fix the versions of all packages and record the hardware of every run, so that the times can be compared exactly."], numbered=True)
    t.p("Each recommendation follows from a finding. The first two recommendations for practice rest on the results of Section 4.1 and Section 4.2, the third on the run times in Section 4.4, and the fourth on the explanations in "
        "Section 4.3. Each recommendation for further research addresses one of the limitations in Section 5.2. The recommendations are limited to the scope of this study and to structured data of a similar kind.")
