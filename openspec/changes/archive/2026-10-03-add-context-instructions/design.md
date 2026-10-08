# Design

## Context

The project already has OpenSpec initialized. We need to add capability specs aligned with the 7-stage Enterprise Agentic Engine architecture and update project documentation to reflect the full vision.

See proposal.md for motivation.

## Goals / Non-Goals

**Goals:**
- Create 7 capability specs covering each architectural component with clear requirements
- Update README with comprehensive architecture documentation
- Ensure OpenCode has clear guidance via OpenSpec

**Non-Goals:**
- Implementing actual code for the subsystems (just defining specs)
- Creating directory structure in src/ beyond what's implied
- Modifying existing OpenSpec config beyond adding context

## Decisions

**Decision 1: Mirror the 7-stage architecture as separate capabilities**
Each stage from the roadmap becomes its own capability spec: intent-engine, swarm-orchestrator, memory-vault, sandbox-runtime, observability, refactor-guardian, test-time-compute. This provides clear contracts per subsystem.

Rationale: Aligns specs with the conceptual architecture; enables independent evolution of each component.

**Decision 2: Keep specs high-level but testable**
Requirements focus on observable behavior (what the system SHALL do) with concrete scenarios. Avoid implementation details like specific class names.

Rationale: Maintains spec/implementation separation as per OpenSpec philosophy.

**Decision 3: Update README to document full architecture**
Include the full context about the Enterprise Agentic Engine, stages, tech stack, and OpenSpec workflow.

Rationale: Improves discoverability and onboarding for developers/agents.

## Risks / Trade-offs

- **Risk**: Specs might be too abstract initially
  - Mitigation: Can refine with more detailed requirements in future changes as implementation progresses
- **Risk**: 7 capabilities could be consolidated, but separation clarifies boundaries
  - Mitigation: Clear boundaries match the stage-based architecture
