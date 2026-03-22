---
name: new-project
description: Initialize a new systematic review project
---

<process>

## Initialize New Systematic Review Project

### Step 1: Create project structure
Create the `.grd/` directory and all required subdirectories:
- `.grd/` — project state and config
- `.grd/observability/sessions/` — session logs
- `.grd/traces/` — execution traces
- `knowledge/` — review knowledge base
- `data/screening/` — screening records
- `data/extraction/` — extraction forms and data
- `.scratch/` — temporary working files (gitignored)

### Step 2: Gather project information
Ask the user:
1. **Project name**: What is this systematic review about?
2. **Research question**: PICO format — Population, Intervention, Comparator, Outcome?
3. **Review type**: systematic (default), scoping, rapid, or umbrella?
4. **Model profile**: comprehensive-review (default), rapid-review, scoping-review, meta-analysis-focused, or protocol-only?
5. **Research mode**: explore, balanced (default), exploit, or adaptive?

### Step 3: Create initial ROADMAP.md
Based on the research question, create a phase breakdown:

```markdown
# [Project Name] — Roadmap

## Phase 1: Protocol Development
**Goal**: Develop review protocol, define PICO, register on PROSPERO

## Phase 2: Search Strategy
**Goal**: Develop and execute comprehensive search across databases

## Phase 3: Screening
**Goal**: Screen titles/abstracts and full texts against inclusion criteria

## Phase 4: Data Extraction
**Goal**: Extract pre-specified data from all included studies

## Phase 5: Quality Assessment
**Goal**: Assess risk of bias / study quality for all included studies

## Phase 6: Data Synthesis
**Goal**: Synthesize evidence — meta-analysis or narrative synthesis

## Phase 7: Manuscript
**Goal**: Write PRISMA-compliant manuscript with flow diagram
```

Adjust phases based on the review type. Scoping reviews skip Phase 5 and 6. Rapid reviews may combine phases.

### Step 4: Initialize state
Create STATE.md and state.json with:
- Project name and creation date
- Phase listing from ROADMAP
- Phase 1 set as active
- Research mode and autonomy mode
- PRISMA flow counters initialized to 0

### Step 5: Initialize config
Create `.grd/config.json` with user's choices.

### Step 6: Initialize git
If not already a git repo, initialize one. Add `.scratch/` to `.gitignore`.
Commit the initial project structure.

### Step 7: Convention prompting
Ask if the user wants to pre-set any review conventions:
- PICO question
- Target databases
- Quality assessment tool
- Effect size measure
- Synthesis method

Lock any conventions the user specifies.

### Step 8: Summary
Display:
- Project structure created
- Phases from roadmap
- Active conventions
- Next step: run `plan-phase` to begin Phase 1 (Protocol Development)

</process>
