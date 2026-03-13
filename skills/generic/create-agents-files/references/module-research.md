# Module Research Reference

## Purpose

Understand a target module well enough to explain what it owns, exposes, how it's wired, how it's used, and what constraints shape changes to it.

## Operating Principle

**Start narrow. Expand only through evidence. Be flexible and inquisitive.**

Investigate the target module and its direct neighborhood, not the whole repository. Use broad codebase packing only as scoped escalation, never as default.

## Investigation Scope

### Strategic Scope

Understand the module as a system boundary:

- Which feature or business capability it serves
- Which layer or subsystem it belongs to (domain, orchestration, adapter, shared utility)
- Which upstream callers and downstream dependencies matter
- Bounded context and integration points

### Tactical Scope

Understand the module internally:

- Public API and exported surface
- Control flow and data flow
- State management and invariants
- Error handling and side effects
- Tests and contracts

## Investigation Strategies

### 1. Symbolic and Lexical Search

**Tool**: `rg` (ripgrep) - recursive, `.gitignore`-aware, supports file filters and context lines.

**Use when**: You know the module path, symbol, or feature term.

```bash
# Find imports and usage
rg -n "TargetModule|TargetSymbol" path/to/module path/to/tests

# Find import statements
rg -n "from '.*target-module.*'|require\\('.*target-module.*'\\)" src tests

# Find configuration references
rg -n -C 3 "feature_flag|config_key|route_name" src config tests

# Type-specific search
rg -n -t ts "TargetSymbol" src tests

# List module files
rg --files path/to/module

# Escalate to unfiltered search if needed
rg -n -uu "TargetSymbol" .
```

#### Finding All Call Sites

**Critical**: Always verify actual usage, not just imports.

```bash
# Find function/method invocations
rg -n "targetFunction\(" src tests

# Find class instantiations
rg -n "new TargetClass\(" src tests

# Find property/method access
rg -n "\.targetMethod\(" src tests

# Combine import and usage verification
rg -n "from.*TargetModule" src | cut -d: -f1 | sort -u | \
  xargs -I {} rg -n "targetSymbol" {}
```

**Verify call sites by**:

- Reading surrounding context (`-C 3` flag)
- Checking if usage is conditional or always executed
- Identifying test vs production usage
- Noting deprecated or commented-out calls

### 2. Concept Location

**Use when**: Business terms and code terms differ.

Search for feature concepts, then connect results by dependencies and nearby symbols. Combine textual search with dependency exploration to locate features.

### 3. Software Reconnaissance

**Use when**: Runtime wiring matters more than static names (DI, registries, plugins, framework conventions).

Observe execution traces and intersect with static reading. Execution evidence reveals dynamic dispatch and runtime configuration.

### 4. Hypothesis-Driven Investigation

Work in short loops:

1. Gather evidence
1. Form hypothesis
1. Test it
1. Update model

Keeps search tight and avoids repository-wide wandering.

### 5. Code Archaeology

For unclear or legacy modules:

- Trust code and tests over comments
- Inspect compatibility seams and adapters
- Compare docs to current code carefully
- Note naming drift and historical layers

Implementation and tests dominate current-state understanding.

## Initial Context Pass

If IDE context tools are available, use them for **scoped initial map**:

1. Detect availability first
1. Constrain to target module or small neighborhood
1. Get module tree, exported symbols, immediate dependents/dependencies
1. Identify entry points, adapters, tests

**Good uses**:

- Module structure overview
- Public surface inspection
- Direct dependency graph
- Entry point identification

**Avoid**:

- Whole-repo indexing by default
- Global architecture summaries before understanding target
- Using compressed context as substitute for call-site verification

## Tool Tactics

### ripgrep (`rg`)

Default discovery tool for targeted search.

### `sed`

Read narrow windows around matches:

```bash
sed -n '1,220p' path/to/module/index.ts
sed -n '80,180p' path/to/module/service.ts
```

### `cat`

Only for short, already-selected files.

### IDE Context Tools

Use only after anchoring on target module path, symbol, or feature term. Request:

- Module summary
- Exported surface
- Direct dependents and dependencies
- Related tests
- Runtime entry points

Verify important claims with local search and file reads.

### `repomix`

**Only use as scoped escalation.**

Detect availability first:

```bash
which repomix
```

Aim at target area, not whole repository:

```bash
# Target specific module
repomix path/to/module

# Include module and tests
repomix --include "path/to/module/**/*,path/to/tests/**/*"

# Include module, shared contracts, exclude generated
repomix --include "path/to/module/**/*,src/shared/contracts/**/*" \
  --ignore "**/*.snap,**/dist/**,**/generated/**"
```

Use when module context is too fragmented to reconstruct with `rg` and narrow file reads.

## Reading Order

1. Module entry point and exports
1. Main orchestrator or public API
1. Direct consumers
1. Direct collaborators
1. Tests
1. Config and wiring
1. Adapters and boundary translators

## Deliverables

### Module Summary

- Purpose
- Key exports
- Major dependencies
- Major consumers

### Usage Map

- Direct call sites
- Indirect wiring (if proven)
- Tests covering the module

### Boundary Map

- What the module owns
- What is external
- Where translation, IO, or framework binding happens

### Open Questions

- Ambiguous runtime behavior
- Dynamic dispatch still unverified
- Missing tests or unclear contracts

## Synthesis Pass

Once evidence gathering is complete, perform deep synthesis to understand the module's practical role.

**Goal**: Answer "How does this module fit into the project, and in an extremely practical sense, what is its 'flow', how is it used and why?"

### Synthesis Questions

1. **What problem does this module solve?** - Not what it does technically, but what business or system need it addresses
1. **Why does it exist separately?** - What boundary, concern, or responsibility justified its extraction
1. **What would break if it were removed?** - Trace impact through call sites and dependent flows
1. **What patterns does it enable?** - How do consumers use it? What workflows does it support?
1. **What constraints does it enforce?** - Invariants, validations, or contracts it maintains
1. **Where does it fit in the request/response cycle?** - Entry point, middleware, domain logic, persistence, or response formatting

### Synthesis Method

Use sequential thinking (if available) or structured reasoning to:

1. Review all gathered evidence (exports, call sites, tests, config, boundaries)
1. Identify the module's position in the system's conceptual architecture
1. Trace concrete usage scenarios from entry point to completion
1. Synthesize a practical narrative: "When X happens, this module does Y because Z"
1. Validate synthesis against evidence - every claim must have a call site or test backing it

**Output**: A concise practical description grounded in observed behavior, not inferred intent.

## Decision Rules

**Always be flexible and reactive.** These are guidelines, not rigid constraints. Adjust your approach based on what the evidence reveals.

### Stay Narrow When

- Direct imports and call sites explain the feature
- Tests cover core behavior
- Runtime wiring is obvious

### Expand Tactically When

- DI, factories, registries, or plugins obscure usage
- Config or flags drive behavior
- Names don't match business terms

### Expand Strategically When

- Module crosses subsystem boundaries
- Multiple consumer groups use it differently
- Module acts as shared infrastructure

## Stop Condition

Stop when you can answer with evidence:

- What the module does
- How it is invoked
- Who depends on it
- What it depends on
- Which paths are core versus incidental
- What remains uncertain

## Anti-Patterns

Avoid:

- Whole-repo summarization before module location
- Whole-repo `repomix` by default
- Long file dumps without hypothesis
- Trusting docs over code and tests
- Claiming runtime usage from imports alone
