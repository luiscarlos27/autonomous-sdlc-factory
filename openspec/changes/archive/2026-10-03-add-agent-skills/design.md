# Design

## Context

We have 7 comprehensive skill prototype files for each stage in the downloads folder. These contain detailed implementation guidance with code examples, patterns, best practices. We need to convert them to opencode skill format and add them to .opencode/skills/.

See proposal.md for motivation.

## Goals / Non-Goals

**Goals:**
- Convert each prototype skill file to proper opencode SKILL.md format
- Place them in .opencode/skills/ with appropriate naming
- Preserve the detailed technical content and examples
- Ensure skills align with existing capability specs

**Non-Goals:**
- Modifying the skill content significantly (preserve as-is, may improve formatting)
- Creating runtime code - only skill definitions for agents
- Changing existing skills

## Decisions

**Decision 1: Create one skill per stage with naming convention skill-{stage-name}**
Map the stage files to skill names matching their capabilities: skill-intent-engine, skill-swarm-orchestrator, etc. Place in .opencode/skills/.

Rationale: Consistent naming with the capability specs and easy discovery.

**Decision 2: Preserve full content from prototype files**
The prototypes contain comprehensive, well-structured guidance. Convert to opencode skill format (with frontmatter if needed, following existing skill patterns like graphify).

Rationale: Maximize value - these are detailed technical references.

## Risks / Trade-offs

- **Risk**: Large skill files increase context when loaded
  - Mitigation: Skills are loaded on-demand when relevant to task; content is valuable
- **Risk**: Content might need adjustment for opencode format
  - Mitigation: Follow opencode skill format conventions (name, description, etc.)
