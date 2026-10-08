# autonomous-sdlc-factory

A factory for autonomous SDLC (Software Development Life Cycle) workflows.

## OpenSpec

This project uses [OpenSpec](https://openspec.dev/) for spec-driven development. OpenSpec provides a structured workflow for defining, implementing, and validating changes through specifications.

### OpenSpec Workflow

1. Propose - Create a change proposal with specs, design, and tasks
2. Implement - Execute tasks against the specs
3. Archive - Promote completed changes to main specs

### OpenSpec Commands

Run from the repository root:

```bash
# Create a new change proposal
npx @fission-ai/openspec new change <change-name>

# Check status of current change
npx @fission-ai/openspec status --change <change-name>

# List specs
npx @fission-ai/openspec list --specs

# Archive completed change
npx @fission-ai/openspec archive <change-name> --yes
```

### AI Agent Integration

This project includes OpenSpec integration for opencode with custom commands and skills in `.opencode/`.

## Development

This project uses Python 3.11+. 

### Setup

```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -e ".[dev]"
```

### Testing

```bash
pytest
mypy src
```
