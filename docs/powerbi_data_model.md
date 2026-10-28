# Power BI semantic model and data marts

## 1. Purpose and implementation status

**Project:** VC Market Intelligence: Venture Capital in the Post-GPT Era  
**Power BI project:** `powerbi/VCMarketIntelligence.pbip`  
**Report coverage:** six interactive pages covering 2019–2025, with curated EdTech rounds from 2022–2025.

The Power BI report and semantic model are **implemented**. The data layer consists of five source-separated dimensions, six fact tables, and a disconnected `_Measures` table. The PBIP project uses Power Query CSV imports, a dimension-to-fact relationship model, and DAX measures for investment totals, shares, period comparisons, growth, and visual formatting.

**Source separation is a modeling requirement.** OECD VC, OECD.AI VC benchmarks, OWID private AI investment, HolonIQ EdTech VC, and the curated company-round sample have different coverage, units, prices, definitions, and sometimes observation grains. Their fact-table amounts are not interchangeable or additive. The shared `DimYear` facilitates filtering, **not** direct cross-source comparison.

## 2. Local generation and dependency chain

The eleven Power BI mart CSV files are created by the Python pipeline, not manually entered in Power BI.

From the repository root, once the five processed source files are present:

```powershell
python -m src.transform.build_powerbi_marts
python -m src.validation.validate_powerbi_marts
python -m unittest discover -s tests -p "test_*.py" -v
```

The mart output location is `data/mart/powerbi/` (eleven CSV files). The five local processed inputs are:

| Source | Required processed input |
|---|---|
| OECD VC market | `data/processed/oecd_vc_annual_2019_2025.csv` |
| OECD.AI publication benchmarks | `data/processed/oecd_ai_benchmarks_2026.csv` |
| OWID / Stanford AI Index | `data/processed/owid_private_ai_genai_2019_2025.csv` |
| HolonIQ EdTech VC | `data/processed/edtech_vc_holoniq_2019_2025_local.csv` |
| Curated EdTech financing rounds | `data/processed/edtech_verified_rounds_2022_2025.csv` |

The generator is intentionally **fail-fast** when inputs are unavailable; it does not fabricate data or automatically replace restricted providers. Source retrieval, vintages, licensing, and access instructions are explained in `docs/data_sources.md` and the provider-specific methodology files.

### Important: local Power Query file paths

The uploaded PBIP snapshot contains absolute Windows file paths within the eleven Power Query `File.Contents(...)` expressions. **A clean GitHub clone is not plug-and-play:** opening and refreshing the report on another machine requires the mart CSVs to be generated locally and the data-source paths to be updated in Power Query. The repository does not include the restricted source data or generated marts. Do not publish any private source files just to make refresh easier.

A reusable folder-path parameter would improve portability, but the current PBIP snapshot **does not yet implement one**. Do not describe the current setup as automatically portable or refreshable from GitHub alone.

## 3. Tables, grains, and observed snapshot row counts

The following counts were verified against the CSV files included in the uploaded project snapshot. The detached `_Measures` table is not one of the eleven CSV marts.

| Table | Rows | Grain / key | Role and unit |
|---|---:|---|---|
| `DimYear` | 7 | `year` | Calendar years 2019–2025; calculated regime classifications |
| `DimOECDCountry` | 37 | `country_code` | Country lookup for OECD facts |
| `DimOECDStage` | 3 | `stage_code` | `SEED`, `START`, `LATER`; excludes total `_T` |
| `DimEdTechCompany` | 6 | `company_id` | Selected companies and attributes |
| `DimEdTechStage` | 4 | `stage_group` | Curated company-round stage groups |
| `FactOECDVCTotal` | 244 | Country × year | OECD total VC, **nominal USD millions** |
| `FactOECDVCStage` | 651 | Country × year × stage | OECD reported complete-stage components, **nominal USD millions** |
| `FactOWIDPrivateAI` | 14 | Year × geography × metric | Global AI and GenAI **private investment**, **constant 2021 USD billions** |
| `FactOECDAIBenchmarks` | 16 | Year × geography × metric | Sparse published OECD.AI / Preqin VC-specific indicators; metric-dependent billions or percentages |
| `FactEdTechMarket` | 7 | Year | HolonIQ global EdTech VC, **nominal USD billions**, December 2025 vintage |
| `FactEdTechRounds` | 12 | `round_id` | Curated financing round amounts, **nominal USD millions** |

