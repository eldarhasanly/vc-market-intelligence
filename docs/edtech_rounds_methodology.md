# Curated AI-enabled EdTech funding rounds: methodology

## Purpose

This is a **purposefully selected case-study sample**, not a random, exhaustive, or statistically representative sample of EdTech financing. It exists to demonstrate source-backed deal-level ETL, dimensional modeling, and investment-round analysis. **Do not calculate global EdTech market shares or market-wide pre/post funding changes from these rows.**

## Data sources and inclusion criteria

Each row describes a separately announced round backed by a linked **company or company-issued announcement**. Sources are recorded at the **individual-round level** in `src/config/edtech_verified_rounds_2022_2025.json`. They are not scraped, and no copyrighted article text or proprietary investment-database extracts are redistributed.

- Inclusion: an educational or workforce-learning product with documented AI functionality at the time of the announcement; distinct, explicitly reported funding round amount; USD denomination; date and stage verifiable from the original article (with `Unspecified` used when stage isn't stated).
- Coverage: 2022–2025; currently a small set of US-based company announcements that is strongly weighted toward 2024–2025. Missing 2019–2021 rows do **not** imply zero funding.
- Time: `source_publication_date` represents publication date, **not** verified close date. A funding round can be announced later than its actual close.
- Currency: numeric USD millions, **nominal at announcement**, not constant-2021 dollars. No exchange-rate conversion is attempted.
- Funding amount: only the newly announced round. Never add `total raised to date`, acquisition values, or valuation figures into the funding total. Example: Brisk's 2024 $5M seed funding should **not** be mistaken for the $6.9M cumulative figure in its announcement.
- Stages: the original series label is preserved. `Series B-2` and `Series B-3` are distinct financing events, not repeats of the initial Series B; `Unspecified` isn't forced into `Seed`.
- AI classification: `AI-native` means the product is principally positioned as AI-driven; `AI-enabled` means AI is a feature of a broader learning solution. This is an analyst-defined distinction, **not a validated provider taxonomy**. The URL used for role evidence is included.
- Geography: intentionally excluded until company-level geography is consistently verified. Do not interpret company location as location of capital use or customers.
- Period: quarterly transition applies to Q4 2022, as in `docs/project_scope.md`; the Speak November 2022 round is tagged `Transition`.

## Pipeline

```powershell
python src/transform/build_edtech_rounds.py
python -m src.validation.validate_edtech_rounds
python -m unittest discover -s tests -p "test_*.py" -v
```

Source manifest: `src/config/edtech_verified_rounds_2022_2025.json`

Output: `data/processed/edtech_verified_rounds_2022_2025.csv`

The CSV is a **derived table** of minimal funding facts, classifications, and URLs. It can be committed with attribution; original third-party webpage text and images are not reproduced. Always check source website terms before expanding the dataset or automating extraction.

## Valid comparisons and limitations

Appropriate: describe financing rounds for the **selected companies**, visualize their sequence, inspect their stage mix, annotate transactions, and compare the exact companies included in the case-study sample.

Inappropriate: extrapolate to global EdTech funding or deal count; divide sample AI funding by HolonIQ EdTech totals to calculate a market share; conclude the post-GPT AI-EdTech universe has grown because most selected companies were founded recently; infer company financial performance or investment returns.

**Future extensions:** Add non-AI comparator companies under a documented selection framework, independently validate country/stage, normalize funding currencies using a documented FX source, capture recurring investor-company relationships, and only then build more extensive sector concentration analysis.