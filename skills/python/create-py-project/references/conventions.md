# Company Conventions

Architectural conventions for Python project generation across all agents.

## Directory Structure

- **`shared/`** - Cross-cutting shared modules and **weak models**
  - Clients (API clients, database clients, external service wrappers)
  - Utilities and helpers
  - Weak models (DTOs, data transfer objects, simple data structures)
  - Infrastructure concerns (logging, config, observability)
- **`modules/`** - **Strong models** and domain services
  - Domain models with business logic
  - Services that utilize underlying `shared/` clients
  - Business logic and domain operations
  - Use cases and application services

## Application to File Generation

### CRITICAL: Always create actual implementation files in shared/ and modules/\*\*

Do NOT just create empty `__init__.py` files. The `{package_name}/` directory should be minimal (just `__init__.py`), but `shared/` and `modules/` must contain actual working code.

**For FastAPI projects:**

- **`shared/`** - Create these files with actual implementations:
  - `shared/config.py` - Settings class using pydantic-settings
  - `shared/{domain}_client.py` - HTTP client or external API wrapper
  - `shared/router.py` - FastAPI router with endpoints (imports from modules, not shared)
  - `shared/models.py` (optional) - Pydantic models for API requests/responses
- **`modules/`** - Create domain services:
  - `modules/{domain}_service.py` - Business logic that uses clients from shared/
  - `modules/models.py` (optional) - Domain models with business rules
- **`{package_name}/`** - For applications: **DO NOT CREATE**. For libraries: create minimal package with `__init__.py` only

**Example: For a domain-specific API project, generate:**

- `shared/config.py` - Settings with API keys, URLs, etc.
- `shared/{domain}_client.py` - Client class with async HTTP methods (infrastructure)
- `modules/{domain}_service.py` - Service with business logic (uses client from shared)
- `shared/router.py` - FastAPI routes that use the service from modules
- **No package directory** - This is an application, not a library

**For CLI projects:**

- **`shared/`** - Create utilities:
  - `shared/file_utils.py` - File I/O helpers
  - `shared/api_client.py` - External API client if needed
  - `shared/config.py` - Configuration management
- **`modules/`** - Create business logic:
  - `modules/{domain}_processor.py` - Core processing logic
  - `modules/models.py` - Domain models
- **`{package_name}/`** - For applications: **DO NOT CREATE**. For libraries: create minimal package with `__init__.py` only

## Orchestration Guidance

When coordinating project generation:

- Ensure both `shared/` and `modules/` directories are created for all projects
- For FastAPI: Guide placement of clients in `shared/`, domain logic in `modules/`
- For CLI: Guide placement of utilities in `shared/`, business logic in `modules/`
- Validate that the structure follows company conventions
