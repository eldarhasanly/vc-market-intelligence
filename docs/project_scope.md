# Project Scope and Analytical Framework

## 1. Project overview

**Project:** VC Market Intelligence: Venture Capital in the Post-GPT Era  
**Implementation:** Python, pandas, Jupyter, Power Query, Power BI, DAX, Git and GitHub  
**Historical coverage:** 2019–2025 (subject to the availability of each source)

This project is an end-to-end business intelligence case study examining reported venture capital (VC) investment, the changing geography and stage composition of VC funding, global private investment in AI and generative AI (GenAI), and the EdTech funding market. It combines source-aware data preparation, quality controls, a dimensional semantic model, and six Power BI report pages.

The analysis is **descriptive, not causal**. “Post-GPT” denotes a historical period following the public release of ChatGPT in November 2022. Changes during this period must not be attributed to that release without a separate causal research design.

## 2. Questions addressed by the delivered report

1. How did reported VC investment change across the 2019–2025 period, especially between the defined pre-GPT and post-GPT windows?
2. How did the observed allocation of VC investment across Seed, Start-up/Early and Later stages change between these windows?
3. How concentrated was reported 2025 VC investment across countries, and how did major reporting markets change between 2023 and 2025?
4. How did the two OWID/Stanford private-investment series for AI and GenAI evolve, including their reported relative magnitudes and annual changes?
5. How did HolonIQ's global EdTech VC funding estimate change from its 2021 peak through 2025?
6. What financing patterns appear **within a deliberately selected sample** of AI-enabled EdTech funding rounds, by year, company and funding stage?

The project does **not** answer whether ChatGPT caused investment changes, nor whether AI-enabled companies captured a specified share of the whole EdTech VC market.

## 3. Time scope and period conventions

The completed report uses **annual observations from 2019 through 2025**, except where an individual source is sparse or covers fewer years. It does not include 2026 year-to-date observations.

The annual OECD comparison on Page 2 uses the following convention:

| Classification | Annual observations | Use |
|---|---|---|
| Pre-GPT | 2019–2021 | Three-year average annual reported VC investment |
| Transition | 2022 | Shown in the annual trend; excluded from the pre/post average comparison |
| Post-GPT | 2023–2025 | Three-year average annual reported VC investment |

The event-time rationale is more granular: **Q4 2022** contains the November 2022 launch of ChatGPT and can reasonably be treated as a transition quarter. Because the completed OECD dashboard uses **annual**, rather than quarterly, data, it excludes **all of 2022** from direct pre/post averages rather than attempting to split that year's observation. These are **different classification granularities**, not interchangeable period definitions.

The company-round source can retain its own announcement-level time and transition classification. Those event labels should not be used to reinterpret the annual OECD comparison.

The pre/post averages compare annual reported totals. They are affected by varying country coverage and the exceptionally elevated 2021 investment figure; they are not like-for-like balanced-panel or causal estimates.

## 4. Sources, definitions and measurement bases

| Source | Delivered use | Observation grain | Measurement and constraint |
|---|---|---|---|
| OECD Venture Capital Investments | Overall VC totals; country rankings; country recovery; funding-stage allocation | Country × year for totals; country × year × stage for complete stage groups | Nominal USD millions before DAX conversion to billions; reporting-country coverage varies |
| Our World in Data / Stanford AI Index (Quid) | Annual private AI and private GenAI investment trends | World × year × metric | Constant 2021 USD billions; external private investment, **not exclusively VC** |
| OECD.AI / Preqin | Curated, published AI/GenAI VC benchmark observations in the data layer | Year × geography × indicator, irregular years | VC-specific; nominal USD billions for amount indicators, proportions for share indicators; **not a continuous annual panel** |
| HolonIQ | Global EdTech VC funding trend and year-on-year changes | Year | Nominal USD billions; **December 2025 publication vintage** (2025 value $2.4B); later reports may revise it |
| Source-linked AI-enabled EdTech company announcements | Deal-sample funding by year, company and funding-stage group | Individually announced financing round | 12 purposively selected USD rounds for six companies, 2022–2025; nominal USD millions |

Provider universes, taxonomies, geographic coverage, reporting dates, currency bases and financing definitions vary. **Do not sum, subtract or calculate market shares across unrelated provider series**. An apparent difference between one provider's AI total and another provider's AI or GenAI figure is not a meaningful funding residual.

Source documentation: [`data_sources.md`](data_sources.md), [`owid_ai_methodology.md`](owid_ai_methodology.md), [`edtech_market_methodology.md`](edtech_market_methodology.md), and [`edtech_rounds_methodology.md`](edtech_rounds_methodology.md).

