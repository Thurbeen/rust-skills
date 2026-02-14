# Context Optimization Guide

> Context optimization strategies and results for Rust Skills

## Overview

Rust Skills uses three methods to optimize context consumption, achieving approximately **68%** token savings in total.

| Optimization Method | Type | Applicable Scenario | Savings |
|---------------------|------|---------------------|---------|
| **Skill Content Splitting** | Static | Large reference skills | 50-60% |
| **context: fork** | Dynamic | Task-execution skills | 75-85% |
| **Three-Layer Parallel Fork** | Dynamic | Multi-skill collaborative analysis | 65-75% |

---

## Method 1: Skill Content Splitting (Static Optimization)

### Principle

Split non-core content from large Skills into sub-files. The main SKILL.md retains only core routing logic, while other content is loaded on demand.

### Case Study: rust-router

| Metric | Before | After | Savings |
|--------|--------|-------|---------|
| File size | 18.7 KB | 8.1 KB | **56%** |
| Approx. tokens | ~4,700 | ~2,000 | **~2,700 tokens** |

### File Structure

```text
skills/rust-router/
├── SKILL.md (8.1KB - core routing, always loaded)
├── patterns/
│   └── negotiation.md (negotiation protocol, loaded on demand)
├── examples/
│   └── workflow.md (workflow examples, loaded on demand)
└── integrations/
    └── os-checker.md (integration notes, loaded on demand)
```

### Content Moved Out

| Content | Moved To | Size |
|---------|----------|------|
| Negotiation Protocol | `patterns/negotiation.md` | 4.5 KB |
| Workflow Example | `examples/workflow.md` | 2.3 KB |
| OS-Checker Integration | `integrations/os-checker.md` | 1.3 KB |
| Skill File Paths | Deleted (redundant) | 1.5 KB |

### Key Point: Auto-Triggering Is Not Affected

Claude Code's auto-trigger mechanism relies solely on the `description` field in the frontmatter:

```yaml
---
name: rust-router
description: "CRITICAL: Use for ALL Rust questions...
Triggers on: Rust, cargo, rustc, E0382, E0597..."
---
```

The SKILL.md body content is guidance logic used **after** triggering. Moving it to sub-files does not affect triggering.

### Applicable Scenarios

- Skills with a large amount of reference content
- Skills with multiple usage scenarios
- Skills with detailed examples/templates

---

## Method 2: context: fork Isolated Execution (Dynamic Optimization)

### Principle

Use `context: fork` to have the Skill execute in an isolated subagent context. Intermediate processes do not pollute the main context; only a summary result is returned.

### Configuration

```yaml
---
name: my-task-skill
description: "Task description"
context: fork
agent: general-purpose  # or Explore
---
```

### Case Studies

| Skill | Typical Execution Tokens | Main Context After Fork | Savings |
|-------|--------------------------|-------------------------|---------|
| `rust-skill-creator` | ~3,000 | ~500 (summary) | **~83%** |
| `core-dynamic-skills` | ~2,000 | ~400 | **~80%** |
| `core-fix-skill-docs` | ~1,500 | ~300 | **~80%** |
| `rust-daily` | ~2,500 | ~500 | **~80%** |

### Fork Characteristics

| Characteristic | Description |
|----------------|-------------|
| Isolated execution | Skill runs in a new, independent context |
| No conversation history | Subagent **cannot access** main conversation history |
| Result summary | Output is summarized before returning to the main conversation |
| Environment inheritance | Working directory, CLAUDE.md, and environment variables are inherited |

### Inheritance Relationship

```text
Main Context
├── Conversation history ────────► Does NOT inherit
├── Current working directory ───► Inherits
├── CLAUDE.md ───────────────────► Inherits (as reference)
├── Preloaded skills ────────────► Accessible
└── Environment variables ───────► Inherits
```

### Applicable Scenarios

- Independent tasks (creating files, syncing data, etc.)
- Operations that do not need conversation history
- Exploration/research tasks

### Not Applicable Scenarios

- Requires interactive follow-up questions with the user
- Requires full reasoning process to be visible
- Result details are important and cannot be summarized

---

## Method 3: Three-Layer Parallel Fork (Experimental)

### Principle

Based on the meta-cognition framework's three-layer model, analysis tasks are distributed in parallel to three isolated layer analyzers. Each analyzes independently and returns a summary; cross-layer synthesis happens in the main context.

