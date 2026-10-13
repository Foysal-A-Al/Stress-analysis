<div align="center">

# Student Stress Factors

### Published study · Open dataset · Reproducibility audit

**A transparent look at the data behind a 2024 study of student stress**

[Read the paper](https://doi.org/10.1007/s44163-024-00169-6) · [Explore the data](StressLevelDataset.csv) · [Original notebook](Stress_analysis.ipynb) · [Run the audit](analysis.py)

</div>

---

> [!IMPORTANT]
> The published materials do not document the original scoring rule for `stress_level` or define the clinical meaning of `blood_pressure` codes 1–3. This audit measures patterns in the CSV; it cannot reconstruct the missing labeling protocol.

## At a glance

| **1,100** records | **20** predictors | **3** stress classes | **5** factor domains |
| :---: | :---: | :---: | :---: |
| Shared CSV | Numeric features | Codes 0, 1, 2 | Psychological · physiological · environmental · academic · social |

This repository accompanies **de Filippis and Foysal (2024)**, *Comprehensive analysis of stress factors affecting students: a machine learning approach*, published in *Discover Artificial Intelligence*, **4**, article 62. The paper explores associations among stress-related factors through descriptive analysis, correlations, visualizations, and random-forest feature importance. [Read the article](https://doi.org/10.1007/s44163-024-00169-6).

The original notebook is preserved as a record of that exploratory work. `analysis.py` is a later, independent reproducibility audit. Its cross-validation numbers are **additional diagnostics**, not results reported in the paper.

## Repository guide

| Resource | Contents | Use |
| :--- | :--- | :--- |
| [`StressLevelDataset.csv`](StressLevelDataset.csv) | 1,100 rows × 21 columns: 20 predictors and `stress_level`. | Stable local audit input. |
| [`Stress_analysis.ipynb`](Stress_analysis.ipynb) | Archived exploratory analysis and visualizations. | Historical analysis; see execution note below. |
| [`analysis.py`](analysis.py) | Schema checks, class counts, association table, and sensitivity comparison. | Run locally for JSON results. |
| [`requirements.txt`](requirements.txt) | Dependency ranges. | Python setup. |

<details>
<summary><strong>Show all 20 predictors by domain</strong></summary>

| Domain | Columns |
| :--- | :--- |
| Psychological | `anxiety_level`, `self_esteem`, `mental_health_history`, `depression` |
| Physiological | `headache`, `blood_pressure`, `sleep_quality`, `breathing_problem` |
| Environmental | `noise_level`, `living_conditions`, `safety`, `basic_needs` |
| Academic | `academic_performance`, `study_load`, `teacher_student_relationship`, `future_career_concerns` |
| Social | `social_support`, `peer_pressure`, `extracurricular_activities`, `bullying` |

</details>

## The research question

The supplied target `stress_level` uses **0 (low), 1 (moderate), and 2 (high)**. The notebook reads these labels; it does not generate them. Neither the public repository nor the paper supplies an original questionnaire, scoring equation, class thresholds, or label-generation script. The available files also do not establish whether `blood_pressure` codes 1–3 are measured categories, self-reports, or preparation codes.

That matters for interpretation: a predictor involved in assigning the target could make a model appear more informative than an independently measured prediction task would justify. Model explanations would then partly describe the label rule.

### Blood pressure and the supplied labels

Counts calculated directly from the committed CSV:

| `blood_pressure` code | Stress 0 | Stress 1 | Stress 2 | Total |
| ---: | ---: | ---: | ---: | ---: |
| **1** | 0 | 300 | 0 | 300 |
| **2** | 300 | 0 | 0 | 300 |
| **3** | 73 | 58 | 369 | 500 |
| **Total** | **373** | **358** | **369** | **1,100** |

Code 1 appears only with class 1; code 2 only with class 0; every class 2 record has code 3. This structured association warrants a provenance check. **It does not prove that blood pressure was used to assign the target**, and it cannot define the blood-pressure codes.

## Run the reproducibility audit

From the repository root, use Python 3.10 or later:

```bash
python -m venv .venv
# Activate: Windows PowerShell .venv\Scripts\Activate.ps1
#           macOS/Linux source .venv/bin/activate
python -m pip install -r requirements.txt
python analysis.py --output audit.json
```

On a Windows machine with [`uv`](https://docs.astral.sh/uv/) and no `python` command:

```powershell
uv run --python 3.12 --with pandas --with scikit-learn analysis.py --output audit.json
```

The script validates the columns and numeric target, prints JSON, and optionally saves `audit.json`. It compares a 200-tree random forest using **all 20 predictors** with the same model **excluding `blood_pressure`**. Both use the same five shuffled stratified folds and seed 42; a majority-class model supplies a reference accuracy. There is no hyperparameter tuning or external validation.

### Results on the committed CSV

| Check | Result |
| :--- | ---: |
| Missing cells / duplicate complete rows | **0 / 0** |
| Majority-class baseline accuracy | 0.3391 |
| All predictors: accuracy / macro F1 | **0.8755 / 0.8757** |
| Without blood pressure: accuracy / macro F1 | **0.8791 / 0.8793** |

Removing blood pressure barely changes this model's cross-validation score. That **does not rule out** overlap between the target and other features; these scores do not establish clinical validity or causal effects. Rerun the audit for another environment or data version.

## Provenance and interpretation

The archived notebook reads a [Kaggle copy of the dataset](https://www.kaggle.com/datasets/rxnach/student-stress-factors-a-comprehensive-analysis) from a Kaggle-specific path. Its embedded temporary download URL has expired, and its final validation cells inherit variables from earlier cells. Use the committed CSV with `analysis.py` for the documented audit.

The paper describes a survey, imputation, scaling, and engineered indicators. Public materials do not include the original questionnaire, collection protocol, complete preprocessing record, or codebook needed to independently verify each step. These are **documentation limits**, not inferred properties of the participants.

For follow-on studies, disclose the provenance limit; compare explanations with and without `blood_pressure`; consider overlap from other predictors; and fit preprocessing and feature selection inside training folds. A definitive answer on target construction requires the original source documentation.

## Cite the work

> de Filippis, R., & Foysal, A. A. (2024). Comprehensive analysis of stress factors affecting students: a machine learning approach. *Discover Artificial Intelligence, 4*, Article 62. https://doi.org/10.1007/s44163-024-00169-6

Acknowledge the public dataset source separately. Describe `analysis.py` as a subsequent audit rather than a published result of the 2024 article.
