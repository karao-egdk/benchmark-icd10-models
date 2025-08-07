# Benchmark as of now

### Benchmarking model: NbAiLab/nb-sbert-base
Results:
- Language: ENG - Recall@5: 0.650, MRR@5: 0.588
- Language: NO - Recall@5: 0.850, MRR@5: 0.800
- Language: overall - Recall@5: 0.750, MRR@5: 0.694

### Benchmarking model: sentence-transformers/all-MiniLM-L6-v2
Results:
- Language: ENG - Recall@5: 0.600, MRR@5: 0.446
- Language: NO - Recall@5: 0.650, MRR@5: 0.600
- Language: overall - Recall@5: 0.625, MRR@5: 0.523

### Benchmarking model: abhinand/MedEmbed-large-v0.1
Results:
- Language: ENG - Recall@5: 0.650, MRR@5: 0.613
- Language: NO - Recall@5: 0.750, MRR@5: 0.725
- Language: overall - Recall@5: 0.700, MRR@5: 0.669

### Benchmarking model: vesteinn/ScandiBERT
Results:
- Language: ENG - Recall@5: 0.300, MRR@5: 0.300
- Language: NO - Recall@5: 0.500, MRR@5: 0.420
- Language: overall - Recall@5: 0.400, MRR@5: 0.360
---

# Medical Diagnosis Embedding Benchmark

## Results

| Model                                  | ENG Recall\@5 | ENG MRR\@5 | NO Recall\@5 | NO MRR\@5 | Overall Recall\@5 | Overall MRR\@5 |
| -------------------------------------- | ------------- | ---------- | ------------ | --------- | ----------------- | -------------- |
| NbAiLab/nb-sbert-base                  | 0.65          | 0.588      | **0.85**     | **0.80**  | **0.75**          | **0.694**      |
| abhinand/MedEmbed-large-v0.1           | 0.65          | **0.613**  | 0.75         | 0.725     | 0.70              | 0.669          |
| sentence-transformers/all-MiniLM-L6-v2 | 0.60          | 0.446      | 0.65         | 0.60      | 0.625             | 0.523          |
| vesteinn/ScandiBERT                    | 0.30          | 0.30       | 0.50         | 0.42      | 0.40              | 0.36           |

---

## What do these numbers mean?

* **Recall\@5:**
  The percentage of cases where the correct diagnosis code is found within the top 5 results retrieved by the model. A higher recall means the model is better at including the right diagnosis among its top guesses.

* **MRR\@5 (Mean Reciprocal Rank):**
  Measures how high up in the top 5 the correct diagnosis appears. Values closer to 1 mean the correct diagnosis is found very early (rank 1 or 2), improving the ranking quality, while values near 0 mean the correct diagnosis is ranked lower or missing.

* **Language columns (ENG and NO):**
  Show the model's performance specifically on English and Norwegian clinical notes.

* **Overall:**
  Aggregated performance across both languages.

---

## Conclusion

* **NbAiLab/nb-sbert-base** is the strongest overall model, especially excelling in Norwegian text, achieving the highest recall and MRR overall. This makes it the best choice for bilingual datasets or Norwegian-heavy tasks.

* **abhinand/MedEmbed-large-v0.1** performs nearly as well, with slightly better MRR in English, suggesting it is very good at ranking the correct diagnosis higher in English clinical notes.

* **sentence-transformers/all-MiniLM-L6-v2** has moderate performance, suitable if speed or model size is a priority but accuracy is less critical.

* **vesteinn/ScandiBERT** shows poor results and is not recommended for diagnosis retrieval.

---
