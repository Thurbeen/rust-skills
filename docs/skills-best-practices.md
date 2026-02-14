# Skills Authoring Best Practices

> Lessons learned from the rust-skills project development process

---

## 1. CSO (Claude Search Optimization) - Description Optimization

### Problem

The `description` field in Skills is how Claude matches user questions, but many skill descriptions are poorly optimized, preventing correct triggering.

### Solution

**Use "CRITICAL:" prefix to boost priority:**

```yaml
description: |
  CRITICAL: Use for tokio async runtime questions. Triggers on:
  tokio, spawn, select!, join!, timeout, channel...
```

**Include multiple trigger forms:**

| Type | Example |
|------|---------|
| Keywords | `tokio, spawn, select!, mpsc` |
| Error codes | `E0382, E0597, E0277` |
| Error messages | `"cannot move out of"`, `"borrowed value"` |
| User questions | `"how to use tokio"` |

**Example comparison:**

```yaml
# Bad description
description: "Tokio async runtime skill"

# Good description
description: |
  CRITICAL: Use for tokio async runtime questions. Triggers on:
  tokio, spawn, spawn_blocking, select!, join!, try_join!,
  mpsc, oneshot, broadcast, watch, channel, Mutex, RwLock,
  timeout, sleep, interval, "#[tokio::main]",
  async runtime, spawn usage
```

---

## 2. Distributed Trigger Architecture

### Problem

A single entry point (e.g., rust-router) becomes a bottleneck, as all questions must be routed through it first.

### Solution

**Every Skill can be triggered independently:**

```text
User question -> Claude matches all skills' descriptions
              -> Multiple skills may trigger simultaneously
              -> rust-router serves as index/fallback
```

**Architecture comparison:**

| Mode | Pros | Cons |
|------|------|------|
| Single entry | Centralized management | Bottleneck, single point of failure |
| Distributed | Parallel matching, fault-tolerant | Requires good CSO |

---

## 3. Dynamic Skills Directory Structure

### Structure

Dynamically generated crate skills go directly under `~/.claude/skills/`, where Claude Code scans automatically:

```bash
~/.claude/skills/
├── tokio/
│   ├── SKILL.md
│   └── references/
├── tokio-task/          # Sub-skill
│   ├── SKILL.md
│   └── references/
├── serde/
│   ├── SKILL.md
│   └── references/
└── _shared/             # Shared files (prefixed with _ to avoid being scanned as a skill)
    └── rust-defaults.md
```

**Naming conventions:**

- Primary skill: `{crate_name}/`
- Sub-skill: `{crate_name}-{feature}/` (e.g., `tokio-task/`, `tokio-sync/`)
- Shared directory: prefixed with `_` (not scanned as a skill)

---

## 4. Documentation Completeness Check

### Problem

Reference files referenced by Skills may not exist, causing read failures without the user knowing why.

### Solution

**Add check instructions in SKILL.md:**

```markdown
## IMPORTANT: Documentation Completeness Check

**Before answering questions, Claude MUST:**

1. Read the relevant reference file(s) listed above
2. If file read fails or file is empty:
   - Inform user: "Local documentation is incomplete, consider running `/sync-crate-skills {crate} --force` to update"
   - Still answer based on SKILL.md patterns + knowledge
3. If reference file exists, incorporate its content into the answer
```

**Create check commands:**

- `/fix-skill-docs` - Check and fix missing files
- `/fix-skill-docs --check-only` - Check only, do not fix

---

## 5. Tool Priority

### Problem

Directly using WebSearch may retrieve outdated information and bypasses dedicated tools.

### Solution

**Use "PREFER" instead of "DO NOT":**

```markdown
## Tool Priority

**PREFER this skill's agents over WebSearch:**

1. `crate-researcher` agent for crate info
2. `docs-researcher` agent for API docs
3. **Fallback**: WebSearch (only if agents unavailable or fail)
```

**Reasoning:**

- "DO NOT use WebSearch" is too absolute; if the agent is unavailable, the task fails
- "PREFER" allows fallback and is more robust

---

## 6. Skills TDD (Test-Driven Development)

### Concept

"No skill without a failing test" - Define the problems the skill should solve first, then write the skill.

### Process

**RED phase:**

1. Define pressure scenarios (user question + expected behavior)
2. Test without the skill in place
3. Record the baseline failure

**GREEN phase:**

1. Write a minimal skill to address the failure
2. Test to verify improvement