### AI / GenAI subset comparability — verified aggregate interpretation and limitations

The OWID AI and GenAI series share the underlying **Quid / Stanford AI Index Report 2026** provider vintage and the same constant-2021-USD price basis. The original [Stanford AI Index 2026, Chapter 4, Section 4.2, p. 179](https://hai.stanford.edu/assets/files/ai_index_report_2026_chapter_4_economy.pdf) describes the private-investment universe as AI/ML companies with over **$1.5 million in funding since 2013**. It expressly states that GenAI companies account for **$170.9 billion of the $344.7 billion private AI total** in 2025, establishing the source's **aggregate GenAI-as-subset** interpretation. The ratio from the nominal report figures (approximately **49.58%**) agrees with the 2025 ratio from OWID's inflation-adjusted versions of those series. The GenAI OWID chart metadata does not independently repeat the threshold; the primary report is the appropriate additional evidence.

Page 4 therefore uses the two **same-vintage, source-defined** annual aggregates to calculate a GenAI share and an **arithmetic non-GenAI residual**. The resulting 100%-stacked chart is an analytical decomposition, **not a separate Quid-published non-GenAI category or a company-level matched-deal audit**. Classification, funding thresholds, underlying data revisions, and the absence of independently audited company-level overlaps remain limitations. Cross-provider fractions or residuals (e.g., OECD.AI versus OWID) remain inappropriate. Details and source links: [`owid_ai_methodology.md`](owid_ai_methodology.md).

## 5. Geographic scope

The OECD country-level extract contains **37 distinct countries** during 2019–2025, with **32 reporting 2025 total-VC observations** in the validated snapshot. Countries included in a particular annual ranking are those with usable records in that year. OECD-reported country totals are **not a comprehensive worldwide VC census**.

The 2025 Top 10 concentration calculation divides the investment of the ten largest reporting countries by the **same year's reported-country total**. The country-recovery chart uses a 2023 baseline and 2025 endpoint, requiring valid observations for both dates and a positive 2023 denominator. Its countries are selected by **2025 investment level**, not by the rate of growth.

Other providers report global indicators under their own methodologies; these are presented separately from the OECD country totals.

## 6. Funding-stage framework

The OECD stage analysis preserves its native categories: `SEED`, `START` and `LATER`. The `_T` code denotes **total VC**, not an additional additive stage. The fact model therefore separates `FactOECDVCTotal` and `FactOECDVCStage`.

Stage-level results use country-years with all three reported stage components; the resulting observed universe is narrower than the total-VC fact. Stage shares are calculated as stage-level investments divided by the sum of the reported stage components **within the same period and eligible country-year set**, not as the mean of annual percentages. A change in shares should not be presented as traced capital physically moving between funding stages.

The EdTech deal-sample stage groups are a **separate project classification**. They must not be treated as equivalent to the OECD stages without an explicit mapping and comparability assessment. See [`edtech_taxonomy.md`](edtech_taxonomy.md).

## 7. EdTech scope and classification

EdTech refers to businesses whose primary products serve education, learning, training, skills development or education workflows. The project includes:

- **A market-level historical series:** HolonIQ's global EdTech VC annual funding estimates, 2019–2025.
- **A separate company-round sample:** twelve documented rounds involving six selected AI-enabled EdTech companies, 2022–2025.

The case-study sample is **purposively selected** and disproportionately reflects companies with public financing announcements. Its round dates are announcement/publication dates when documented as such, and its amounts are the **newly announced round amounts**, not company lifetime funding, valuations, acquisitions or undisclosed transactions. Company counts are distinct counts; the number of companies across years must not be added to estimate the full-period count.

The sample may support rankings, observed funding concentrations, round counts and stage mix **within that sample only**. It cannot establish worldwide EdTech deal counts, the market-wide share of AI-enabled EdTech, the sector's median deal size, or a representative sector recovery trend. Do not divide the selected-round sum by the HolonIQ aggregate to infer a market share.

## 8. Delivered analytical pages

| Page | Title | Primary analytical content |
|---|---|---|
| 01 | VC Market Overview | Separate executive views of OECD-reported VC, OWID private AI/GenAI, and HolonIQ EdTech VC |
| 02 | Post-GPT Market Regime | Three-year pre/post mean investment, annual VC investment, observed stage allocation |
| 03 | Geographic VC Investment Analysis | 2025 country ranking/concentration and 2023–2025 recovery among leading reporting markets |
| 04 | AI Investment and the GenAI Funding Shift | Private AI/GenAI series, same-vintage source-defined composition and annual share changes **subject to Section 4 limitations** |
| 05 | EdTech VC Market Analysis | Peak-versus-2025 comparison, waterfall of annual changes, year-on-year growth |
| 06 | AI-Enabled EdTech Deal Intelligence | Selected-round funding activity, company ranking and funding-stage distribution |

The report contains **six analytical pages**. Source and methodology details are maintained primarily in GitHub documentation and concise page footnotes; there is no separate seventh methodology report page.

The OECD.AI benchmark mart exists in the semantic model as a **sparse supporting source**, but the originally proposed separate benchmark table was omitted from the final Page 4 layout.

## 9. Analytical measures and interpretation

The completed dashboard uses existing DAX measures and derived visuals to describe:

- Reported annual investment levels, year-on-year growth and fixed-year comparisons.
- Pre- versus post-GPT average annual OECD VC investment (2022 excluded), alongside the full annual trajectory.
- Funding-stage composition based on eligible, stage-disaggregated OECD observations.
- Geographic shares within the 2025 OECD reporting universe and observed investment changes between 2023 and 2025.
- Private AI and GenAI investment trends, their same-vintage source-defined share, and a derived non-GenAI residual (see Section 4).
- HolonIQ EdTech investment changes: its 2021 peak, subsequent annual declines and the flat 2024–2025 comparison. The waterfall is a **reconciliation of annual-level changes**, not a causal attribution.
- Selected funding-round totals and distribution by company, year and funding stage.

Some source-specific OECD.AI metrics (including its published mega-deal share indicator) are retained as sparse benchmarks, **not as independently calculated market-wide mega-round statistics**. No comprehensive deal-level market database exists in this project for deriving global deal counts, market-wide median deal size, market concentration indices or the impact of individual mega-rounds.

## 10. Data engineering and semantic-model design

Python extraction/transformation and validation code prepares source-aware local outputs. The Power BI dataset is loaded from **11 CSV marts: five dimensions and six fact tables**. The model uses **11 active, single-direction one-to-many dimension-to-fact relationships**, with a separate DAX-measures table.

Key design safeguards:

- The OECD `_T` totals and additive stage components are never summed together.
- Source fact tables remain separate even where they share year keys.
- The selected EdTech rounds are not joined or aggregated into the HolonIQ market totals.
- Missing OECD.AI benchmark observations remain blank rather than being fabricated or interpolated.
- Numeric measures remain numeric despite report display formatting.

See [`powerbi_data_model.md`](powerbi_data_model.md) for grains, prerequisites, and model details.

## 11. Data governance, licensing and reproducibility

The public repository contains project code, tests, documentation, manifests and Power BI model/report definitions. Some raw, processed and provider-derived files are maintained **locally and excluded from Git**, consistent with provider-use restrictions and the project's conservative redistribution policy. An initial checkout may therefore **not** be sufficient to reproduce all report values without retrieving approved inputs.

Rebuilding the marts requires five source-specific processed inputs. The Power BI project snapshot also contains **machine-specific absolute CSV paths** that need adjustment before refresh on another computer. Validation results obtained from the local snapshot do not guarantee portability of data refresh from a public clone.

The MIT license applies to the author's original code and documentation and does **not** automatically license third-party underlying data. Dashboard screenshots or extracts reproducing materially restricted provider data should not be published until the applicable reuse conditions are checked.

## 12. Limitations and non-causal interpretation

1. **Coverage and reporting:** OECD country coverage varies across years; complete stage groups cover fewer observations. Recently published numbers may be revised.
2. **Comparability:** OECD, OWID, OECD.AI and HolonIQ differ in source universes, funding definitions, classification and/or price bases. OWID AI/GenAI subset interpretation and the limits of the derived residual are described in Section 4.
3. **Pre/post inference:** Annual periods are convenient descriptive groupings. The 2021 peak and changing coverage can affect averages. Interest rates, valuations, exit markets and other changes are confounders.
4. **Deal-sample bias:** The company-round dataset is selected and non-exhaustive; public announcement availability favors visible transactions. No market-representative inference follows.
5. **EdTech vintage:** HolonIQ's December 2025 estimate is retained consistently instead of mixing numbers from later revised vintages.
6. **Publication rights:** Provider data and certain image reproductions may have redistribution restrictions independent of repository-code licensing.

## 13. Explicitly out of scope for the delivered version

The completed report does **not** implement quarterly US VC analysis, 2026 YTD VC comparisons, comprehensive global deal counts, median or mean deal size across the VC population, HHI market concentration, estimated investment returns, investor rankings, private-company valuations, causal estimates of ChatGPT's impact, or a representative AI-versus-non-AI EdTech funding-share comparison.

These were possible extensions in the original project plan, **not delivered analyses**. Any future extension requires appropriately granular, validated data and an updated methodology.