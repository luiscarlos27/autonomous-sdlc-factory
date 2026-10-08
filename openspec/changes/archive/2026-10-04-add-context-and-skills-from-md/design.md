# Design

## Context

The research files contain valuable insights about agentic engineering evolution, empirical findings (EvoClaw benchmark), governance patterns, and practical workflows. We should integrate these by creating new capability specs, converting the weekly skill, and enhancing existing specs.

See proposal.md for motivation.

## Goals / Non-Goals

**Goals:**
- Create specs for agent-governance and context-management based on research
- Convert skill_agentic_engineering_weekly.md to opencode skill format
- Add the weekly skill to .opencode/skills/
- Enhance existing specs with relevant insights

**Non-Goals:**
- Duplicating content verbatim - extract and structure meaningfully
- Creating excessive specs - focus on key differentiators
- Modifying research files

## Decisions

**Decision 1: Extract governance concepts into agent-governance capability**
Key concepts: agent drift control, retry limits, human-in-the-loop, DoD enforcement, quality gates.

**Decision 2: Extract memory/context concepts into context-management capability**
Key concepts: tri-memory (episodic/semantic/procedural), context compression, drift prevention.

**Decision 3: Convert weekly skill preserving structure**
Transform skill_agentic_engineering_weekly.md to proper opencode SKILL.md with frontmatter.

## Risks / Trade-offs

- **Risk**: May overlap with existing specs (e.g., observability for drift)
  - Mitigation: Enhance existing specs rather than duplicating; create focused new specs for governance aspects
- **Risk**: Research is forward-looking (2026-2030)
  - Mitigation: Focus on actionable, current-relevant aspects
