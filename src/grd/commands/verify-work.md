---
name: verify-work
description: Run the 12-check systematic review verification framework
---

<process>

## Verify Work

### Overview
Run post-hoc verification on completed phase work using the 12-check framework.

### Step 1: Collect Artifacts
Gather all output from the current phase:
- Search logs and strategies
- Screening records and decisions
- Extraction forms and data tables
- Quality assessment scores
- Meta-analysis outputs (forest plots, summary tables)
- PRISMA flow diagram data

### Step 2: Build Evidence Registry
Extract verification evidence from artifacts:
- PRISMA items reported/missing
- Databases searched with strategies documented
- Screening decisions with reasons
- Extraction fields specified vs extracted
- Quality assessment tool and domain scores
- Statistical model and heterogeneity metrics
- Publication bias assessment results
- GRADE domain ratings
- Sensitivity analyses planned vs conducted
- Narrative vs data consistency
- Protocol deviations
- Citation accuracy

### Step 3: Run Verification
Spawn grd-verifier with:
- All phase artifacts
- Evidence registry
- Convention locks
- LLM error catalog

### Step 4: Process Verdict
Parse the VERIFICATION-REPORT.md:
- If PASS: record in state, proceed
- If PARTIAL: create targeted gap-closure for MAJOR failures
- If FAIL: create gap-closure for CRITICAL failures, block downstream

### Step 5: Route Failures
For each failure, route to the appropriate agent:
- PRISMA gaps → grd-paper-writer (manuscript) or grd-executor (data)
- Search issues → grd-researcher (strategy revision)
- Statistical errors → grd-statistician (re-analysis)
- Quality assessment gaps → grd-executor (targeted assessment)
- Convention drift → convention resolution
- Citation errors → grd-paper-writer

### Step 6: Update State
Record verification results in STATE.md:
- Verdict hash (content-addressed)
- Pass/fail counts
- Any unresolved issues

</process>
