---
name: create-github-issue
description: Create GitHub issues in the appropriate -tickets repository based on source repo family. Performs duplicate detection and produces crystallized, outcome-oriented issue content. Use when a user request implies creating a ticket from code context, discussion, or identified work.
compatibility: Designed for agent runtimes that support Agent Skills and GitHub MCP integration.
---

# Create GitHub Issue

Create well-formed GitHub issues in the correct tickets repository (`insightt-tickets` or `foundd-tickets`) based on source repository context. Follows a research-first approach to avoid duplicates and produces terse, outcome-oriented issue content.

> **Agent Directive:** Assume the [create-github-issue agent persona](agents/github-issue-agent.md) when executing this skill.

## Execution Flow

Follow this sequence. Each phase gates the next. Do not skip the user confirmation step.

### Phase 1: Discovery

#### 1. Determine Target Repository

- Extract source repository from context (active file path, user mention, or explicit repo name)
- Apply org family detection:
  - If repo name contains "insightt" → target `rapid-recovery-agency-inc/insightt-tickets`
  - If repo name contains "foundd" → target `rapid-recovery-agency-inc/foundd-tickets`
  - If unclear → check MCP memory for org hints
  - If still unclear → ask user to confirm target repo
- Validate detected target repo:
  - Check if target repo is accessible (use GitHub MCP if available)
  - If not accessible, fall back to asking user for correct repo
  - Prevents routing to archived/legacy repos like "insightt-archive"

#### 2. Gather Context (Evidence-First)

- Aggressively gather evidence before asking user anything. See [references/module-research.md](references/module-research.md).
- Identify: repo name, affected system, problem, expected outcome, scope clues
- Optionally check for `.github/ISSUE_TEMPLATE/` files in target repo (low priority, non-blocking):
  - If templates exist, extract useful hints (e.g., required fields, specific labels mentioned)
  - Use as supplementary guidance only; never let templates override skill's format
  - Primary behavior: always use skill's own format from [references/issue-format.md](references/issue-format.md)
- Apply **Question Priority Discriminator** if questions needed:
  - **P0 (Critical):** Blocks creation (wrong repo, ambiguous scope) → Ask immediately
  - **P1 (High):** No business problem inferable → Ask if no evidence
  - **P2 (Medium):** Improves quality but draft usable without → Infer and draft
  - **P3 (Low):** Formatting preferences → Never ask; skill owns these
- Default: Make smart assumptions for P2/P3. Only ask P0/P1.

#### 3. Duplicate Detection

- Search the **target tickets repo** (not source repo) using:
  - Exact symptom search: distinctive error messages or problem descriptions
  - Feature/domain search: component names, modules, or feature areas
  - Outcome search: similar desired outcomes or acceptance criteria
- Use `search_issues` with concise queries, then `issue_read` to inspect suspected duplicates
- Decision:
  - Clear duplicate with open status → Add comment via `add_issue_comment`, stop here
  - Related but distinct → Proceed, will reference in RELATED ISSUES
  - No duplicates → Proceed
  - Ambiguous → Proceed, will create with explicit scope and link related

### Phase 2: Draft Creation

#### 4. Generate Issue Draft

- Select format variant from [references/issue-format.md](references/issue-format.md) based on detected type:
  - Bug → Use Bug Report template
  - Feature request → Use Feature Request template
  - Investigation/analysis → Use Investigation/Task template
  - Customer support → Use CS template
- Apply crystallized writing from [references/technical-writing.md](references/technical-writing.md):
  - No filler text
  - No hedging unless uncertainty matters
  - No repeated context from title in body
  - Use MUST/SHOULD/MAY for acceptance criteria
- Draft the complete issue (title + body) but **do not submit yet**

#### 5. Select Labels (Optional)

- Use `list_labels` to fetch available labels from target repo
- Intelligently match content patterns to available labels:
  - Error/bug/crash → look for `bug`, `Bug`, `type/bug` variants
  - Customer mention → look for `customer-support`, `CS`, `support`
  - New feature → look for `feature`, `enhancement`, `New-Feature`
  - Platform mentions → look for `mobile`, `web`, `ios`, `android`
  - Priority indicators → look for `priority/high`, `HIGH-PRIORITY`, `urgent`
