# EdTech classification rules (v1)

## Classification unit

For future curated deal-level analysis, classify the **primary business of the funded company at the date of the round**. Every manually classified company must be supported by a linked source and an as-of date. This is a project taxonomy and should not be presented as the taxonomy used by HolonIQ or Brighteye.

## Primary sector

Include companies whose main customer-facing service is education, formal instruction, learning assessment, student/teacher workflows, learning management, education administration, or workforce learning. Exclude general-purpose AI infrastructure, generic HR software, recruiting-only software, consulting, or content production where education is not the company's primary offering.

## Mutually exclusive subsectors

| Code | Category | Examples of eligible primary functions |
|---|---|---|
| EARLY | Early childhood | Early learning tools, early childhood administration |
| K12 | K–12 | School platforms, school curriculum, tutoring for school pupils |
| HIGHER | Higher/post-secondary | University learning, degree-pathway technology, student success |
| WORKFORCE | Workforce and corporate learning | Upskilling, skills assessment, corporate L&D |
| LANGUAGE | Language learning | Language instruction and assessment |
| INFRA | Education infrastructure | Education-specific LMS, administration, analytics, assessment infrastructure |
| OTHER | Other or multi-segment EdTech | Education primary; not classifiable more precisely |
| UNKNOWN | Unknown pending review | Insufficient evidence |

Assign a company to one primary subsector for non-overlapping charts. Record secondary activities in optional tags rather than duplicate deal values across categories. If categories overlap (e.g., K–12 language tutoring), apply the company's principal product and customer segment, and record the decision rationale.

## AI-enabled classification is a separate dimension

`ai_status` has three values:

- `VERIFIED_AI`: contemporaneous primary evidence documents meaningful AI-powered functionality in the funded product.
- `NOT_VERIFIED`: reviewed sources do not establish qualifying AI functionality. **Do not label this group "non-AI" without stronger evidence.**
- `UNKNOWN`: evidence not yet reviewed or insufficient.

`genai_status` similarly distinguishes documented generative-AI functionality from unverified or unknown cases; it is a **subset of AI**. A company's marketing use of the letters “AI” by itself is not sufficient. Record `ai_evidence_url` and `ai_evidence_date`, and flag retrospective reclassification risks.

## Funding-event boundaries

A funding-round record should have an announcement date, amount (or missing if undisclosed), currency, company and source URL. Distinguish **venture-equity rounds** from debt, grants, acquisitions and corporate expenditures. Do not count acquisitions as financing rounds. When source articles disagree, document the conflict and favor a primary company/investor announcement.

## Coverage and inference

Future selected-round data are **non-exhaustive**. Charts may rank selected companies or characterize observed case studies, but the sample cannot support claims about global deal counts, sector totals, average round size of the market, or AI's share of all EdTech capital.