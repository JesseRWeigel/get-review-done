"""Configuration — model tiers, autonomy modes, research modes.

Adapted from GPD's config.py for systematic reviews and meta-analyses.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .constants import (
    AUTONOMY_BALANCED,
    RESEARCH_BALANCED,
    TIER_1,
    TIER_2,
    TIER_3,
    VALID_AUTONOMY_MODES,
    VALID_RESEARCH_MODES,
    ProjectLayout,
)


# -- Model Profiles ---------------------------------------------------------
# Each profile maps agent roles to model tiers.

MODEL_PROFILES: dict[str, dict[str, str]] = {
    "comprehensive-review": {
        "planner": TIER_1,
        "executor": TIER_1,
        "verifier": TIER_1,
        "researcher": TIER_1,
        "statistician": TIER_1,
        "paper_writer": TIER_1,
        "referee": TIER_1,
    },
    "rapid-review": {
        "planner": TIER_2,
        "executor": TIER_2,
        "verifier": TIER_2,
        "researcher": TIER_2,
        "statistician": TIER_1,
        "paper_writer": TIER_2,
        "referee": TIER_2,
    },
    "scoping-review": {
        "planner": TIER_2,
        "executor": TIER_2,
        "verifier": TIER_2,
        "researcher": TIER_1,
        "statistician": TIER_3,
        "paper_writer": TIER_2,
        "referee": TIER_2,
    },
    "meta-analysis-focused": {
        "planner": TIER_2,
        "executor": TIER_2,
        "verifier": TIER_1,
        "researcher": TIER_2,
        "statistician": TIER_1,
        "paper_writer": TIER_1,
        "referee": TIER_1,
    },
    "protocol-only": {
        "planner": TIER_1,
        "executor": TIER_3,
        "verifier": TIER_2,
        "researcher": TIER_1,
        "statistician": TIER_3,
        "paper_writer": TIER_2,
        "referee": TIER_2,
    },
}

# -- Research Mode Parameters -----------------------------------------------

RESEARCH_MODE_PARAMS: dict[str, dict[str, Any]] = {
    "explore": {
        "candidate_databases": 8,
        "search_strategy_iterations": (3, 5),
        "screening_passes": 2,
        "planning_style": "parallel",
        "description": "Maximum breadth — search many databases, iterative strategy refinement.",
    },
    "balanced": {
        "candidate_databases": 5,
        "search_strategy_iterations": (2, 3),
        "screening_passes": 2,
        "planning_style": "sequential",
        "description": "Standard depth — core databases, validated search strategy.",
    },
    "exploit": {
        "candidate_databases": 3,
        "search_strategy_iterations": (1, 2),
        "screening_passes": 1,
        "planning_style": "focused",
        "description": "Narrow focus — known databases, established search terms.",
    },
    "adaptive": {
        "candidate_databases": 8,
        "search_strategy_iterations": (2, 5),
        "screening_passes": 2,
        "planning_style": "adaptive",
        "description": "Starts broad, narrows when saturation criteria met.",
        "transition_criteria": {
            "search_saturation": True,
            "min_convention_locks": 8,
            "no_new_relevant_studies": True,
            "screening_kappa_threshold": 0.8,
        },
    },
}


@dataclass
class GRDConfig:
    """Project configuration."""

    model_profile: str = "comprehensive-review"
    model_overrides: dict[str, dict[str, str]] = field(default_factory=dict)
    autonomy: str = AUTONOMY_BALANCED
    research_mode: str = RESEARCH_BALANCED
    commit_docs: bool = True
    review_type: str = "systematic"  # systematic | scoping | rapid | umbrella
    workflow: dict[str, Any] = field(default_factory=lambda: {
        "verify_between_waves": "auto",
        "max_plan_tasks": 10,
        "max_deviation_retries": 2,
        "context_budget_warning_pct": 80,
        "dual_screening": True,
        "dual_extraction": True,
    })

    def get_tier_for_role(self, role: str) -> str:
        """Get the model tier for an agent role."""
        profile = MODEL_PROFILES.get(self.model_profile, MODEL_PROFILES["comprehensive-review"])
        return profile.get(role, TIER_2)

    def get_research_params(self) -> dict[str, Any]:
        """Get parameters for current research mode."""
        return RESEARCH_MODE_PARAMS.get(
            self.research_mode,
            RESEARCH_MODE_PARAMS["balanced"],
        )

    @classmethod
    def load(cls, layout: ProjectLayout) -> "GRDConfig":
        """Load config from .grd/config.json."""
        config_path = layout.config_json
        if config_path.exists():
            data = json.loads(config_path.read_text())
            return cls(**{
                k: v for k, v in data.items()
                if k in cls.__dataclass_fields__
            })
        return cls()

    def save(self, layout: ProjectLayout) -> None:
        """Save config to .grd/config.json."""
        layout.grd_dir.mkdir(parents=True, exist_ok=True)
        data = {
            "model_profile": self.model_profile,
            "model_overrides": self.model_overrides,
            "autonomy": self.autonomy,
            "research_mode": self.research_mode,
            "commit_docs": self.commit_docs,
            "review_type": self.review_type,
            "workflow": self.workflow,
        }
        layout.config_json.write_text(json.dumps(data, indent=2))

    def validate(self) -> list[str]:
        """Validate config. Returns list of error messages."""
        errors = []
        if self.model_profile not in MODEL_PROFILES:
            errors.append(
                f"Unknown model_profile: {self.model_profile}. "
                f"Valid: {list(MODEL_PROFILES.keys())}"
            )
        if self.autonomy not in VALID_AUTONOMY_MODES:
            errors.append(
                f"Unknown autonomy mode: {self.autonomy}. "
                f"Valid: {VALID_AUTONOMY_MODES}"
            )
        if self.research_mode not in VALID_RESEARCH_MODES:
            errors.append(
                f"Unknown research_mode: {self.research_mode}. "
                f"Valid: {VALID_RESEARCH_MODES}"
            )
        valid_review_types = {"systematic", "scoping", "rapid", "umbrella"}
        if self.review_type not in valid_review_types:
            errors.append(
                f"Unknown review_type: {self.review_type}. "
                f"Valid: {valid_review_types}"
            )
        return errors