- Select matching labels (case-insensitive, handle variations)
- **Never create labels**, only use existing ones
- If no labels match or `list_labels` unavailable, proceed without labels

#### 6. Assign to Project (Optional)

- Check if target repo has existing "Backlog" project (use GitHub MCP if available)
- If "Backlog" project exists, prepare to add issue to it after creation
- **Never create projects**, only use existing ones
- If no "Backlog" project exists, skip project assignment
- Keep as silent/automatic behavior (P3 - never ask user)

### Phase 3: Review and Confirm

#### 7. Present Draft for User Review

**CRITICAL:** Before creating the issue, present the complete draft to the user:

I've prepared a draft issue for {target_repo}:

______________________________________________________________________

**Title:** [Draft title here]

**Body:**
[Draft body here in full]

**Labels:** [Selected labels or "None"]

______________________________________________________________________

**Target Repository:** {target_repo}
**Duplicate Check:** [Summary of duplicate search results]

Does this look correct? Reply with:

- **"OK"** or **"yes"** → I will create the issue

- **"Edit: [specific change]"** → I will revise and re-present

- **"Cancel"** → I will discard the draft

- Wait for explicit user confirmation

- Do not proceed to Phase 4 without user approval

- If user requests edits, revise and re-present (return to Phase 2)

### Phase 4: Submission

#### 8. Submit Issue (After User Confirmation)

- Use `issue_write` with `method=create` using the confirmed draft
- If "Backlog" project was identified in step 6, add issue to project after creation
- If creation fails, report specific error and offer to retry or save draft

#### 9. Confirm and Output

- Output: "Issue created: [URL as clickable link]"
- Brief summary of what was created
- Stop. Do not proceed further without new user input.

## Tool Configuration

### Tool Priority Hierarchy

| Priority | Tool Source               | Detection                  | Usage                                                                                |
| -------- | ------------------------- | -------------------------- | ------------------------------------------------------------------------------------ |
| 1st      | `github-mcp-server` (MCP) | MCP tools available        | Use `issue_write`, `search_issues`, `issue_read`, `add_issue_comment`, `list_labels` |
| 2nd      | `gh` CLI                  | `which gh` returns path    | Use `gh issue create`, `gh issue list`, `gh issue view`, `gh issue comment`          |
| 3rd      | None available            | Neither MCP nor `gh` found | Short-circuit: output issue content as markdown code fence in chat                   |

### Short-Circuit Mode (No Tools)

When neither MCP nor `gh` CLI is available:

1. Do not attempt to post the issue
1. Do not ask user to install tools
1. Output the fully formatted issue content in a markdown code fence in chat
1. Include a note: "GitHub tools not available. Issue content prepared above — copy/paste to create manually."
1. At the very end, provide a helpful hint: "Setting up `github-mcp-server` or `gh` CLI tool would allow automatic submission of the issue."

## Quality Bar

"Crystallized" means:

- No filler text
- No hedging unless uncertainty matters
- No repeated context from title in body
- No mixing business need with implementation speculation
- Reads like a clean PM/eng ticket, not a chat transcript

## Error Handling

| Error                         | Response                                              |
| ----------------------------- | ----------------------------------------------------- |
| Issue creation fails          | Log error, inform user with specific failure reason   |
| Duplicate detection ambiguous | Note uncertainty in body, proceed with explicit scope |
| Target repo inaccessible      | Inform user which repo was targeted and why           |
| Label selection fails         | Create issue without labels, note in response         |
| User cancels at review        | Discard draft, confirm cancellation                   |

## Trigger Phrases

Activate this skill when user says:

- `create an issue for this`
- `file a ticket`
- `should we open an issue`
- `this needs a ticket`
- `track this in GitHub`
- `create a GitHub issue`

## References

- [Issue Format Specification](references/issue-format.md)
- [Technical Writing Standard](references/technical-writing.md)
- [Module Research Methodology](references/module-research.md)
- [Agent Skills Specification](https://agentskills.io/specification)
- [GitHub MCP Server](https://github.com/github/github-mcp-server)
