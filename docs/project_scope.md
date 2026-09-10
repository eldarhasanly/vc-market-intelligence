# Project Scope and Analytical Framework

## 1. Project Overview

**Project title:** VC Market Intelligence: Venture Capital in the Post-GPT Era

This project develops an end-to-end venture capital (VC) market intelligence solution using Python, Power BI, Power Query, and DAX.

The analysis investigates how VC activity changed during the period following the emergence of GenAI, with particular attention to funding concentration, AI investment, mega-round activity, geography, investment stage, and the EdTech sector.

The project is designed as a market intelligence and business intelligence case study rather than as a causal economic study. Its objective is to identify and communicate observable changes in VC allocation across different market periods.

## 2. Analytical Problem

Headline VC investment can increase even when financing conditions do not improve broadly across the startup market.

A relatively small number of very large funding rounds, particularly in AI, can substantially increase aggregate investment while deal counts, early-stage activity, or investment in other sectors remain comparatively weak.

For this reason, aggregate funding alone is insufficient for evaluating the condition of the VC market.

The project therefore examines both the scale and the distribution of VC investment.

My central analytical question is:

> How much has the VC market changed in the post-GPT era? Is the apparent rebound a reflection of broad-based increase in investments, or is it a story of capital concentration in AI companies, mega-rounds, select stages and geographies?

A dedicated EdTech analysis investigates how these broader structural changes are reflected within a sector directly affected by GenAI.

## 3. Research Questions

The project addresses the following questions:

1. How have VC funding and deal activity evolved over time?

2. How do funding levels, deal counts, and deal sizes differ between the pre-GPT and post-GPT periods?

3. What proportion of VC investment is allocated to AI and GenAI companies?

4. To what extent are recent funding totals driven by mega-rounds?

5. Has VC become more concentrated among a smaller number of companies?

6. How does capital allocation differ across funding stages?

7. How does venture investment differ across major geographic markets?

8. How has EdTech venture funding evolved relative to the broader VC market?

9. Within EdTech, has GenAI contributed to a broad funding recovery or primarily increased investment in a smaller set of AI-enabled companies?

## 4. Time Scope

The primary historical analysis will cover:

**2019–2025**

This period provides several years of observations before and after the emergence of generative AI while avoiding direct comparison between complete historical years and an incomplete current year.

Where sufficiently complete and methodologically compatible data are available, **2026 year-to-date (YTD)** results may be included as a separate current-market indicator.

2026 YTD values will not be directly compared with complete annual observations unless equivalent YTD periods are used.

### Analytical Periods

For comparative analysis, the timeline will be divided into three regimes:

| Period | Definition |
|---|---|
| Pre-GPT | Q1 2019 – Q3 2022 |
| Transition | Q4 2022 |
| Post-GPT | Q1 2023 – Q4 2025 |
| Current | 2026 YTD, where available |

