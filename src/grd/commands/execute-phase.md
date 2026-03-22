---
name: execute-phase
description: Execute the current phase — the main review loop
---

<process>

## Execute Phase

Read `{GRD_INSTALL_DIR}/specs/workflows/execute-phase-workflow.md` first. Do NOT improvise.

### Overview
This is the main execution loop. It:
1. Loads ROADMAP.md and STATE.md
2. Discovers all PLAN.md files for the current phase
3. Computes dependency-ordered waves
4. Executes tasks in parallel within each wave via subagent delegation
5. Verifies artifacts after each wave
6. Runs post-phase verification
7. Handles gap closure if verification fails

### Pre-execution
1. Load state via grd-state
2. Check conventions via grd-conventions (especially review parameters)
3. Verify plans exist for current phase
4. Create rollback checkpoint tag

### Wave Execution Loop
For each wave (in order):
1. Log wave start
2. For each plan/task in the wave (parallel):
   a. Spawn grd-executor subagent with task context
   b. Collect return envelope
   c. Verify artifacts on disk (artifact recovery protocol)
   d. Commit task artifacts
   e. Update PRISMA flow counts
3. Log wave completion
4. Run inter-wave verification if configured (PRISMA count checks, convention checks)
5. Update STATE.md

### Post-Phase Verification
After all waves complete:
1. Spawn grd-verifier with all phase artifacts
2. Parse verification verdict
3. If PASS: mark phase complete, advance to next phase
4. If FAIL: create gap-closure plans for failed checks
5. Re-execute gap-closure plans with --gaps-only flag
6. Maximum 2 gap-closure iterations, then flag UNRESOLVED

### Phase-Specific Behavior

#### Protocol Phase
- Lock all 14 convention fields by end of phase
- Generate PROSPERO registration draft

#### Search Phase
- Track database-specific hit counts
- Merge and deduplicate citations
- Update PRISMA identification counts

#### Screening Phase
- Dual screening with calibration
- Track inter-rater agreement (kappa)
- Update PRISMA screening counts

#### Extraction Phase
- Dual extraction recommended
- Track completeness per study
- Flag missing data

#### Quality Assessment Phase
- Apply locked RoB/quality tool
- Generate per-study, per-domain assessments

#### Synthesis Phase
- Invoke grd-statistician for meta-analysis
- Generate forest plots, funnel plots
- Run sensitivity and subgroup analyses

#### Manuscript Phase
- Invoke grd-paper-writer
- Generate PRISMA flow diagram
- Complete PRISMA checklist

### Error Handling
- Subagent failure: analyze, create targeted re-execution plan
- Convention violation: route to convention resolution
- Context pressure: checkpoint and resume in fresh session

</process>
