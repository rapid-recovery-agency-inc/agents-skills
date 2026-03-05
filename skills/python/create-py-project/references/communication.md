# Communication Patterns

User communication guidelines for interactive project setup.

## User Communication Tips

### Use Formatting

- ✅ for success
- ❌ for errors
- ⚠️ for warnings
- 📦, 🚀, 🔧 for sections
- Code blocks for commands

### Keep It Short

- One concept per paragraph
- Bullet points over long sentences
- Examples over explanations

### Be Contextual

Reference the user's specific choices:

- "Since you chose FastAPI..."
- "With poetry, you can..."
- "For a CLI tool, consider adding..."

## Practical Communication

Translate complex technical jargon into concise, easy-to-understand dialogue. Reduce cognitive friction for the user.

### Guidelines

- **Avoid unnecessary jargon**: Use "install packages" instead of "resolve dependencies"
- **Use analogies when helpful**: "Think of it like a postal service for your code"
- **Skip the ceremony**: Get to the point quickly without formal preamble
- **Focus on outcomes**: "This will make your code faster" beats "This implements memoization caching"
- **Offer choices simply**: Present trade-offs in plain language, not technical specification

### Examples

**Instead of:**

> "We'll implement a dependency injection container to decouple your service layer from infrastructure concerns."

**Say:**

> "We'll set up your code so you can swap out the database later without changing your business logic."

**Instead of:**

> "The AST parsing reveals a circular import violation requiring topological reordering."

**Say:**

> "Two of your files are trying to import each other. Let's move the shared code to a third file."

**Instead of:**

> "Would you prefer Poetry or uv for your package management solution?"

**Say:**

> "Pick your package manager:
>
> - Poetry: tried and tested
> - uv: faster, newer"

### When Technical Terms Are OK

Use precise terms when:

- The user demonstrates familiarity (mentions "Docker containers", "async/await")
- It's necessary for accuracy ("TypeError" vs "something broke")
- You're explaining the term immediately after using it

## Asking Questions

Use the `ask_user_question` tool when it is available. Check for tool availability at the start of the workflow.

### When `ask_user_question` is Available

- **Menu-based questions (≤4 options)**: Use `ask_user_question` with predefined options
- **Text input**: Use `ask_user_question` with empty options for free-form text
- **One question at a time**: Wait for each answer before proceeding

### When `ask_user_question` is Unavailable

Fall back to plain chat questions:

- Ask one question at a time
- Wait for user response
- Provide clear defaults in [brackets]
- Keep questions concise and contextual

## Communication During Generation

When generating files:

- Show progress for each file created
- Report any assumptions made
- Highlight customizations applied
- Note any TODO items left for the user
- Explain non-obvious choices

## Error Recovery

When things go wrong:

1. **Explain what happened** in plain language
1. **Show the error** (truncated if very long)
1. **Suggest fixes** based on error type
1. **Offer to retry** or continue with workarounds
