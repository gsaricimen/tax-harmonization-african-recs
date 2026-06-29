# -*- coding: utf-8 -*-
import os, glob, re, random
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, models
import torch

random.seed(0); np.random.seed(0); torch.manual_seed(0)
if torch.cuda.is_available(): torch.cuda.manual_seed_all(0)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

BASE_DIR = r"PATH_TO_DIRECTORY_CONTAINING_REC_FOLDERS"

FOLDER_NAMES = [
    "UMA","CEN-SAD","COMESA","EAC","ECCAS","ECCAS-CEMAC",
    "ECOWAS","ECOWAS-WAEMU","SACU","SADC"
]

TARGET_SECTIONS = [
    "E_TF",     
    "E1_DT",    
    "E11_CT",   
    "E12_PT",   
    "E2_VT",    
    "E3_Ex",    
    "E4_PW"     
]

META_EXCLUDE = {"A_Country", "B_Currency", "C_RECs", "D_report_source"}

ALPHAS = [0.5]
USE_VALUES_ONLY_FOR_EMBEDDINGS = False

NUMERIC_TOLERANCE = 0.0
BETA = 0.00
MISSING_PENALTY = 0.0


def normalize_scalar_value(x):
    if x is None: return ""
    s = str(x).strip().lower()
    s = re.sub(r"(\d+),(\d+)", r"\1.\2", s)
    s = re.sub(r"\b(\d+(?:\.\d+)?)\s*per\s*cent\b", r"\1%", s)
    s = re.sub(r"\b(\d+(?:\.\d+)?)\s*percent\b", r"\1%", s)
    s = re.sub(r"%\s*(\d+(?:\.\d+)?)", r"\1%", s)
    s = re.sub(r"(\d+(?:\.\d+)?)\s*%", r"\1%", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def extract_xml_data(element, include_tags=False):
    out = []
    if element.tag in META_EXCLUDE:
        return out

    text_val = normalize_scalar_value(element.text)
    if text_val:
        out.append(f"{element.tag} {text_val}" if include_tags else text_val)

    for child in element:
        out.extend(extract_xml_data(child, include_tags=include_tags))
    return out


def tokenize_to_set(text_list):
    full_text = " ".join(text_list).lower()
    tokens = re.findall(r"\w+", full_text)
    return set(tokens)


def build_label_percent_map(text_list_with_tags):
    mp = {}
    for s in text_list_with_tags:
        if not s:
            continue
        parts = s.split(" ", 1)
        if len(parts) < 2:
            continue
        label, rest = parts[0], parts[1]

        m = re.search(r'(\d+(?:\.\d+)?)%', rest)
        if m:
            mp.setdefault(label, []).append(float(m.group(1)))

    return mp


def greedy_match_score(a_list, b_list, tol=5.0):
    a = sorted(a_list)
    b = sorted(b_list)
    used = [False] * len(b)

    score_sum = 0.0
    for aval in a:
        best_j, best_diff = None, None
        for j, bval in enumerate(b):
            if used[j]:
                continue
            diff = abs(aval - bval)
            if best_diff is None or diff < best_diff:
                best_diff = diff
                best_j = j

        if best_j is not None:
            used[best_j] = True
            s = max(0.0, 1.0 - (best_diff / tol)) if tol > 0 else (1.0 if best_diff == 0 else 0.0)
            score_sum += s

    denom = max(len(a), len(b))
    return (score_sum / denom) if denom else 1.0


def numerical_similarity_label_based(textA_with_tags, textB_with_tags, tol=5.0, missing_penalty=0.5):
    mapA = build_label_percent_map(textA_with_tags)
    mapB = build_label_percent_map(textB_with_tags)

    labels = set(mapA.keys()) | set(mapB.keys())
    if not labels:
        return 1.0

    per_label_scores = []
    for lab in labels:
        a_vals = mapA.get(lab, [])
        b_vals = mapB.get(lab, [])
        if a_vals and b_vals:
            per_label_scores.append(greedy_match_score(a_vals, b_vals, tol=tol))
        else:
            per_label_scores.append(missing_penalty)

    return float(np.mean(per_label_scores))


def load_country_sets_and_texts(data_dir, target_tag=None):
    country_sets, country_texts_embed, country_texts_numeric = {}, {}, {}
    files = sorted(glob.glob(os.path.join(data_dir, "*.xml")))

    for fp in files:
        try:
            tree = ET.parse(fp)
            root = tree.getroot()
        except ET.ParseError:
            print(f"XML Parse Error: {fp}")
            continue

        relevant_elements = []
        if target_tag:
            found_node = root.find(f".//{target_tag}")
            if found_node is not None:
                relevant_elements.append(found_node)
        else:
            relevant_elements.append(root)

        full_text_list_context = []
        full_text_list_values = []

        for el in relevant_elements:
            full_text_list_context.extend(extract_xml_data(el, include_tags=True))
            full_text_list_values.extend(extract_xml_data(el, include_tags=False))

        if not full_text_list_context:
            continue

        if USE_VALUES_ONLY_FOR_EMBEDDINGS and any(v.strip() for v in full_text_list_values):
            texts_for_embed = full_text_list_values
        else:
            texts_for_embed = full_text_list_context

        base_name = os.path.splitext(os.path.basename(fp))[0]
        clean_name = base_name.replace("TaxProfile", "").replace("copy", "").replace("_", " ").strip()

        country_sets[clean_name] = tokenize_to_set(full_text_list_context)
        country_texts_embed[clean_name] = texts_for_embed
        country_texts_numeric[clean_name] = full_text_list_context

    return country_sets, country_texts_embed, country_texts_numeric


word_embedding_model = models.Transformer("nlpaueb/legal-bert-base-uncased")
pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(), pooling_mode_mean_tokens=True)
model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
model.max_seq_length = 512


