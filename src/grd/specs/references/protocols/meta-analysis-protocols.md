# Meta-Analysis Protocols

> Step-by-step methodology guides for conducting quantitative evidence synthesis.

## Protocol: Fixed-Effect vs Random-Effects Decision

### When to Use
Deciding which meta-analysis model to use.

### Decision Framework
1. **Clinical question**: Are all studies estimating the same underlying effect?
   - If YES (identical populations, interventions, outcomes) → consider **fixed-effect**
   - If NO (some variation expected) → use **random-effects**
2. **Statistical assessment**:
   - I-squared < 40% AND Q-test p > 0.10 → fixed-effect may be appropriate
   - I-squared > 40% → random-effects strongly preferred
3. **Number of studies**:
   - Few studies (< 5): random-effects may be unstable; consider Hartung-Knapp adjustment
   - Many studies (>= 10): both models feasible
4. **Default**: random-effects (DerSimonian-Laird or REML) unless strong justification for fixed-effect

### Common LLM Pitfalls
- Using fixed-effect when I-squared is high (E003)
- Ignoring that random-effects gives wider CIs with few studies
- Not reporting prediction intervals alongside random-effects estimates
- Using DerSimonian-Laird without Hartung-Knapp when k < 10

---

## Protocol: Effect Size Calculation from Reported Data

### When to Use
Calculating study-level effect sizes from various reporting formats.

### For Dichotomous Outcomes (OR, RR)
1. **From 2x2 table**: Direct calculation
2. **From event rates + N**: Reconstruct 2x2 table
3. **From OR/RR + CI**: Extract log(OR/RR) and SE from CI width
4. **From p-value + N**: Convert via standard normal distribution (last resort)

### For Continuous Outcomes (SMD, MD)
1. **From mean + SD + N per group**: Direct calculation
2. **From mean difference + CI**: SE = (upper - lower) / (2 * 1.96)
3. **From median + IQR**: Use Wan et al. (2014) method to estimate mean and SD
4. **From median + range**: Use Hozo et al. (2005) method
5. **From change scores**: Use change-from-baseline means and SDs
6. **From p-value + N**: Convert via t-distribution (last resort)

### Hedges' g Correction
- Apply Hedges' correction factor J = 1 - 3/(4*df - 1) for small sample sizes
- df = n1 + n2 - 2

### Common LLM Pitfalls
- Using SD where SE is needed (or vice versa) (E002, E007)
- Not applying Hedges' correction for small studies
- Mixing change scores and final values without adjustment
- Double-counting control groups in multi-arm trials

---

## Protocol: Heterogeneity Assessment

### When to Use
After every meta-analysis, before interpreting pooled results.

### Steps
1. **Visual inspection of forest plot**
   - Do confidence intervals overlap?
   - Is the pattern consistent or scattered?
2. **Cochran's Q test**
   - H0: all studies share common effect
   - Use alpha = 0.10 (low power with few studies)
   - Report Q statistic, df, and p-value
3. **I-squared statistic**
   - I-squared = (Q - df)/Q * 100%
   - Thresholds (Cochrane): 0-40% low, 30-60% moderate, 50-90% substantial, 75-100% considerable
   - Note: overlapping ranges are intentional (context matters)
4. **Tau-squared**
   - Absolute between-study variance
   - Useful for prediction intervals
5. **Prediction interval**
   - Range where 95% of true effects in future settings would fall
   - Much wider than CI of pooled estimate
   - MUST report for random-effects models
6. **If heterogeneity is substantial (I-squared > 50%)**:
   - Explore sources via subgroup analysis or meta-regression
   - Consider whether pooling is appropriate
   - Report narrative synthesis if pooling is inappropriate

### Common LLM Pitfalls
- Interpreting I-squared as a measure of absolute heterogeneity (it's relative)
- Ignoring high heterogeneity and reporting pooled estimate without caveat (E003)
- Using Q-test p-value as sole indicator (low power with few studies)
- Not reporting prediction intervals

---

## Protocol: Publication Bias Assessment

### When to Use
When meta-analysis includes >= 10 studies for a given outcome.

### Steps
1. **Funnel plot**
   - X-axis: effect size, Y-axis: SE (inverted) or precision
   - Symmetric funnel → no evidence of bias
   - Asymmetric → possible bias (but other explanations exist)
2. **Egger's regression test** (for continuous outcomes)
   - Regresses standardized effect against precision
   - p < 0.10 suggests asymmetry
3. **Peters' test** (for binary outcomes with OR)
   - More appropriate than Egger's for odds ratios
4. **Trim-and-fill**
   - Imputes "missing" studies and recalculates pooled estimate
   - Report both original and adjusted estimates
5. **Sensitivity analysis**
   - If bias detected: how much would results change?
   - Selection models (Vevea-Hedges) for formal adjustment
6. **Report limitations**
   - Funnel plot asymmetry does not prove publication bias
   - Could be: true heterogeneity, chance, methodological differences

### Common LLM Pitfalls
- Conducting Egger's test with < 10 studies (unreliable)
- Interpreting funnel plot asymmetry as definitive proof of bias
- Not discussing alternative explanations for asymmetry
- Forgetting to report trim-and-fill adjusted estimate

---

## Protocol: GRADE Assessment

### When to Use
Rating certainty of evidence for each critical/important outcome.

### Steps (per outcome)
1. **Start at HIGH certainty** for RCTs, **LOW** for observational studies
2. **Consider downgrading** (5 domains):
   a. **Risk of bias**: Serious concerns across studies → downgrade 1-2 levels
   b. **Inconsistency**: Unexplained heterogeneity (I-squared > 50%, prediction interval crosses null) → downgrade
   c. **Indirectness**: PICO mismatch between evidence and question → downgrade
   d. **Imprecision**: Wide CI crossing clinical decision threshold, OIS not met → downgrade
   e. **Publication bias**: Strong suspicion from funnel plot/tests → downgrade
3. **Consider upgrading** (observational only, 3 domains):
   a. Large effect (RR > 2 or < 0.5 with no confounders)
   b. Dose-response gradient
   c. Residual confounding would reduce effect
4. **Assign final rating**: High / Moderate / Low / Very Low
5. **Document rationale** for each domain decision
6. **Create Summary of Findings table**

### Certainty-to-Language Mapping
- **High**: "X results in Y" / "X does Y"
- **Moderate**: "X probably results in Y"
- **Low**: "X may result in Y"
- **Very Low**: "The evidence is very uncertain about the effect of X on Y"

### Common LLM Pitfalls
- Starting observational studies at HIGH instead of LOW (E011)
- Not downgrading for imprecision when OIS not met
- Downgrading twice for the same issue (e.g., once for heterogeneity in meta-analysis, again in GRADE inconsistency)
- Overstating conclusions relative to certainty level (E014)