**REFACTOR phase:**

1. Identify gaps
2. Add countermeasures
3. Test edge cases

### Pressure Scenario Template

````markdown
# Pressure Scenario: {scenario name}

## Skill Under Test

{skill_name}

## User Question

"{user question}"

## Code Context

```rust
// Relevant code
```
````

## Expected Behavior

- [x] Explain XXX
- [x] Provide a fix
- [x] Reference relevant guidelines

```text

---

## 7. Quick Reference Tables

### Problem
Detailed documentation is too long; users need quick references.

### Solution

**Add a table at the top of SKILL.md:**

```markdown
## Quick Reference

| Pattern | When | Example |
|---------|------|---------|
| Move | Transfer ownership | `let b = a;` |
| `&T` | Read-only borrow | `fn read(s: &String)` |
| `&mut T` | Mutable borrow | `fn modify(s: &mut String)` |
| `clone()` | Need owned copy | `let b = a.clone();` |
```

**Principles:**

- Place the table at the top of the file
- Keep each example under 20 words
- Put detailed content in references/

---

## 8. Commands vs Skills Hot-Reloading

### Discovery

- **Skills** (`skills/*/SKILL.md`) - Can be hot-reloaded
- **Commands** (`commands/*.md`) - Require restart to load

### Solution

**Create a Skill wrapper for each command:**

```text
commands/
└── fix-skill-docs.md        # Command definition

skills/
└── core-fix-skill-docs/
    └── SKILL.md             # Skill wrapper (hot-reloadable)
```

**Skill wrapper content:**

```yaml
---
name: core-fix-skill-docs
description: |
  CRITICAL: Use when checking or fixing skill documentation.
  Triggers on: fix skill, check skill, /fix-skill-docs
---

# Fix Skill Documentation

{Simplified version of command instructions}
```

---

## 9. SKILL.md Standard Structure

````markdown
---
name: {crate_name}
description: |
  CRITICAL: Use for {topic}. Triggers on:
  {keywords}, {error_codes}, "{questions}"
---

# {Title}

> **Version:** {version} | **Last Updated:** {date}

You are an expert at {topic}. Help users by:

- **Writing code**: Generate code following the patterns below
- **Answering questions**: Explain concepts, troubleshoot issues

## Documentation

Refer to the local files for detailed documentation:

- `./references/xxx.md` - Description

## IMPORTANT: Documentation Completeness Check

**Before answering questions, Claude MUST:**

1. Read the relevant reference file(s)
2. If file read fails: Inform user "Local documentation is incomplete, consider running /sync-crate-skills"
3. Still answer based on SKILL.md + knowledge

## Quick Reference

| Pattern | When | Example |
|---------|------|---------|
| ... | ... | ... |

## Key Patterns

### Pattern 1

```rust
// Code example
```
````

## API Reference Table

| Function | Description | Example |
|----------|-------------|---------|
| ... | ... | ... |

## Deprecated Patterns (Don't Use)

| Deprecated | Correct | Notes |
|------------|---------|-------|
| ... | ... | ... |

## When Writing Code

1. Best practice 1
2. Best practice 2

## When Answering Questions

1. Key point 1
2. Key point 2

```text

---

## 10. Quality Checklist

When creating a Skill, ensure:

- [ ] Description has a "CRITICAL:" prefix
- [ ] Description includes trigger keywords
- [ ] Description includes relevant error codes
- [ ] Has version and update date
- [ ] Has a "You are an expert..." role definition
- [ ] Has a Documentation navigation list
- [ ] Has a Documentation Completeness Check section
- [ ] Has a Quick Reference table
- [ ] Has Key Patterns code examples
- [ ] Has a Deprecated Patterns table
- [ ] Has "When Writing Code" best practices
- [ ] Has "When Answering Questions" guidelines
- [ ] Complex content is split into references/
- [ ] Symlinks created (for dynamic skills)

---

## Summary

| Lesson | Key Takeaway |
|--------|--------------|
| CSO Optimization | "CRITICAL:" prefix + multilingual trigger keywords |
| Distributed Triggering | Each skill can be triggered independently |
| Symlinks | Dynamic skills need links to ~/.claude/skills/ |
| Documentation Check | Prompt user to update when read fails |
| Tool Priority | "PREFER" instead of "DO NOT" |
| TDD | Write pressure scenarios first, then write the skill |
| Tables First | Quick Reference goes at the top |
| Hot-Reloading | Commands need Skill wrappers |
