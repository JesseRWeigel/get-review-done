"""Research contracts — Pydantic models for PICO questions, deliverables, and acceptance tests.

Adapted from GPD's contracts.py for systematic literature reviews and meta-analyses.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any


class PICOQuestion(BaseModel):
    """A structured research question in PICO/PECO format."""

    id: str
    population: str
    intervention: str  # or Exposure for PECO
    comparator: str
    outcome: str
    question_type: str = "intervention"  # intervention | diagnostic | prognostic | etiology
    full_statement: str = ""
    status: str = "draft"  # draft | registered | active | answered


class InclusionCriteria(BaseModel):
    """Criteria for study inclusion in the systematic review."""

    study_designs: list[str] = Field(default_factory=list)  # RCT, cohort, case-control, etc.
    population_criteria: list[str] = Field(default_factory=list)
    intervention_criteria: list[str] = Field(default_factory=list)
    outcome_criteria: list[str] = Field(default_factory=list)
    date_range: str = ""
    language_restrictions: list[str] = Field(default_factory=list)
    publication_types: list[str] = Field(default_factory=list)


class ExclusionCriteria(BaseModel):
    """Criteria for study exclusion."""

    reasons: list[str] = Field(default_factory=list)
    study_design_exclusions: list[str] = Field(default_factory=list)
    population_exclusions: list[str] = Field(default_factory=list)


class Deliverable(BaseModel):
    """An expected output artifact from a phase/plan."""

    id: str
    description: str
    artifact_type: str  # protocol | search_log | prisma_flow | data_table | forest_plot | manuscript_section | screening_form
    file_path: str = ""
    acceptance_tests: list[str] = Field(default_factory=list)
    status: str = "pending"  # pending | delivered | verified | rejected


class AcceptanceTest(BaseModel):
    """A concrete test for a deliverable."""

    id: str
    description: str
    test_type: str  # existence | completeness | reproducibility | statistical_validity | prisma_compliance
    predicate: str = ""  # Human-readable predicate
    status: str = "pending"  # pending | passed | failed


class ForbiddenProxy(BaseModel):
    """Something that must NOT be used as evidence of completion.

    Prevents agents from claiming success based on superficial signals.
    """

    description: str
    reason: str


class ResearchContract(BaseModel):
    """A complete research contract for a systematic review phase or plan.

    Defines what must be achieved, how to verify it, and what NOT to accept.
    """

    phase_id: str
    plan_id: str = ""
    goal: str

    pico_questions: list[PICOQuestion] = Field(default_factory=list)
    inclusion_criteria: InclusionCriteria = Field(default_factory=InclusionCriteria)
    exclusion_criteria: ExclusionCriteria = Field(default_factory=ExclusionCriteria)
    deliverables: list[Deliverable] = Field(default_factory=list)
    acceptance_tests: list[AcceptanceTest] = Field(default_factory=list)

    forbidden_proxies: list[ForbiddenProxy] = Field(
        default_factory=lambda: [
            ForbiddenProxy(
                description="Agent stating 'search is comprehensive' without search log",
                reason="Full search strategy with database-specific queries must exist on disk.",
            ),
            ForbiddenProxy(
                description="Screening decisions without documented rationale",
                reason="Every include/exclude decision must cite specific criteria.",
            ),
            ForbiddenProxy(
                description="Meta-analysis results without heterogeneity assessment",
                reason="Pooled estimates require I-squared, Q-test, and tau-squared reporting.",
            ),
            ForbiddenProxy(
                description="GRADE assessment without domain-by-domain justification",
                reason="Each GRADE domain must be individually rated with explicit reasoning.",
            ),
            ForbiddenProxy(
                description="Forest plot without individual study data",
                reason="Forest plots must show individual study estimates, weights, and CIs.",
            ),
            ForbiddenProxy(
                description="Risk of bias assessment without per-domain scores",
                reason="Each bias domain must be scored separately with supporting judgment.",
            ),
        ]
    )

    def all_questions_answered(self) -> bool:
        return all(q.status == "answered" for q in self.pico_questions)

    def all_deliverables_verified(self) -> bool:
        return all(d.status == "verified" for d in self.deliverables)

    def all_tests_passed(self) -> bool:
        return all(t.status == "passed" for t in self.acceptance_tests)


class AgentReturn(BaseModel):
    """Structured return envelope from subagents.

    Every subagent MUST produce this in their SUMMARY.md.
    The orchestrator uses this — not prose — to determine success.
    """

    status: str  # completed | checkpoint | blocked | failed
    files_written: list[str] = Field(default_factory=list)
    files_modified: list[str] = Field(default_factory=list)
    issues: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)
    studies_screened: int = 0
    studies_included: int = 0
    studies_excluded: int = 0
    conventions_proposed: dict[str, str] = Field(default_factory=dict)
    verification_evidence: dict[str, Any] = Field(default_factory=dict)
