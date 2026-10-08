# skill-swarm-orchestrator Specification

## Purpose
Defines the skill for swarm orchestrator guidance for LangGraph MCP Redis.

## Requirements

### Requirement: Skill provides implementation guidance
The system SHALL provide a skill file with structured guidance for implementing skill-swarm-orchestrator components.

#### Scenario: Skill file exists in correct location
- **WHEN** the skill is installed
- **THEN** SKILL.md exists under .opencode/skills/skill-swarm-orchestrator/.

#### Scenario: Skill includes implementation patterns
- **WHEN** the skill is consulted
- **THEN** it provides relevant technology patterns and best practices.
