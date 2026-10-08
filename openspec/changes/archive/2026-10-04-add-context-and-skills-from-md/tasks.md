# Tasks

## 1. Create Capability Specs

- [ ] 1.1 Create agent-governance main spec at openspec/specs/agent-governance/spec.md based on delta and verify format
- [ ] 1.2 Create context-management main spec at openspec/specs/context-management/spec.md based on delta and verify format

## 2. Create Weekly Practice Skill

- [ ] 2.1 Create .opencode/skills/agentic-engineering-weekly/ directory
- [ ] 2.2 Convert skill_agentic_engineering_weekly.md to SKILL.md with proper opencode frontmatter (name, description, trigger if applicable) and preserve content
- [ ] 2.3 Verify the skill is properly formatted

## 3. Validate

- [ ] 3.1 Validate the change with `npx --yes @fission-ai/openspec@1.14.0 validate add-context-and-skills-from-md`
- [ ] 3.2 Verify new specs and skill are created correctly
- [ ] 3.3 Verify change status is complete
