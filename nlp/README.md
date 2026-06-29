# NLP-Based Similarity Analysis

This contains the code and methodological documentation for the NLP-based component of the study.

The analysis measures similarity among country tax-feature profiles within each Regional Economic Community (REC). It applies a hybrid similarity framework to structured XML tax-feature sets. The framework combines:

* LegalBERT-based semantic similarity, calculated through cosine similarity; and
* token-level Jaccard similarity, calculated from tag–value representations of the tax features.

The hybrid similarity score is calculated with equal weights for the semantic and word-overlap components (`alpha = 0.50`).

## Files

| File                             | Description                                                                                                                |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `Hybrid_Similarity_Script_v1.py` | Python script that calculates REC-level and tax-category-level similarity scores and exports pairwise similarity matrices. |
| `methodology.md`                 | Description of the pre-processing, text representation, similarity measures, and aggregation procedure.                    |
| `references.md`                  | Methodological and software references used in the NLP analysis.                                                           |
| `requirements.txt`               | Python packages required to run the script.                                                                                |

## Input structure

The script is designed to process XML tax-feature profiles organised in separate folders for each REC. The base directory is specified through the `BASE_DIR` variable in `Hybrid_Similarity_Script_v1.py`.

The script excludes descriptive metadata fields, including country name, currency, REC membership, and source information, before calculating similarity. It then produces overall and section-level similarity results for the tax-feature structure defined in the XML schema.

## Data availability

The script is shared without completed country profiles, underlying tax-feature values, source texts, or country-level similarity matrices. The underlying tax-feature values derive from the IBFD and PwC databases and remain subject to the respective providers’ terms of use.

Researchers with lawful access to these sources may populate the XML schema and use the script to reproduce, verify, extend, or adapt the computational similarity analysis.
