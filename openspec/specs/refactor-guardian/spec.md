# refactor-guardian Specification

## Purpose
Defines AST analysis with Tree-sitter and mutation testing with Mutmut to enforce anti-snowball code control and reject complexity increases in CI.

## Requirements

### Requirement: System analyzes AST complexity
The system SHALL analyze code complexity using Tree-sitter AST parsing.

#### Scenario: Calculate cyclomatic complexity
- **WHEN** code is analyzed
- **THEN** cyclomatic complexity is computed from AST

#### Scenario: Detect complexity increases
- **WHEN** comparing against baseline
- **THEN** increases trigger alerts

### Requirement: Enforce anti-snowball rules in CI
The system SHALL reject PRs that increase technical debt via GitHub Actions CI.

#### Scenario: CI gate on complexity
- **WHEN** PR is submitted
- **THEN** CI checks complexity thresholds

#### Scenario: Mutation testing validation
- **WHEN** tests are validated
- **THEN** Mutmut validates test effectiveness
