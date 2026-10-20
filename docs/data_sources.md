# Data Sources and Source Governance

## 1. Purpose

This document records the data sources evaluated for this project and defines how each source may be used in the analytical pipeline.

The project prioritizes reproducibility, source provenance, methodological transparency, and legal redistribution.

## 2. Source Classification

Sources are classified into four categories:

### Primary
Structured sources used directly in the analytical model.

### Benchmark
Sources used to validate or contextualize primary data.

### Context
Research used to interpret market developments but not loaded directly into the analytical model.

### Excluded
Sources that cannot currently be used because of licensing, access, provenance, or methodological limitations.

## 3. OECD Venture Capital Investments Database

Provider: OECD (Organisation for Economic Co-operation and Development)

Status: PRIMARY

Coverage:
- Annual VC investment
- Country-level observations
- Business development stage
- Historical data through 2025
- USD values and GDP-relative measures

Access:
OECD SDMX REST API.

Dataset:
`OECD.SDD.TPS,DSD_VC@DF_VC_INV,1.0`

Extraction period:
2019–2025

Frequency:
Annual

Unit used in the project:
Millions of US dollars, exchange-rate converted.

Extraction implementation:
`src/extract/extract_oecd_vc.py`

The raw API response is stored locally under `data/raw/oecd_vc/` and is not committed to the repository. The extractor also records retrieval metadata and a SHA-256 checksum for source-version tracking.

Planned use:
- Geographic VC analysis
- Stage analysis
- Cross-country comparisons
- Reproducible API extraction

Repository policy:
Raw observations may be retrieved automatically from the official OECD API.

Licence:
OECD open-access policy / CC BY 4.0, subject to source-specific notices.

Limitations:
- Annual rather than quarterly frequency
- Coverage differs by country and year
- National VC definitions are harmonized but not perfectly identical
- Missing observations exist for some countries

### Reproducibility

The OECD dataset is retrieved programmatically rather than manually downloaded.

Running:

`python src/extract/extract_oecd_vc.py`

recreates the local raw dataset used as the input to the transformation pipeline.

## 4. PitchBook-NVCA Venture Monitor and Yearbook

Providers:
PitchBook and National Venture Capital Association

Status: PRIMARY BENCHMARK

Coverage:
- Global annual VC activity
- US quarterly VC activity
- Funding stages
- Sectors
- Mega-deals
- Fundraising
- Exits
- Geographic US analysis
- AI concentration

Planned use:
- Global market headline validation
- US quarterly post-GPT analysis
- Mega-round analysis
- US stage and sector analysis

Repository policy:
Original PitchBook/NVCA files will NOT be redistributed through this repository.

Publicly available source files may be downloaded locally into data/raw/ where required.

Limitations:
- Proprietary PitchBook methodology
- Redistribution restrictions
- Primarily detailed for the United States
- Historical values may be revised

## 5. OECD.AI Venture Capital Data

Provider:
OECD.AI Policy Observatory

Underlying data:
Preqin

Status: PRIMARY AI BENCHMARK

Coverage:
- Global AI venture investment
- Generative AI investment
- Country
- Industry
- Investment stage
- Historical analysis from 2012 through 2025

Planned use:
- AI funding trend
- AI share of VC
- GenAI trend
- Geographic AI concentration
- AI industry composition
- Potential education-and-training AI analysis

Repository policy:
Only appropriately licensed OECD-published aggregate statistics will be used publicly.

Underlying Preqin data will not be redistributed.

Limitations:
- Underlying data originate from a proprietary provider
- Historical observations may be revised
- AI classification depends on provider and OECD classification methodology

### OECD AI published-benchmark ingestion (October 2026)

A small table of individually verified, **published aggregate** indicators has been curated from the OECD (2026) policy brief, *Venture capital investments in artificial intelligence through 2025*:

- Source publication: https://doi.org/10.1787/a13752f5-en
- Input transcription: `src/config/oecd_ai_report_2026.json`
- Transformation: `src/transform/build_oecd_ai_benchmarks.py`
- Validation: `src/validation/validate_oecd_ai_benchmarks.py`
- Output: `data/processed/oecd_ai_benchmarks_2026.csv`
- Unit: nominal USD billions for funding amounts; percentage points for shares.

Each record includes its own metric, observation year, geography, precision qualifier and source-evidence note. The table intentionally contains only values explicitly stated in the report. **Missing years are not zero values and must not be interpolated.** It is not a 2019–2025 time-series panel, and it does not provide deal counts or company-level data.

