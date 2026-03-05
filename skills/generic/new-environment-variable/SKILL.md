---
name: new-environment-variable
description: This skill provides instructions on how to add new environment variables and ensures robust, testable, and maintainable environment variable usage across both TypeScript and Python projects.
---

# Skill Instructions

This skill provides instructions into how to add new environment variables, and also, provided context, guidelines and patterns for managing environment variables in both TypeScript and Python projects. It emphasizes best practices for loading, validating, and accessing environment variables to ensure consistency and maintainability across the codebase.

## Principles

- 12-Factor App: All config is stored in environment variables, never hardcoded.
- Centralized Access: All environment variable instrumentation is maintained in "shared/environment.ts" for TypeScript and "shared/environment.py" for Python; and access is through a single exported function "env()".
- Validation: Required variables are validated at startup; missing keys are reported.
- Type Safety: Use interfaces/types (TypeScript) or dataclasses (Python) to define expected variables.
- Runtime Loading: Always load environment variables at runtime, not at module load time.
- Override for Flexibility and Testing: Provide a function "setEnvironment(new_environment)" for TypeScript and "set_environment(new_environment)" for Python to set or override variables values.
- No Magic Strings: Never use raw string keys for env vars outside the central module.

## When to use the skill

Use this skill whenever you need to add a new environment variable to the project, or when you need to access environment variables in your code. This skill ensures that you follow best practices for environment variable management, which helps maintain a clean and consistent codebase.

## Step-by-step procedures to follow

1. Identify the new environment variable you need to add, and determine its name and expected type.
1. Open the central environment variable module: "shared/environment.ts" for TypeScript or "shared/environment.py" for Python.
1. Add the new environment variable to the appropriate interface/type (TypeScript) or dataclass (Python) that defines the expected environment variables.
1. Implement validation logic for the new variable in the "env()" function to ensure it is present and of the correct type at startup.
1. Use the "env()" function to access the environment variable in your code, ensuring you do not use raw string keys for accessing it.
