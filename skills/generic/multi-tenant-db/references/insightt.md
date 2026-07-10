# Insightt — Multi-Tenant Database Reference

## Architecture

| Property          | Value                                                    |
| ----------------- | -------------------------------------------------------- |
| **Engine**        | MySQL                                                    |
| **Platform DB**   | `platform_db` (co-located on server_1)                   |
| **Routing table** | `platform_companies`                                     |
| **Server table**  | `server`                                                 |
| **Tenant DBs**    | `rra_db` (company_id=1, legacy) + `db_{id}` (all others) |
| **Servers**       | 6 servers (ids: 1, 3-7; no id=2), ~179 tenants           |
| **Region**        | us-east-2                                                |

## Routing — `platform_companies`

Key routing columns:

| Column               | Purpose                                                                                |
| -------------------- | -------------------------------------------------------------------------------------- |
| `id`                 | Company ID, used for `db_{id}` naming                                                  |
| `name`               | Agency name                                                                            |
| `db_name`            | Schema name: `rra_db` or `db_{id}`                                                     |
| `server_id`          | FK to `server` table                                                                   |
| `status`             | ENUM: `approved`, `pending`, `rejected`, `suspended`, `marked_for_deletion`, `removed` |
| `rdn_key`            | RDN API key                                                                            |
| `drn_key`            | DRN API key (UUID; `"0"` = disabled; NULL = never configured)                          |
| `stripe_customer_id` | Link to Stripe billing                                                                 |
| `db_username`        | Per-tenant DB username                                                                 |
| `db_user_password`   | Per-tenant DB password                                                                 |

**Server topology:**

| Server | Capacity | Tenants   | Secret Name                |
| ------ | -------- | --------- | -------------------------- |
| 1      | 30       | 33 (over) | `main/insightt/database-0` |
| 3      | 40       | 39        | `main/insightt/database-1` |
| 4      | 40       | 39        | `main/insightt/database-2` |
| 5      | 40       | 37        | `main/insightt/database-3` |
| 6      | 40       | 16        | `main/insightt/database-4` |
| 7      | 40       | 15        | `main/insightt/database-5` |

**Co-location:** `platform_db` and server_1 tenant schemas share the same MySQL instance. Cross-schema joins work within server_1. Servers 3-7 require separate connections.

## Schema Uniformity

Tenant databases share the same core schema but **diverge**. The legacy tenant `rra_db` has 4 extra tables (`bonuses`, `platform_companies`, `platform_roles`, `platform_users`) absent from other tenants. Feature-gated tables vary widely in row count (e.g., `drn_purchased_hit_cluster`: 78K in rra_db, 0 in db_114). Migrations run across all tenants but conditionally create or gate some feature tables.

## Tenant Database Internal Patterns

Within each tenant database, tables organize into subsystems by namespace prefix:

| Namespace                | Tables | Subsystem                                                                                       |
| ------------------------ | ------ | ----------------------------------------------------------------------------------------------- |
| `rdn_*`                  | 21     | RDN case details — updates, repossessions, events, logs, lender, lienholder, branch assignments |
| `drn_*`                  | 11     | LPR data pipeline — hits, camera scans, clusters, reviews, cluster assignments                  |
| `shift_*`                | 6      | Agent shift scheduling and time tracking                                                        |
| `checklist_*`            | 6      | Inspection checklists, items, questions, responses                                              |
| `spotted_*`              | 5      | Agent spotted-vehicle reports, notes, photos                                                    |
| `user_*`                 | 4      | Insightt user accounts, branch assignments, commissions                                         |
| `collateral_*`           | 3      | Vehicle collateral records                                                                      |
| `task_*`                 | 3      | Task management                                                                                 |
| `target_recovery_rate_*` | 3      | Lender/lienholder recovery rate targets                                                         |
| `camera_*`               | 2      | Legacy non-DRN camera tables (not part of the DRN pipeline)                                     |
| PascalCase               | 5+     | `cases`, `CaseAddress`, `Cache`, `Infraction`, `MissedRepossession`                             |

**`cases` is the central hub.** Explore from `cases.case_id` and join outward through namespace subsystems.

