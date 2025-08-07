import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from collections import defaultdict

def load_diag_codes(filepath):
    """
    Load ICD-10 Norway diagnosis codes and descriptions from Excel.
    """
    df = pd.read_excel(filepath)
    codes = df["Kode"].astype(str).tolist()
    descriptions = df["Tekst uten lengdebegrensning"].astype(str).tolist()
    return codes, descriptions

def load_eval_data(filepath):
    """
    Load SOAP notes with expected diagnosis codes and language from CSV.
    expected_codes should be comma-separated strings.
    """
    df = pd.read_csv(filepath)
    eval_list = []
    for _, row in df.iterrows():
        expected = [code.strip() for code in row["expected_codes"].split(",")]
        eval_list.append({
            "soap": row["soap"],
            "expected": expected,
            "lang": row["lang"]
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

def benchmark_model(model_name, diag_codes, diag_descs, eval_data):
    print(f"\nBenchmarking model: {model_name}")
    model = SentenceTransformer(model_name)

    print("Encoding diagnosis descriptions...")
    diag_embeds = model.encode(diag_descs, convert_to_numpy=True)

    index = build_faiss_index(diag_embeds)

    results = defaultdict(lambda: {"recall": [], "mrr": []})

    for item in eval_data:
        soap_emb = model.encode(item["soap"], convert_to_numpy=True).reshape(1, -1)
        D, I = index.search(soap_emb, k=5)
        retrieved_codes = [diag_codes[i] for i in I[0]]

        rec = recall_at_k(retrieved_codes, item["expected"])
        mrr = mrr_at_k(retrieved_codes, item["expected"])

        results[item["lang"]]["recall"].append(rec)
        results[item["lang"]]["mrr"].append(mrr)
        results["overall"]["recall"].append(rec)
        results["overall"]["mrr"].append(mrr)

    print("Results:")
    for lang in sorted(results.keys()):
        avg_recall = mean(results[lang]["recall"])
        avg_mrr = mean(results[lang]["mrr"])
        print(f"  Language: {lang} - Recall@5: {avg_recall:.3f}, MRR@5: {avg_mrr:.3f}")

    return results

def main():
    diag_codes_file = "icd10_norway.xlsx"
    eval_data_file = "soap_eval_data.csv"

    models = [
        "NbAiLab/nb-sbert-base",
        "sentence-transformers/all-MiniLM-L6-v2",
        "abhinand/MedEmbed-large-v0.1",
        "vesteinn/ScandiBERT"
    ]

    print("Loading ICD-10 Norway diagnosis codes...")
    diag_codes, diag_descs = load_diag_codes(diag_codes_file)

    print("Loading SOAP notes evaluation data...")
    eval_data = load_eval_data(eval_data_file)

    for model_name in models:
        benchmark_model(model_name, diag_codes, diag_descs, eval_data)

if __name__ == "__main__":
    main()
