---
name: multi-tenant-db
description: Use when deciding which database MCP tool to call, routing between platform vs tenant databases, looking up tenant or company info, or any task referencing routing tables (platform_companies, client, server) or tenant data tables (address_*, case_*, hotspot_*, lpr_*, drn_*).
version: 1.0.0
license: MIT
---

# Multi-Tenant Database Patterns

Two database systems share recurring architectural patterns. Recognize them to avoid repeated schema exploration and wrong-tool mistakes.

## When to Use

Triggers that should load this skill:

- Deciding **which database MCP tool** to call — platform vs tenant source
- Mentioning a **tenant or company** by name
- Mentioning **routing tables** (`platform_companies`, `client`, `server`)
- Mentioning **tenant data tables** (e.g. `address_*`, `case_*`, `hotspot_*`, `lpr_*`, `drn_*`)
- Questions about **server capacity**, **tenant isolation**, or **schema uniformity**
- Figuring out whether data lives in **platform DB vs tenant DB**
- Any **DRN/RDN/LPR routing question** — which tenant does this data belong to?
- Looking up a tenant's **db_name**, **server_id**, or credentials
- Reasoning about **shared reference data** across tenants (enumeration tables, system settings)

## Patterns

### 1. Multi-Tenant Routing

A platform database indexes tenants across servers.

**Why:** A single RDS instance supports limited tenants (~30-40). Multiple servers scale horizontally.

**Components:**

- **Platform database** — routing table (tenant → `server_id` + `db_name`), server table (→ credentials), subscription data, shared references
- **Tenant databases** — one per tenant, isolated at the database level (no `tenant_id` column)
- **Server instances** — RDS hosts tracked by capacity and AWS Secrets

**Flow:** `App → platform.routing_table → server_table → AWS Secrets → tenant_db`

**Naming:** `db_{id}` or `{prefix}_{name}`. Legacy exceptions exist for first tenants predating multi-tenancy.

### 2. Schema Uniformity

Tenant databases share the same core schema. Migrations run in lockstep. Only the platform database differs.

**Implication:** Examine one tenant to understand all of them, but verify for feature-gated extras in legacy tenants.

### 3. Shared Reference Enumerations

Platform database hosts enumeration tables that all tenants reference via short exchange codes.

**Structure:** `exchange_code` (authoritative key) + `human_label` + timestamps. Codes stay consistent across tenants and external partners.

**Usage:** Tenant tables store codes, not labels (e.g., `address_type = "1"` = "Borrower - Home").

### 4. Billing & Subscription

Platform database tracks tenant plans, active status, and payment integration. Join the routing table with subscription tables to identify active tenants.

### 5. Which MCP Service? (Insightt vs Foundd)

Two separate MCP services, each with their own database infrastructure. Route by question type:

| Question / Task                                                                     | MCP Service  | Why                                                      |
| ----------------------------------------------------------------------------------- | ------------ | -------------------------------------------------------- |
| **Agency/company lookup** by name ("who is Rapid?", "what server is company X on?") | **Insightt** | `platform_companies` table lives in Insightt platform DB |
| **Tenant routing** — find server_id, db_name for a company                          | **Insightt** | Platform DB has the routing table                        |
| **LPR/DRN data** — scans, purchased hits, camera hits                               | **Insightt** | LPR Classifier and DRN data live in Insightt tenant DBs  |
| **Tenant application data** — cases, addresses                                      | **Insightt** | Application tables in tenant MySQL schemas               |
| **Hotspot scores, repossession events**                                             | **Foundd**   | Scoring engine data lives in Foundd Postgres             |
| **Client-specific data** (Ally, Westlake)                                           | **Foundd**   | Isolated client DBs under Foundd                         |

**Default direction:** If in doubt about which MCP, ask: "Is this about the *agency/company* itself (Insightt) or about *scoring/hotspot outcomes* (Foundd)?"

### 6. MCP Tool Routing

MCP tools mirror the database split — each database in the TOML config generates two tools per source: one for executing SQL, one for schema exploration.

**The naming pattern is `{service}_{action}_{source_id}`:**

- `{service}` — the MCP server name (e.g. `insightt`, `foundd`)
- `{action}` — what the tool does (`execute_sql`, `search_objects`)
- `{source_id}` — the source ID from the TOML config (e.g. `platform_db`, `server_1_tenant_db`, `client_ally`)

**The routing rule is always the same:**

- **Platform source** → platform database (routing, references, billing, auth)
- **Tenant sources** → per-tenant databases (application data: cases, hotspots, scores)

When in doubt, check the TOML config or reference files for the exact source IDs and tool names.

## Reference Documents

| System                  | Reference                                          |
| ----------------------- | -------------------------------------------------- |
| **DBHub** (MCP Gateway) | [`references/dbhub.md`](references/dbhub.md)       |
| **Insightt** (MySQL)    | [`references/insightt.md`](references/insightt.md) |
| **Foundd** (PostgreSQL) | [`references/foundd.md`](references/foundd.md)     |

## Key Foot Guns

- `foundd_platform_db` ≠ `platform_db` — a dead `platform_db` exists on the same server. See [foundd.md](references/foundd.md).
- Not all servers are reachable via MCP. Check the reference files.
