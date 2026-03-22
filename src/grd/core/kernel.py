"""Content-addressed verification kernel.

Runs 12 PRISMA/methodology predicates over evidence registries and produces SHA-256 verdicts.
Adapted from GPD's kernel.py for systematic review and meta-analysis verification.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable

from .constants import VERIFICATION_CHECKS, SEVERITY_CRITICAL, SEVERITY_MAJOR, SEVERITY_MINOR, SEVERITY_NOTE


class Severity(str, Enum):
    CRITICAL = SEVERITY_CRITICAL
    MAJOR = SEVERITY_MAJOR
    MINOR = SEVERITY_MINOR
    NOTE = SEVERITY_NOTE


@dataclass
class CheckResult:
    """Result of a single verification check."""

    check_id: str
    name: str
    status: str  # PASS | FAIL | SKIP | WARN
    severity: Severity
    message: str = ""
    evidence: dict[str, Any] = field(default_factory=dict)
    suggestions: list[str] = field(default_factory=list)


@dataclass
class Verdict:
    """Complete verification verdict with content-addressed hashes."""

    registry_hash: str
    predicates_hash: str
    verdict_hash: str
    overall: str  # PASS | FAIL | PARTIAL
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    results: dict[str, CheckResult] = field(default_factory=dict)
    summary: str = ""

    @property
    def critical_failures(self) -> list[CheckResult]:
        return [
            r
            for r in self.results.values()
            if r.status == "FAIL" and r.severity == Severity.CRITICAL
        ]

    @property
    def major_failures(self) -> list[CheckResult]:
        return [
            r
            for r in self.results.values()
            if r.status == "FAIL" and r.severity == Severity.MAJOR
        ]

    @property
    def all_failures(self) -> list[CheckResult]:
        return [r for r in self.results.values() if r.status == "FAIL"]

    @property
    def pass_count(self) -> int:
        return sum(1 for r in self.results.values() if r.status == "PASS")

    @property
    def fail_count(self) -> int:
        return sum(1 for r in self.results.values() if r.status == "FAIL")

    def to_dict(self) -> dict[str, Any]:
        return {
            "registry_hash": self.registry_hash,
            "predicates_hash": self.predicates_hash,
            "verdict_hash": self.verdict_hash,
            "overall": self.overall,
            "timestamp": self.timestamp,
            "summary": self.summary,
            "results": {
                k: {
                    "check_id": v.check_id,
                    "name": v.name,
                    "status": v.status,
                    "severity": v.severity.value,
                    "message": v.message,
                    "evidence": v.evidence,
                    "suggestions": v.suggestions,
                }
                for k, v in self.results.items()
            },
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


# -- Predicate Type ---------------------------------------------------------

# A predicate takes an evidence registry and returns a CheckResult
Predicate = Callable[[dict[str, Any]], CheckResult]


# -- Built-in Systematic Review Predicates ----------------------------------

def check_prisma_compliance(evidence: dict[str, Any]) -> CheckResult:
    """Check adherence to PRISMA 2020 27-item checklist."""
    prisma_items_reported = evidence.get("prisma_items_reported", [])
    prisma_items_missing = evidence.get("prisma_items_missing", [])
    total_items = 27

    if not prisma_items_reported and not prisma_items_missing:
        return CheckResult(
            check_id="prisma_compliance",
            name="PRISMA Compliance",
            status="SKIP",
            severity=Severity.CRITICAL,
            message="No PRISMA checklist data provided.",
        )

    reported_count = len(prisma_items_reported)
    if prisma_items_missing:
        return CheckResult(
            check_id="prisma_compliance",
            name="PRISMA Compliance",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"Missing {len(prisma_items_missing)} of {total_items} PRISMA items.",
            evidence={"missing_items": prisma_items_missing},
            suggestions=[f"Address missing PRISMA item: {item}" for item in prisma_items_missing[:5]],
        )

    return CheckResult(
        check_id="prisma_compliance",
        name="PRISMA Compliance",
        status="PASS",
        severity=Severity.CRITICAL,
        message=f"All {reported_count} PRISMA items addressed.",
    )


def check_search_reproducibility(evidence: dict[str, Any]) -> CheckResult:
    """Check that search strategies are fully reproducible."""
    databases_searched = evidence.get("databases_searched", [])
    search_strategies_documented = evidence.get("search_strategies_documented", [])
    search_dates_recorded = evidence.get("search_dates_recorded", False)

    if not databases_searched:
        return CheckResult(
            check_id="search_reproducibility",
            name="Search Reproducibility",
            status="FAIL",
            severity=Severity.CRITICAL,
            message="No databases documented in search strategy.",
            suggestions=["Document all databases searched with full search strings."],
        )

    undocumented = [db for db in databases_searched if db not in search_strategies_documented]
    issues = []
    if undocumented:
        issues.append(f"Missing search strategy for: {', '.join(undocumented)}")
    if not search_dates_recorded:
        issues.append("Search dates not recorded")

    if issues:
        return CheckResult(
            check_id="search_reproducibility",
            name="Search Reproducibility",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"Search reproducibility issues: {'; '.join(issues)}",
            evidence={"undocumented_databases": undocumented},
            suggestions=["Provide complete search strategy for each database."],
        )

    return CheckResult(
        check_id="search_reproducibility",
        name="Search Reproducibility",
        status="PASS",
        severity=Severity.CRITICAL,
        message=f"Search strategies documented for all {len(databases_searched)} databases.",
    )


def check_screening_consistency(evidence: dict[str, Any]) -> CheckResult:
    """Check inter-rater agreement in screening."""
    screening_method = evidence.get("screening_method", "")
    dual_screening = evidence.get("dual_screening", False)
    kappa_score = evidence.get("screening_kappa", None)
    calibration_conducted = evidence.get("calibration_conducted", False)
    disagreements_resolved = evidence.get("disagreements_resolved", False)

    if not screening_method:
        return CheckResult(
            check_id="screening_consistency",
            name="Screening Consistency",
            status="SKIP",
            severity=Severity.MAJOR,
            message="No screening data provided.",
        )

    issues = []
    if not dual_screening:
        issues.append("Single-reviewer screening (dual recommended)")
    if kappa_score is not None and kappa_score < 0.6:
        issues.append(f"Low inter-rater agreement (kappa={kappa_score})")
    if not calibration_conducted:
        issues.append("No calibration exercise documented")

    if issues:
        return CheckResult(
            check_id="screening_consistency",
            name="Screening Consistency",
            status="WARN" if len(issues) == 1 else "FAIL",
            severity=Severity.MAJOR,
            message=f"Screening issues: {'; '.join(issues)}",
            suggestions=["Conduct calibration exercises before full screening."],
        )

    return CheckResult(
        check_id="screening_consistency",
        name="Screening Consistency",
        status="PASS",
        severity=Severity.MAJOR,
        message="Screening process documented with adequate agreement.",
    )


def check_extraction_completeness(evidence: dict[str, Any]) -> CheckResult:
    """Check that all pre-specified data fields were extracted."""
    fields_specified = evidence.get("extraction_fields_specified", [])
    fields_extracted = evidence.get("extraction_fields_extracted", [])
    studies_with_missing_data = evidence.get("studies_with_missing_data", [])

    if not fields_specified:
        return CheckResult(
            check_id="extraction_completeness",
            name="Extraction Completeness",
            status="SKIP",
            severity=Severity.MAJOR,
            message="No extraction field specification provided.",
        )

    missing_fields = [f for f in fields_specified if f not in fields_extracted]
    if missing_fields:
        return CheckResult(
            check_id="extraction_completeness",
            name="Extraction Completeness",
            status="FAIL",
            severity=Severity.MAJOR,
            message=f"{len(missing_fields)} pre-specified field(s) not extracted.",
            evidence={"missing_fields": missing_fields},
        )

    if studies_with_missing_data:
        return CheckResult(
            check_id="extraction_completeness",
            name="Extraction Completeness",
            status="WARN",
            severity=Severity.MAJOR,
            message=f"{len(studies_with_missing_data)} study/ies with incomplete data.",
            evidence={"studies_with_gaps": studies_with_missing_data},
        )

    return CheckResult(
        check_id="extraction_completeness",
        name="Extraction Completeness",
        status="PASS",
        severity=Severity.MAJOR,
        message=f"All {len(fields_specified)} extraction fields complete.",
    )


def check_quality_assessment_validity(evidence: dict[str, Any]) -> CheckResult:
    """Check risk of bias / quality assessment was conducted per protocol."""
    tool_used = evidence.get("quality_assessment_tool", "")
    studies_assessed = evidence.get("studies_assessed", 0)
    studies_total = evidence.get("studies_included", 0)
    per_domain_scores = evidence.get("per_domain_scores", False)

    if not tool_used:
        return CheckResult(
            check_id="quality_assessment_validity",
            name="Quality Assessment Validity",
            status="FAIL",
            severity=Severity.CRITICAL,
            message="No quality assessment tool specified or used.",
            suggestions=["Select and apply RoB 2, ROBINS-I, Newcastle-Ottawa, or other appropriate tool."],
        )

    if studies_total > 0 and studies_assessed < studies_total:
        return CheckResult(
            check_id="quality_assessment_validity",
            name="Quality Assessment Validity",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"Only {studies_assessed}/{studies_total} studies assessed for quality.",
        )

    if not per_domain_scores:
        return CheckResult(
            check_id="quality_assessment_validity",
            name="Quality Assessment Validity",
            status="FAIL",
            severity=Severity.MAJOR,
            message="Per-domain risk of bias scores not provided.",
            suggestions=["Report individual domain scores, not just overall judgment."],
        )

    return CheckResult(
        check_id="quality_assessment_validity",
        name="Quality Assessment Validity",
        status="PASS",
        severity=Severity.CRITICAL,
        message=f"Quality assessed for all {studies_assessed} studies using {tool_used}.",
    )


def check_statistical_validity(evidence: dict[str, Any]) -> CheckResult:
    """Check statistical methods are appropriate and correctly applied."""
    meta_analysis_conducted = evidence.get("meta_analysis_conducted", False)
    model_type = evidence.get("model_type", "")  # fixed | random
    heterogeneity_assessed = evidence.get("heterogeneity_assessed", False)
    i_squared = evidence.get("i_squared", None)
    effect_measure = evidence.get("effect_measure", "")
    pooling_appropriate = evidence.get("pooling_appropriate", True)

    if not meta_analysis_conducted:
        return CheckResult(
            check_id="statistical_validity",
            name="Statistical Validity",
            status="SKIP",
            severity=Severity.CRITICAL,
            message="No meta-analysis conducted (narrative synthesis only).",
        )

    issues = []
    if not model_type:
        issues.append("Statistical model not specified (fixed/random)")
    if not heterogeneity_assessed:
        issues.append("Heterogeneity not assessed")
    if i_squared is not None and i_squared > 75 and model_type == "fixed":
        issues.append(f"High heterogeneity (I-squared={i_squared}%) with fixed-effect model")
    if not effect_measure:
        issues.append("Effect measure not specified")
    if not pooling_appropriate:
        issues.append("Studies may be too heterogeneous to pool")

    if issues:
        return CheckResult(
            check_id="statistical_validity",
            name="Statistical Validity",
            status="FAIL",
            severity=Severity.CRITICAL,
            message=f"Statistical issues: {'; '.join(issues)}",
            evidence={"i_squared": i_squared, "model": model_type},
            suggestions=["Review statistical model choice given heterogeneity levels."],
        )

    return CheckResult(
        check_id="statistical_validity",
        name="Statistical Validity",
        status="PASS",
        severity=Severity.CRITICAL,
        message=f"Meta-analysis valid: {model_type}-effects model, {effect_measure}, I-squared={i_squared}%.",
    )


def check_publication_bias(evidence: dict[str, Any]) -> CheckResult:
    """Check publication bias was assessed."""
    assessment_conducted = evidence.get("publication_bias_assessed", False)
    methods_used = evidence.get("publication_bias_methods", [])
    sufficient_studies = evidence.get("studies_for_bias_test", 0) >= 10
    bias_detected = evidence.get("publication_bias_detected", None)

    if not assessment_conducted:
        return CheckResult(
            check_id="publication_bias",
            name="Publication Bias",
            status="FAIL",
            severity=Severity.MAJOR,
            message="Publication bias not assessed.",
            suggestions=[
                "Conduct funnel plot analysis (if >= 10 studies).",
                "Apply Egger's test or trim-and-fill method.",
            ],
        )

    if not sufficient_studies:
        return CheckResult(
            check_id="publication_bias",
            name="Publication Bias",
            status="WARN",
            severity=Severity.MAJOR,
            message="Fewer than 10 studies — statistical tests for funnel plot asymmetry unreliable.",
            evidence={"methods_used": methods_used},
        )

    if bias_detected:
        return CheckResult(
            check_id="publication_bias",
            name="Publication Bias",
            status="WARN",
            severity=Severity.MAJOR,
            message="Publication bias detected — interpret pooled estimates with caution.",
            evidence={"methods_used": methods_used, "bias_detected": True},
        )

    return CheckResult(
        check_id="publication_bias",
        name="Publication Bias",
        status="PASS",
        severity=Severity.MAJOR,
        message=f"Publication bias assessed using {', '.join(methods_used)}.",
    )


def check_grade_assessment(evidence: dict[str, Any]) -> CheckResult:
    """Check GRADE certainty of evidence assessment."""
    grade_conducted = evidence.get("grade_conducted", False)
    outcomes_graded = evidence.get("outcomes_graded", [])
    outcomes_total = evidence.get("outcomes_total", 0)
    domains_assessed = evidence.get("grade_domains_assessed", [])
    required_domains = ["risk_of_bias", "inconsistency", "indirectness", "imprecision", "publication_bias"]

    if not grade_conducted:
        return CheckResult(
            check_id="grade_assessment",
            name="GRADE Assessment",
            status="FAIL",
            severity=Severity.MAJOR,
            message="GRADE certainty of evidence not assessed.",
            suggestions=["Apply GRADE framework to each critical/important outcome."],
        )

    missing_domains = [d for d in required_domains if d not in domains_assessed]
    if missing_domains:
        return CheckResult(
            check_id="grade_assessment",
            name="GRADE Assessment",
            status="FAIL",
            severity=Severity.MAJOR,
            message=f"GRADE domains missing: {', '.join(missing_domains)}",
            evidence={"missing_domains": missing_domains},
        )

    if outcomes_total > 0 and len(outcomes_graded) < outcomes_total:
        return CheckResult(
            check_id="grade_assessment",
            name="GRADE Assessment",
            status="FAIL",
            severity=Severity.MAJOR,
            message=f"Only {len(outcomes_graded)}/{outcomes_total} outcomes graded.",
        )

    return CheckResult(
        check_id="grade_assessment",
        name="GRADE Assessment",
        status="PASS",
        severity=Severity.MAJOR,
        message=f"GRADE assessed for {len(outcomes_graded)} outcomes across all 5 domains.",
    )


def check_sensitivity_analysis(evidence: dict[str, Any]) -> CheckResult:
    """Check pre-specified sensitivity analyses were conducted."""
    analyses_planned = evidence.get("sensitivity_analyses_planned", [])
    analyses_conducted = evidence.get("sensitivity_analyses_conducted", [])

    if not analyses_planned:
        return CheckResult(
            check_id="sensitivity_analysis",
            name="Sensitivity Analysis",
            status="WARN",
            severity=Severity.MAJOR,
            message="No sensitivity analyses pre-specified.",
            suggestions=[
                "Pre-specify leave-one-out analysis.",
                "Pre-specify analysis excluding high risk-of-bias studies.",
            ],
        )

    missing = [a for a in analyses_planned if a not in analyses_conducted]
    if missing:
        return CheckResult(
            check_id="sensitivity_analysis",
            name="Sensitivity Analysis",
            status="FAIL",
            severity=Severity.MAJOR,
            message=f"{len(missing)} pre-specified sensitivity analysis/es not conducted.",
            evidence={"missing_analyses": missing},
        )

    return CheckResult(
        check_id="sensitivity_analysis",
        name="Sensitivity Analysis",
        status="PASS",
        severity=Severity.MAJOR,
        message=f"All {len(analyses_planned)} sensitivity analyses conducted.",
    )


def check_narrative_consistency(evidence: dict[str, Any]) -> CheckResult:
    """Check text matches tables, figures, and data."""
    inconsistencies = evidence.get("narrative_inconsistencies", [])
    tables_checked = evidence.get("tables_cross_checked", 0)
    figures_checked = evidence.get("figures_cross_checked", 0)

    if inconsistencies:
        return CheckResult(
            check_id="narrative_consistency",
            name="Narrative Consistency",
            status="FAIL",
            severity=Severity.MINOR,
            message=f"{len(inconsistencies)} inconsistency/ies between text and data.",
            evidence={"inconsistencies": inconsistencies},
        )

    if tables_checked == 0 and figures_checked == 0:
        return CheckResult(
            check_id="narrative_consistency",
            name="Narrative Consistency",
            status="SKIP",
            severity=Severity.MINOR,
            message="No tables or figures cross-checked.",
        )

    return CheckResult(
        check_id="narrative_consistency",
        name="Narrative Consistency",
        status="PASS",
        severity=Severity.MINOR,
        message=f"Cross-checked {tables_checked} tables and {figures_checked} figures.",
    )


def check_registration_consistency(evidence: dict[str, Any]) -> CheckResult:
    """Check results match registered protocol (PROSPERO)."""
    registered = evidence.get("protocol_registered", False)
    deviations = evidence.get("protocol_deviations", [])
    deviations_explained = evidence.get("deviations_explained", False)

    if not registered:
        return CheckResult(
            check_id="registration_consistency",
            name="Registration Consistency",
            status="WARN",
            severity=Severity.MINOR,
            message="Protocol not registered (PROSPERO recommended).",
            suggestions=["Register protocol on PROSPERO before conducting searches."],
        )

    if deviations and not deviations_explained:
        return CheckResult(
            check_id="registration_consistency",
            name="Registration Consistency",
            status="FAIL",
            severity=Severity.MINOR,
            message=f"{len(deviations)} protocol deviation(s) not explained.",
            evidence={"deviations": deviations},
        )

    if deviations and deviations_explained:
        return CheckResult(
            check_id="registration_consistency",
            name="Registration Consistency",
            status="PASS",
            severity=Severity.MINOR,
            message=f"{len(deviations)} deviation(s) documented and justified.",
        )

    return CheckResult(
        check_id="registration_consistency",
        name="Registration Consistency",
        status="PASS",
        severity=Severity.MINOR,
        message="Results consistent with registered protocol.",
    )


def check_citation_accuracy(evidence: dict[str, Any]) -> CheckResult:
    """Check references are accurate and complete."""
    citations_checked = evidence.get("citations_checked", 0)
    citation_errors = evidence.get("citation_errors", [])
    missing_citations = evidence.get("missing_citations", [])

    if citations_checked == 0:
        return CheckResult(
            check_id="citation_accuracy",
            name="Citation Accuracy",
            status="SKIP",
            severity=Severity.MINOR,
            message="No citations checked.",
        )

    issues = []
    if citation_errors:
        issues.append(f"{len(citation_errors)} citation error(s)")
    if missing_citations:
        issues.append(f"{len(missing_citations)} missing citation(s)")

    if issues:
        return CheckResult(
            check_id="citation_accuracy",
            name="Citation Accuracy",
            status="FAIL",
            severity=Severity.MINOR,
            message=f"Citation issues: {'; '.join(issues)}",
            evidence={"errors": citation_errors, "missing": missing_citations},
        )

    return CheckResult(
        check_id="citation_accuracy",
        name="Citation Accuracy",
        status="PASS",
        severity=Severity.MINOR,
        message=f"All {citations_checked} citations verified.",
    )


# -- Default predicate registry ---------------------------------------------

DEFAULT_PREDICATES: dict[str, Predicate] = {
    "prisma_compliance": check_prisma_compliance,
    "search_reproducibility": check_search_reproducibility,
    "screening_consistency": check_screening_consistency,
    "extraction_completeness": check_extraction_completeness,
    "quality_assessment_validity": check_quality_assessment_validity,
    "statistical_validity": check_statistical_validity,
    "publication_bias": check_publication_bias,
    "grade_assessment": check_grade_assessment,
    "sensitivity_analysis": check_sensitivity_analysis,
    "narrative_consistency": check_narrative_consistency,
    "registration_consistency": check_registration_consistency,
    "citation_accuracy": check_citation_accuracy,
}


# -- Verification Kernel ----------------------------------------------------

class VerificationKernel:
    """Content-addressed verification kernel.

    Runs predicates over evidence registries and produces
    SHA-256 verdicts for reproducibility and tamper-evidence.
    """

    def __init__(self, predicates: dict[str, Predicate] | None = None):
        self.predicates = predicates or dict(DEFAULT_PREDICATES)

    def _hash(self, data: str) -> str:
        return f"sha256:{hashlib.sha256(data.encode()).hexdigest()}"

    def verify(self, evidence: dict[str, Any]) -> Verdict:
        """Run all predicates against evidence and produce a verdict."""
        # Hash inputs
        evidence_json = json.dumps(evidence, sort_keys=True, default=str)
        registry_hash = self._hash(evidence_json)

        predicate_names = json.dumps(sorted(self.predicates.keys()))
        predicates_hash = self._hash(predicate_names)

        # Run predicates
        results: dict[str, CheckResult] = {}
        for check_id, predicate in self.predicates.items():
            try:
                result = predicate(evidence)
                results[check_id] = result
            except Exception as e:
                results[check_id] = CheckResult(
                    check_id=check_id,
                    name=check_id.replace("_", " ").title(),
                    status="FAIL",
                    severity=Severity.MAJOR,
                    message=f"Predicate raised exception: {e}",
                )

        # Determine overall status
        has_critical_fail = any(
            r.status == "FAIL" and r.severity == Severity.CRITICAL
            for r in results.values()
        )
        has_major_fail = any(
            r.status == "FAIL" and r.severity == Severity.MAJOR
            for r in results.values()
        )

        if has_critical_fail:
            overall = "FAIL"
        elif has_major_fail:
            overall = "PARTIAL"
        else:
            overall = "PASS"

        # Hash the results for tamper-evidence
        results_json = json.dumps(
            {k: v.message for k, v in results.items()},
            sort_keys=True,
        )
        verdict_hash = self._hash(
            f"{registry_hash}:{predicates_hash}:{results_json}"
        )

        # Build summary
        pass_count = sum(1 for r in results.values() if r.status == "PASS")
        fail_count = sum(1 for r in results.values() if r.status == "FAIL")
        skip_count = sum(1 for r in results.values() if r.status == "SKIP")
        warn_count = sum(1 for r in results.values() if r.status == "WARN")

        summary = (
            f"{overall}: {pass_count} passed, {fail_count} failed, "
            f"{warn_count} warnings, {skip_count} skipped "
            f"out of {len(results)} checks."
        )

        return Verdict(
            registry_hash=registry_hash,
            predicates_hash=predicates_hash,
            verdict_hash=verdict_hash,
            overall=overall,
            results=results,
            summary=summary,
        )