**Important distinctions:**

- `FactOECDVCTotal` holds the OECD `_T` total. `FactOECDVCStage` holds only complete `SEED`/`START`/`LATER` groups. Do **not** add these fact totals together. Stage sums can be lower than overall OECD totals because not every country-year has the necessary stage coverage; the complete-stage reconciliation tolerance is USD 0.05 million at country-year level.
- `FactOWIDPrivateAI` includes distinct AI and GenAI series, not two additive categories. The dashboard's non-GenAI residual is computed as *AI minus GenAI*; see the methodological caveat in Section 7.
- `FactOECDAIBenchmarks` represents selected publication observations, not a filled annual panel. Unavailable year–metric combinations must remain **blank**, not zero or interpolated.
- `FactEdTechRounds` is a **purposively selected sample** of 12 documented rounds across 6 companies. It does not support market-share estimates or generalization to global EdTech activity. Round amounts do not equal lifetime capital raised or valuation.

## 4. Relationship architecture

The intended analytical design contains **eleven active, one-to-many, single-direction dimension-to-fact relationships**. The date and dimension tables are on the `1` side; the facts are on the `*` side.

| Dimension key | Fact foreign key |
|---|---|
| `DimYear[year]` | `FactOECDVCTotal[year]` |
| `DimYear[year]` | `FactOECDVCStage[year]` |
| `DimYear[year]` | `FactOWIDPrivateAI[year]` |
| `DimYear[year]` | `FactOECDAIBenchmarks[year]` |
| `DimYear[year]` | `FactEdTechMarket[year]` |
| `DimYear[year]` | `FactEdTechRounds[year]` |
| `DimOECDCountry[country_code]` | `FactOECDVCTotal[country_code]` |
| `DimOECDCountry[country_code]` | `FactOECDVCStage[country_code]` |
| `DimOECDStage[stage_code]` | `FactOECDVCStage[stage_code]` |
| `DimEdTechCompany[company_id]` | `FactEdTechRounds[company_id]` |
| `DimEdTechStage[stage_group]` | `FactEdTechRounds[stage_group]` |

**What is actually stored in the inspected PBIP snapshot:** `relationships.tmdl` contains **14** relationship definitions. Alongside the eleven intended relationships, Power BI has generated **three additional relationships** from `source_publication_date` columns to hidden automatic local date tables (for OECD.AI benchmarks, HolonIQ EdTech, and curated EdTech rounds). The model also references four Power BI-managed date tables, including the date table template. These are **not** additional business data marts and do not change the eleven-table source model. They should not be counted as deliberate analytical joins. They can be reviewed if auto date/time is disabled in a later model-cleanup pass.

There are no intentional fact-to-fact links. The `_Measures` table is disconnected; its numeric placeholder column is hidden.

## 5. Measures and semantic conventions

The inspected `_Measures.tmdl` contains **40 DAX measures**, including 18 original core measures and additional page-specific calculations and formatting measures. They cover:

| Measure family | Examples and logic |
|---|---|
| OECD VC market | Total in USD M/B, year-over-year growth, stage investment and share |
| Post-GPT comparison | Average annual VC 2019–2021 versus 2023–2025; 2022 excluded; change percentage |
| Geographic analysis | Reporting-country count, country shares, 2025 Top 10 concentration, 2023–2025 country recovery |
| Private AI / GenAI | AI and GenAI investment, GenAI share, non-GenAI residual, 2022–2025 percentage-point change and annual share changes |
| OECD.AI publication benchmarks | AI VC, GenAI VC, AI share of global VC, AI mega-deal share; blank for unavailable observations |
| HolonIQ EdTech market | Annual VC, YoY growth, 2021/2025 comparison, decline versus peak, waterfall contributions |
| Curated EdTech deals | Funding sum, round count, distinct companies, company and stage funding shares |
| Visual formatting | Regime, recovery, GenAI share-change and EdTech growth colors |

