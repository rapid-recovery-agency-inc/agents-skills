# Issue Format Specification

Unified issue format applicable to both `insightt-tickets` and `foundd-tickets` repositories.

## Title Format

Flexible patterns based on issue type:

**Standard Pattern:**

```text
[System/Scope] | [Platform] | [Concrete outcome]
```

Examples:

- `Scoring Engine | Add AGENTS.md Redirect for Windsurf Skills`
- `LexisNexis | Billing Spike Investigation: Dec 2025 - Jan 2026`
- `Web | Assignments Detail View | Deprecate CaseAddress Full Address field`

**Terse Standalone:**

```text
[Concrete outcome with context]
```

Examples:

- `Navigation dot moves away from navigation line when location/car info pops up`
- `Update logging in worker with configurable verbosity levels`

**Customer Support Pattern:**

```text
CS - [Company] (db_[id]) | [Module/Area] | [Issue summary]
```

Examples:

- `CS - Paramount (db_296) | Requesting A Timing Change For Their Company`
- `CS - 5280 Asset Recovery (db_385) | Creating Spotting Alert Error`

## Body Structure

### Universal Template

````markdown
[Executive Summary: 1-2 paragraphs explaining business need and current problem.
If issue is complex, more paragraphs may be included but minimize to reduce
cognitive friction and complexity.]

### WORK TO DO
- [ ] Action-oriented deliverable or validation step
- [ ] Another testable checkbox item
- [ ] 3-7 bullets usually

### RELATED ISSUES (only if present)
- #123 (dependency or prior attempt)
- owner/other-repo#456 (cross-repo links)

### SQL (optional)
Pretty printed code fenced SQL if applicable:
```sql
SELECT * FROM table WHERE condition = 'value';
````

### NOTES (optional)

- Context that doesn't fit elsewhere

````text

## Format Variants by Issue Type

### Bug Report

```markdown
[1-2 sentence problem summary]

### STEPS TO REPRODUCE
1. Step one
2. Step two

### EXPECTED
What should happen

### ACTUAL
What actually happens

### ACCEPTANCE CRITERIA
- [ ] Fix verified in staging
- [ ] Regression test added
- [ ] Edge cases handled
````

### Feature Request

```markdown
[Business value: why we need this]

### SPECS
- Key technical requirements
- Architecture notes
- API changes

### ACCEPTANCE CRITERIA
- [ ] Testable outcome
- [ ] Another outcome
- [ ] E2E tests passing

### FEATURE FLAG
- [ ] FLAG_NAME

### DEPENDENCIES
- #123 (blocking issue)
- Backend ticket for schema changes
```

### Investigation/Task

```markdown
[Goal/purpose of work]

### WORK TO DO
- [ ] Action item with checkbox
- [ ] Another deliverable
- [ ] Investigation step

### DATA / CONTEXT
[If applicable: SQL, schema, background, data sources]

### NEXT STEPS
- Follow-up actions after completion
```

### Customer Support (CS)

```markdown
[Client name and brief issue summary]

[Context from customer - what they reported]

[Screenshots or links to evidence]

[Additional context for dev team]
```

## Writing Principles

1. **Crystallized**: No filler, no hedging, no repeated context from title
1. **Outcome-oriented**: Actionable checkboxes, not vague tasks
1. **Flexible**: Structure adapts to bug reports, features, investigations, or CS tickets
1. **Concise**: Executive summary is key; keep it brief but informative
1. **Practical**: Focused on actionable outcomes, not just problem description
1. **Efficient**: Minimize cognitive load; smart defaults; only ask when unclear

## Acceptance Criteria Guidelines

Use declarative language (MUST/SHOULD/MAY) in acceptance criteria:

- **Good**: "[ ] Toggle MUST be visible in User Settings on Web, Mobile, and Tablet"
- **Avoid**: "Make sure the toggle works everywhere"

## Label Application

**Note:** Labels are discovered dynamically at runtime via `list_labels`. Never create labels; only use existing ones. If no matching labels exist, create the issue without labels.

Common label patterns to look for when matching:

| Issue Type       | Common Label Patterns                                   |
| ---------------- | ------------------------------------------------------- |
| Bug              | `bug`, `Bug`, `type/bug`                                |
| Feature          | `feature`, `enhancement`, `New-Feature`                 |
| Customer Support | `customer-support`, `CS`, `support`, `Customer-Support` |
| Platform         | `mobile`, `web`, `ios`, `android`, `Mobile`, `Web`      |
| Priority         | `priority/high`, `HIGH-PRIORITY`, `urgent`              |
| Design           | `Need-Design`, `design`, `needs-design`                 |

## Examples

### Example 1: Bug Report

```markdown
Uploaded spot photo not displayed in RHL until app is restarted.

### STEPS TO REPRODUCE
1. Spot a vehicle and attach a photo during the spotting flow
2. Submit the spot successfully
3. Navigate to the RHL to view the spot

### EXPECTED
Photo appears immediately in RHL alongside Evox images

### ACTUAL
Only Evox images shown; uploaded photo visible only after app restart

### ACCEPTANCE CRITERIA
- [ ] Photo appears immediately after upload
- [ ] Cache invalidation works correctly
- [ ] Test added for photo display in RHL
```

### Example 2: Feature Request

```markdown
Provide granular control over LPR Spot notifications to improve UX and prevent inbox fatigue.

### SPECS
- Update User Settings / Notifications Preference screen
- Add toggle for "LPR Spot" under notification settings
- Checkbox reads/writes to backend preference field
- Implement E2E tests

### ACCEPTANCE CRITERIA
- [ ] "LPR Spot Emails" toggle visible in User Settings on Web, Mobile, and Tablet
- [ ] Toggle successfully saves preference via API
- [ ] E2E tests implemented and passing

### FEATURE FLAG
- [ ] NOTIFICATIONS_LPR_SPOT_EMAIL

### DEPENDENCIES
- Backend ticket for GraphQL schema update
```

### Example 3: Investigation

```markdown
Investigate LexisNexis API billing spike in Dec 2025 (~60K requests) and Jan 2026 (~20K requests).
Suspected cause: Connex AI logic flaw triggering person searches for every VIN registrant.

### WORK TO DO
- [ ] Configure database access for lexnex-cache
- [ ] Execute volume analysis queries
- [ ] Calculate request type ratios
- [ ] Confirm or refute hypothesis
- [ ] Document findings and financial impact
- [ ] Transfer issue to appropriate repository once confirmed
```
