# Search Strategy Protocols

> Step-by-step methodology guides for developing and executing systematic search strategies.

## Protocol: PICO-to-Search Translation

### When to Use
Translating a structured PICO question into database search strategies.

### Steps
1. **Break PICO into search concepts** — typically 2-3 concepts (usually P + I, sometimes + O)
2. **For each concept, identify**:
   a. Free-text terms (synonyms, spelling variants, abbreviations)
   b. Controlled vocabulary (MeSH for PubMed, Emtree for Embase)
   c. Related terms and broader/narrower terms
3. **Combine terms within concepts using OR**
4. **Combine concepts using AND**
5. **Add filters judiciously** — date, language, study design (with caution)
6. **Test strategy against known relevant studies** — must retrieve all known key papers
7. **Iterate to optimize sensitivity/precision balance**

### Common LLM Pitfalls
- Missing important synonyms or variant spellings (E001)
- Over-reliance on MeSH terms (not all studies indexed yet)
- Using NOT operators too aggressively (excluding relevant studies)
- Applying study design filters that miss relevant designs

---

## Protocol: PubMed/MEDLINE Search

### When to Use
Searching PubMed for biomedical literature.

### Steps
1. **Use both MeSH and free-text terms**
   - MeSH: `"Term"[Mesh]` or `"Term"[Mesh:NoExp]` (no explosion)
   - Free text: `term[tiab]` (title/abstract) or `term[tw]` (text word)
2. **Use explosion by default** for MeSH (includes narrower terms)
3. **Truncation**: `*` for wildcard (e.g., `random*` matches randomized, randomised, randomization)
4. **Proximity**: Not available in PubMed (use phrase searching instead)
5. **Combine with Boolean**: `(concept1) AND (concept2) AND (concept3)`
6. **Record the full strategy** including line numbers
7. **Record date of search and number of results**

### Sensitivity Filters
- Cochrane Highly Sensitive Search Strategy for RCTs
- BMJ Clinical Queries filters
- SIGN search filters for observational studies

---

## Protocol: Embase Search (via Ovid)

### When to Use
Searching Embase for biomedical literature (broader than MEDLINE, strong drug/pharmacology coverage).

### Steps
1. **Use both Emtree and free-text terms**
   - Emtree: `exp term/` (exploded) or `term/` (not exploded)
   - Free text: `term.mp.` (multi-purpose) or `term.ti,ab.` (title/abstract)
2. **Combine within concepts using OR**
3. **Truncation**: `*` for wildcard, `?` for single character
4. **Proximity**: `adj3` means within 3 words in any order
5. **Remove MEDLINE overlap if needed**: `not (medline or pubmed).tw.`
6. **Record full strategy with line numbers**

---

## Protocol: Cochrane CENTRAL Search

### When to Use
Searching Cochrane Central Register of Controlled Trials.

### Steps
1. **Use MeSH and free-text** (Cochrane uses MeSH headings)
2. **Search in title/abstract/keyword fields**
3. **No study design filter needed** (CENTRAL is pre-filtered for trials)
4. **Export all results** for deduplication against PubMed/Embase

---

## Protocol: Grey Literature Search

### When to Use
Every systematic review should search for unpublished and grey literature to minimize publication bias.

### Sources to Search
1. **Trial registries**: ClinicalTrials.gov, WHO ICTRP, EU Clinical Trials Register
2. **Preprint servers**: medRxiv, bioRxiv, SSRN, arXiv
3. **Dissertation databases**: ProQuest Dissertations, OpenDOAR
4. **Conference proceedings**: relevant specialty conferences
5. **Organization websites**: WHO, FDA, EMA, NICE
6. **Contact study authors** for unpublished data

### Steps
1. **Document each source searched** with date
2. **Document search terms used** (often simpler than database searches)
3. **Record number of results** per source
4. **Screen results against inclusion criteria**
5. **Document any access limitations**

---

## Protocol: Deduplication

### When to Use
After searching multiple databases, before screening.

### Steps
1. **Import all citations into reference manager** (e.g., Zotero, EndNote, Rayyan)
2. **Automated deduplication** by DOI (exact match)
3. **Automated deduplication** by title + first author (fuzzy match)
4. **Manual review** of potential duplicates flagged by automation
5. **Record**: N total imported, N duplicates removed, N unique for screening
6. **Document deduplication method**

### Common LLM Pitfalls
- Counting pre-deduplication numbers in PRISMA (should report post-dedup for screening)
- Missing duplicates with slight title variations across databases
- Over-aggressive deduplication removing truly distinct studies
