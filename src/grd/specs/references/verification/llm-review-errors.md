# Known LLM Systematic Review Failure Modes

> This catalog documents systematic failure patterns of LLMs in literature review and meta-analysis.
> The verifier and plan-checker cross-reference against these patterns.

## Critical Errors (High Frequency)

### E001: Missing Relevant Studies from Incomplete Search
**Pattern**: LLM generates search strategies that miss key studies due to insufficient synonyms, missing MeSH terms, or overly narrow Boolean logic.
**Example**: Searching only "cognitive behavioral therapy" but missing "CBT", "cognitive behaviour therapy", "cognitive restructuring".
**Guard**: Use established search filters. Test strategy against known relevant studies (sensitivity check). Include multiple synonyms, spelling variants, and controlled vocabulary terms.

### E002: Incorrect Effect Size Calculations
**Pattern**: LLM miscalculates effect sizes from reported statistics, especially when converting between different formats.
**Example**: Computing SMD from medians as if they were means, or using total N instead of per-group n for standard error.
**Guard**: Verify effect size calculations against at least two independent methods. Show all intermediate steps. Cross-check with calculator tools.

### E003: Inappropriate Pooling of Heterogeneous Studies
**Pattern**: LLM pools studies that are too clinically or methodologically diverse, producing meaningless summary estimates.
**Example**: Meta-analyzing studies with different outcome measures, timepoints, or fundamentally different interventions.
**Guard**: Explicitly assess clinical and methodological heterogeneity BEFORE statistical pooling. If I-squared > 75%, question whether pooling is appropriate.

### E004: Misclassified Study Designs
**Pattern**: LLM incorrectly classifies study designs, leading to wrong risk of bias tools and inappropriate synthesis.
**Example**: Classifying a quasi-experimental study as an RCT, or a cross-sectional study as a cohort study.
**Guard**: Check randomization method, allocation concealment, and follow-up to verify RCT status. Look for explicit design statements by study authors.

### E005: Cherry-Picking Studies for Inclusion
**Pattern**: LLM inconsistently applies inclusion criteria, including studies that support the expected conclusion while excluding similar studies that don't.
**Example**: Including a small positive study while excluding a similarly-sized negative study for a vaguely cited "quality" reason.
**Guard**: Apply inclusion criteria blinded to results. Document every exclusion reason. Track whether excluded studies differ systematically from included ones.

## Serious Errors (Medium Frequency)

### E006: Incorrect Risk of Bias Assessments
**Pattern**: LLM assigns low risk of bias without sufficient evidence, or applies wrong domains for the study design.
**Example**: Rating selection bias as "low risk" when the study does not describe allocation concealment.
**Guard**: Require explicit evidence from the study text for each domain judgment. "Not reported" should default to "unclear" or "high" risk, not "low".

### E007: Statistical Errors in Meta-Analysis
**Pattern**: LLM makes errors in weight calculations, variance estimation, or model specification.
**Example**: Using standard deviation where standard error is needed, double-counting multi-arm trials, incorrect df for Hartung-Knapp adjustment.
**Guard**: Verify that forest plot weights sum to 100%. Check that fixed-effect and random-effects give identical results when I-squared = 0. Verify degrees of freedom.

### E008: Failing to Report Negative/Null Results
**Pattern**: LLM emphasizes statistically significant results while downplaying or omitting null findings.
**Example**: Reporting subgroup analyses that reach significance while not reporting the overall non-significant result.
**Guard**: Report ALL pre-specified outcomes regardless of significance. State the primary outcome result in the abstract even if null. Avoid selective emphasis.

### E009: PRISMA Flow Diagram Arithmetic Errors
**Pattern**: Numbers in the PRISMA flow diagram don't add up — studies appear or disappear between stages.
**Example**: 500 screened, 50 excluded at title/abstract, but 400 (not 450) proceed to full-text.
**Guard**: Verify: identified - duplicates = screened. Screened - excluded = full-text assessed. Full-text - excluded (with reasons) = included.

### E010: Fabricated or Hallucinated Study Data
**Pattern**: LLM generates plausible-looking but incorrect study characteristics, sample sizes, or results.
**Example**: Stating a study had n=245 when it actually had n=124, or attributing results from one study to another.
**Guard**: Every extracted datum must include the specific page/table/figure reference from the source study. Cross-verify a sample of extractions against original papers.

## Moderate Errors (Common but Usually Caught)

### E011: Incorrect GRADE Domain Ratings
**Pattern**: LLM rates GRADE domains without applying standard decision rules.
**Example**: Not downgrading for imprecision when the optimal information size is not met, or downgrading for inconsistency based solely on a non-significant Q-test.
**Guard**: Apply GRADE guidance documents for each domain. Document the specific reason for each rating decision.

### E012: Missing Sensitivity Analyses
**Pattern**: LLM reports only the primary analysis without conducting pre-specified sensitivity analyses.
**Example**: Not conducting leave-one-out analysis, or not comparing fixed vs random-effects results.
**Guard**: Create a checklist of pre-specified sensitivity analyses at protocol stage. Verify all are conducted and reported.

### E013: Confusing Within-Study and Between-Study Comparisons
**Pattern**: LLM draws conclusions about between-study differences from within-study subgroup data, or vice versa.
**Example**: Concluding that Drug A is better than Drug B based on separate meta-analyses of each, without a head-to-head network meta-analysis.
**Guard**: Use interaction tests for subgroup comparisons. Clearly distinguish direct and indirect evidence.

### E014: Overstating Conclusions Relative to Evidence Certainty
**Pattern**: LLM draws strong conclusions from low or very low certainty evidence.
**Example**: "Drug X is effective" when GRADE certainty is "very low" — should be "Drug X may be effective, but the evidence is very uncertain."
**Guard**: Match conclusion language to GRADE certainty level (high: "is/does", moderate: "probably", low: "may", very low: "very uncertain whether").

### E015: Duplicate Study Population Counting
**Pattern**: LLM includes multiple publications from the same study as independent studies in meta-analysis.
**Example**: Including both the 6-month and 12-month reports of the same RCT as separate studies, double-counting participants.
**Guard**: Check author lists, study registration numbers, recruitment sites and dates, and sample sizes for overlap. Link multiple reports to single studies.

## How to Use This Catalog

1. **Plan-checker**: Before execution, identify tasks where specific errors are likely. Add explicit guards.
2. **Executor**: Consult relevant entries when performing work of that type. Follow guards.
3. **Verifier**: After execution, cross-reference results against applicable error patterns.
4. **Pattern library**: When a new error pattern is discovered, add it here.
