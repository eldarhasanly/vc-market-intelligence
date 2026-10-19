# EdTech venture capital: historical benchmark methodology

## Purpose

This pipeline normalizes a **local, source-vintage-specific transcription** of the annual global EdTech venture-capital chart in HolonIQ's *2026 Global Education Outlook*. Its purpose is to evaluate the sector's funding trajectory between 2019 and 2025. It is an **external published benchmark**, not a comprehensive EdTech deal-level dataset.

## Source and version

- **Original provider:** HolonIQ.
- **Primary source:** [2026 Global Education Outlook, Figure 2](https://www.holoniq.com/notes/2026-global-education-outlook).
- **Publication date:** 2025-12-19.
- **Figure title:** Global Education Venture Capital Funding, 2010–2025 in USD billions.
- **Selected years:** 2019–2025 (the project's comparison period).
- **Unit:** nominal USD **billions**, rounded chart labels; historical exchange rates at the time of each funding event.
- **Market:** Global EdTech, according to HolonIQ's coverage and taxonomy; **excludes private equity**.
- **Sampling:** Provider's reported market totals, not totals computed from an independently compiled sample.

### Important: subsequent revisions

A later HolonIQ article, [*EdTech hits $2.6B in investment*](https://www.holoniq.com/notes/edtech-hits-2-6b-in-investment-as-the-market-stabilizes-bigger-bets-in-ai-and-workforce-training), published 2026-02-06, reports **$2.6B for 2025**. The December 2025 outlook reports **$2.4B for 2025**. We retain the December 2025 value in this snapshot and **do not silently replace individual years from a newer report**. A subsequent source-vintage reconciliation should choose a consistent update policy.

## Local reproducibility

1. Obtain the published chart, check year labels and units, and transcribe its 2019–2025 annual labels to `data/raw/edtech/holoniq_2026_outlook_2019_2025_local.csv` with columns `year,edtech_vc_usd_billions`.
2. Run `python src/transform/build_edtech_market.py`.
3. Run `python src/validation/validate_edtech_market.py`.
4. Run `python -m unittest discover -s tests -p "test_*.py"`.

The output is `data/processed/edtech_vc_holoniq_2019_2025_local.csv`. It retains the original reporting unit and adds explicit provenance columns. No currency conversion, inflation adjustment, interpolation, or sector reclassification is performed.

## Source governance

HolonIQ's [terms of service](https://www.holoniq.com/terms-of-service) restrict making platform data public, copying and distributing it without authorization. The original chart may be available on a public research page, but **that alone does not establish rights to publish its underlying dataset**. To minimize redistribution risk, the transcribed inputs and processed observations are **excluded from Git**, while the pipeline, metadata, taxonomy, and synthetic tests are version-controlled. Do not include the data files in a Git release or public report download until permitted use is clarified. Attribute findings and original market data to HolonIQ and link to its publication.

The project should resolve publication rights before distributing dashboard assets that reproduce the chart or a material part of its numerical series. Until then, describe the findings with attribution and share reproducible code; do not redistribute the provider-derived rows.

## Analytical constraints

- Do **not** calculate an EdTech funding share by dividing the HolonIQ series by OECD or OWID funding series. Their coverage and capital types differ.
- Do **not** join this seven-row aggregate series to individual funding-round observations; it would duplicate the aggregate totals.
- Do **not** treat changes around 2022 as causal effects of ChatGPT.
- Do **not** treat missing detail on AI-enabled EdTech, deals, stages, companies, or countries as zero.
- Brighteye's broader **Learning & Work** funding universe must be analyzed separately from HolonIQ's EdTech universe.
- Values are chart-level rounded estimates; derived YoY rates are approximate.

## Follow-on work

Create a source-verified selected company/deal dataset with `source_url`, `announced_date`, `funding_stage`, `amount`, `amount_currency`, `company`, `subsector`, `ai_evidence_url`, and `classification_status`. It must be labelled **selected announced rounds** and must not be used to estimate complete EdTech market totals or a population-wide AI-EdTech funding share.