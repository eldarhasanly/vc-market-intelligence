# Data

This directory contains the datasets used in this project.

## Structure

### `raw/`
Original source data preserved without analytical transformations.

### `processed/`
Cleaned and standardized datasets used for analysis and Power BI.

Data provenance, licensing, definitions, and download instructions will be documented before datasets are added.

## Data Governance

Not all data used in this project may be redistributed.

The `raw/` directory is intended for local source files and API responses. Proprietary or redistribution-restricted source files must not be committed to Git.

The `processed/` directory may contain derived datasets only when their underlying licences permit redistribution.

Source provenance, licensing, and methodological limitations are documented in `docs/data_sources.md`.

No dataset should be added to the analytical model without a documented source and retrieval method.

## Processed Datasets

### OECD Venture Capital Investment

File:

`processed/oecd_vc_annual_2019_2025.csv`

Source:

OECD Venture Capital Investments (market statistics)

Coverage:

2019–2025

Frequency:

Annual

Unit:

Millions of US dollars, exchange-rate converted

Transformation:

`src/transform/transform_oecd_vc.py`

The processed dataset retains country, business development stage, observation status, unit, and currency metadata from the source dataset.

The combination of country, stage, and year is treated as the analytical key.

The processed dataset is generated from the raw OECD SDMX response and should not be manually edited.

## Data Quality

Processed OECD data are validated using:

`src/validation/validate_oecd_vc.py`

The validation pipeline checks:

- required schema
- analytical-key uniqueness
- missing investment values
- negative investment values
- expected year coverage
- expected business-development stages
- currency and unit consistency
- country-year-stage coverage

Reported total investment is also compared with available stage components as a diagnostic check. Differences are not automatically treated as errors because national reporting methodologies and stage coverage may vary.