### Architecture

```text
User Question
     |
     v
meta-cognition-parallel (coordinator)
     |
     +--- Fork -> layer1-analyzer --> L1 summary
     |           (language mechanics analysis)
     |
     +--- Fork -> layer2-analyzer --> L2 summary    [parallel]
     |           (design choice analysis)
     |
     +--- Fork -> layer3-analyzer --> L3 summary
                 (domain constraint analysis)
     |
     v
Cross-Layer Synthesis (main context)
     |
     +-> Domain-correct architectural solution
```

### Context Consumption Comparison

**Traditional approach (main context):**

```text
+-- Read m01-ownership    +1,200 tokens
+-- Read m02-resource     +1,000 tokens
+-- Read domain-fintech   +1,500 tokens
+-- Intermediate reasoning +2,500 tokens
+-- Final answer           +1,800 tokens
                          ------------
                          ~8,000 tokens
```

**Three-layer parallel fork:**

```text
+-- L1 summary returned   +600 tokens
+-- L2 summary returned   +600 tokens
+-- L3 summary returned   +600 tokens
+-- Cross-layer synthesis  +700 tokens
                          ------------
                          ~2,500 tokens
```

**Savings: ~69%**

### Related Files

- `skills/meta-cognition-parallel/SKILL.md` - Coordinator Skill
- `agents/layer1-analyzer.md` - Language mechanics analysis (m01-m07)
- `agents/layer2-analyzer.md` - Design choice analysis (m09-m15)
- `agents/layer3-analyzer.md` - Domain constraint analysis (domain-*)

### Usage Command

```bash
/meta-parallel <your Rust question>
```

### Test Scenarios

```bash
# Test 1: Trading system
/meta-parallel Trading system reports E0382, trade record was moved

# Test 2: Web API
/meta-parallel Web API with multiple handlers needing to share a database connection pool

# Test 3: CLI tool
/meta-parallel How should a CLI tool handle priority between config files and command-line arguments
```

---

## Combined Effect Estimate

Assuming a typical Rust Q&A session:

| Phase | Before Optimization | After Optimization |
|-------|--------------------|--------------------|
| rust-router loading | 4,700 | 2,000 |
| Multi-skill analysis | 8,000 | 2,500 |
| Task execution | 3,000 | 500 |
| **Total** | **15,700** | **5,000** |
| **Savings** | - | **~68%** |

---

## Selection Decision Tree

```text
Question type
    |
    +-- Large reference Skill?
    |   +-- YES -> Method 1: Content splitting
    |             Move non-core content to sub-files
    |
    +-- Independent execution task?
    |   +-- YES -> Method 2: context: fork
    |             Add context: fork to the frontmatter
    |
    +-- Multi-layer collaborative analysis?
        +-- YES -> Method 3: Three-layer parallel fork
                  Use meta-cognition-parallel
```

---

## Best Practices

### 1. Content Splitting Principles

- Keep core routing logic in SKILL.md
- Move examples and templates to `examples/`
- Move integration notes to `integrations/`
- Move detailed references to `references/`

### 2. Fork Usage Principles

- Only use fork for task-oriented Skills
- Do not use fork for reference/guidance Skills
- Do not use fork when user interaction is needed

### 3. Parallel Analysis Principles

- Each analysis task should be independent, with no dependencies
- Synthesis reasoning is completed in the main context
- Explicitly pass all necessary information to the fork

---

## Validation Checklist

### Method 1 Validation

- [ ] rust-router auto-trigger test

  ```bash
  claude -p "How to fix E0382"
  claude -p "Compare tokio and async-std"
  ```

### Method 2 Validation

- [ ] Fork skill execution test

  ```bash
  /sync-crate-skills
  /rust-daily
  ```

### Method 3 Validation

- [ ] Three-layer parallel analysis test

  ```bash
  /meta-parallel Trading system reports E0382
  ```

---

## Version History

| Version | Date | Optimization |
|---------|------|-------------|
| 2.0.0 | 2025-01-22 | rust-router content splitting (56% savings) |
| 2.0.4 | 2025-01-22 | 4 skills added context: fork (thanks @pinghe) |
| 2.0.5 | 2025-01-22 | Three-layer parallel fork experimental support |

---

**Created:** 2025-01-21
**Updated:** 2025-01-22
**Status:** Implemented (Methods 1-3)
