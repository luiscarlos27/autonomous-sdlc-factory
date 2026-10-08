# skill-refactor-guardian Specification

## Purpose
Defines the skill for refactor guardian guidance for Tree-sitter Mutmut.

## Requirements

### Requirement: Skill provides implementation guidance
The system SHALL provide a skill file with structured guidance for implementing skill-refactor-guardian components.

#### Scenario: Skill file exists in correct location
- **WHEN** the skill is installed
- **THEN** SKILL.md exists under .opencode/skills/skill-refactor-guardian/.

#### Scenario: Skill includes implementation patterns
- **WHEN** the skill is consulted
- **THEN** it provides relevant technology patterns and best practices.
