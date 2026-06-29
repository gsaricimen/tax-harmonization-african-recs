# Methodology for the NLP-Based Similarity Analysis

## Scope

The NLP-based analysis provides a complementary assessment of de jure tax harmonization across countries within each Regional Economic Community (REC). It applies a hybrid similarity framework to structured country tax-feature profiles stored in XML format.

The analysis covers the tax features examined in the study across corporate income tax, personal income tax, value-added tax, excise duties, and property and wealth taxes. The underlying analytical profiles contained completed values for all selected tax features.

The purpose of the NLP-based analysis is not to replace the feature-based comparative legal analysis or the HHI-based assessment. Rather, it evaluates whether similarity patterns derived from structured tax-language representations broadly correspond to the patterns identified through the comparative legal analysis.

## Pre-processing

The XML profiles contain both tax-feature values and descriptive metadata. Before calculating similarity, the script excludes the following metadata fields:

* country name;
* currency;
* REC membership; and
* source information.

This exclusion prevents descriptive information from generating artificial similarity between country profiles.

The remaining tax-feature values are standardised before analysis. The pre-processing function converts text to lower case, normalises decimal separators, standardises percentage expressions, and removes unnecessary whitespace.

## Tax-feature representation

Each country is represented through its tax-feature values in a tag–value format. The XML tag is retained together with the relevant value in order to preserve the legal and tax-category context of short, numerical, or otherwise ambiguous entries.

For example, the analytical representation distinguishes a percentage recorded under a corporate income tax rate tag from a percentage recorded under a withholding-tax or VAT tag. The tag–value structure therefore allows the model and the lexical-similarity measure to assess tax-related information within its corresponding legal field.

The analysis does not treat an entire country profile as one continuous document. Instead, individual tag–value entries are represented separately and subsequently aggregated at the country level. This avoids exceeding the maximum input length of the transformer model and preserves the structure of the tax-feature framework.

## Semantic similarity

Semantic similarity is measured using the `nlpaueb/legal-bert-base-uncased` model. LegalBERT is implemented through the SentenceTransformers framework with mean pooling over token-level transformer representations.

Each tag–value entry is encoded separately. The resulting feature-level embeddings are then averaged to produce one embedding vector for each country profile.

For each pair of countries, cosine similarity is calculated between the country-level embedding vectors:

$$
S^{\text{cos}}_{ij} = \cos(\mathbf{e}_i,\mathbf{e}_j)
$$

where $\mathbf{e}_i$ and $\mathbf{e}_j$ represent the averaged LegalBERT embeddings for countries $i$ and $j$.

The cosine similarity score is then rescaled to the interval from 0 to 1:

$$
S^{\text{sem}}*{ij} = \frac{S^{\text{cos}}*{ij} + 1}{2}
$$

This component captures semantic proximity between tax-feature descriptions, including related legal terminology that may not rely on exact word matching.

## Lexical similarity

The lexical component is calculated through the token-level Jaccard index.

For each country profile, the tag–value representations are combined and tokenised. Let $T_i$ and $T_j$ denote the sets of tokens associated with countries $i$ and $j$. The Jaccard similarity score is: $S^{\mathrm{Jac}}_{ij} = \frac{|T_i \cap T_j|}{|T_i \cup T_j|}$.

The Jaccard component captures exact lexical overlap across the tax-feature representations. Because the XML tags are retained in the tokenised representation, similarity is assessed in relation to the relevant legal and tax-category field rather than as unstructured text alone.

## Hybrid similarity score

TThe semantic and lexical similarity components are combined through an equally weighted hybrid score: $S^{\mathrm{hyb}}{ij} = \alpha S^{\mathrm{sem}}{ij} + (1-\alpha)S^{\mathrm{Jac}}_{ij}, \quad \alpha = 0.50$.

Accordingly, LegalBERT-based semantic similarity and token-level Jaccard similarity each contribute 50% to the final pairwise similarity score.

## REC-level and tax-category-level aggregation

For each REC, the script calculates pairwise hybrid similarity scores for all countries included in the relevant folder. The REC-level score is the mean of all off-diagonal pairwise similarity values: $\overline{S}{\mathrm{REC}} = \frac{2}{n(n-1)} \sum{i<j} S^{\mathrm{hyb}}_{ij}$.

Here, $n$ is the number of country profiles in the REC.
The script also produces similarity results for the following XML sections:

| XML section | Tax area                  |
| ----------- | ------------------------- |
| `E_TF`      | All tax features          |
| `E1_DT`     | Direct taxation           |
| `E11_CT`    | Corporate income tax      |
| `E12_PT`    | Personal income tax       |
| `E2_VT`     | Value-added tax           |
| `E3_Ex`     | Excise duties             |
| `E4_PW`     | Property and wealth taxes |

For each REC and section, the script exports a pairwise similarity matrix and records the corresponding mean off-diagonal similarity score.

## Reproducibility

The script requires XML tax-feature profiles organised in separate REC folders. The parent directory is specified through the `BASE_DIR` variable in `Hybrid_Similarity_Script_v1.py`.

The code uses a fixed random seed for Python, NumPy, and PyTorch in order to support reproducible execution. The required Python packages are listed in `requirements.txt`.

## Data availability and use

The code and XML schema are shared without the underlying country-level tax-feature values, completed XML profiles, source texts, or country-level similarity matrices. The underlying tax-feature values derive from the IBFD and PwC databases and remain subject to the respective providers’ terms of use.

Researchers with lawful access to these sources may populate the XML schema and use the code to reproduce, verify, extend, or adapt the computational similarity analysis. Relevant methodological and software references are listed in `references.md`.
