# Proposal

## Why

OpenSpec will provide a structured, specification-driven development workflow for the autonomous-sdlc-factory project. It helps maintain clear separation between what needs to be built (specs) and how it's built (implementation), ensuring alignment on requirements and enabling systematic validation. This is particularly valuable for an autonomous SDLC factory - having explicit specs allows AI agents and developers to work against well-defined contracts.

## What Changes

- Establish OpenSpec as the specification framework for the project
- Create foundational capability specs for the autonomous SDLC system
- Add workflow artifacts (proposal, specs, design, tasks) for planned changes
- Configure OpenSpec integration for opencode CLI agent

## Capabilities

### New Capabilities

- `autonomous-sdlc-core`: Core capabilities of the autonomous SDLC factory including specification parsing, workflow orchestration, and code generation pipelines
- `agent-orchestration`: Management and coordination of AI agents within the SDLC pipeline

### Modified Capabilities

None

## Impact

- Adds `openspec/` directory with specs, changes, and config
- Adds `.opencode/` commands and skills for OpenSpec workflows (opencode integration)
- No changes to existing runtime code (initial setup)
- Documentation in README and OpenSpec artifacts
