"""Convention lock management for systematic review methodology consistency.

Ensures review parameters don't drift across phases.
Adapted from GPD's conventions.py for systematic reviews.
"""

from __future__ import annotations

from typing import Any

from .constants import CONVENTION_FIELDS
from .state import StateEngine, ConventionLock


# -- Convention Field Descriptions ------------------------------------------

CONVENTION_DESCRIPTIONS: dict[str, str] = {
    "research_question": (
        "Structured research question in PICO format: Population (who), "
        "Intervention/Exposure (what), Comparator (versus what), Outcome (measured how). "
        "For diagnostic reviews use PIRD; for etiology use PECO."
    ),
    "inclusion_criteria": (
        "Criteria for including studies: eligible study designs (RCT, cohort, "
        "case-control, cross-sectional), population characteristics, intervention "
        "details, outcome definitions, publication date range, language restrictions."
    ),
    "exclusion_criteria": (
        "Criteria for excluding studies: ineligible designs (case reports, editorials), "
        "population exclusions, intervention exclusions, insufficient reporting, "
        "duplicate populations."
    ),
    "search_databases_and_dates": (
        "Databases to search (PubMed/MEDLINE, Cochrane CENTRAL, Embase, CINAHL, "
        "PsycINFO, Web of Science, Scopus, etc.), date ranges, and access/search dates. "
        "Also grey literature sources (ClinicalTrials.gov, WHO ICTRP, conference proceedings)."
    ),
    "search_strategy": (
        "Full search strategy: free-text terms, MeSH/Emtree subject headings, "
        "Boolean operators (AND, OR, NOT), wildcards/truncation, proximity operators, "
        "field restrictions (title, abstract, all fields). Strategy per database."
    ),
    "quality_assessment_tool": (
        "Tool for assessing risk of bias or study quality: "
        "RoB 2 (randomized trials), ROBINS-I (non-randomized interventions), "
        "Newcastle-Ottawa Scale (observational), JBI Critical Appraisal (various), "
        "QUADAS-2 (diagnostic accuracy), AMSTAR 2 (systematic reviews)."
    ),
    "outcome_definitions": (
        "Primary and secondary outcomes with precise definitions: "
        "measurement instrument/scale, time points, minimal clinically important "
        "difference, how missing data will be handled."
    ),
    "effect_size_measure": (
        "Effect size metric for quantitative synthesis: "
        "OR (odds ratio), RR (risk ratio), HR (hazard ratio), "
        "SMD (standardized mean difference, Hedges' g or Cohen's d), "
        "MD (mean difference), correlation coefficient (r)."
    ),
    "synthesis_method": (
        "Method for combining results: "
        "fixed-effect (Mantel-Haenszel, inverse-variance), "
        "random-effects (DerSimonian-Laird, REML, Hartung-Knapp), "
        "narrative synthesis (SWiM guidance), network meta-analysis."
    ),
    "heterogeneity_assessment": (
        "Methods for assessing between-study heterogeneity: "
        "Cochran's Q test (with threshold), I-squared (with interpretation thresholds: "
        "0-40% low, 30-60% moderate, 50-90% substantial, 75-100% considerable), "
        "tau-squared, prediction intervals."
    ),
    "publication_bias_assessment": (
        "Methods for detecting publication bias: "
        "funnel plot visual inspection, Egger's regression test, "
        "Begg's rank correlation, trim-and-fill method, p-curve analysis, "
        "selection models. Note: requires >= 10 studies for statistical tests."
    ),
    "certainty_of_evidence": (
        "Framework for rating certainty/quality of evidence body: "
        "GRADE (Grading of Recommendations Assessment, Development and Evaluation) "
        "with 5 domains: risk of bias, inconsistency, indirectness, imprecision, "
        "publication bias. Rate as high/moderate/low/very low."
    ),
    "sensitivity_analysis_params": (
        "Pre-specified sensitivity analyses: leave-one-out (influence analysis), "
        "excluding high risk-of-bias studies, fixed vs random-effects comparison, "
        "different effect measures, different inclusion thresholds, "
        "intention-to-treat vs per-protocol."
    ),
    "subgroup_analysis_criteria": (
        "Pre-specified subgroup analyses with rationale: "
        "patient characteristics (age, sex, severity), intervention characteristics "
        "(dose, duration, delivery), study characteristics (design, setting, region). "
        "Limit to 5-6 subgroups to avoid multiplicity."
    ),
}

