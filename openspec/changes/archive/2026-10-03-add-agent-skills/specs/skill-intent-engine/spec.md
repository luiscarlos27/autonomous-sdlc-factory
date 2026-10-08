# Spec Delta

## Purpose

Defines the skill for intent engine implementation guidance including Pydantic V2, Instructor, DSPy patterns.

## ADDED Requirements

### Requirement: Skill provides intent engine implementation guidance
The system SHALL provide a skill file with structured guidance for implementing intent engine components.

#### Scenario: Skill file exists in correct location
- **WHEN** the skill is installed
- **THEN** SKILL.md exists under .opencode/skills/skill-intent-engine/

#### Scenario: Skill includes type hints and patterns
- **WHEN** the skill is consulted
- **THEN** it provides Pydantic V2, Instructor, and DSPy implementation patterns with type hints
