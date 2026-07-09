# DBHub — MCP Database Gateway

DBHub bridges databases to AI agents via the Model Context Protocol (MCP). It runs as Docker containers, each serving one platform. See [github.com/bytebase/dbhub](https://github.com/bytebase/dbhub) for full documentation.

## Location

```
~/.dbhub/
├── .env                  Credentials (never commit)
├── compose.yml           Docker Compose — one container per platform
├── generate_config.py    Auto-discovers tenants from platform_db
├── {platform}.toml       Auto-generated per-platform DB configs
└── README.md             Full docs
```

## Architecture

**One Docker container per platform.** Each container reads a TOML config that lists every database connection as a `[[sources]]` entry. DBHub exposes these sources as MCP tools over HTTP.

**Wiring:** Containers are mapped to local ports in `compose.yml`, then registered as remote MCP servers in `~/.config/opencode/opencode.json`:

```json
"insightt": { "type": "remote", "url": "http://localhost:18081/mcp" },
"foundd":   { "type": "remote", "url": "http://localhost:18082/mcp" }
```

## TOML Config Pattern

Each `[[sources]]` entry defines one database connection:

```toml
[[sources]]
id = "platform_db"
name = "Foundd Platform Database"
dsn = "postgresql://user:pass@host:5432/dbname?sslmode=disable"

[[sources]]
id = "client_ally"
name = "Ally (foundd_ally)"
dsn = "postgresql://user:pass@host:5432/foundd_ally?sslmode=disable"
```

**Fields:**

- `id` — Short identifier, becomes part of the MCP tool name
- `name` — Human-readable label
- `dsn` — Full connection string: `{protocol}://{user}:{pass}@{host}:{port}/{db}`

**Source ID → MCP tool name convention:**

| TOML source          | Generates                                                                     |
| -------------------- | ----------------------------------------------------------------------------- |
| `id = "platform_db"` | `{service}_execute_sql_platform_db`<br>`{service}_search_objects_platform_db` |
| `id = "client_ally"` | `{service}_execute_sql_client_ally`<br>`{service}_search_objects_client_ally` |

Where `{service}` is the MCP server name (e.g., `insightt`, `foundd`).

## Custom Tools for Multi-Tenant Queries

DBHub supports defining parameterized SQL operations as MCP tools in the TOML config. These register as first-class tools the model can invoke directly. Good candidates for this codebase:

- **Tenant lookup** — `get_tenant_by_name(name)` → queries `platform_companies` or `client` routing table
- **Server tenants** — `list_tenants_on_server(server_id)` → lists all tenants on a given server
- **Schema check** — `table_exists_in_tenant(db_name, table_name)` → checks if a feature-gated table exists

See [dbhub.ai/tools/custom-tools](https://dbhub.ai/tools/custom-tools) for the TOML syntax.

## Auto-Discovery

`generate_config.py` queries each platform's platform database to discover tenants:

1. Connects to the platform database using credentials from `.env`
1. Queries the routing table (`platform_companies` or `client`)
1. Generates `{platform}.toml` with one `[[sources]]` per tenant database
1. Source IDs follow naming: `server_{N}_tenant_db` (Insightt) or `client_{name}` (Foundd)

```bash
# Regenerate configs after adding tenants
dbhub -dbs
docker compose restart insightt foundd
```

## Adding a New Connection

1. Add credentials to `.env`
1. If tenant exists in routing table: run `dbhub -dbs` to auto-discover
1. If manual/local connection: add a `[[sources]]` entry manually to the TOML
1. Restart the container