# -- Convention Validation --------------------------------------------------

# Common valid values for quick validation
CONVENTION_EXAMPLES: dict[str, list[str]] = {
    "quality_assessment_tool": [
        "RoB 2 (Cochrane risk of bias tool for randomized trials)",
        "ROBINS-I (Risk Of Bias In Non-randomised Studies of Interventions)",
        "Newcastle-Ottawa Scale (observational studies)",
        "JBI Critical Appraisal Checklist",
        "QUADAS-2 (diagnostic accuracy studies)",
        "AMSTAR 2 (systematic reviews of interventions)",
    ],
    "effect_size_measure": [
        "OR (odds ratio) with 95% CI",
        "RR (risk ratio) with 95% CI",
        "HR (hazard ratio) with 95% CI",
        "SMD (Hedges' g) with 95% CI",
        "MD (mean difference) with 95% CI",
        "Correlation coefficient (r) with 95% CI",
    ],
    "synthesis_method": [
        "Random-effects (DerSimonian-Laird)",
        "Random-effects (REML with Hartung-Knapp adjustment)",
        "Fixed-effect (Mantel-Haenszel)",
        "Fixed-effect (inverse-variance)",
        "Narrative synthesis (SWiM reporting guideline)",
        "Network meta-analysis (frequentist)",
    ],
    "heterogeneity_assessment": [
        "I-squared + Q-test + tau-squared + prediction intervals",
        "I-squared (thresholds: <25% low, 25-75% moderate, >75% high)",
        "Visual inspection of forest plot + I-squared + prediction intervals",
    ],
    "publication_bias_assessment": [
        "Funnel plot + Egger's test (if >= 10 studies)",
        "Funnel plot + trim-and-fill + Egger's test",
        "P-curve analysis + funnel plot",
    ],
    "certainty_of_evidence": [
        "GRADE (5 domains, Summary of Findings table)",
        "GRADE with GRADE-CERQual (qualitative evidence)",
    ],
}


def get_field_description(field: str) -> str:
    """Get the description for a convention field."""
    return CONVENTION_DESCRIPTIONS.get(field, f"Convention field: {field}")


def get_field_examples(field: str) -> list[str]:
    """Get example values for a convention field."""
    return CONVENTION_EXAMPLES.get(field, [])


def list_all_fields() -> list[dict[str, Any]]:
    """List all convention fields with descriptions and examples."""
    return [
        {
            "field": f,
            "description": get_field_description(f),
            "examples": get_field_examples(f),
        }
        for f in CONVENTION_FIELDS
    ]


def check_conventions(engine: StateEngine) -> dict[str, Any]:
    """Check which conventions are locked and which are missing.

    Returns a report dict with locked, unlocked, and coverage stats.
    """
    state = engine.load()
    locked = {}
    unlocked = []

    for field in CONVENTION_FIELDS:
        if field in state.conventions:
            locked[field] = {
                "value": state.conventions[field].value,
                "locked_by": state.conventions[field].locked_by,
                "rationale": state.conventions[field].rationale,
            }
        else:
            unlocked.append(field)

    return {
        "locked": locked,
        "unlocked": unlocked,
        "coverage": f"{len(locked)}/{len(CONVENTION_FIELDS)}",
        "coverage_pct": round(100 * len(locked) / len(CONVENTION_FIELDS), 1)
        if CONVENTION_FIELDS
        else 100.0,
    }


def diff_conventions(
    engine: StateEngine,
    proposed: dict[str, str],
) -> dict[str, Any]:
    """Compare proposed convention values against current locks.

    Returns conflicts, new fields, and matching fields.
    """
    state = engine.load()
    conflicts = {}
    new_fields = {}
    matching = {}

    for field, proposed_value in proposed.items():
        if field in state.conventions:
            current = state.conventions[field].value
            if current != proposed_value:
                conflicts[field] = {
                    "current": current,
                    "proposed": proposed_value,
                }
            else:
                matching[field] = current
        else:
            new_fields[field] = proposed_value

    return {
        "conflicts": conflicts,
        "new_fields": new_fields,
        "matching": matching,
        "has_conflicts": bool(conflicts),
    }
