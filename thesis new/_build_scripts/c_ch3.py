from dx import *
from eqs import EQ
import json

A = "/tmp/claude-1000/-home-krishna-Desktop-Thesis-Hairfall-Thesis/3a0d67b6-c14e-4ab2-95b7-3de697bbdd86/scratchpad/assets/"
R = json.load(open(A + "analysis.json"))


def chapter3(t):
    t.chapter_heading(3, "Methodology")
    t.p("This chapter describes how the study was conducted to meet the research objectives stated in Section 1.4. It covers the research "
        "design and approach, the study area and population, sample selection and size, the data collection, the data analysis approach and "
        "tools, and the ethical considerations. Table 3.1 links each method to the objective it serves.")
    t.table("Link between the research objectives and the methods used", ["Specific objective (Section 1.4)", "Method used", "Section"], [
        ["1. Compare predictive performance and test significance", "Common train/test split; CatBoost tuning; TabPFN and TabFM inference; macro-averaged metrics, ROC-AUC, ordinal-aware measures; McNemar's test at every training size", "3.5, 3.8.3, 3.8.4, 3.8.7"],
        ["2. Evaluate the effect of training context size", "Every model trained on, or supplied with, 500, 2,000 and all 17,284 training rows and scored on the same 4,322 test records", "3.8.5"],
        ["3. Explain predictions with SHAP", "Descriptive analysis of the data; TreeExplainer for CatBoost, KernelExplainer for TabPFN and TabFM, at every training size", "3.8.2, 3.8.6"],
        ["4. Assess computational cost and implementation limitations", "Recording fit and prediction times; documenting memory and software problems and their workarounds", "3.8.8"]],
        [5.0, 8.0, 2.5], align=["l", "l", "c"])

    t.h2("3.1 Research design")
    t.p("The study used a quantitative, experimental design based on secondary data. It was a model-comparison (benchmarking) study: the same "
        "dataset, the same train/test partition and the same evaluation measures were applied to three models at three training sizes, so that "
        "differences in results could be attributed to the models and to the amount of training data, and not to the data. No primary data were "
        "collected from people, so there was no field study area and no direct contact with respondents.")
    t.p("The study followed the pipeline in Fig. 3.1. The data were validated, cleaned and split once. CatBoost was tuned by cross-validation and "
        "trained on the training rows, while TabPFN and TabFM received the same rows as context without any training. All nine model runs (three "
        "models at three sizes) were evaluated on the same held-out test partition, compared with a statistical test at each size, and explained with SHAP. "
        "Each stage of Fig. 3.1 was implemented as one numbered step (Steps 1 to 10) in a locally developed browser-based notebook, the Hairfall Lab "
        "(Section 3.8.9), which stores the code, printed output, figures and result files of every run.")
    t.figure(A + "method.png", "Block diagram of the research methodology", 13.5)
    t.p("The design was chosen because the research questions ask for a like-for-like comparison of models on one task. An experimental design is "
        "appropriate when the aim is to compare methods under controlled conditions, and a benchmarking study fits the objectives because none of them "
        "requires new data collection: each asks how existing methods behave on a defined task. A single fixed split and a fixed random seed (42) made the "
        "results reproducible. Each stage of Fig. 3.1 is linked to an objective in Table 3.1, so that no step was included without a purpose in the research.")

    t.h2("3.2 Research approach")
    t.p("A quantitative, deductive approach was used. The proposition examined was that zero-shot tabular foundation models can match a tuned "
        "gradient-boosted model on multi-tier hair fall risk classification, and that the size of the training data changes the comparison. It was "
        "examined with numerical performance measures and statistical tests, and the predictions were then explained with SHAP. A quantitative approach "
        "was suitable because the research questions ask about measurable differences in performance, data efficiency, feature contribution and cost.")

    t.h2("3.3 Study area")
    t.p("The study was not a field study, so there was no geographical study area. The data were taken from a company dataset [27]. The model "
        "runs were executed in Kaggle Notebooks on a cloud GPU, and the analysis of the results was done on a local computer (Section 3.8.9).")

    t.h2("3.4 Study population")
    c = R["classes"]
    t.p(f"The population was the set of patient records describing demographic, biochemical, clinical and lifestyle attributes related to hair fall. "
        f"The dataset had {R['n']:,} records with 23 columns: an identifier (id), a name (full_name), 20 predictor variables and the target variable hair_fall. "
        f"There were no duplicate rows and no missing values. The target had three ordinal tiers: 0 (Low, {c[0]:,} records, {100*c[0]/R['n']:.1f}%), "
        f"1 (Moderate, {c[1]:,} records, {100*c[1]/R['n']:.1f}%) and 2 (High, {c[2]:,} records, {100*c[2]/R['n']:.1f}%). The classes were therefore "
        "unequal in size, which is the reason for the macro-averaged measures in Section 3.8.7.")

    t.h2("3.5 Sample selection")
    t.p("The whole dataset was used, so no separate sampling of records was done. It was divided into a training and a test partition by a stratified "
        "80/20 split with a fixed random seed of 42, so that class proportions were preserved in both parts. The test partition was held out and was not "
        "used to tune any model. The same partition was used for all three models at all training sizes.")
    t.p("For the training-size experiment (Section 3.8.5), the training subsets of 500 and 2,000 rows were drawn from the training partition by "
        "stratified random sampling (seed 42), so that every subset kept the 45%, 35% and 20% class shares. The third size, Full, was the whole "
        "training partition of 17,284 rows. The same subset was given to all three models at a given size.")

    t.h2("3.6 Sample size")
    t.p("The full dataset had 21,606 records. The split gave 17,284 training records and 4,322 test records (1,945 Low, 1,513 Moderate and 864 High). "
        "Each model was run with 500, 2,000 and 17,284 training rows (about 2.9%, 11.6% and 100% of the training partition), which gives nine model runs. "
        "All nine were evaluated on all 4,322 test records, so no run used a reduced test set.")

    t.h2("3.7 Methods of data collection")
    t.p("No primary data were collected from people. The study used secondary data and computational modelling and measurement.")
    t.p("The dataset was provided by a company [27]. It contains physiological biomarker data, which are continuous clinical indicators relevant to hair health, "
        "together with demographic, lifestyle and hereditary risk factors. The respondent names in the dataset are stored only in encoded form and were not used. "
        "It is a company dataset and not a clinical registry. The consequences "
        "for the interpretation of the results are discussed in Chapter 4 and Chapter 5.")
    t.p("The 20 predictor variables fell into four groups (Table 3.2).")
    t.table("Predictor variables", ["Group", "Variables"], [
        ["Demographics and heredity", "age (years); gender (Female, Male, Other); family_hair_fall_history (0/1)"],
        ["Serum and physiological biomarkers", "total_protein (g/dL); iron (µg/dL); calcium (mg/dL); vitamin_d (ng/mL); manganese (µg/L); alt_liver (U/L); body_water_content (%); stress_level (0–40, modelled on the Perceived Stress Scale)"],
        ["Hair condition scores", "total_keratine and hair_texture (composite 0–100 scores, not standard laboratory measurements)"],
        ["Clinical and lifestyle flags (0/1)", "chronic_illness, anemia, stress, late_night_sleep, sleep_disturbance, water_reason (exposure to hard or chemically treated water), chemical_use (hair dyes, relaxers and other chemical treatments)"]],
        [4.6, 10.9], align=["l", "l"])
    t.p("Table 3.3 gives the range of the continuous predictors in the full dataset.")
    unit = {"age": "age (years)", "total_protein": "total_protein (g/dL)", "calcium": "calcium (mg/dL)", "iron": "iron (µg/dL)", "vitamin_d": "vitamin_d (ng/mL)",
            "alt_liver": "alt_liver (U/L)", "manganese": "manganese (µg/L)", "body_water_content": "body_water_content (%)", "stress_level": "stress_level (0–40)",
            "total_keratine": "total_keratine (0–100)", "hair_texture": "hair_texture (0–100)"}
    rows = [[unit[k], f"{v['mean']:.2f}", f"{v['sd']:.2f}", f"{v['min']:.2f}", f"{v['max']:.2f}"] for k, v in R["desc"].items()]
    t.table(f"Descriptive statistics of the continuous predictors (all {R['n']:,} records)", ["Predictor", "Mean", "Standard deviation", "Minimum", "Maximum"], rows,
            [5.5, 2.4, 3.2, 2.2, 2.2], align=["l", "c", "c", "c", "c"])
    g = R["gender"]
    t.p(f"The predictors cover plausible ranges for adults aged 20 to 55 years. The two hair-condition scores span the whole 0 to 100 scale with means near 50, "
        f"and the stress score spans the whole 0 to 40 scale. The gender attribute had {g['Male']:,} male, {g['Female']:,} female and {g['Other']} other records, "
        "so the \"other\" group was too small to be analysed separately.")
    t.p("Model outputs (predictions, class probabilities, SHAP values) and running times were collected by running the experiments in Section 3.8, "
        "which is the measurement part of the study.")

    t.h2("3.8 Data analysis approach and tools")
    t.p("The data were analysed in the steps below. The analysis was done in Python, and the tools are listed in Section 3.8.9. The code of every step is given in Appendix A.")
    t.h3("3.8.1 Data preprocessing")
    t.p("The following steps were applied before modelling (Steps 2 and 3 of the pipeline).")
    t.bullets([
        "**Validation against clinical reference ranges.** Seven biomarkers were compared with a normal range and with limits of physiological impossibility (Table 3.4). "
        "Abnormal but possible values were kept, because they carry the signal that predicts hair fall. Only impossible values would have been removed, and none was found.",
        "**Identifier removal.** The columns id and full_name carry no predictive information and could create false associations, so they were removed.",
        "**Encoding.** The gender attribute was mapped to numbers (0 = Female, 1 = Male, 2 = Other). The target was already coded as 0, 1 and 2. All other predictors were numeric "
        "or binary and were used as they were. TabPFN and TabFM received these raw values without scaling.",
        "**Missing values and duplicates.** The data were checked and no missing values or duplicate rows were found, so no imputation was needed."], numbered=True)
    t.table("Biomarkers compared with clinical reference ranges (all 21,606 records)", ["Biomarker", "Normal range", "Below normal", "Above normal", "Impossible values", "Outside normal range (%)"], [
        ["total_protein (g/dL)", "6.0–8.3", "406", "605", "0", "4.7"], ["calcium (mg/dL)", "8.5–10.5", "1,675", "392", "0", "9.6"],
        ["iron (µg/dL)", "60–170", "2,217", "209", "0", "11.2"], ["vitamin_d (ng/mL)", "25–80", "8,606", "0", "0", "39.8"],
        ["alt_liver (U/L)", "7–56", "2,300", "403", "0", "12.5"], ["manganese (µg/L)", "4–15", "1,960", "208", "0", "10.0"],
        ["body_water_content (%)", "45–65", "2,225", "2,227", "0", "20.6"]], [4.3, 2.5, 2.3, 2.3, 2.3, 2.5], size=9.5)
    t.p("No fitted transformation (such as scaling or target encoding) was applied, so the warning of Widowati et al. [1] about leakage from preprocessing did not apply "
        "to the modelling stage: nothing was learned from the test records before evaluation.")

    t.h3("3.8.2 Descriptive analysis of the dataset")
    t.p("Before interpreting the models, the relationship between each predictor and the risk tier was described in the full dataset. For each continuous predictor, "
        "the mean was calculated in each risk tier, and for the binary flags the share of records with the flag was calculated in each tier. For all predictors, "
        "Spearman's rank correlation with the ordinal risk tier was calculated. This analysis was done with the pandas and SciPy packages. It was not used to select "
        "features or to train any model. Its purpose was to provide an independent reference against which the SHAP explanations could be compared (Section 4.3).")

    t.h3("3.8.3 Models and justification")
    t.p("Three models were selected to represent three different approaches to tabular prediction, in line with Objective 1.")
    t.h4("3.8.3.1 CatBoost")
    t.p("CatBoost [7] is a gradient-boosted decision tree method that builds trees one after another, each correcting the errors of the ensemble so far, as described in "
        "Section 2.2. At iteration t it minimises a regularised objective:")
    t.equation(EQ[6], 6)
    t.p("where L is the multi-class cross-entropy loss, F~t−1~ is the ensemble built so far, h~t~ is the new tree and Ω penalises tree complexity. CatBoost reduces "
        "target leakage through ordered target statistics and builds symmetric (oblivious) trees, which limits overfitting. It was selected as the tuned, "
        "well-established baseline whose performance the foundation models had to match. Grid search was used to tune two hyperparameters that control model "
        "complexity and learning speed: the tree depth (deeper trees model more interactions but overfit more easily) and the learning rate (smaller values need more trees).")
    t.h4("3.8.3.2 TabPFN")
    t.p("TabPFN [8], [20] is a transformer pretrained offline on synthetic datasets. It does not train on the target data. It receives the labelled training rows "
        "D~train~ and a query x~test~ together and returns the predictive distribution in a single forward pass:")
    t.equation(EQ[7], 7)
    t.p("This is done with the self-attention mechanism of Eq. (3). TabPFN was selected as the established tabular foundation model, which needs no hyperparameter tuning or feature scaling.")
    t.h4("3.8.3.3 TabFM")
    t.p("TabFM [9] is a tabular foundation model released by Google Research. It alternates row-wise and column-wise attention over the table before an in-context "
        "transformer produces the prediction, and it also needs no training or tuning:")
    t.equation(EQ[8], 8)
    t.p("TabFM was selected as a second, independently developed foundation model, so that the study could test whether the behaviour of zero-shot models holds for more than one architecture.")

    t.h3("3.8.4 Experimental setup")
    t.p("**CatBoost.** For each training size, a grid search was run over tree depth {4, 6, 8} and learning rate {0.01, 0.03, 0.1}. Each of the nine combinations was scored by "
        "stratified 5-fold cross-validation on the training rows of that size, using macro-F1. Within each fold, up to 1,000 iterations were allowed with early stopping after "
        "50 rounds monitored on the validation fold of the training data, and the number of iterations of a combination was the mean of the best iteration over the five folds. "
        "All models used the MultiClass loss, l2_leaf_reg = 3 and a random seed of 42. The combination with the highest mean macro-F1 was chosen, and the final model was "
        "trained on all rows of that size with the chosen depth, learning rate and iteration count, with no further early stopping. The test partition was therefore not used "
        "at any point to tune or to stop training.")
    t.p("**TabPFN.** The default configuration of the TabPFN package was run on a GPU with a random seed of 42 and the option that lifts the package's pretraining size limits. "
        "The training rows of each size were supplied as context, and no tuning was done.")
    t.p("**TabFM.** The PyTorch implementation of TabFM version 1.0.1 was used with a single ensemble member (n_estimators = 1), on a GPU. The training rows of each size were "
        "supplied as context, and no tuning was done. Because the full 17,284-row context exceeded the memory of the GPU with the default attention implementation, the attention "
        "was evaluated in chunks of 1,024 queries and the column chunk size was set to 4. These settings change the memory use and not the computation (Section 3.8.8).")
    t.p("The settings of the three models are summarised in Table 3.5.")
    t.table("Settings of the three models", ["Setting", "CatBoost", "TabPFN", "TabFM"], [
        ["Tuning", "Grid search over depth and learning rate; 5-fold stratified CV; macro-F1", "None", "None"],
        ["Training data used", "500, 2,000 and 17,284 rows (fitted)", "500, 2,000 and 17,284 rows (context)", "500, 2,000 and 17,284 rows (context)"],
        ["Main parameters", "MultiClass loss, l2_leaf_reg 3, up to 1,000 iterations with early stopping (50 rounds) inside CV; final iterations from CV", "Package defaults; pretraining limits lifted", "Version 1.0.1, PyTorch backend, n_estimators = 1"],
        ["Hardware", "CPU", "GPU (NVIDIA Tesla T4)", "GPU (NVIDIA Tesla T4)"],
        ["Random seed", "42", "42", "42 (context sampling and package default)"]],
        [3.0, 4.9, 3.8, 3.8], size=9.5, align=["l", "l", "l", "l"])
    t.p("The choices in the setup have reasons. The split was stratified so that the three tiers had the same proportions in the training and test partitions. Macro-F1 was "
        "used to select the CatBoost setting because it gives each tier equal weight, which is consistent with the macro-averaged measures used for evaluation. Five folds were "
        "used as a compromise between the reliability of the score and the computing time. Early stopping ends training when the score has not improved for 50 rounds, which "
        "limits overfitting. The grid was small (nine combinations) because it covered the two parameters that most affect complexity and speed and kept the search within the available computing time.")
    t.p("The tuning effort was deliberately unequal: CatBoost was tuned by grid search, while TabPFN and TabFM were not tuned. This asymmetry is central to the research question, "
        "which asks whether models that need no tuning can match one that does.")

    t.h3("3.8.5 Training size experiment")
    t.p("To meet Objective 2, all three models were run with training sizes of 500, 2,000 and 17,284 (Full) rows. CatBoost was tuned and fitted separately at each size, and "
        "TabPFN and TabFM received the rows of each size as context. Every run was evaluated on the full test partition of 4,322 records, so the nine results are directly "
        "comparable, and the three models at each size used exactly the same rows.")

    t.h3("3.8.6 Explainability analysis")
    t.p("To meet Objective 3, post-hoc explanations were produced with SHAP [11], whose additive form is given in Eq. (4) and whose Shapley values are defined in Eq. (5). "
        "An explanation was produced for every model at every training size, which gives nine analyses.")
    t.p("For CatBoost, TreeExplainer [22] was used, which computes exact Shapley values from the tree structure, on 1,000 test records drawn at random (seed 42). TabPFN and TabFM "
        "have no tree structure, so KernelExplainer was used, which estimates the values by querying the model repeatedly. Because each query passes through the full in-context "
        "mechanism, these analyses used a random subset of the test partition (seed 42): 30 records for TabPFN and 20 for TabFM, 100 kernel evaluations per explained record, and a "
        "background sample summarised by k-means with 10 centres for TabPFN and 5 for TabFM. A wrapper padded single-row queries, because some models fail on one row. The High "
        "risk class was chosen for the beeswarm plots because it is the tier of greatest clinical interest and because a single class is needed to show the direction of an effect.")
    t.p("For each analysis, the mean absolute SHAP value of every feature was computed for each class and averaged over the three classes to give a global importance, and the "
        "features were ranked by it. Global importance bar plots and beeswarm plots for the High risk class were produced. Features were compared across models by rank and not by the "
        "size of the values, since the numbers of explained records differed.")

    t.h3("3.8.7 Evaluation metrics and statistical testing")
    t.p("To meet Objective 1, predictions were evaluated on the test partition with macro-averaged measures [23], which give the three classes equal weight. TP~k~, FP~k~ and FN~k~ are "
        "the true positives, false positives and false negatives of class k, and N is the number of test records.")
    for n in (9, 10, 11, 12):
        t.equation(EQ[n], n)
    t.p("Because the tiers are ordered, four further measures were calculated from the confusion matrices. Cohen's kappa [28] measures the agreement between the predicted and true "
        "tiers beyond the agreement expected by chance:")
    t.equation(EQ[13], 13)
    t.p("where p~o~ is the observed share of correct predictions and p~e~ is the share expected by chance from the row and column totals of the confusion matrix. Quadratic weighted kappa "
        "[29] uses the same idea but penalises an error by the squared distance between the true and predicted tiers, so that confusing Low with High counts four times as much as "
        "confusing neighbouring tiers. The share of predictions within one tier of the true tier and the mean absolute error, in tiers,")
    t.equation(EQ[14], 14)
    t.p("describe how far the errors were from the true tier.")
    t.p("A confusion matrix counts, for each true tier, how many records were assigned to each predicted tier. Precision for a tier is the share of records predicted as that tier that "
        "truly belong to it, and recall is the share of records of that tier that were found. The F1-score combines the two into one value that is high only when both are high. "
        "ROC-AUC was computed with a one-vs-rest strategy and macro-averaged. Per-class F1-scores and confusion matrices were also produced. Macro-averaging was used because the classes "
        "were unequal in size (Section 3.4).")
    t.p("Pairwise differences in accuracy between the models were tested with McNemar's test [24] with continuity correction on the same test records, using the counts b and c of "
        "records that one model classified correctly and the other did not:")
    t.equation(EQ[15], 15)
    t.p("The test was applied to the three pairs of models at each of the three training sizes, which gives nine tests. The uncertainty of each accuracy value that comes from the finite "
        "size of the test sample was described with 95% Wilson score confidence intervals [30], calculated from the accuracy and the number of test records. A difference was called "
        "significant at α = 0.05. McNemar's test was chosen because each model was trained and run once on one split, a situation for which it has a low false-positive rate [25].")

    t.h3("3.8.8 Computational assessment")
    t.p("To meet Objective 4, the running time of each model was recorded during training or context fitting and during prediction, and the practical problems met when running the models "
        "(memory limits, software errors and the workarounds used) were documented.")
    t.p("Running times were measured as wall-clock time with a timer around the fitting call and around the prediction call. Predictions for the test partition were made in batches (500 records for "
        "TabPFN and 100 for TabFM), and the results were written to a checkpoint file after each batch, so that a run interrupted by a session limit could be resumed. The Kaggle runs also "
        "halved the batch size automatically after a GPU out-of-memory error. Because the runs were made on shared cloud hardware, the times are approximate and can vary between "
        "sessions, and they are used to show how the cost changes with the context size and not to give exact benchmarks. One run, TabFM with 500 rows, was resumed from a checkpoint, so its "
        "prediction time was not measured (Section 4.4).")

    t.h3("3.8.9 Tools and environment")
    t.p("The experiments were written in Python. The final runs of the models and of the SHAP analyses were executed in Kaggle Notebooks on an NVIDIA Tesla T4 GPU (Table 3.6). The code was "
        "developed and stored in the Hairfall Lab, a browser-based notebook written for this study, in which the steps are run one at a time in a persistent Python kernel. Every run is saved with its "
        "code, printed output, figures and result files in a database and an object store, and in a folder per step. The Lab runs on a local Ubuntu computer (eight CPU cores, 16 GB of RAM, no GPU), "
        "where the first runs and the development were done. The steps run on Kaggle are packaged as notebook files, and their result files are imported back into the Lab so that all results are kept in one place.")
    t.p("Data handling used pandas and NumPy, and scikit-learn [31] was used for the split, cross-validation and metrics. The models came from the catboost, tabpfn and tabfm (PyTorch backend) "
        "packages, the explanations from the shap package, the significance test from statsmodels, and the plots from matplotlib.")
    t.table("Experimental environment", ["Item", "Specification"], [
        ["Platform of the final model and SHAP runs", "Kaggle Notebooks (cloud)"],
        ["GPU", "NVIDIA Tesla T4 (TabPFN, TabFM and the SHAP analyses of both); CatBoost ran on the CPU"],
        ["Memory", "33.7 GB RAM"],
        ["Operating system", "Linux (glibc 2.35)"],
        ["Language", "Python 3.12.13"],
        ["Main libraries", "CatBoost 1.2.10, TabFM 1.0.1 (PyTorch), scikit-learn 1.6.1, pandas 2.3.3, NumPy 2.0.2, statsmodels 0.14.6; TabPFN and SHAP were installed at run time without a fixed version (version 9.0.0 and 0.52.0 on the local computer)"],
        ["Development computer", "Ubuntu Linux, 8 CPU cores, 16 GB RAM, no GPU (Hairfall Lab)"]], [5.4, 10.1], align=["l", "l"])

    t.h2("3.9 Ethical considerations")
    t.p("The study used only secondary data from a company dataset [27]. No participants were recruited, no interviews or surveys were carried out, and no intervention was made, "
        "so ethical approval for data collection was not required. The columns id and full_name were dropped before modelling, and no attempt "
        "was made to identify any individual. The name column of the dataset holds encoded strings, and it was dropped in the cleaning step before any model was built. The dataset is "
        "a single company dataset. It is described as such throughout the thesis, and the results are presented as a benchmark of model behaviour. They are not presented as a clinical "
        "finding or as a diagnostic tool. Model outputs must not be used to make decisions about real patients without validation on real clinical data and review by a qualified clinician.")

    t.h2("3.10 Validity, reliability and reproducibility")
    t.p("Several steps were taken to make the comparison valid and the results reproducible. To protect the validity of the comparison, all three models used the same records, the same split and "
        "the same measures. The test partition was not used for hyperparameter tuning or for early stopping (Section 3.8.4), and no fitted transformation was applied to the data, so information "
        "from the test records did not flow into the models through preprocessing.")
    t.p("To protect reliability, random seeds were fixed at 42 wherever a random choice was made in the modelling: the split, the cross-validation folds, the training subsets, the samples of test "
        "records used for SHAP and the model initialisation. The result of a single seed and a single split cannot show how much the numbers vary from run to run, and this is acknowledged as a "
        "limitation in Section 5.2. The reruns of the same step in the Lab gave results that differed slightly in the third decimal place (for example, CatBoost with 500 rows scored 0.6976 in an earlier "
        "run on a local CPU and 0.6937 in the final run), which shows the size of the variation that comes from the computing platform and library versions.")
    t.p("To support reproducibility, the code is given in Appendix A, the software packages are listed in Section 3.8.9, and the dataset is described in Section 3.7. Some parts cannot be reproduced "
        "exactly. TabPFN is used through a package that needs a licence token, its version and that of SHAP were not fixed in the Kaggle runs, and TabFM version 1.0.1 may change in later releases.")
    t.p("Because the dataset came from a single company, the study has no external validity for real patients until it is repeated on clinical data. Its internal validity, meaning whether the comparison "
        "between the models is fair, rests on the steps described above.")
