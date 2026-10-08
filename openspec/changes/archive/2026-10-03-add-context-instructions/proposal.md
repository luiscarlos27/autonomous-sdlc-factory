# Proposal

## Why

The project needs clear architecture context, technology stack definitions, and operational instructions for AI agents (OpenCode) to follow. The provided context document defines the Enterprise Agentic Engine vision, monorepo structure, 7-stage roadmap, and coding standards. We need to integrate this context into the project properly and create OpenSpec capability specs aligned with the actual project architecture.

## What Changes

- Create capability specs aligned with the 7-stage architecture (Intent Engine, Swarm Orchestrator, Memory Vault, Sandbox Runtime, Observability/eBPF, Refactor Guardian, Test-Time Compute)
- Add OpenSpec context/configuration to capture project constraints
- Update README to reflect the full project architecture
- Ensure OpenCode can properly understand the project via OpenSpec specs

## Capabilities

### New Capabilities

- `intent-engine`: Ingestion of intentions and structured contract generation using Pydantic V2, Instructor, DSPy
- `swarm-orchestrator`: Multi-agent orchestration using LangGraph and MCP servers with Redis checkpointing
- `memory-vault`: Hierarchical memory with Pgvector, Redis, and Hermes Skills dynamic loader
- `sandbox-runtime`: Secure sandboxing with gVisor, OPA/Rego policy enforcement
- `observability`: Kernel-to-cognitive observability with OpenTelemetry and eBPF
- `refactor-guardian`: AST analysis with Tree-sitter and mutation testing with Mutmut for anti-snowball code control
- `test-time-compute`: Tree of Thoughts (ToT), MCTS, and Model-as-a-Judge for deliberative reasoning

### Modified Capabilities

None

## Impact

- Adds 7 capability specs under openspec/specs/ covering the full architecture
- Updates README with detailed architecture documentation
- Configures OpenSpec context to guide future changes
- Provides clear contracts for each subsystem