**Provider comparability:** the OECD.AI figures use Preqin's global deal coverage and must not be divided by, joined numerically with, or presented as the sector subset of the separate OECD country-level VC series (`DSD_VC@DF_VC_INV`). The global 2025 total of USD 427.1B in this benchmark belongs to the *Preqin-based* analytical universe only.

**Geography:** EU27 is an aggregate region while United States, China and United Kingdom refer to recipient-firm jurisdictions. These observations are not investor-origin flows. Only an explicitly disjoint set of geography observations should be summed.

**Mega-deal definition:** the report describes mega-deals as funding rounds **over** USD 100 million; this may differ from datasets using *at least* USD 100 million.

The OECD publication is publicly accessible, but its underlying Preqin transactions are proprietary. This repository reproduces a limited set of attributed published summary figures, not Preqin source records. OECD's open-content permissions do not automatically apply to third-party source materials. Recheck applicable source notices before redistributing additional figures or data.

## 6. Our World in Data / Stanford AI Index

**Providers:** Our World in Data (OWID), Stanford University AI Index

**Underlying data:** Quid via AI Index Report (2026), with inflation adjustments using U.S. Bureau of Labor Statistics data.

**Status:** PRIMARY COMPLEMENTARY DATASET (AI and GenAI private-investment trends)

### Coverage

- Annual global private investment in artificial intelligence
- Annual global private investment in generative AI
- AI investment series: 2013–2025
- Generative AI investment series: 2019–2025
- Project extraction period: 2019–2025
- Frequency: Annual
- Unit: Constant 2021 US dollars (inflation-adjusted)

### Data Sources

**Artificial Intelligence:**

