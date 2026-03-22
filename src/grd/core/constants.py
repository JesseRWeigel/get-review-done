"""Single source of truth for all directory/file names and environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


# -- Environment Variables --------------------------------------------------

ENV_GRD_HOME = "GRD_HOME"
ENV_GRD_PROJECT = "GRD_PROJECT"
ENV_GRD_INSTALL_DIR = "GRD_INSTALL_DIR"
ENV_GRD_DEBUG = "GRD_DEBUG"
ENV_GRD_AUTONOMY = "GRD_AUTONOMY"

# -- File Names -------------------------------------------------------------

STATE_MD = "STATE.md"
STATE_JSON = "state.json"
STATE_WRITE_INTENT = ".state-write-intent"
ROADMAP_MD = "ROADMAP.md"
CONFIG_JSON = "config.json"
CONVENTIONS_JSON = "conventions.json"

PLAN_PREFIX = "PLAN"
SUMMARY_PREFIX = "SUMMARY"
RESEARCH_MD = "RESEARCH.md"
RESEARCH_DIGEST_MD = "RESEARCH-DIGEST.md"
CONTINUE_HERE_MD = ".continue-here.md"

# -- Directory Names --------------------------------------------------------

GRD_DIR = ".grd"
OBSERVABILITY_DIR = "observability"
SESSIONS_DIR = "sessions"
TRACES_DIR = "traces"
KNOWLEDGE_DIR = "knowledge"
PAPER_DIR = "paper"
SCRATCH_DIR = ".scratch"
DATA_DIR = "data"
SCREENING_DIR = "screening"
EXTRACTION_DIR = "extraction"

# -- Git --------------------------------------------------------------------

CHECKPOINT_TAG_PREFIX = "grd-checkpoint"
COMMIT_PREFIX = "[grd]"

# -- Autonomy Modes --------------------------------------------------------

AUTONOMY_SUPERVISED = "supervised"
AUTONOMY_BALANCED = "balanced"
AUTONOMY_YOLO = "yolo"
VALID_AUTONOMY_MODES = {AUTONOMY_SUPERVISED, AUTONOMY_BALANCED, AUTONOMY_YOLO}

# -- Research Modes ---------------------------------------------------------

RESEARCH_EXPLORE = "explore"
RESEARCH_BALANCED = "balanced"
RESEARCH_EXPLOIT = "exploit"
RESEARCH_ADAPTIVE = "adaptive"
VALID_RESEARCH_MODES = {RESEARCH_EXPLORE, RESEARCH_BALANCED, RESEARCH_EXPLOIT, RESEARCH_ADAPTIVE}

# -- Model Tiers ------------------------------------------------------------

TIER_1 = "tier-1"  # Highest capability
TIER_2 = "tier-2"  # Balanced
TIER_3 = "tier-3"  # Fastest

# -- Verification Severity --------------------------------------------------

SEVERITY_CRITICAL = "CRITICAL"  # Blocks all downstream work
SEVERITY_MAJOR = "MAJOR"        # Must resolve before conclusions
SEVERITY_MINOR = "MINOR"        # Must resolve before publication
SEVERITY_NOTE = "NOTE"          # Informational

# -- Convention Lock Fields (Systematic Review) -----------------------------

CONVENTION_FIELDS = [
    "research_question",              # PICO/PECO format
    "inclusion_criteria",             # Study designs, populations, interventions, outcomes
    "exclusion_criteria",             # What to exclude and why
    "search_databases_and_dates",     # Databases searched, date ranges, access dates
    "search_strategy",                # Search terms, Boolean operators, MeSH/Emtree terms
    "quality_assessment_tool",        # RoB 2, ROBINS-I, Newcastle-Ottawa, JBI, etc.
    "outcome_definitions",            # Primary and secondary outcomes with measurement details
    "effect_size_measure",            # OR, RR, HR, SMD, MD, correlation coefficient
    "synthesis_method",               # Fixed-effect, random-effects (DL, REML), narrative
    "heterogeneity_assessment",       # I-squared, Q-test, tau-squared, prediction intervals
    "publication_bias_assessment",    # Funnel plot, Egger's test, trim-and-fill, p-curve
    "certainty_of_evidence",          # GRADE framework domains and approach
    "sensitivity_analysis_params",    # Leave-one-out, influence analysis, subgroup thresholds
    "subgroup_analysis_criteria",     # Pre-specified subgroups and rationale
]

# -- Verification Checks (12 PRISMA/Methodology) --------------------------

VERIFICATION_CHECKS = [
    "prisma_compliance",              # 27-item PRISMA 2020 checklist adherence
    "search_reproducibility",         # Search strategies reproducible across databases
    "screening_consistency",          # Inter-rater agreement, calibration exercises
    "extraction_completeness",        # All pre-specified data fields extracted
    "quality_assessment_validity",    # Risk of bias assessed per protocol
    "statistical_validity",           # Appropriate models, assumptions checked
    "publication_bias",               # Assessed and reported
    "grade_assessment",               # Certainty of evidence for each outcome
    "sensitivity_analysis",           # Pre-specified analyses conducted
    "narrative_consistency",          # Text matches tables, figures, and data
    "registration_consistency",       # Results match registered protocol (PROSPERO)
    "citation_accuracy",             # References accurate and complete
]


@dataclass(frozen=True)
class ProjectLayout:
    """Resolved paths for a GRD project."""

    root: Path

    @property
    def grd_dir(self) -> Path:
        return self.root / GRD_DIR

    @property
    def state_md(self) -> Path:
        return self.grd_dir / STATE_MD

    @property
    def state_json(self) -> Path:
        return self.grd_dir / STATE_JSON

    @property
    def state_write_intent(self) -> Path:
        return self.grd_dir / STATE_WRITE_INTENT

    @property
    def roadmap_md(self) -> Path:
        return self.grd_dir / ROADMAP_MD

    @property
    def config_json(self) -> Path:
        return self.grd_dir / CONFIG_JSON

    @property
    def conventions_json(self) -> Path:
        return self.grd_dir / CONVENTIONS_JSON

    @property
    def observability_dir(self) -> Path:
        return self.grd_dir / OBSERVABILITY_DIR

    @property
    def sessions_dir(self) -> Path:
        return self.observability_dir / SESSIONS_DIR

    @property
    def traces_dir(self) -> Path:
        return self.grd_dir / TRACES_DIR

    @property
    def knowledge_dir(self) -> Path:
        return self.root / KNOWLEDGE_DIR

    @property
    def paper_dir(self) -> Path:
        return self.root / PAPER_DIR

    @property
    def scratch_dir(self) -> Path:
        return self.root / SCRATCH_DIR

    @property
    def data_dir(self) -> Path:
        return self.root / DATA_DIR

    @property
    def screening_dir(self) -> Path:
        return self.data_dir / SCREENING_DIR

    @property
    def extraction_dir(self) -> Path:
        return self.data_dir / EXTRACTION_DIR

    @property
    def continue_here(self) -> Path:
        return self.grd_dir / CONTINUE_HERE_MD

    def phase_dir(self, phase: str) -> Path:
        return self.root / f"phase-{phase}"

    def plan_path(self, phase: str, plan_number: str) -> Path:
        return self.phase_dir(phase) / f"{PLAN_PREFIX}-{plan_number}.md"

    def summary_path(self, phase: str, plan_number: str) -> Path:
        return self.phase_dir(phase) / f"{SUMMARY_PREFIX}-{plan_number}.md"

    def ensure_dirs(self) -> None:
        """Create all required directories."""
        for d in [
            self.grd_dir,
            self.observability_dir,
            self.sessions_dir,
            self.traces_dir,
            self.knowledge_dir,
            self.scratch_dir,
            self.data_dir,
            self.screening_dir,
            self.extraction_dir,
        ]:
            d.mkdir(parents=True, exist_ok=True)


def find_project_root(start: Path | None = None) -> Path:
    """Walk up from start (or cwd) looking for .grd/ directory."""
    current = start or Path.cwd()
    while current != current.parent:
        if (current / GRD_DIR).is_dir():
            return current
        current = current.parent
    raise FileNotFoundError(
        f"No {GRD_DIR}/ directory found. Run 'grd init' to create a project."
    )


def get_layout(start: Path | None = None) -> ProjectLayout:
    """Get the project layout, finding the root automatically."""
    env_project = os.environ.get(ENV_GRD_PROJECT)
    if env_project:
        return ProjectLayout(root=Path(env_project))
    return ProjectLayout(root=find_project_root(start))
