# Get Review Done

> An AI copilot for autonomous systematic literature reviews and meta-analyses — from research question to PRISMA-compliant publication.

**Inspired by [Get Physics Done](https://github.com/psi-oss/get-physics-done)** — the open-source AI copilot that autonomously conducts physics research. Get Review Done adapts GPD's architecture for systematic reviews, the gold standard of evidence synthesis in medicine, social science, and policy.

## Vision

Systematic reviews are the most rigorous form of literature synthesis, but they're notoriously labor-intensive — a typical Cochrane review takes 12-18 months. The methodology is highly standardized (PRISMA 2020, Cochrane Handbook, GRADE framework), making it an ideal target for AI automation with rigorous guardrails.

Get Review Done wraps LLM capabilities in a verification-first framework that:
- **Locks review parameters** across phases (search strategy, inclusion/exclusion criteria, quality assessment tools, outcome definitions, effect size measures)
- **Follows established standards** — PRISMA 2020 checklist, Cochrane methodology, GRADE certainty assessment
- **Decomposes reviews** into standard phases: protocol registration → search → screening → extraction → quality assessment → synthesis → GRADE assessment → manuscript
- **Maintains audit trails** — every screening decision, every extraction, every quality judgment is logged and reproducible

## Architecture

Adapted from GPD's three-layer design:

### Layer 1 — Core Library (Python)
State management, phase lifecycle, git operations, convention locks, verification kernel.

### Layer 2 — MCP Servers
- `grd-state` — Project state queries
- `grd-conventions` — Review parameter lock management
- `grd-protocols` — Methodology protocols (search strategy, screening, extraction, meta-analysis methods)
- `grd-patterns` — Cross-review learned patterns
- `grd-verification` — PRISMA compliance and methodological rigor checks
- `grd-errors` — Known LLM systematic review failure modes

### Layer 3 — Agents & Commands
- `grd-planner` — Review protocol development and task planning
- `grd-executor` — Primary search, screening, and extraction execution
- `grd-verifier` — Methodological rigor and PRISMA compliance verification
- `grd-researcher` — Database search and source discovery
- `grd-statistician` — Meta-analysis and statistical synthesis
- `grd-paper-writer` — PRISMA-compliant manuscript generation
- `grd-referee` — Methodological peer review panel

## Convention Lock Fields

Review-specific parameter consistency:
1. Research question (PICO/PECO format)
2. Inclusion criteria (population, intervention, comparator, outcome, study design)
3. Exclusion criteria
4. Search databases and date ranges
5. Search strategy (terms, Boolean operators, MeSH/keywords)
6. Quality assessment tool (RoB 2, ROBINS-I, Newcastle-Ottawa, etc.)
7. Outcome definitions and measurement
8. Effect size measure (OR, RR, SMD, MD, etc.)
9. Synthesis method (fixed-effect, random-effects, narrative)
10. Heterogeneity assessment method
11. Publication bias assessment method
12. Certainty of evidence framework (GRADE)
13. Sensitivity analysis parameters
14. Subgroup analysis criteria

## Verification Framework

1. **PRISMA compliance** — all 27 checklist items addressed
2. **Search reproducibility** — strategies executable, databases specified, dates recorded
3. **Screening consistency** — inter-rater agreement, decision audit trail
4. **Extraction completeness** — all pre-specified outcomes extracted
5. **Quality assessment validity** — tool appropriate for study design, all domains assessed
6. **Statistical validity** — correct model choice, heterogeneity assessed, confidence intervals reported
7. **Publication bias** — funnel plot, Egger's test, trim-and-fill (when ≥10 studies)
8. **GRADE assessment** — all five domains evaluated per outcome
9. **Sensitivity analysis** — pre-specified analyses completed
10. **Narrative consistency** — abstract matches results, conclusions supported by evidence
11. **Registration consistency** — deviations from protocol documented
12. **Citation accuracy** — all cited studies exist and are correctly characterized

## Status

**Early development** — Building core infrastructure. Contributions welcome!

## Relationship to GPD

This project reuses GPD's domain-agnostic infrastructure and replaces physics-specific components with systematic review methodology. The wave-based execution maps naturally: Wave 1 = search, Wave 2 = screening, Wave 3 = extraction, Wave 4 = quality assessment, Wave 5 = synthesis, Wave 6 = manuscript.

We plan to showcase this in the [GPD Discussion Show & Tell](https://github.com/psi-oss/get-physics-done/discussions) once operational.

## Getting Started

```bash
# Coming soon
npx get-review-done
```

## Contributing

We're looking for contributors with:
- Experience conducting systematic reviews or meta-analyses
- Knowledge of PRISMA, Cochrane methodology, or GRADE
- Statistical meta-analysis expertise (R/Python)
- Familiarity with GPD's architecture

See the [Issues](../../issues) for specific tasks.

## License

MIT
