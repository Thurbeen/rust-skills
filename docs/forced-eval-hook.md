# Forced Eval Hook Principles

> Solving the unreliable auto-triggering problem in Claude Code Skills

## Background

### Claude's Behavioral Characteristics

> "Claude is so goal focused that it barrels ahead with what it thinks is the best approach. It doesn't check for tools unless explicitly told to."

Claude is very goal-focused and will directly use what it considers the best approach. **It will not proactively check available skills**, even if the skill's description contains matching keywords.

### Trigger Success Rate Comparison

| Method | Success Rate | Notes |
|--------|-------------|-------|
| Description keywords only | **~20%** | Claude rarely checks proactively |
| Simple instruction hook | 40-50% | "Suggests" checking; Claude may ignore |
| **Forced Eval Hook** | **~84%** | Forces evaluation; most effective |
| LLM Eval Hook | ~80% | Requires additional API call |

## Forced Eval Hook Principles

### Core Idea

**Force** Claude to evaluate each skill before executing a task, rather than "suggesting" it check.

The key is using **imperative language**:

- `MANDATORY`
- `CRITICAL`
- `MUST`
- `DO NOT skip`

### Workflow

```text
+-------------------------------------------------------------+
|                     User Prompt                              |
|              "How to fix E0382"                              |
+---------------------+---------------------------------------+
                      |
                      v
+-------------------------------------------------------------+
|              UserPromptSubmit Hook                           |
|                                                             |
|  1. Regex matcher checks for a match                        |
|     (?i)(rust|cargo|E0\d{3,4}|...)                          |
|                                                             |
|  2. Match found -> execute hook script                      |
+---------------------+---------------------------------------+
                      |
                      v
+-------------------------------------------------------------+
|              Hook Script Output                             |
|                                                             |
|  === MANDATORY SKILL EVALUATION ===                         |
|                                                             |
|  CRITICAL: Before proceeding, you MUST:                     |
|  1. EVALUATE each skill against this prompt                 |
|  2. State: "[skill-name]: YES/NO - [reason]"               |
|  3. ACTIVATE matching skills using Skill(name)              |
|  4. Only THEN proceed with response                         |
|                                                             |
|  DO NOT skip this evaluation.                               |
+---------------------+---------------------------------------+
                      |
                      v
+-------------------------------------------------------------+
|              Claude Processing                              |
|                                                             |
|  Receives: Hook output + User Prompt                        |
|                                                             |
|  Executes:                                                  |
|  1. Evaluates each skill                                    |
|     m01-ownership: YES - E0382 is an ownership error        |
|     m02-resource: NO - does not involve smart pointers      |
|     ...                                                     |
|  2. Invokes Skill(m01-ownership)                            |
|  3. Uses skill content to answer the question               |
+-------------------------------------------------------------+
```

### Three-Step Process

```text
EVALUATE -> ACTIVATE -> IMPLEMENT
```

1. **EVALUATE**: Make a YES/NO judgment for each skill
2. **ACTIVATE**: Invoke matching skills using `Skill(skill-name)`
3. **IMPLEMENT**: Only begin the actual answer after activation

## Implementation Details

### 1. Hook Configuration (settings.json)

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "(?i)(rust|cargo|crate|E0\\d{3,4}|...)",
        "command": ".claude/hooks/rust-skill-eval-hook.sh"
      }
    ]
  }
}
```

**Configuration notes**:

- `UserPromptSubmit`: Triggered when the user submits a prompt
- `matcher`: Regular expression; the hook executes only when matched
- `command`: Script path to execute (relative to project root)

### 2. Hook Script

```bash
#!/bin/bash
cat << 'EOF'

=== MANDATORY SKILL EVALUATION ===

CRITICAL: Before proceeding with this Rust-related request, you MUST:

1. EVALUATE each available rust-skill against this prompt:

   OWNERSHIP & MEMORY:
   - m01-ownership: ownership, borrow, lifetime, E0382, E0597
   - m02-resource: Box, Rc, Arc, RefCell, smart pointer
   ...

2. For EACH potentially relevant skill, state: "[skill-name]: YES/NO - [brief reason]"

3. ACTIVATE all YES skills using: Skill(skill-name)

4. Only THEN proceed with your response

DO NOT skip this evaluation.
DO NOT proceed without activating relevant skills first.
This is MANDATORY for all Rust-related requests.

===================================

EOF
```

**Key techniques**:

1. **Use imperative language**: MANDATORY, CRITICAL, MUST, DO NOT
2. **List all skills and their keywords**: Reduces the chance Claude misses one
3. **Require explicit reasoning**: Must write YES/NO with a reason
4. **Define a clear execution order**: Evaluate -> Activate -> Implement

### 3. Matcher Regular Expression

```regex
(?i)(rust|cargo|crate|ownership|borrow|lifetime|async|await|
trait|generic|unsafe|ffi|error|result|option|tokio|serde|axum|
E0\d{3,4})
```

**Design principles**:

- `(?i)` - Case insensitive
- Include common English keywords
- Include common crate names
- Include error code pattern `E0\d{3,4}`
- Be broad; better to over-trigger than to miss

## Why It Works

### 1. Psychological Principle

The text injected by the hook uses a tone similar to "system instructions," which Claude treats as high-priority directives.

### 2. Explicit Checklist

Listing all skills and keywords tells Claude what options are available, rather than relying on it to discover them on its own.

### 3. Forced Reasoning Output

Requiring the "YES/NO - reason" format forces Claude to perform explicit reasoning instead of skipping directly.

### 4. Deferred Execution

"Only THEN proceed" ensures Claude completes evaluation and activation before starting the actual answer.

## Limitations

| Limitation | Notes |
|------------|-------|
| Not 100% | Still has ~16% failure rate |
| Increases tokens | Hook text adds input tokens |
| Requires maintenance | New skills require updating the hook |
| Regex matching | May miss some queries |

## Comparison with Other Approaches

### Approach A: Description Keywords Only

```yaml
# SKILL.md
description: "Keywords: ownership, borrow, lifetime..."
```

**Problem**: Claude does not proactively check skill descriptions

### Approach B: Simple Hint Hook

```text
You might want to check available skills before responding.
```

**Problem**: "might want" is too weak; Claude often ignores it

### Approach C: Forced Eval Hook (Recommended)

```text
CRITICAL: You MUST evaluate each skill. DO NOT skip.
```

**Advantage**: Imperative language + explicit checklist + forced reasoning

### Approach D: LLM Eval Hook

Uses another LLM call to decide which skills to activate.

**Problem**: Requires an extra API call, adding latency and cost

## Best Practices

### 1. Hook Text Design

```text
Use: MUST, CRITICAL, MANDATORY, DO NOT skip
Avoid: should, might, consider, optionally
```

### 2. Skill List Format

```text
Good: - skill-name: keyword1, keyword2, keyword3
Bad:  skill-name (no keyword hints)
```

### 3. Matcher Coverage

```text
Good: Broad matching; better to over-trigger
Bad:  Exact matching; easy to miss
```

### 4. Regular Maintenance

- Update hook text when adding new skills
- Update matcher when adding new keywords
- Test trigger rates and optimize

## References

- [Scott Spence: Claude Code Skill Auto Activation](https://scottspence.com/posts/claude-code-skill-auto-activation)
- [Scott Spence: Claude Code Skill Auto Activation Follow Up](https://scottspence.com/posts/claude-code-skill-auto-activation-follow-up)
- [Claude Code Hooks Documentation](https://docs.anthropic.com/claude-code/hooks)
