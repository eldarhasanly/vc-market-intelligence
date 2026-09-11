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
SDMX API / OECD Data Explorer

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

## 6. EdTech Research Sources

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