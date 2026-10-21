# Power BI data model: source-aware staging marts

## Purpose

This commit prepares **local, source-separated CSV fact/dimension tables** for a Power BI semantic model. It does **not** yet create a `.pbip`, Power Query queries, relationships, measures, or report pages inside Power BI Desktop. Those are subsequent commits.

The central restriction is that the project draws on **different observation grains, data universes, vintages, and monetary bases**. The purpose of multiple fact tables is to make those distinctions structurally visible and stop invalid cross-source arithmetic.

## Generation and local reproducibility

Run these commands from the repository root after the earlier pipelines have been executed:

```powershell
python -m src.transform.build_powerbi_marts
python -m src.validation.validate_powerbi_marts
python -m unittest discover -s tests -p "test_*.py" -v
```

Output: `data/mart/powerbi/` — **11 CSV files**, which are ignored by Git. The generator fails if it cannot find all five processed inputs. It does not substitute fabricated observations or silently download third-party data. Read the corresponding documentation if an input is missing.

The required inputs are:

| Source | Local input file |
|---|---|
| OECD market VC | `data/processed/oecd_vc_annual_2019_2025.csv` |
| OECD.AI publication benchmarks | `data/processed/oecd_ai_benchmarks_2026.csv` |
| OWID / AI Index private investment | `data/processed/owid_private_ai_genai_2019_2025.csv` |
| HolonIQ historical EdTech | `data/processed/edtech_vc_holoniq_2019_2025_local.csv` |
| Curated EdTech announced rounds | `data/processed/edtech_verified_rounds_2022_2025.csv` |

**Licensing:** These marts inherit the restrictions of their underlying sources. Keep all generated files local and do not upload them to GitHub. The code, schema, and offline tests are version-controlled instead.

## Tables and grains

| CSV table | Grain / unique key | Contents |
|---|---|---|
| `DimYear` | Year | 2019–2025 calendar filter |
| `DimOECDCountry` | Country code | OECD national coverage only |
| `DimOECDStage` | Stage code | OECD seed/early/later stage labels (no `_T`) |
| `DimEdTechCompany` | Company ID | Attributes of selected case-study companies |
| `DimEdTechStage` | Stage group | Curated round stage group |
| `FactOECDVCTotal` | Country × Year | OECD total market VC, nominal USD millions |
| `FactOECDVCStage` | Country × Year × Stage | OECD **complete-stage** groups only, nominal USD millions |
| `FactOWIDPrivateAI` | Year × Geography × Metric | AI and GenAI *private investment*, constant **2021 USD billions** |
| `FactOECDAIBenchmarks` | Year × Geography × Metric | Sparse OECD.AI published indicators; some nominal USD billions, some percent |
| `FactEdTechMarket` | Year | HolonIQ published EdTech VC, nominal USD billions, frozen publication vintage |
| `FactEdTechRounds` | Announced funding round ID | *Purposively selected* AI EdTech financing, nominal USD millions |

### Why there are two OECD country-VC facts

`_T` is an OECD *total* observation, not a fourth additive investment stage. If it were placed in the same fact as `SEED`, `START` and `LATER` and summed over all stages, the investment amount would be double-counted.

- `FactOECDVCTotal` contains only `_T` observations.
- `FactOECDVCStage` contains only `SEED`, `START` and `LATER`, and only country-year groups reporting **all three components**.
- Where stage data are complete, the pipeline checks the sum of components against the corresponding reported country-year total, allowing USD 0.05 million of tolerance to reflect rounding.
- **Never sum the two fact tables together.**