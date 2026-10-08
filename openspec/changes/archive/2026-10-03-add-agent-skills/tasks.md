# Tasks

## 1. Create Skill Directories

- [ ] 1.1 Create .opencode/skills/skill-intent-engine/ directory and copy/convert skill-etapa-1-intent-engine.md content to SKILL.md with proper opencode skill format - verify SKILL.md is valid
- [ ] 1.2 Create .opencode/skills/skill-swarm-orchestrator/ directory and copy/convert skill-etapa-2-swarm-orchestrator.md content to SKILL.md with proper opencode skill format - verify content preserved
- [ ] 1.3 Create .opencode/skills/skill-memory-vault/ directory and copy/convert skill-etapa-3-memory-vault.md content to SKILL.md with proper opencode skill format - verify content preserved
- [ ] 1.4 Create .opencode/skills/skill-sandbox-runtime/ directory and copy/convert skill-etapa-4-sandbox-runtime.md content to SKILL.md with proper opencode skill format - verify content preserved
- [ ] 1.5 Create .opencode/skills/skill-observability/ directory and copy/convert skill-etapa5-observabilidad.md content to SKILL.md with proper opencode skill format - verify content preserved
- [ ] 1.6 Create .opencode/skills/skill-refactor-guardian/ directory and copy/convert skill-etapa6-refactor-guardian.md content to SKILL.md with proper opencode skill format - verify content preserved
- [ ] 1.7 Create .opencode/skills/skill-test-time-compute/ directory and copy/convert skill-etapa7-capstone-inference.md content to SKILL.md with proper opencode skill format - verify content preserved

## 2. Enhance Skills with Metadata

- [ ] 2.1 Add proper frontmatter (name, description, trigger) to each SKILL.md following opencode skill conventions - verify all skills have consistent metadata

## 3. Validate

- [ ] 3.1 Validate the change with `npx --yes @fission-ai/openspec@1.14.0 validate add-agent-skills` and ensure it passes
- [ ] 3.2 Verify all 7 skills are created under .opencode/skills/ with correct structure
- [ ] 3.3 Verify the change status is complete with `npx --yes @fission-ai/openspec@1.14.0 status --change add-agent-skills`