Conventions:

- Investment figures are **numeric measures**, not formatted text; format strings add `$`, `B`/`M`, `%`, and `pp` only at display time.
- The pre-GPT and post-GPT period measures fix their years explicitly while preserving country filters. These averages reflect the available reporting countries in each year; they are **not balanced-panel estimators**.
- Growth calculations return blank where a required comparison-year observation is missing or the baseline is invalid.
- Percentage-point measures compute the difference between percentage shares, multiplied by 100, and display `pp` rather than `%`.
- Company counts are distinct counts; a company appearing in multiple years is counted once in the full-period KPI.

## 6. Implemented report pages

The PBIP snapshot contains the following report pages (Power BI tab names):

1. `01 - Overview`: cross-source executive overview (OECD, OWID, HolonIQ).
2. `02 - Post-GPT`: pre/post annual investment comparison and stage allocation.
3. `03 - Geography`: 2025 country concentration and 2023–2025 recovery.
4. `04 - GenAI Shift`: broader private AI / GenAI composition and annual share changes.
5. `05 - EdTech Market`: HolonIQ funding drawdown and annual growth.
6. `06 - AI-Enabled EdTech Deals`: curated financing rounds, company concentration, funding-stage allocation.

These are separate analytical sections, with a common navigation system and page-level source notes. The methodology is maintained in repository documentation rather than a seventh report page.

## 7. Known limitations and publication safeguards

1. **OWID AI/GenAI composition is supported at the published aggregate level, with limits.** Stanford *AI Index Report 2026*, Chapter 4, p. 179 (https://hai.stanford.edu/assets/files/ai_index_report_2026_chapter_4_economy.pdf) describes GenAI as part of overall private AI financing (2025: $170.9B of $344.7B, nominal), consistent with the **49.58%** ratio of the same-vintage OWID constant-2021-USD series. The original private-AI universe uses a $1.5M funding screen. The OWID GenAI chart does not independently restate that screen; the primary report supports the published subset relationship, **not** an audited annual deal-by-deal classification reconciliation. `Private Non-GenAI Investment (2021 USD B)` is a model-derived difference between two published aggregates, not an independently observed category. Document classification and revision risk; never subtract or divide across different providers. See `docs/owid_ai_methodology.md`.
2. **Different sources must not be combined into one total.** OECD national VC totals, OECD.AI/Preqin VC metrics, OWID broad private investment, and HolonIQ EdTech VC are distinct statistical universes. Even amounts denominated in `USD B` may use different price bases.
3. **Country and stage coverage vary.** OECD country-year totals are not a complete estimate of global VC investment; complete-stage observations are a smaller panel.
4. **Sample selection bias is material.** The EdTech financing sample is deliberately curated, not representative of sector-wide transactions or financing levels.
5. **Refresh requires private/local inputs.** Marts are generated locally; the snapshot's Power Query uses absolute Windows paths. Restricted and locally generated provider-derived datasets must not be committed or bundled as public release assets without appropriate rights.
6. **Historical series and source vintages may be revised.** Reproducibility assumes the documented source files and relevant publication versions, not a silently refreshed latest provider dataset.

## 8. Verification and maintenance

Run the mart builder, validator, and offline test suite using the commands in Section 2. The uploaded project audit previously recorded **21 passing Python tests** and **six passing validators**, but Power BI graphical rendering and interaction behavior must also be checked in Desktop; they are not proved by Python tests alone.

Suggested Power BI DAX Query View checks: row counts, dimension-key uniqueness, referential-integrity `EXCEPT` checks across the eleven intended dimension–fact relationships, period KPI reconciliation, fact-source-specific units, and blank preservation for sparse benchmarks. See the README and source methodology documents for analytical context.

**Repository policy:** version-control source code, semantic model definitions, report definitions, synthetic tests, and documentation. Keep local cache, private raw inputs, source-restricted derived CSVs, and machine-specific Power BI state out of public commits.