# Annual private investment in AI and generative AI (2019–2025)

## Purpose

This data layer supplies **annual, reproducible historical context** for external private financing of AI and generative-AI companies. It supplements, but does not replace, the project's OECD.AI/Preqin **VC-specific, nominal-USD** published benchmarks.

## Public sources and access

| Metric in project | Our World in Data chart | Years used |
|---|---|---|
| `private_ai_investment` | [External funding for privately held AI companies raising above $1.5 million](https://ourworldindata.org/grapher/private-investment-in-artificial-intelligence) | 2019–2025 |
| `private_genai_investment` | [External funding for privately held generative AI companies](https://ourworldindata.org/grapher/global-investment-in-generative-ai) | 2019–2025 |

**Original underlying sources:** Quid via *Stanford AI Index Report 2026*, plus US CPI data from the US Bureau of Labor Statistics. OWID processed the data, including inflation adjustment. Each chart supplies CSV and JSON metadata download endpoints. See the source pages for provider descriptions, citations, and reuse terms.

## Metric definitions and noncomparability

- These are **external private-market investment** flows; do not label them *VC investment* without qualification. OWID explicitly mentions venture-capital and private-equity financing.
- **Prices:** constant **2021 US dollars**, converted from USD to **USD billions** by dividing by 1,000,000,000.
- The AI indicator has a disclosed **$1.5 million** minimum financing threshold. The GenAI chart does not explicitly assert the same threshold. **Do not calculate a GenAI share of all AI funding** from these two sources without verifying that their deal universe, threshold, and taxonomies align.
- The data are distinct from the OECD.AI/Preqin nominal VC benchmarks and the country-level OECD VC database. **Do not sum or divide values across these three separate universes.** They can be presented as separate lines with explicit source and price-basis labels.
- This dataset provides no deal counts, funding stages, company-level observations, or AI-in-EdTech classification.
- The private investment values may be retrospectively revised as underlying reports and OWID processing change.

## Reproducible pipeline

From the repository root:

```bash
python -m pip install -r requirements.txt
python src/extract/extract_owid_ai.py
python src/transform/transform_owid_ai.py
python src/validation/validate_owid_ai.py
python -m unittest discover -s tests -p 'test_*.py'
```

The extractor preserves raw CSV and JSON metadata for each series under `data/raw/owid/`, plus an extraction manifest with download URLs, UTC timestamp, and SHA-256 hashes. The transformer keeps only the `World` observations for 2019–2025, converts the original value in constant 2021 US dollars to billions, and records lineage. The validator requires **two complete seven-year series**, unique keys, correct units, nonnegative finite amounts, and unambiguous provenance.

Local output: `data/processed/owid_private_ai_genai_2019_2025.csv`

## Redistribution policy

Although OWID-authored material is generally CC BY, its charts explicitly caution that underlying **third-party data may be subject to their original provider's licensing conditions**. Until the source-data redistribution rights have been resolved, the raw downloads and the generated time-series CSV should **remain local and untracked** in GitHub. The repository publishes the retrieval/transformation code, test fixtures (synthetic only), methodological context, and source URLs instead. This is a conservative repository policy, not a conclusion that merely viewing or downloading the OWID API data is prohibited.

## Scope relative to the EdTech deep dive

These series answer whether aggregate private AI financing accelerated or recovered. They **cannot** answer how much EdTech funding went to AI-native companies. That question requires a separate, defensible EdTech taxonomy and source dataset.