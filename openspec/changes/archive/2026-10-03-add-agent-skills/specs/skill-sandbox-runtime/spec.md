# Spec Delta

## Purpose

Defines the skill for sandbox runtime guidance for gVisor OPA Rego.

## ADDED Requirements

### Requirement: Skill provides implementation guidance
The system SHALL provide a skill file with structured guidance for implementing skill-sandbox-runtime components.

#### Scenario: Skill file exists in correct location
- **WHEN** the skill is installed
- **THEN** SKILL.md exists under .opencode/skills/skill-sandbox-runtime/.

#### Scenario: Skill includes implementation patterns
- **WHEN** the skill is consulted
- **THEN** it provides relevant technology patterns and best practices.

