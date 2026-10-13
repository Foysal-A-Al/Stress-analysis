# Student stress factors: published analysis and reproducibility audit

This repository contains the 1,100-row `StressLevelDataset.csv` used in the published case study, the original exploratory notebook, and a separate, runnable audit of the target and predictors. The audit is an additional analysis; it does **not** reproduce the paper's figures or establish how the original labels were made.

> R. de Filippis and A. A. Foysal (2024), “Comprehensive analysis of stress factors affecting students: a machine learning approach,” *Discover Artificial Intelligence* 4, article 62. [DOI: 10.1007/s44163-024-00169-6](https://doi.org/10.1007/s44163-024-00169-6).

## Files

| File | Purpose |
| --- | --- |
| `StressLevelDataset.csv` | The 1,100-row, 21-column public data copy: 20 predictors and `stress_level`. |
| `Stress_analysis.ipynb` | Archived exploratory notebook associated with the paper. It uses a Kaggle-specific path and contains environment-specific download code. Its last validation cells depend on variables left by preceding cells, so it should not be treated as a clean evaluation pipeline. |
| `analysis.py` | Independent data audit and five-fold sensitivity analysis using the committed CSV. |
| `requirements.txt` | Python dependency ranges for the script and original notebook. |

## Run the audit

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python analysis.py --output audit.json
```

The command prints JSON and optionally saves it to `audit.json`. Use Python 3.10 or later. The script validates the columns and numeric data, reports class counts and the `blood_pressure` versus `stress_level` table, and evaluates a random forest with and without blood pressure against a majority-class baseline. It uses the same five shuffled stratified folds in both experiments and computes accuracy and macro F1. A fixed seed makes this comparison repeatable. This is a **new diagnostic**, not a result claimed by the 2024 paper. No tuning is done; the cross-validation scores should not be presented as an externally validated clinical prediction system.

## Target and variable provenance

The CSV supplies `stress_level` with codes **0, 1, 2**, commonly described as low, medium, and high stress. Neither this repository nor the paper provides an original questionnaire, a verified scoring equation, threshold values, or a generator that assigns these labels. The notebook reads the supplied target; it does not construct it. The interpretation of `blood_pressure` codes **1, 2, 3** as actual pressure ranges, measured readings, or self-reported categories is also not documented here. Do not convert these codes to clinical blood-pressure categories without an original codebook.

The archived notebook's input path points to a [Kaggle copy named `student-stress-factors-a-comprehensive-analysis`](https://www.kaggle.com/datasets/rxnach/student-stress-factors-a-comprehensive-analysis). Its embedded, time-limited storage URL is expired. The committed CSV is the stable local input for `analysis.py`. The paper describes a survey, imputation, scaling, and engineered indicators, but the publicly committed materials do not supply a participant-level questionnaire, source collection protocol, or complete preprocessing provenance sufficient to verify each of those steps. The audit makes no new claim about recruitment or measurement.

## Association and leakage check

The committed CSV has no missing values or duplicate full rows. The observed contingency table is:

| `blood_pressure` | stress 0 | stress 1 | stress 2 |
| ---: | ---: | ---: | ---: |
| 1 | 0 | 300 | 0 |
| 2 | 300 | 0 | 0 |
| 3 | 73 | 58 | 369 |

This unusually structured association warrants a label-provenance check. It does **not** prove that blood pressure was used to create the target: the data alone cannot establish temporal order, coding rules, or causal relationships. Excluding this one variable is a useful sensitivity check, but a similar score after exclusion does not rule out shared label information in other features.

In a local run of `analysis.py` on this CSV (five-fold stratified CV, seed 42, 200 trees), the majority-class baseline accuracy was **0.3391**. Random-forest accuracy was **0.8755** with all predictors and **0.8791** without `blood_pressure` (macro F1: **0.8757** and **0.8793**, respectively). The difference is small and should not be interpreted as proof that labels are independently measured. Rerun the script in your environment for your report.

## Research use and limitations

Report the dataset's origin and lack of documented target construction. For explanation studies such as SHAP, compare feature attributions with and without `blood_pressure`, and consider whether the other psychological and physiological inputs could overlap with an undocumented label rule. Fit any preprocessing, feature selection, and model tuning inside training folds. Do not claim clinical validity or causal effects from feature importance or correlations.

For a validated account of label construction and variable coding, the original dataset creator's questionnaire, codebook, or data-generation procedure is needed. Additional documentation can be linked here if recovered and verified; inferred rules must be clearly identified as hypotheses.

## Citation

Please cite the [published article](https://doi.org/10.1007/s44163-024-00169-6) when discussing its analysis, and separately acknowledge the public dataset source and any additional audit performed with this repository. The code in `analysis.py` is distinct from the published notebook.
