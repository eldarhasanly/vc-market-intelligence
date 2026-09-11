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