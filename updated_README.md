# Benchmarking Report: ICD-10 Norway Diagnosis Code Embedding Models

## Input Files and Models Used

- **Diagnosis Codes File:** `icd10_norway.xlsx`
- **Evaluation Data Files:**
  - Before Refactoring: `before_gemini_refactor.csv`
  - After Refactoring: `gemini_refactor_soap.csv`

### Bi-Encoder Models Tested

- `NbAiLab/nb-sbert-base`
- `sentence-transformers/all-MiniLM-L6-v2`

### Cross-Encoder Models Tested

- `cross-encoder/ms-marco-MiniLM-L-6-v2`
- `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1`

---

## Overview

This report summarizes benchmarking results of different embedding and cross-encoder pipelines applied to ICD-10 Norway diagnosis codes and SOAP notes evaluation data. The benchmarking is performed under four scenarios:

1. Embedding model for test cases **before** input refactoring through Gemini
2. Embedding + cross-encoder pipeline for test cases **before** input refactoring
3. Embedding model for test cases **after** input refactoring through Gemini
4. Embedding + cross-encoder pipeline for test cases **after** input refactoring

---

## Metrics Explained

- **Recall\@5**: Percentage of relevant diagnoses found in the top 5 results.
- **MRR\@5 (Mean Reciprocal Rank @5)**: Average inverse rank of the first correct diagnosis within top 5 results.

Higher values indicate better retrieval performance.

---

## Scenario 1: Embed Model Before Refactoring

| Model                                  | Language | Recall\@5 | MRR\@5 |
| -------------------------------------- | -------- | --------- | ------ |
| NbAiLab/nb-sbert-base                  | ENG      | 0.230     | 0.110  |
| sentence-transformers/all-MiniLM-L6-v2 | ENG      | 0.280     | 0.209  |

**Summary:**

- The all-MiniLM-L6-v2 model outperforms NbAiLab model by about 21.7% relative increase in Recall\@5 and 90% in MRR\@5.
- Recall rates are relatively low (\~23-28%), indicating limited retrieval effectiveness before input refactoring.

---

## Scenario 2: Embed + Cross Encoder Before Refactoring

| Pipeline Bi-Encoder + Cross-Encoder                  | Language | Recall\@5 | MRR\@5 |
| ---------------------------------------------------- | -------- | --------- | ------ |
| NbAiLab/nb-sbert-base + ms-marco-MiniLM-L-6-v2       | ENG      | 0.370     | 0.287  |
| NbAiLab/nb-sbert-base + mmarco-mMiniLMv2-L12-H384-v1 | ENG      | 0.110     | 0.060  |
| all-MiniLM-L6-v2 + ms-marco-MiniLM-L-6-v2            | ENG      | 0.400     | 0.345  |
| all-MiniLM-L6-v2 + mmarco-mMiniLMv2-L12-H384-v1      | ENG      | 0.090     | 0.062  |

**Summary:**

- Adding cross-encoders generally improves performance over embedding-only models.
- Best Recall\@5 is 0.400 (40%) with all-MiniLM-L6-v2 + ms-marco-MiniLM-L-6-v2 pipeline.
- Some cross-encoder combinations (e.g., mmarco-mMiniLMv2-L12-H384-v1) performed worse, indicating model compatibility matters.

---

## Scenario 3: Embed Model After Refactoring

| Model                                  | Language | Recall\@5 | MRR\@5 |
| -------------------------------------- | -------- | --------- | ------ |
| NbAiLab/nb-sbert-base                  | ENG      | 0.760     | 0.636  |
| sentence-transformers/all-MiniLM-L6-v2 | ENG      | 0.380     | 0.299  |

**Summary:**

- Refactoring input with Gemini drastically improved NbAiLab model performance, boosting Recall\@5 from 23% to 76% (over 3x improvement).
- NbAiLab model is clearly better here, outperforming all-MiniLM-L6-v2 by roughly 100% relative Recall\@5.
- MRR\@5 also significantly improved, showing the model ranks correct diagnoses higher.

---

## Scenario 4: Embed + Cross Encoder After Refactoring

| Pipeline Bi-Encoder + Cross-Encoder                  | Language | Recall\@5 | MRR\@5 |
| ---------------------------------------------------- | -------- | --------- | ------ |
| NbAiLab/nb-sbert-base + ms-marco-MiniLM-L-6-v2       | ENG      | 0.580     | 0.451  |
| NbAiLab/nb-sbert-base + mmarco-mMiniLMv2-L12-H384-v1 | ENG      | 0.800     | 0.713  |
| all-MiniLM-L6-v2 + ms-marco-MiniLM-L-6-v2            | ENG      | 0.440     | 0.368  |
| all-MiniLM-L6-v2 + mmarco-mMiniLMv2-L12-H384-v1      | ENG      | 0.470     | 0.430  |

**Summary:**

- Cross-encoder pipelines benefit from input refactoring but results are mixed depending on bi-encoder + cross-encoder combinations.
- Best performance: NbAiLab + mmarco-mMiniLMv2-L12-H384-v1 with Recall\@5 = 80% and MRR\@5 = 71.3%.
- Recall\@5 increased by \~33% relative to scenario 3 embedding-only NbAiLab model.
- All MiniLM pipelines benefit less from cross-encoding after refactoring compared to NbAiLab pipelines.

---

## Overall Comparison & Recommendations

| Scenario                | Best Model / Pipeline                     | Recall\@5 (ENG) | MRR\@5 (ENG) | Relative Success |
| ----------------------- | ----------------------------------------- | --------------- | ------------ | ---------------- |
| 1. Embed before         | sentence-transformers/all-MiniLM-L6-v2    | 0.280           | 0.209        | Baseline         |
| 2. Embed + Cross before | all-MiniLM-L6-v2 + ms-marco-MiniLM-L-6-v2 | 0.400           | 0.345        | +43% Recall      |
| 3. Embed after          | NbAiLab/nb-sbert-base                     | 0.760           | 0.636        | +171% Recall     |
| 4. Embed + Cross after  | NbAiLab + mmarco-mMiniLMv2-L12-H384-v1    | 0.800           | 0.713        | +186% Recall     |

---

## Final Recommendation

Use the **NbAiLab/nb-sbert-base + mmarco-mMiniLMv2-L12-H384-v1 cross-encoder pipeline with input refactoring through Gemini** (Scenario 4) for the best retrieval accuracy on ICD-10 Norway diagnosis codes, achieving Recall\@5 of 80% and MRR\@5 of 71.3%.

---
