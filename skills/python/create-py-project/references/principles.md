# Architecture Principles

Apply these principles when generating code:

- **KISS** - Keep solutions simple and straightforward
- **YAGNI** - Do not add functionality until needed
- **DevEx** - Optimize for developer productivity and clarity
- **Clean Architecture** - Separate concerns, dependency inversion, domain-centric
- **Orthogonal** - Components should be independent and composable
- **Practical** - Pragmatic solutions over theoretical purity
- **DDD** - Model the domain, ubiquitous language, bounded contexts

## Clean Architecture Applied

### Two-Layer Rule (KISS)

Keep architecture to two layers by default:

1. **`shared/`** - Infrastructure, clients, utilities (weak models)
1. **`modules/`** - Domain logic, services (strong models)

Add a third layer only with explicit justification and written ADR.

### Dependency Direction

Dependencies always flow inward:

- `modules/` → `shared/` (domain uses infrastructure)
- Never: `shared/` → `modules/` (infrastructure knows about domain)

### Thin Controllers, Thick Services

**Router/Controller layer (in `shared/`):**

- Minimal logic
- Input validation
- Call services from `modules/`
- Return responses
- Delegate ALL business logic to services

**Service layer (in `modules/`):**

- Contains ALL business logic
- Data transformation and mapping
- Business rules and validations
- Orchestration of multiple client calls
- Caching logic
- Error handling with business context
- Data enrichment and aggregation
- Services import from `shared/` (clients, config)
- Routers import from `modules/` (services)

This maintains proper architectural layering:

```text
Router (shared/) → Service (modules/) → Client (shared/)
```

## Import Conventions

### Forbidden Pattern

**NEVER use `from __future__ import ...`** in generated code:

- `from __future__ import annotations` - Not needed, use native type hints
- Any other `__future__` imports - Avoid entirely

**Why avoid `__future__` imports:**

- Indicates poor project structure or circular dependency issues
- Orthogonal design eliminates the need for deferred evaluation
- Modern Python versions (3.12+) support native type hint syntax
- Clean architecture prevents import cycles naturally
