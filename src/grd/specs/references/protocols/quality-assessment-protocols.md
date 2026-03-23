# Quality Assessment Protocols

> Step-by-step methodology guides for assessing risk of bias and certainty of evidence.

## Protocol: Risk of Bias 2 (RoB 2) for Randomized Controlled Trials

### When to Use
Assessing risk of bias in individually randomized parallel-group trials or cluster-randomized trials.

### Steps
1. **Define the target trial** — specify the effect of interest: intention-to-treat (assignment) or per-protocol (adherence)
2. **Assess Domain 1: Randomization process** — was the allocation sequence random? Was it concealed? Were there baseline imbalances suggesting problems?
3. **Assess Domain 2: Deviations from intended interventions** — were participants/carers aware of assignment? Were there deviations due to the trial context? Was an appropriate analysis used?
4. **Assess Domain 3: Missing outcome data** — were outcome data available for (nearly) all participants? Could missingness depend on the true value? Were adequate methods used to handle missing data?
5. **Assess Domain 4: Measurement of the outcome** — could the outcome measure have been influenced by knowledge of intervention? Were assessors blinded?
6. **Assess Domain 5: Selection of the reported result** — were multiple outcomes measured? Multiple time points? Multiple analyses? Was the reported result likely selected from among these?
7. **Assign domain-level judgments** — Low risk / Some concerns / High risk for each domain
8. **Derive the overall judgment** — Low risk (all domains low), Some concerns (some concerns in at least one domain, no high risk), High risk (high risk in at least one domain, or some concerns in multiple domains)

### Common LLM Pitfalls
- Conflating lack of blinding with high risk of bias (blinding matters only if outcome assessment could be influenced)
- Assessing risk of bias at the study level rather than the outcome level (RoB 2 is outcome-specific)
- Not specifying whether the assessment targets the ITT or per-protocol effect
- Using the original RoB tool (Cochrane 2011) instead of RoB 2 (2019 revision)

---

## Protocol: ROBINS-I for Non-Randomized Studies

### When to Use
Assessing risk of bias in non-randomized studies of interventions (cohort studies, case-control studies, before-after studies).

### Steps
1. **Specify the target trial** — describe the hypothetical pragmatic randomized trial that the non-randomized study is attempting to emulate
2. **Assess Domain 1: Confounding** — were important confounding domains identified? Were appropriate methods used to control for them?
3. **Assess Domain 2: Selection of participants** — was selection into the study related to both intervention and outcome?
4. **Assess Domain 3: Classification of interventions** — was intervention status well-defined and determined at the start of follow-up?
5. **Assess Domain 4: Deviations from intended interventions** — were there important co-interventions or switches?
6. **Assess Domain 5: Missing data** — were outcome data reasonably complete? Could missingness be related to the true outcome?
7. **Assess Domain 6: Measurement of outcomes** — were outcome assessors blinded to intervention status? Were methods comparable across groups?
8. **Assess Domain 7: Selection of reported result** — as in RoB 2
9. **Assign judgments** — Low / Moderate / Serious / Critical / No information for each domain
10. **Derive overall judgment** — driven by the worst domain-level judgment

### Common LLM Pitfalls
- Assigning "Low risk" for confounding when unmeasured confounders are plausible (this should be at best "Moderate")
- Not specifying the target trial, making the assessment unanchored
- Confusing ROBINS-I (for interventions) with tools for prognostic studies or diagnostic accuracy studies
- Applying RoB 2 domains to non-randomized studies instead of using ROBINS-I

---

## Protocol: Newcastle-Ottawa Scale (NOS)

### When to Use
Quick quality assessment of cohort and case-control studies when ROBINS-I is too resource-intensive.

### Steps
1. **Select the correct version** — cohort NOS or case-control NOS (different items)
2. **Assess Selection** (max 4 stars for cohort, 4 for case-control) — representativeness of exposed cohort, selection of comparator, ascertainment of exposure, outcome not present at start
3. **Assess Comparability** (max 2 stars) — control for the most important factor (1 star) and any additional factor (1 star)
4. **Assess Outcome/Exposure** (max 3 stars) — assessment method, follow-up length and adequacy (cohort) or ascertainment of exposure (case-control)
5. **Sum the stars** — maximum 9 stars; commonly categorized as good (7–9), fair (4–6), poor (0–3)
6. **Report item-level scores**, not just the total — the total can mask important domain-level weaknesses
7. **Pre-specify the thresholds** for each star item in the review protocol

### Common LLM Pitfalls
- Using the cohort version for a case-control study or vice versa
- Awarding comparability stars without specifying which confounders were controlled
- Reporting only the total score without item-level breakdown (obscures specific weaknesses)
- Treating NOS as equivalent in rigor to ROBINS-I (NOS is less comprehensive)

---

## Protocol: GRADE (Grading of Recommendations, Assessment, Development and Evaluations)

### When to Use
Rating the certainty of the body of evidence for each outcome across studies (not individual study quality).

### Steps
1. **Start with the baseline** — RCTs start at High certainty, observational studies start at Low certainty
2. **Assess reasons to rate DOWN** (each can reduce by 1 or 2 levels):
   - **Risk of bias** — serious methodological limitations across studies
   - **Inconsistency** — unexplained heterogeneity in results (I² > 50%, disparate point estimates)
   - **Indirectness** — differences in population, intervention, comparator, or outcome from the review question
   - **Imprecision** — wide confidence intervals crossing the null or clinically important thresholds, small sample size
   - **Publication bias** — funnel plot asymmetry, small-study effects, evidence of suppressed results
3. **Assess reasons to rate UP** (observational studies only):
   - **Large magnitude of effect** — RR > 2 or < 0.5 with no plausible confounders (+1), RR > 5 or < 0.2 (+2)
   - **Dose-response gradient** — clear dose-response relationship
   - **Plausible confounders would reduce the effect** — residual confounding would bias toward the null
4. **Assign final rating** — High, Moderate, Low, or Very Low
5. **Create a Summary of Findings table** — one row per outcome, columns for effect estimate, CI, number of studies, certainty rating, and footnotes explaining each downgrade/upgrade

### Common LLM Pitfalls
- Applying GRADE to individual studies instead of the body of evidence for an outcome
- Rating down for both risk of bias and indirectness when only one applies
- Upgrading RCT evidence (upgrades are only for observational studies starting at Low)
- Not providing explicit footnotes explaining each rating decision in the Summary of Findings table
