# Narrative Synthesis Protocols

> Step-by-step methodology guides for non-quantitative evidence synthesis in systematic reviews.

## Protocol: Deciding When Narrative Synthesis Is Appropriate

### When to Use
Determining whether meta-analysis is feasible or whether narrative synthesis is the appropriate approach.

### Steps
1. **Assess clinical/methodological heterogeneity** — do studies differ substantially in populations, interventions, comparators, outcomes, or designs?
2. **Assess statistical heterogeneity** — if a preliminary meta-analysis yields I² > 75% with no plausible explanation, or the prediction interval crosses both benefit and harm
3. **Check outcome reporting** — are effect estimates and variability measures reported consistently enough to pool?
4. **Count available studies** — with fewer than 3 studies for an outcome, meta-analysis may be unreliable
5. **Apply the decision rule** — use narrative synthesis when: (a) studies are too heterogeneous to pool meaningfully, (b) insufficient data for meta-analysis, or (c) the outcome is qualitative
6. **Document the rationale** — explicitly state why quantitative synthesis was not performed for each outcome
7. **Plan the synthesis strategy** — select from the methods below (SWiM, tabulation, grouping, vote counting)

### Common LLM Pitfalls
- Defaulting to narrative synthesis without attempting meta-analysis or explaining why it was infeasible
- Treating narrative synthesis as "just a literature review" rather than a structured synthesis method
- Using narrative synthesis to avoid dealing with heterogeneity that could be explored in subgroup/meta-regression analysis

---

## Protocol: Synthesis Without Meta-Analysis (SWiM) Reporting

### When to Use
Structuring and reporting a narrative synthesis according to the SWiM guideline (Campbell et al. 2020).

### Steps
1. **Item 1: Grouping** — describe how studies were grouped for synthesis (by intervention type, population, outcome, etc.) and justify the grouping
2. **Item 2: Standardized metric** — describe the metric used to compare results across studies (e.g., direction of effect, effect size, p-value)
3. **Item 3: Synthesis method** — describe the method used to synthesize results within each group (vote counting based on direction, combining p-values, structured summary, albatross plots)
4. **Item 4: Reporting the synthesis** — present results for each group with appropriate tables or forest plots without pooled estimates (harvest plots, effect direction plots)
5. **Item 5: Effect heterogeneity** — describe methods used to explore variation in effects (subgrouping, sensitivity analysis)
6. **Item 6: Certainty of evidence** — assess using GRADE (see quality-assessment-protocols.md), noting additional imprecision from not pooling
7. **Item 7: Data presentation** — provide tabular summaries of all included studies with key characteristics and results
8. **Item 8: Limitations** — describe the limitations of the synthesis method and how they might affect the conclusions
9. **Use the SWiM checklist** — ensure all 9 items are addressed in the manuscript

### Common LLM Pitfalls
- Reporting narrative synthesis as unstructured prose without following SWiM items
- Omitting the standardized metric (Item 2), making it impossible to compare across studies
- Not applying GRADE to narrative syntheses (GRADE applies regardless of synthesis method)
- Failing to present individual study results in a structured table

---

## Protocol: Vote Counting Based on Direction of Effect

### When to Use
Synthesizing results when effect sizes cannot be calculated but the direction of effect can be determined for each study.

### Steps
1. **Classify each study result** — positive effect, negative effect, or no evidence of effect, based on the direction of the point estimate (NOT statistical significance)
2. **Count the results** — tally the number of studies in each direction category
3. **Apply a sign test** — test whether the proportion of positive effects differs from 0.5 using a binomial test (H₀: p = 0.5)
4. **Present results** — report the count in each direction, the sign test p-value, and the confidence interval for the proportion
5. **Create an effect direction plot** — visual display of vote counts with study characteristics
6. **Interpret with caution** — vote counting has very low power with few studies and does not account for study size or effect magnitude
7. **Do NOT use statistical significance** as the criterion — a study with p = 0.06 showing benefit should be counted as "positive direction," not "no effect"
8. **Acknowledge limitations** — vote counting cannot estimate the magnitude of effect; it answers only "is there evidence of a consistent direction?"

### Common LLM Pitfalls
- Counting "statistically significant" results instead of direction of effect (this is the classic error that invalidates vote counting)
- Interpreting vote counting as providing strong evidence (it has very low statistical power)
- Confusing vote counting with "box score" reviews that tally significant vs non-significant results
- Not applying a formal sign test (just reporting "3 of 5 studies found a positive effect" without a test)

---

## Protocol: Structured Tabular Synthesis

### When to Use
Organizing and presenting study-level results in tables to facilitate cross-study comparison when narrative synthesis is used.

### Steps
1. **Design the table structure** — one row per study, columns for: study ID, population (N, characteristics), intervention, comparator, outcome measure, effect estimate (or direction), key findings
2. **Order studies meaningfully** — by intervention type, population, date, or another characteristic relevant to the synthesis
3. **Highlight patterns** — use visual indicators (shading, symbols) to draw attention to consistent findings or important differences
4. **Cross-reference with risk of bias** — include a column for overall RoB judgment so readers can weigh evidence quality
5. **Synthesize across rows** — below the table, provide a narrative summary of the patterns observed (e.g., "4 of 6 studies in adults found a positive effect, while both pediatric studies found no effect")
6. **Separate tables by outcome** — one table per outcome to maintain clarity
7. **Include all included studies** — every study that met inclusion criteria must appear, even if it reported no usable numerical data
8. **Use the table to support, not replace, the narrative** — the text should interpret the table, not merely restate it

### Common LLM Pitfalls
- Creating tables with inconsistent columns across studies (all studies should have entries for all columns, even if "NR" for not reported)
- Omitting studies with null results from the table (introduces reporting bias into the synthesis)
- Presenting the table without any accompanying narrative interpretation
- Not aligning the table structure with the SWiM grouping strategy
