# Data Extraction Protocols

> Step-by-step methodology guides for systematic review data extraction.

## Protocol: Extraction Form Design

### When to Use
Creating a standardized form to collect data from included studies before synthesis.

### Steps
1. **Derive fields from the review question** — map each PICOS element to specific extraction fields
2. **Include study identifiers** — author, year, journal, country, funding source, registration number
3. **Include population fields** — sample size, demographics, inclusion/exclusion criteria, setting
4. **Include intervention/exposure fields** — type, dose, duration, frequency, delivery method, co-interventions
5. **Include outcome fields** — primary/secondary outcomes, measurement instruments, time points, effect estimates (mean, SD, OR, RR, HR), confidence intervals, p-values
6. **Include quality/risk-of-bias fields** — domain-level judgments (see quality-assessment-protocols.md)
7. **Pilot the form** — extract from 3–5 studies, refine fields for clarity and completeness
8. **Specify the data management tool** — Covidence, RevMan, Excel, or REDCap with locked fields for completed extractions

### Common LLM Pitfalls
- Including so many fields that extraction becomes unreliable (prioritize fields needed for synthesis)
- Omitting fields for effect size calculation (need both point estimate AND variability measure)
- Not specifying units for continuous outcomes
- Forgetting to include a free-text "notes" field for unexpected findings

---

## Protocol: Coding Rules and Decision Rules

### When to Use
Standardizing how extractors handle ambiguous, incomplete, or inconsistent reporting in primary studies.

### Steps
1. **Define each variable precisely** — provide operational definitions, not just labels (e.g., "age" = mean age at enrollment, not age at diagnosis)
2. **Specify the hierarchy for multiple reports** — if a study has several publications, define which takes precedence for each variable
3. **Handle multiple time points** — pre-specify which time point(s) to extract (e.g., longest follow-up, closest to 12 months)
4. **Handle multiple effect measures** — specify preference order (e.g., adjusted OR > unadjusted OR > raw counts)
5. **Code categorical variables** — provide the coding scheme with explicit categories and rules for edge cases
6. **Handle subgroups** — extract overall results by default; extract subgroups only if pre-specified in the protocol
7. **Document all decision rules** in a codebook accompanying the extraction form
8. **Update rules iteratively** — when new ambiguities arise, resolve them, add to the codebook, and back-check previous extractions

### Common LLM Pitfalls
- Making ad hoc decisions during extraction instead of following pre-specified rules
- Extracting adjusted and unadjusted estimates inconsistently across studies
- Failing to back-check earlier extractions when decision rules are updated
- Not distinguishing between "not reported" and "zero" for missing data

---

## Protocol: Handling Missing Data in Extraction

### When to Use
Deciding how to handle outcomes, effect sizes, or study characteristics that are not reported or partially reported.

### Steps
1. **Distinguish types of missing data** — not measured, measured but not reported, reported incompletely (e.g., "p < 0.05" without the estimate)
2. **Contact study authors** — email corresponding authors for missing numerical data; allow 2–4 weeks, send one reminder
3. **Compute from available data** — derive SD from SE (SD = SE × √n), CI, p-value, or interquartile range using validated formulas (Wan et al. 2014, Luo et al. 2018)
4. **Extract from figures** — use digitization tools (WebPlotDigitizer) for Kaplan-Meier curves or bar charts; report that data were extracted from figures
5. **Code the data source** — mark each extracted value as "reported directly," "calculated," "digitized from figure," or "obtained from authors"
6. **Do NOT impute** in the extraction stage — imputation is a sensitivity analysis decision, not an extraction decision
7. **Document all transformations** — record the original reported values and the formula used to derive the extracted value
8. **Assess the impact** — in sensitivity analysis, compare results with and without studies that required extensive derivation

### Common LLM Pitfalls
- Inventing plausible-sounding data to fill gaps instead of coding as missing
- Using incorrect SD ↔ SE conversion (forgetting to multiply/divide by √n)
- Digitizing survival curves without accounting for censoring
- Not recording whether extracted values were reported directly or derived

---

## Protocol: Double Extraction and Discrepancy Resolution

### When to Use
Ensuring accuracy and reliability of extracted data through independent dual extraction.

### Steps
1. **Both extractors extract independently** — no discussion of individual studies during extraction
2. **Compare all fields** — use a discrepancy detection tool or side-by-side comparison spreadsheet
3. **Classify discrepancies** — transcription error (typo), interpretation error (different reading of the source), or judgment difference (ambiguous reporting)
4. **Resolve by consensus** — both extractors review the source together for factual discrepancies
5. **Involve a third reviewer** — for unresolved disagreements, especially judgment-based ones
6. **Compute extraction agreement** — report percent agreement or kappa for key variables
7. **If resources are limited**: extract all studies once, then have the second reviewer verify a random 20–30% sample; if error rate is >5%, re-verify all
8. **Lock the dataset** — once discrepancies are resolved, lock the extraction database before analysis begins

### Common LLM Pitfalls
- Having one extractor check the other's work instead of true independent dual extraction
- Not resolving discrepancies before proceeding to synthesis
- Failing to document how discrepancies were resolved
- Assuming high agreement on study characteristics means outcomes were also extracted correctly (check separately)
