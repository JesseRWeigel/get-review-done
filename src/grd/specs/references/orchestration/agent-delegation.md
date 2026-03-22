# Agent Delegation Protocol

> How the orchestrator spawns subagents, collects results, and handles failures.

## Task Delegation Pattern

```
orchestrator
  ├── spawn(grd-researcher, {pico_question, phase_goal})  → RESEARCH.md + search logs
  ├── spawn(grd-planner, {research, phase_goal})  → PLAN.md
  ├── validate(plan)  → PLAN-CHECK result
  │   └── if REVISE: loop back to planner (max 3 iterations)
  ├── for each wave:
  │   ├── spawn(grd-executor, {task_1})  → artifacts + SUMMARY  (search/screen/extract)
  │   ├── spawn(grd-executor, {task_2})  → artifacts + SUMMARY  (parallel)
  │   └── verify_artifacts_on_disk() + update_prisma_counts()
  ├── spawn(grd-statistician, {extraction_data})  → analysis + figures
  ├── spawn(grd-verifier, {phase_artifacts})  → VERIFICATION-REPORT.md
  │   └── if FAIL: create gap-closure plans, re-execute
  ├── spawn(grd-paper-writer, {all_artifacts})  → manuscript + PRISMA diagram
  ├── spawn(grd-referee, {manuscript})  → REVIEW-REPORT.md
  │   └── if REVISE: loop back to paper-writer (max 3 iterations)
  └── update STATE.md
```

## Artifact Recovery Protocol

**CRITICAL**: Never trust that a subagent's reported success means files were written.

After every subagent returns:
1. Parse the `grd_return` envelope from SUMMARY.md
2. Verify every file in `files_written` exists on disk
3. If missing: attempt to extract content from the agent's response text
4. If still missing: log error and flag for re-execution

## Return Envelope Parsing

Every subagent MUST produce a `grd_return:` YAML block in their SUMMARY.md:

```yaml
grd_return:
  status: completed | checkpoint | blocked | failed
  files_written: [...]
  files_modified: [...]
  issues: [...]
  next_actions: [...]
  studies_screened: N
  studies_included: N
  studies_excluded: N
  conventions_proposed: {field: value}
  verification_evidence: {...}
```

The orchestrator uses this structured data — NOT the agent's prose — to determine:
- Whether to proceed to the next wave
- What files to verify
- What convention proposals to evaluate
- What PRISMA flow counts to update
- What verification evidence to feed to the verifier

## Failure Handling

| Agent Status | Orchestrator Action |
|-------------|-------------------|
| `completed` | Verify artifacts, update PRISMA counts, proceed |
| `checkpoint` | Save state, can resume later |
| `blocked` | Analyze blocker, may route to different agent |
| `failed` | Analyze failure, create targeted re-execution plan |

## Context Budget

Each subagent gets a fresh context window. The orchestrator targets ~15% of its own context for coordination. Budget allocation per phase type:

| Phase Type | Orchestrator | Planner | Executor | Verifier | Statistician |
|-----------|-------------|---------|----------|----------|-------------|
| Protocol | 15% | 20% | 40% | 25% | 0% |
| Search | 10% | 5% | 70% | 15% | 0% |
| Screening | 10% | 5% | 70% | 15% | 0% |
| Extraction | 10% | 5% | 70% | 15% | 0% |
| Quality assessment | 10% | 5% | 60% | 25% | 0% |
| Synthesis | 10% | 5% | 20% | 25% | 40% |
| Manuscript | 10% | 5% | 50% | 20% | 15% |
