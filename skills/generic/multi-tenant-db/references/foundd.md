# Foundd — Multi-Tenant Database Reference

## Architecture

| Property          | Value                                                    |
| ----------------- | -------------------------------------------------------- |
| **Engine**        | PostgreSQL                                               |
| **Platform DB**   | `foundd_platform_db`                                     |
| **Routing table** | `client`                                                 |
| **Server table**  | `server`                                                 |
| **Tenant DBs**    | `foundd_{name}` (e.g., `foundd_ally`, `foundd_westlake`) |
| **Servers**       | 1 server, 2 clients                                      |
| **Region**        | us-east-2                                                |

## Routing — `client`

Key routing columns:

| Column                   | Purpose                                                    |
| ------------------------ | ---------------------------------------------------------- |
| `id`                     | UUID PK                                                    |
| `name`                   | Human-readable: `Ally`, `Westlake`                         |
| `rdn_client_id`          | RDN-side client identifier (unique)                        |
| `rdn_client_ids_aliases` | `text[]` — additional RDN client IDs mapped to this tenant |
| `db_name`                | Database name: `foundd_ally`, `foundd_westlake`            |
| `server_id`              | FK to `server.id`                                          |

**Current clients:**

| Name     | rdn_client_id | Aliases   | db_name         |
| -------- | ------------- | --------- | --------------- |
| Westlake | 201883        | —         | foundd_westlake |
| Ally     | 1951513       | [1321075] | foundd_ally     |

**⚠️ Alias gotcha:** Ally's alias `1321075` routes RDN hits with client_id=1321075 to `foundd_ally`. Both 1951513 and 1321075 contribute to Ally's LPR hit volume.

**Server table:**

| Column            | Purpose                                                    |
| ----------------- | ---------------------------------------------------------- |
| `id`              | Serial PK                                                  |
| `secret_name`     | AWS Secrets Manager secret (e.g., `dev/foundd/database-1`) |
| `aws_region_name` | AWS region (e.g., `us-east-2`)                             |

Credentials never appear inline; the system fetches them from AWS Secrets Manager at runtime.

## Schema Uniformity

All client databases (`foundd_ally`, `foundd_westlake`) share an identical 55-table schema — no extra tables in either. No `client_id` column exists; tenant identity is implicit in which database you connect to.

## Tenant Database Internal Patterns

Within each tenant database, tables organize into subsystems by namespace prefix:

| Namespace    | Tables | Subsystem                                                          |
| ------------ | ------ | ------------------------------------------------------------------ |
| `hotspot_*`  | 5      | Hotspot clusters, scores, scoring logs, check-in usage, user locks |
| `check_in_*` | 5      | Field agent check-ins, reports, answers, media uploads, reviews    |
| `account_*`  | 4      | Accounts, events, locks, phases                                    |
| `vehicle_*`  | 4      | Vehicles, owners, registrations, vehicle-owner mapping             |
| `address_*`  | 4      | Addresses, overwrites, parsing errors, position overrides          |
| `rdn_*`      | 3      | RDN agent users, case events, update events                        |
| `lex_nex_*`  | 3      | LexisNexis address, person, and vehicle searches                   |
| `insightt_*` | 2      | Insightt repossession and spotted events                           |
| `case_*`     | 2      | Case-address mapping, case events                                  |
| `location_*` | 2      | Locations and location types                                       |

**`location` is the central bridge table** — it links `case_id`, `address_id`, and `hotspot_id`. No single "hub" table dominates, but `location` is the only one bridging all three FK types:

```
account_id → account_event, account_lock, account_phase, inbox_item, sync_log
case_id    → case_address, case_event, check_in, location, lex_nex_address, repossessed_collateral, spotted_collateral
hotspot_id → hotspot_log, hotspot_score, hotspot_user_lock, check_in_report, location
address_id → address_position_override, case_address, check_in, check_in_report, lex_nex_address, location, lpr_purchased_hit, repossessed_collateral, spotted_collateral
```

**Important:** Tenant DBs do NOT have `spotted_vehicle_report` or `lpr_spotted_vehicle_report` tables. The equivalents are `spotted_collateral` (manual vehicle sightings) and `insightt_spotted_event` (LPR-triggered events from Insightt).

## Auth — `user_user_role`

Users have role assignments via `user_user_role` (in platform_db, not tenant DBs):

| Column         | Purpose                                                  |
| -------------- | -------------------------------------------------------- |
| `user_id`      | FK to `user`                                             |
| `user_role_id` | FK to `user_role`                                        |
| `client_id`    | Optional — scopes role to a specific client (e.g., Ally) |
| `agent_id`     | Optional — scopes role to a specific agency              |

Role distribution: FOUNDD_AGENT (28), AGENT_USER (13), CLIENT_USER (11), INTERNAL (5).

## Billing

Billing is minimal — no subscription tables in platform_db. With only 2 clients, billing is likely separate or N/A.

## MCP Tools

| Tool                                    | Connects To                       |
| --------------------------------------- | --------------------------------- |
| `foundd_execute_sql_platform_db`        | `foundd_platform_db` (PostgreSQL) |
| `foundd_search_objects_platform_db`     | `foundd_platform_db` (PostgreSQL) |
| `foundd_execute_sql_client_ally`        | `foundd_ally` database            |
| `foundd_search_objects_client_ally`     | `foundd_ally` database            |
| `foundd_execute_sql_client_westlake`    | `foundd_westlake` database        |
| `foundd_search_objects_client_westlake` | `foundd_westlake` database        |

## Other platform_db Tables

| Table                                   | Rows | Purpose                                                            |
| --------------------------------------- | ---- | ------------------------------------------------------------------ |
| `agent`                                 | 1    | Repossession agency info                                           |
| `user`                                  | 29   | Cognito-linked user accounts                                       |
| `user_role`                             | 4    | Role definitions (FOUNDD_AGENT, AGENT_USER, CLIENT_USER, INTERNAL) |
| `user_role_permission`                  | 915  | Fine-grained permission grants                                     |
| `feature_flag`                          | 27   | Per-client or global feature toggles                               |
| `system_setting`                        | 16   | Global scoring parameters — also mirrored in each tenant DB        |
| `user_location_tracking`                | 141K | GPS tracking records                                               |
| `session`                               | ~580 | Auth sessions                                                      |
| `email_log`                             | ~540 | Email delivery tracking                                            |
| `scoring_engine_request_logger_request` | 1    | Scoring request log                                                |
| `_prisma_migrations`                    | 32   | ORM migration tracking (Prisma)                                    |

## Foot Guns

- **`foundd_platform_db` ≠ `platform_db`.** A separate dead `platform_db` database exists on the same Postgres server. Do not use it.
- **Platform DB cannot join client DBs** — they are separate PostgreSQL instances. Cross-database queries require two round-trips.
- **`system_setting` exists in both platform_db and tenant DBs** — platform_db uses the `name` column; tenant DBs use `key`. Both hold the same 16 settings.
