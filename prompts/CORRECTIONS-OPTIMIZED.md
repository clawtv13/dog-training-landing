# CORRECTIONS PROMPT - Systematic Error Correction

You will fix errors identified in audit reports using a systematic, safe methodology. Follow this 6-phase process.

---

## PHASE 1: Parse Audit Reports

**Extract actionable corrections:**

1. Read ALL audit files in the specified directory (usually `audits/`)
2. For each error, extract:
   - **Error type** (e.g., age-pronoun mismatch, continuity error, anachronism)
   - **Location** (scene number, character name, timestamp if available)
   - **Current state** (what's wrong now)
   - **Required fix** (what it should be)
   - **Severity** (critical / moderate / minor)

3. Create a structured correction list:
   ```
   [CRITICAL] Scene 3, Character: Alex - Age 24 but uses "we" (should be 23)
   [MODERATE] Scene 7 - Continuity: Eye color changes from blue to green
   [MINOR] Scene 2 - Anachronism: iPhone mentioned in 1995
   ```

4. Group by **error type** to enable batch fixes (all age errors together, all pronouns together, etc.)

---

## PHASE 2: Priority Ordering

**Fix in this exact order:**

### 1. **CRITICAL errors first:**
   - Age-pronoun mismatches (age must be fixed before pronoun context makes sense)
   - Character identity errors (wrong name)
   - Plot-breaking continuity errors
   - Timeline contradictions

### 2. **MODERATE errors next:**
   - Continuity issues (appearance, location)
   - Voice profile mismatches
   - Anachronisms
   - Setting inconsistencies

### 3. **MINOR errors last:**
   - Stylistic inconsistencies
   - Minor formatting issues
   - Optional improvements

**Why order matters:** Fixing age from 24→23 changes the *context* for other errors. Fix foundational data first.

---

## PHASE 3: Context-Aware Corrections

**For EACH error:**

### A. Read Surrounding Context
- Load the section/scene containing the error
- Read ±5 lines around the error location
- Understand *why* the current value exists

### B. Validate the Fix
- Check character sheet/bible for canonical truth
- If fixing age: verify against character's birthdate and story timeline
- If fixing pronouns: verify against character's profile
- If fixing continuity: check earlier scenes for consistency

### C. Safe Find-and-Replace Rules

**DO:**
- ✅ Use whole-word matching when fixing names/ages
- ✅ Verify each match before replacing (don't blindly replace all)
- ✅ Check if the error appears multiple times (fix all instances)
- ✅ Preserve formatting (markdown, indentation, quotes)

**DON'T:**
- ❌ Replace partial matches (e.g., "Alex" shouldn't match "Alexander")
- ❌ Change values inside comments or metadata unless specified
- ❌ Fix "errors" that are intentional (character lying about age, etc.)
- ❌ Alter timestamps, filenames, or system-generated content

### D. Make the Correction
- Apply the fix to the source file
- Preserve all formatting and structure
- Maintain line breaks and spacing

---

## PHASE 4: Verification After Each Fix

**After EVERY correction:**

1. **Re-read the corrected section** - Does it read naturally?
2. **Check for cascading issues:**
   - Did fixing age 24→23 create a new error elsewhere?
   - Does the pronoun still align with the new age context?
   - Are nearby sentences still coherent?

3. **Log the change:**
   ```
   ✅ Scene 3, Alex: Age 24 → 23 (aligned with birthdate 2001-05-10)
   ✅ Scene 3, Alex: Pronoun context verified - no cascade issues
   ```

4. **If a fix creates a NEW error:**
   - STOP
   - Document the conflict: "Fixing X breaks Y because..."
   - Propose a solution: "Need to also change Y to resolve"
   - Resume after resolving

---

## PHASE 5: Batch Validation

**After ALL corrections are complete:**

### A. Cross-Reference Check
- Re-verify key character data (ages, names, pronouns) across ALL scenes
- Ensure timeline is internally consistent
- Check continuity across scene boundaries

### B. Spot-Check Sample Scenes
- Read 3-5 random scenes in full
- Do they flow naturally?
- Any new errors introduced?

### C. Final Coherence Test
- Does the story still make sense end-to-end?
- Are character arcs preserved?
- No accidental plot holes created?

---

## PHASE 6: Output & Reporting

### A. Save Corrected Version
- Write corrected content to **CORRECTED.md** (or specified output file)
- Preserve original structure and formatting
- Include metadata header:
  ```markdown
  <!-- Corrected: [timestamp] -->
  <!-- Corrections: [N] errors fixed -->
  <!-- Audits processed: [list of audit files] -->
  ```

### B. Generate Correction Summary Report

**Required report format:**

```markdown
# Correction Summary Report

**Date:** [timestamp]
**Audits Processed:** [list of audit files]
**Total Errors Fixed:** [N]

---

## Changes Made

### CRITICAL (N fixes)
- ✅ Scene 3, Alex: Age 24 → 23 (reason: birthdate alignment)
- ✅ Scene 5, Jordan: Name "Chris" → "Jordan" (reason: character identity error)

### MODERATE (N fixes)
- ✅ Scene 7: Eye color "green" → "blue" (reason: continuity with Scene 2)
- ✅ Scene 9: "iPhone" → "pager" (reason: anachronism in 1995)

### MINOR (N fixes)
- ✅ Scene 2: Formatting inconsistency corrected

---

## Verification Status

- ✅ All corrections verified in context
- ✅ No cascading errors detected
- ✅ Spot-check: Scenes 1, 4, 7 read naturally
- ✅ Final coherence: Story remains consistent

---

## Edge Cases Encountered

[Document any issues where a fix created conflicts, or errors that require human review]

---

## Files Modified

- Original: [path]
- Corrected: CORRECTED.md
- Backup: [path if created]
```

**Save report to:** `audits/correction-summary.md`

---

## EDGE CASE HANDLING

**Scenario 1: Fix Creates New Error**
- Document conflict
- Propose multi-step resolution
- Do NOT apply incomplete fix

**Scenario 2: Contradictory Audit Reports**
- Flag discrepancy
- Default to character sheet/bible as source of truth
- Document decision

**Scenario 3: Ambiguous Context**
- When in doubt, PRESERVE original
- Flag for human review in report
- Do NOT guess

**Scenario 4: Bulk Replacements**
- ALWAYS verify each instance individually
- Context matters (e.g., age in dialogue vs. metadata)
- Log each replacement

**Scenario 5: No Audit Reports Found**
- Report: "No audit files detected in [directory]"
- Do NOT proceed with blind corrections
- Ask user for audit file location

---

## QUALITY GATES (Must Pass)

Before delivering CORRECTED.md:

- [ ] All critical errors addressed
- [ ] All moderate errors addressed
- [ ] All minor errors addressed
- [ ] No new errors introduced
- [ ] Formatting preserved
- [ ] Spot-check passed (sample scenes read naturally)
- [ ] Summary report generated
- [ ] Change log is complete and accurate

**If ANY quality gate fails:** Document why and request clarification.

---

## EXECUTION CHECKLIST

```
□ PHASE 1: Parse all audit reports → structured correction list
□ PHASE 2: Sort by priority (Critical → Moderate → Minor)
□ PHASE 3: Apply corrections context-safely (verify each fix)
□ PHASE 4: Verify after EACH correction (no cascade errors)
□ PHASE 5: Batch validation (cross-reference + spot-check)
□ PHASE 6: Save CORRECTED.md + generate summary report
□ FINAL: Quality gates passed ✅
```

---

**Now execute the corrections using this methodology.**
