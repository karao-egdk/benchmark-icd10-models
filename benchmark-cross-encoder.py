import pandas as pd
from sentence_transformers import SentenceTransformer, CrossEncoder
import faiss
import numpy as np
from collections import defaultdict

def load_diag_codes(filepath):
    df = pd.read_excel(filepath)
    codes = df["Kode"].astype(str).tolist()
    descriptions = df["Tekst uten lengdebegrensning"].astype(str).tolist()
    return codes, descriptions

def load_eval_data(filepath):
    df = pd.read_csv(filepath)
    eval_list = []
    for _, row in df.iterrows():
        expected = [code.strip() for code in row["expected_codes"].split(",")]
        eval_list.append({
            "soap": row["soap"],
            "expected": expected,
            "lang": row["lang"] if "lang" in row and pd.notna(row["lang"]) else "ENG"
        })
    return eval_list

def build_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index

def recall_at_k(retrieved_codes, expected_codes, k=5):
    return int(any(code in retrieved_codes[:k] for code in expected_codes))

def mrr_at_k(retrieved_codes, expected_codes, k=5):
    for i, code in enumerate(retrieved_codes[:k]):
        if code in expected_codes:
            return 1 / (i + 1)
    return 0.0

def mean(lst):
    return sum(lst) / len(lst) if lst else 0

def benchmark_bi_cross(
    bi_model_name,
    cross_model_name,
    diag_codes,
    diag_descs,
    eval_data,
    top_k_bi=50,
    top_k_final=5
):
    print(f"\nBenchmarking pipeline: BI='{bi_model_name}' + CROSS='{cross_model_name}'")

    # Load models
    bi_model = SentenceTransformer(bi_model_name)
    cross_model = CrossEncoder(cross_model_name)

    # Encode diagnosis descriptions for bi-encoder retrieval
    print("Encoding diagnosis descriptions (bi-encoder)...")
    diag_embeds = bi_model.encode(diag_descs, convert_to_numpy=True)
    index = build_faiss_index(diag_embeds)

    results = defaultdict(lambda: {"recall": [], "mrr": []})

    for idx, item in enumerate(eval_data):
        # Step 1: Bi-encoder retrieval (top_k_bi)
        soap_emb = bi_model.encode(item["soap"], convert_to_numpy=True).reshape(1, -1)
        D, I = index.search(soap_emb, k=top_k_bi)

        top_codes = [diag_codes[i] for i in I[0]]
        top_descs = [diag_descs[i] for i in I[0]]

        # Step 2: Cross-encoder reranking
        pairs = [(item["soap"], desc) for desc in top_descs]
        scores = cross_model.predict(pairs)
        ranked = sorted(zip(top_codes, top_descs, scores), key=lambda x: x[2], reverse=True)
        reranked_codes = [code for code, _, _ in ranked[:top_k_final]]

        # Step 3: Evaluation
        rec = recall_at_k(reranked_codes, item["expected"], k=top_k_final)
        mrr = mrr_at_k(reranked_codes, item["expected"], k=top_k_final)

        results[item["lang"]]["recall"].append(rec)
        results[item["lang"]]["mrr"].append(mrr)
        results["overall"]["recall"].append(rec)
        results["overall"]["mrr"].append(mrr)

        # Debug print for first 5 samples
        # if idx < 5:
        #     print("\n" + "="*80)
        #     print(f"Sample #{idx+1}")
        #     print(f"SOAP note: {item['soap']}")
        #     print(f"Expected codes: {item['expected']}")
        #     print("\n[Bi-encoder top 50]")
        #     for code, desc in zip(top_codes, top_descs):
        #         print(f"  {code} - {desc}")
        #     print("\n[Cross-encoder top 5 after reranking]")
        #     for code, desc, score in ranked[:top_k_final]:
        #         print(f"  {code} - {desc} (score={score:.4f})")
        #     print("="*80)

    # Print summary metrics
    print("\nResults:")
    for lang in sorted(results.keys()):
        avg_recall = mean(results[lang]["recall"])
        avg_mrr = mean(results[lang]["mrr"])
        print(f"  Language: {lang} - Recall@{top_k_final}: {avg_recall:.3f}, MRR@{top_k_final}: {avg_mrr:.3f}")

    return results

def main():
    diag_codes_file = "icd10_norway.xlsx"
    eval_data_file = "gemini_refactor_soap.csv"

    # Bi-encoder candidates
    bi_models = [
        "NbAiLab/nb-sbert-base",
        "sentence-transformers/all-MiniLM-L6-v2"
    ]

    # Cross-encoder candidates
    cross_models = [
        "cross-encoder/ms-marco-MiniLM-L-6-v2",  # English
        "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"  # Multilingual
    ]

    print("Loading ICD-10 Norway diagnosis codes...")
    diag_codes, diag_descs = load_diag_codes(diag_codes_file)

    print("Loading SOAP notes evaluation data...")
    eval_data = load_eval_data(eval_data_file)

    for bi in bi_models:
        for cross in cross_models:
            benchmark_bi_cross(bi, cross, diag_codes, diag_descs, eval_data)

if __name__ == "__main__":
    main()