ChatGPT was publicly released on [30 November 2022.](https://x.com/sama/status/1598038815599661056?s=20)

Q4 2022 is treated as a transition period because assigning the entire quarter to either the pre-GPT or post-GPT regime would create an artificial classification.

The transition quarter will therefore normally be excluded from direct pre/post averages.

## 5. Interpretation of the Post-GPT Period

The term **post-GPT** is used as a temporal market classification.

It does not imply that the release of ChatGPT caused subsequent changes in VC markets.

VC activity during this period was also affected by:

- interest rates,
- monetary conditions,
- startup valuations,
- public-market conditions,
- exit markets,
- geopolitical developments,
- investor risk appetite,
- technological developments beyond GenAI.

The dashboard will therefore describe market changes associated with the period.

## 6. Geographic Scope

The primary scope is the **global VC market**, subject to data availability and consistency.

Regional analysis will prioritize:

- United States / North America
- Europe
- Asia
- Other regions where sufficient observations exist

Country-level analysis may be included where the underlying source provides reliable and comparable data.

Geographic classifications will be standardized during the data transformation stage.

## 7. Sector Scope

The project will analyze the broader VC market while giving particular attention to:

- Artificial Intelligence
- Generative AI
- EdTech

Other sectors may be retained for benchmarking and comparison.

Sector classifications will follow source-provided taxonomies where possible.

Because different market intelligence providers may use different sector definitions, incompatible classifications will not be combined without documented harmonization rules.

## 8. AI and GenAI Definitions

### Artificial Intelligence

A company or investment will be classified as AI-related when it is identified as such by the underlying data provider or by a documented classification methodology.

### GenAI

GenAI represents a subset of AI involving systems capable of generating new content such as text, images, audio, video, software code, or other structured outputs.

Where source datasets provide explicit GenAI classifications, those classifications will be preserved.

If manual company-level classification is required, the classification rules and evidence will be documented separately.

AI and GenAI classifications will not be inferred solely from company names.

## 9. EdTech Definition

EdTech refers to technology companies whose primary products or services support education, learning, training, skills development, or educational administration.

Potential EdTech subsectors include:

- K-12 education
- Higher education
- Workforce learning and upskilling
- Corporate learning
- Language learning
- Tutoring
- Learning platforms
- Education infrastructure
- AI-enabled learning products

The final subsector taxonomy will depend on the available data.

Companies whose educational activity is secondary to their principal business will not automatically be classified as EdTech.

## 10. Funding Stage Framework

Funding-stage labels differ across data providers.

Where harmonization is required, detailed stages will be mapped into broader analytical categories:

| Analytical Stage | Examples |
|---|---|
| Pre-seed / Seed | Pre-seed, Seed |
| Early Stage | Series A, Series B |
| Late / Growth Stage | Series C+, Growth |
| Other / Unknown | Unclassified, corporate, other |

The exact mapping will be documented once the datasets have been selected.

Original source-stage values will be preserved before transformation.

## 11. Mega-Round Definition

A **mega-round** is defined as a venture funding round of:

**USD 100 million or more**

Where company-level funding-round data are available, the following metrics will be calculated:

- Mega-round count
- Mega-round funding
- Mega-round share of total VC investment

Mega-round share is defined as:

$$
\text{Mega-Round Share}
=
\frac{\text{Funding from rounds } \geq \$100\text{M}}
{\text{Total VC Funding}}
$$

This measure will help determine whether aggregate funding growth reflects broad market participation or a relatively small number of large transactions.

## 12. Core Market Metrics

The dashboard will prioritize the following measures:

### Funding Activity

- Total VC funding
- Deal count
- Average deal size
- Median deal size
- Quarter-over-quarter funding growth
- Year-over-year funding growth
- Year-over-year deal growth

### AI Metrics

- AI funding
- AI deal count
- AI share of VC funding
- GenAI funding
- GenAI share of AI funding

### Capital Concentration

- Mega-round funding
- Mega-round share
- Top 5 company funding share
- Top 10 company funding share
- Funding concentration index

### Market Segmentation

- Funding by geography
- Funding by stage
- Funding by sector
- Deal count by geography
- Deal count by stage

### EdTech Metrics

- EdTech funding
- EdTech deal count
- Median EdTech round
- EdTech share of total VC
- AI-enabled EdTech funding share
- EdTech funding by subsector
- EdTech funding by geography
- EdTech funding by stage
- Top-company concentration

## 13. Capital Concentration

Where sufficiently granular company-level data are available, concentration will be measured using both simple concentration ratios and the Herfindahl-Hirschman Index (HHI).

For company-level funding shares:

$$
HHI = \sum_{i=1}^{n} s_i^2
$$

where:

- $s_i$ represents company $i$'s share of total funding within the selected market and period;
- $n$ represents the number of companies.

The metric will be used comparatively rather than as a regulatory antitrust measure.

Increasing HHI values indicate that funding is becoming more concentrated among fewer recipients.

## 14. Primary Comparative Framework

The main comparison will evaluate:

**Pre-GPT vs Post-GPT**

across:

- total funding,
- deal count,
- average and median deal size,
- AI funding share,
- mega-round share,
- company concentration,
- stage distribution,
- geographic distribution,
- EdTech investment.

Quarterly observations will generally be preferred over annual observations for structural comparisons because they preserve more information about market timing.

## 15. EdTech Analytical Framework

The EdTech section will operate as a sector-level case study within the broader venture market.

It will investigate three dimensions.

### Market Performance

How did EdTech funding and deal activity change before and after 2022?

### Relative Performance

Did EdTech outperform or underperform the overall VC market?

### AI Reallocation

Within EdTech, did GenAI produce broad investment growth or increase concentration around a smaller number of AI-enabled companies?

Where data allow, AI-enabled and non-AI EdTech companies will be compared directly.

## 16. Unit of Analysis

The project may contain two analytical levels depending on source availability.

### Market-Level Data

Typical unit:

**Quarter × Geography × Sector × Stage**

Used for long-term market trends and comparisons.

### Deal-Level Data

Typical unit:

**Individual funding round**

Used for:

- company rankings,
- mega-round analysis,
- median round calculations,
- concentration metrics,
- AI/EdTech classification.

Market-level aggregates and deal-level observations will not be combined as though they represent the same unit of analysis.

## 17. Data Source Principles

Data sources will be selected according to:

1. provenance,
2. methodological transparency,
3. historical coverage,
4. reproducibility,
5. licensing or redistribution conditions,
6. granularity,
7. consistency over time.

Preference will be given to original market intelligence providers, official statistical sources, and downloadable structured datasets.

Third-party datasets will not be used solely because they are convenient if their origin or methodology cannot be established.

Every source used in the final analytical model will be documented with:

- provider,
- dataset/report name,
- URL,
- coverage,
- access date,
- unit of analysis,
- important definitions,
- transformations,
- known limitations,
- redistribution conditions.

## 18. Data Harmonization Principles

The project will not assume that funding statistics published by different providers are directly comparable.

Differences may result from:

- definition of VC,
- company classification,
- geography definitions,
- funding-stage taxonomy,
- treatment of debt,
- accelerator funding,
- corporate venture transactions,
- undisclosed transactions,
- currency conversion,
- data revision practices.

Where datasets cannot be reconciled reliably, they will be presented as separate analytical series or used only as external benchmarks.

A single canonical source will be selected for each major time series wherever possible.

## 19. Analytical Limitations

The project is expected to face several limitations.

### Source Coverage

No public dataset necessarily captures every private venture transaction.

### Classification Differences

AI, GenAI, and EdTech definitions may vary across providers.

### Reporting Lag

Recent funding observations may be incomplete and subsequently revised.

### Survivorship and Visibility Bias

Large or publicly announced rounds are more likely to appear in public datasets.

### Causal Interpretation

Pre/post comparisons identify temporal differences but do not establish causal effects.

### Current-Year Comparability

2026 YTD observations are incomplete and must not be interpreted as directly equivalent to full-year totals.

These limitations will be incorporated into dashboard documentation and interpretation.

## 20. Out of Scope

Version 1.0 of the project will not attempt to:

- predict startup success,
- recommend individual VC investments,
- value private companies,
- estimate investment returns,
- construct VC fund portfolios,
- establish causal effects of ChatGPT,
- rank individual investors unless sufficiently reliable investor-level data are obtained.

These areas may become extensions of the project but are not required for the initial portfolio release.

## 21. Expected Deliverable

The final output will be an interactive Power BI market intelligence report supported by a reproducible analytical workflow.

The report is expected to contain six analytical pages:

1. VC Market Overview
2. Post-GPT Market Regime
3. AI and Capital Concentration
4. Geography and Funding Stage
5. EdTech Deep Dive
6. Methodology and Data Quality

Supporting repository documentation will describe the data sources, transformations, semantic model, DAX measures, analytical findings, and project limitations.

## 22. Technology Stack

The planned stack is:

- Python
- pandas
- Jupyter Notebook
- Power Query
- Power BI
- DAX
- Git
- GitHub

Python will primarily support reproducible data preparation, validation, and exploratory analysis.

Power Query will support BI-specific transformation and ingestion tasks.

Power BI and DAX will provide the semantic model, analytical measures, and interactive reporting layer.