def compute_jaccard(set_dict, countries):
    n = len(countries)
    sim = np.zeros((n, n), dtype=float)
    for i in range(n):
        si = set_dict.get(countries[i], set())
        for j in range(i, n):
            if i == j:
                val = 1.0
            else:
                sj = set_dict.get(countries[j], set())
                inter = len(si & sj); union = len(si | sj)
                val = (inter / union) if union > 0 else 0.0
            sim[i, j] = sim[j, i] = val
    return sim


def get_averaged_embedding(text_list):
    if not text_list:
        return np.zeros(model.get_sentence_embedding_dimension())
    embeddings = model.encode(text_list, convert_to_tensor=False, show_progress_bar=False)
    return np.mean(embeddings, axis=0)


def compute_similarity(country_sets, country_texts_embed, country_texts_numeric, alpha,
                       countries=None, tol=NUMERIC_TOLERANCE, beta=BETA, missing_penalty=MISSING_PENALTY):
    countries = list(country_texts_embed.keys()) if countries is None else list(countries)
    if not countries:
        return 0.0, np.array([]), []

    country_embeddings = []
    for c in countries:
        emb_vec = get_averaged_embedding(country_texts_embed[c])
        country_embeddings.append(emb_vec)

    final_embeddings_matrix = np.vstack(country_embeddings)
    sim_emb = (cosine_similarity(final_embeddings_matrix) + 1) / 2

    sim_jac = compute_jaccard(country_sets, countries)
    sim_hyb = alpha * sim_emb + (1 - alpha) * sim_jac

    n = len(countries)
    sim_num = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(i, n):
            if i == j:
                val = 1.0
            else:
                val = numerical_similarity_label_based(
                    country_texts_numeric[countries[i]],
                    country_texts_numeric[countries[j]],
                    tol=tol,
                    missing_penalty=missing_penalty
                )
            sim_num[i, j] = sim_num[j, i] = val

    sim_final = (1 - beta) * sim_hyb + beta * sim_num

    iu = np.triu_indices(n, 1)
    score = sim_final[iu].mean() if len(iu[0]) else 0.0
    return score, sim_final, countries


