# Proposal

## Why

The project has comprehensive skill prototypes in the downloads folder for each of the 7 stages. These skill definitions provide detailed technical guidance for implementing each component with best practices (type hints, security, patterns). We should integrate these as opencode skills in the project to make them available to AI agents working on the codebase.

## What Changes

- Add specialized opencode skills for each of the 7 stages based on the prototype skill files
- Create skill directories under .opencode/skills/ for each stage with proper SKILL.md files
- Ensure skills align with the capability specs already defined
- Add any supporting skill assets/templates as needed

## Capabilities

### New Capabilities

- `skill-intent-engine`: AI agent skill for intent engine implementation (Pydantic V2, Instructor, DSPy)
- `skill-swarm-orchestrator`: AI agent skill for swarm orchestration (LangGraph, MCP, Redis)
- `skill-memory-vault`: AI agent skill for memory vault (Pgvector, Redis, Hermes Skills)
- `skill-sandbox-runtime`: AI agent skill for sandbox runtime (gVisor, OPA/Rego)
- `skill-observability`: AI agent skill for observability (OpenTelemetry, eBPF)
- `skill-refactor-guardian`: AI agent skill for refactor guardian (Tree-sitter, Mutmut)
- `skill-test-time-compute`: AI agent skill for test-time compute (ToT, MCTS, Model-as-a-Judge)

### Modified Capabilities

None

## Impact

- Adds 7 skill files under .opencode/skills/ with detailed implementation guidance
- Enhances AI agent capabilities when working on specific components
- Aligns skills with existing OpenSpec capability definitions
- No changes to runtime code, only tooling/instructions for agents
