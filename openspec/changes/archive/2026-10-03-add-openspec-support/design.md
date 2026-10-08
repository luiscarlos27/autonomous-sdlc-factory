# Design

## Context

The autonomous-sdlc-factory repository currently has minimal structure (just README.md) with OpenSpec and opencode already initialized. OpenSpec CLI is installed and available. We need to solidify and structure the spec framework for this project.

See proposal.md for motivation.

## Goals / Non-Goals

**Goals:**
- Establish clear capability boundaries for autonomous SDLC operations
- Create foundational specs that future changes can extend
- Ensure proper OpenSpec structure is in place for spec-driven development

**Non-Goals:**
- Implementing the actual SDLC logic or agents (just setting up specs for them)
- Modifying runtime code beyond spec structure
- Creating detailed implementation of agent orchestration logic

## Decisions

**Decision 1: Define two core capability areas**
- **autonomous-sdlc-core**: Covers OpenSpec initialization, workflow management, spec validation - foundational infrastructure
- **agent-orchestration**: Covers coordination of AI agents in the SDLC pipeline

Rationale: Separation of concerns - core spec framework vs runtime orchestration concerns.

**Decision 2: Specs as delta files in changes, then archive to main specs**
Following OpenSpec's standard workflow - write deltas in the change directory, then archive to promote to main specs. This matches how the tool is designed.

Rationale: Maintains clear history and enables review of spec changes before promoting to main.

## Risks / Trade-offs

- **Risk**: Over-specifying early for an empty project
  - Mitigation: Keep specs at high level focused on observable behavior, not implementation details
- **Risk**: Capability boundaries might evolve as the project grows
  - Mitigation: Design capabilities to be cohesive and evolvable; can refine in future changes