def align_matrix(sim, labels, target_labels):
    idx_map = {lab: i for i, lab in enumerate(labels)}
    keep_idx = [idx_map[lab] for lab in target_labels if lab in idx_map]
    if not keep_idx:
        return sim, labels
    sim2 = sim[np.ix_(keep_idx, keep_idx)]
    labels2 = [lab for lab in target_labels if lab in idx_map]
    return sim2, labels2


if __name__ == "__main__":
    print("Run started.")
    all_results = []

    for folder in FOLDER_NAMES:
        DATA_DIR = os.path.join(BASE_DIR, folder)
        if not os.path.exists(DATA_DIR):
            print(f"Skipping missing folder: {DATA_DIR}")
            continue

        results = []
        print(f"\n[{folder}]")

        for alpha in ALPHAS:
            sets_gen, texts_embed_gen, texts_num_gen = load_country_sets_and_texts(DATA_DIR, target_tag=None)

            if not sets_gen or not texts_embed_gen:
                print("no xml data found")
                continue

            score_gen, sim_gen, countries_gen = compute_similarity(
                sets_gen, texts_embed_gen, texts_num_gen,
                alpha, tol=NUMERIC_TOLERANCE, beta=BETA, missing_penalty=MISSING_PENALTY
            )
            print(f"General a={alpha}: {score_gen:.4f}")
            results.append(("General", alpha, score_gen))

            out_csv = os.path.join(DATA_DIR, f"similarity_matrix_general_alpha{alpha}.csv")
            pd.DataFrame(sim_gen, index=countries_gen, columns=countries_gen).to_csv(out_csv, encoding="utf-8-sig")

            for sec in TARGET_SECTIONS:
                sets_sec, texts_embed_sec, texts_num_sec = load_country_sets_and_texts(DATA_DIR, target_tag=sec)

                if not texts_embed_sec or all(len(v) == 0 for v in texts_embed_sec.values()):
                    print(f"{sec}: empty or not found")
                    continue

                score_sec, sim_sec, countries_sec = compute_similarity(
                    sets_sec, texts_embed_sec, texts_num_sec,
                    alpha, tol=NUMERIC_TOLERANCE, beta=BETA, missing_penalty=MISSING_PENALTY
                )

                sim_sec_aligned, countries_sec_aligned = align_matrix(sim_sec, countries_sec, countries_gen)

                print(f"{sec} a={alpha}: {score_sec:.4f}")
                results.append((sec, alpha, score_sec))

                out_csv_sec = os.path.join(DATA_DIR, f"similarity_matrix_{sec}_alpha{alpha}.csv")
                pd.DataFrame(sim_sec_aligned, index=countries_sec_aligned, columns=countries_sec_aligned).to_csv(
                    out_csv_sec, encoding="utf-8-sig"
                )

        if results:
            df_results = pd.DataFrame(results, columns=["Section","Alpha","MeanSimilarity"])
            out_res = os.path.join(DATA_DIR, "similarity_results_all_alphas.csv")
            df_results.to_csv(out_res, encoding="utf-8-sig", index=False)
            print(f"saved: {out_res}")
            all_results.extend([(folder, *row) for row in results])

    if all_results:
        df_all = pd.DataFrame(all_results, columns=["Folder","Section","Alpha","MeanSimilarity"])
        out_long = os.path.join(BASE_DIR, "all_folders_similarity_results_long.csv")
        df_all.to_csv(out_long, encoding="utf-8-sig", index=False)
        print(f"\nSaved long: {out_long}")

        pivot = df_all.pivot_table(index=["Section","Alpha"], columns="Folder", values="MeanSimilarity")
        out_pivot = os.path.join(BASE_DIR, "all_folders_similarity_results_pivot.csv")
        pivot.to_csv(out_pivot, encoding="utf-8-sig")
        print(f"Saved pivot: {out_pivot}\n")
        print("PIVOT:")
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(pivot.round(4))

    print("\nDone.")