[Private Investment in Artificial Intelligence](https://ourworldindata.org/grapher/private-investment-in-artificial-intelligence)

**Generative AI:**

[Global Investment in Generative AI](https://ourworldindata.org/grapher/global-investment-in-generative-ai)

Both datasets are accessible through the Our World in Data API as CSV files accompanied by JSON metadata.

### Measurement Definition

These indicators measure external private-market investment in AI and generative AI companies, including venture capital and private equity.

They do not exclusively measure venture capital investment.

The indicators exclude internal corporate research and development, capital expenditures, public-sector funding, and investment in publicly traded companies.

The general AI series covers privately held AI companies raising more than USD 1.5 million.

### Price Basis

The investment figures are expressed in constant 2021 US dollars.

Our World in Data adjusts the original investment values using the U.S. Consumer Price Index (CPI) to improve comparability across years.

Consequently, these figures must not be directly combined with nominal investment figures from OECD.AI, PitchBook/NVCA, or other market intelligence providers.

### Planned Use

- Analyze historical private investment in AI and GenAI
- Compare investment trends before and after 2022
- Examine the relative growth of generative AI investment
- Provide contextual evidence for the broader post-GPT analysis
- Compare directional trends with OECD.AI venture capital benchmarks

### Extraction and Transformation

Extraction implementation:

`src/extract/extract_owid_ai.py`

Transformation implementation:

`src/transform/transform_owid_ai.py`

Validation implementation:

`src/validation/validate_owid_ai.py`

Processed local dataset:

`data/processed/owid_private_ai_genai_2019_2025.csv`

The pipeline downloads the original data and metadata, transforms the relevant observations into a standardized analytical structure, and validates the resulting dataset.

### Repository and Redistribution Policy

The series relies on third-party data provided through Our World in Data.

Although OWID-produced content is generally available under Creative Commons Attribution licensing, third-party data remain subject to the original providers' licensing conditions.

Until redistribution rights for the underlying investment data are confirmed:

- Raw downloaded files will not be committed to Git.
- The generated processed investment dataset will remain local.
- Python extraction, transformation, and validation scripts may be version-controlled.
- Source metadata and methodological documentation will be maintained.
- Published findings will provide appropriate attribution to OWID, Stanford AI Index, Quid, and other relevant data providers.

### Limitations

- The investment universe includes private equity and is not restricted to venture capital.
- AI and GenAI company classifications depend on the underlying provider's methodology.
- Large investment transactions may substantially influence annual totals.
- Inflation adjustments use a general consumer price index rather than an AI-specific investment price index.
- The series cannot be directly combined with nominal OECD.AI venture capital observations.
- The data do not establish a causal relationship between ChatGPT's release and subsequent investment trends.

### Methodological Documentation

Detailed extraction procedures, transformation rules, validation requirements, and source-specific limitations are documented in:

[`docs/owid_ai_methodology.md`](owid_ai_methodology.md)

The OWID series will be maintained as a separate analytical source from OECD.AI venture capital benchmarks to preserve methodological consistency.

## 7. EdTech Research Sources

### HolonIQ

Status: CONTEXT / BENCHMARK

Purpose:
- Global EdTech funding trends
- EdTech sector and subsector context
- External validation

Repository policy:
HolonIQ raw or platform data will not be redistributed.

### Brighteye Ventures

Status: CONTEXT / BENCHMARK

Purpose:
- EdTech funding trends
- Deal-size distribution
- European EdTech
- Learning & Work taxonomy
- External validation

Important note:
Brighteye's definition of EdTech / Learning & Work differs from other providers. Figures will therefore not be merged directly with HolonIQ or other sector datasets.

### HolonIQ EdTech VC Historical Benchmark

**Status:** Primary EdTech market benchmark (local data)

**Source:** [2026 Global Education Outlook](https://www.holoniq.com/notes/2026-global-education-outlook)

**Publication date:** 19 December 2025

**Coverage:** 2019–2025

**Frequency:** Annual

**Unit:** Nominal USD billions

**Market:** Global EdTech venture capital, excluding private equity.

The historical series is based on the published chart in HolonIQ's 2026 Global Education Outlook.

The dataset preserves the December 2025 publication vintage.
A February 2026 update revised the reported 2025 funding figure
from $2.4B to $2.6B. These releases are not combined.

Original and processed numerical observations remain local because public redistribution rights have not been established.

See:
- [EdTech methodology](edtech_market_methodology.md)
- [EdTech classification rules](edtech_taxonomy.md)

### Curated AI-Enabled EdTech Funding Rounds

**Status:** Curated company-level case-study dataset

**Coverage:** 2022–2025

**Unit of analysis:** Individual announced funding round

**Currency:** Nominal USD millions

**Selection:** Publicly announced rounds involving selected AI-enabled EdTech companies.

**Source:** Company and company-issued funding announcements, with source URLs preserved for individual observations.

**Input:**
`src/config/edtech_verified_rounds_2022_2025.json`

**Processed dataset:**
`data/processed/edtech_verified_rounds_2022_2025.csv`

**Methodology:**
[EdTech Funding Rounds Methodology](edtech_rounds_methodology.md)

This dataset is a purposefully selected sample rather than a comprehensive representation of global EdTech investment.

It must not be used to estimate global EdTech funding, market-wide investment growth, or AI's share of total EdTech venture capital.

## 7. Dealroom

Status: BENCHMARK ONLY

Purpose:
- Validate global VC direction
- Current market context
- Compare stage and geography trends

Repository policy:
Dealroom data will not be scraped or redistributed.

## 8. Crunchbase

Status: EXCLUDED FROM VERSION 1.0

Reason:
Full structured CSV access requires an appropriate commercial licence.

The source may be reconsidered if licensed access becomes available.

## 9. Canonical Source Mapping

| Analytical Question | Canonical Source |
|---|---|
| Cross-country VC investment | OECD VC Database |
| VC investment by stage | OECD VC Database |
| Global annual VC trend | NVCA/PitchBook benchmark |
| US quarterly VC trend | NVCA/PitchBook |
| US mega-round activity | NVCA/PitchBook |
| AI investment | OECD.AI |
| Generative AI investment | OECD.AI |
| EdTech total market | To be finalized |
| AI-enabled EdTech | OECD.AI + curated dataset |
| Company-level EdTech rounds | Curated primary-source dataset |

## 10. Source Integration Rule

Statistics from different providers will not be combined into a single continuous series unless their definitions and methodologies are demonstrably compatible.

Every analytical observation will retain a Source identifier.

Provider-specific values will be compared as separate series where appropriate.

## 11. Data Versioning

Each source ingestion will record:

- source provider
- retrieval date
- source publication or dataset
- reporting period
- original unit
- original geography
- transformation status

Raw source files will remain unchanged after ingestion.

Transformations will produce new files in data/processed/.

## 12. Outstanding Data Gap

A reproducible, openly redistributable global EdTech deal-level dataset covering both the pre-GPT and post-GPT periods has not yet been identified.

Version 1.0 will therefore distinguish between:

1. published EdTech market benchmarks; and
2. a curated company-level EdTech funding dataset based on primary public funding announcements.

The curated dataset will not be used to estimate total global EdTech funding unless its coverage is sufficiently comprehensive.