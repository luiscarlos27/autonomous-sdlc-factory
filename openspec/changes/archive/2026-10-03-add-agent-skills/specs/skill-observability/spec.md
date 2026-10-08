# Spec Delta

## Purpose

Defines the skill for observability guidance for OTel eBPF.

## ADDED Requirements

### Requirement: Skill provides implementation guidance
The system SHALL provide a skill file with structured guidance for implementing skill-observability components.

#### Scenario: Skill file exists in correct location
- **WHEN** the skill is installed
- **THEN** SKILL.md exists under .opencode/skills/skill-observability/.

#### Scenario: Skill includes implementation patterns
- **WHEN** the skill is consulted
- **THEN** it provides relevant technology patterns and best practices.

