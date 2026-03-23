# Screening Protocols

> Step-by-step methodology guides for systematic review screening stages.

## Protocol: Title and Abstract Screening

### When to Use
Applying inclusion/exclusion criteria to identify potentially relevant studies from search results.

### Steps
1. **Finalize the eligibility criteria** — define PICOS (Population, Intervention, Comparator, Outcome, Study design) inclusion/exclusion before screening begins
2. **Calibrate screeners** — pilot screen 50–100 records together, discuss disagreements, refine criteria definitions
3. **Apply liberal inclusion** — at title/abstract stage, include any study that might be relevant; exclude only clear irrelevance
4. **Screen independently** — two reviewers screen all records independently; do not discuss individual records during screening
5. **Record decisions** — mark each record as Include, Exclude, or Uncertain with the primary exclusion reason
6. **Resolve conflicts** — compare decisions, discuss disagreements, involve a third reviewer for unresolved conflicts
7. **Compute inter-rater reliability** — calculate Cohen's kappa (κ) on a sample or the full set; report in the methods
8. **Document the yield** — record the number screened, included, excluded (by reason) for the PRISMA flow diagram

### Common LLM Pitfalls
- Applying overly strict criteria at the title/abstract stage (should err on inclusion)
- Fabricating kappa values instead of computing them from actual agreement data
- Failing to specify exclusion reasons for each excluded record
- Confusing sensitivity (finding all relevant studies) with specificity (excluding irrelevant ones) — screening prioritizes sensitivity

---

## Protocol: Full-Text Review

### When to Use
Evaluating the complete text of studies that passed title/abstract screening against detailed eligibility criteria.

### Steps
1. **Obtain full texts** — retrieve PDFs/HTML for all included records; document any that could not be obtained
2. **Apply eligibility criteria systematically** — check each PICOS element against the full text
3. **Record the specific exclusion reason** — use a single primary reason per excluded study (hierarchy: wrong population > wrong intervention > wrong comparator > wrong outcome > wrong design)
4. **Screen independently** — two reviewers assess each full text; disagreements resolved by discussion or third reviewer
5. **Contact authors** if eligibility is unclear from the published text — document all correspondence
6. **Handle multiple reports of one study** — link publications from the same study, designate a primary report
7. **Update the PRISMA flow diagram** — record full texts assessed, excluded (with reasons), and included in synthesis
8. **Compute full-text kappa** — inter-rater reliability at this stage is typically higher than title/abstract (κ > 0.80 expected)

### Common LLM Pitfalls
- Listing multiple exclusion reasons per study instead of one primary reason
- Failing to identify duplicate publications of the same study
- Not documenting studies that could not be retrieved
- Applying criteria inconsistently across reviewers (calibration drift)

---

## Protocol: Inter-Rater Reliability (Kappa)

### When to Use
Quantifying agreement between two or more independent screeners or raters.

### Steps
1. **Construct the 2×2 agreement table** — rows = Reviewer 1 decisions, columns = Reviewer 2 decisions
2. **Compute observed agreement** P_o = (a + d) / N, where a = both include, d = both exclude
3. **Compute expected agreement** P_e = P(both include by chance) + P(both exclude by chance)
4. **Calculate kappa** κ = (P_o − P_e) / (1 − P_e)
5. **Interpret the value** — poor (<0.00), slight (0.00–0.20), fair (0.21–0.40), moderate (0.41–0.60), substantial (0.61–0.80), almost perfect (0.81–1.00) (Landis & Koch)
6. **For >2 raters**: use Fleiss' kappa or Krippendorff's alpha
7. **Report prevalence and bias indices** — kappa is affected by prevalence; PABAK (prevalence-adjusted bias-adjusted kappa) may be informative
8. **If κ < 0.60**: re-calibrate, revise criteria definitions, and re-screen a sample before proceeding

### Common LLM Pitfalls
- Computing percent agreement instead of kappa (percent agreement ignores chance)
- Applying Cohen's kappa to more than two raters (requires Fleiss' kappa)
- Ignoring the kappa paradox — high agreement can yield low kappa when prevalence is extreme
- Not reporting the number of records on which kappa was calculated

---

## Protocol: PRISMA Flow Diagram Construction

### When to Use
Documenting and reporting the flow of studies through identification, screening, eligibility, and inclusion.

### Steps
1. **Identification box** — report total records from each database, registers, and other sources; report duplicates removed
2. **Screening box** — records screened (title/abstract), records excluded
3. **Eligibility box** — full-text articles assessed, full-text articles excluded with reasons (tabulate each reason and count)
4. **Included box** — studies included in qualitative synthesis, studies included in quantitative synthesis (meta-analysis) if applicable
5. **Report previous studies** — for updated reviews, include studies from prior version
6. **Use the PRISMA 2020 template** — includes separate flows for databases/registers and other sources
7. **Ensure numbers reconcile** — each level's included + excluded must equal the input from the level above
8. **Include the diagram in the manuscript** — typically as Figure 1; reference the PRISMA 2020 statement

### Common LLM Pitfalls
- Using the outdated PRISMA 2009 template instead of the 2020 version
- Numbers not adding up between screening stages (arithmetic errors in flow)
- Omitting exclusion reasons at the full-text stage
- Forgetting to report records identified from sources other than databases (citation searching, grey literature)