**Query discipline:** Always constrain queries to a recent time window (max 3-4 days). Unbounded queries against large tables like `rdn_case_event` (49M+ rows) will time out. Use `WHERE created_at >= ... AND created_at < ...` on every query.

## Shared Reference Enumerations — `Rdn*` Tables

12 tables in `platform_db`. 11 follow the same 5-column pattern. **One exception: `RdnEventType`** has an extra `description` (VARCHAR, nullable) column.

```
id          INT AUTO_INCREMENT  (surrogate, unused by tenants)
rdn_id      VARCHAR(N)          (authoritative exchange code)
type        VARCHAR             (human-readable label)
created_at  DATETIME
updated_at  DATETIME
```

**Tables:** `RdnAddressType`, `RdnBankruptcyType`, `RdnDocumentType`, `RdnEventType`, `RdnKeyType`, `RdnOdometerType`, `RdnOverallConditionType`, `RdnPhoneFlagType`, `RdnPhonePartyType`, `RdnPhoneType`, `RdnUpdatePriority`, `RdnUpdateType`

Tenant tables reference these via `rdn_id` codes. These codes follow the RDN industry standard — consistent across all tenants and external RDN partners.

## Billing & Subscription

| Table                          | Purpose                                                                |
| ------------------------------ | ---------------------------------------------------------------------- |
| `subscription_details`         | Plan tier definitions (Basic/Advanced, per-user pricing)               |
| `company_subscription_details` | Maps company to active plan                                            |
| `company_payment_method`       | Payment methods per company                                            |
| `stripe_*` (7 tables)          | Stripe payment integration (subscriptions, prices, invoices, webhooks) |

Join `platform_companies` with `company_subscription_details` to determine active vs inactive tenants.

## MCP Tools

| Tool                                         | Connects To                                                            |
| -------------------------------------------- | ---------------------------------------------------------------------- |
| `insightt_execute_sql_platform_db`           | **Insightt Platform DB (MySQL 8.0)** — the actual Insightt platform_db |
| `insightt_search_objects_platform_db`        | Insightt Platform DB (MySQL 8.0)                                       |
| `insightt_execute_sql_server_1_tenant_db`    | Server 1 MySQL — `platform_db` + all server_1 tenant schemas           |
| `insightt_search_objects_server_1_tenant_db` | Server 1 MySQL                                                         |

**Note:** Both "platform_db" tools connect to the same Insightt platform_db (MySQL). The LPR Classifier runs on a separate Postgres database not accessible through these MCP tools.

**⚠️ No MCP access to servers 3-7.** Only server_1 tenants support MCP queries.

## Other platform_db Tables (45 total)

### Routing & Platform

| Table                              | Rows   | Purpose                                          |
| ---------------------------------- | ------ | ------------------------------------------------ |
| `platform_users`                   | ~7,600 | Cross-tenant user accounts                       |
| `platform_roles`                   | 9      | 9-role hierarchy                                 |
| `platform_locations`               | ~1.7M  | Cross-tenant location tracking (lat/lng/address) |
| `platform_settings`                | ~35    | App-wide settings                                |
| `platform_log`                     | ~17    | Audit log                                        |
| `registration_requested_companies` | ~59    | Pre-registration queue                           |
| `platform_company_sessions`        | 0      | Session tracking                                 |
| `platform_invitation_tokens`       | ~2     | Invitation tokens                                |
| `platform_password_reset_tokens`   | ~10    | Password reset tokens                            |

### RDN Reference

| Table             | Rows | Purpose                        |
| ----------------- | ---- | ------------------------------ |
| `rdn_company_key` | ~164 | Per-company RDN API key config |

### Feature Flags & Identity

| Table                 | Rows | Purpose                |
| --------------------- | ---- | ---------------------- |
| `feature_flag`        | ~369 | Feature toggles        |
| `identity_sync_event` | ~362 | Identity sync tracking |

### Infrastructure

| Table           | Rows | Purpose            |
| --------------- | ---- | ------------------ |
| `SequelizeMeta` | ~100 | Migration tracking |
| `cache`         | ~140 | App cache          |
