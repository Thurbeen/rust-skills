# Skill Inheritance Mechanism

> Claude Code Skills have no native inheritance, but similar effects can be achieved through various methods

## Background

Claude Code Skills are independent:

- Each skill triggers independently based on `description` keywords
- Parent skills are not automatically loaded
- Shared rules need to be repeated in each skill

## Solution Comparison

| Solution | Portability | Maintenance Cost | Applicable Scenario |
|----------|-------------|------------------|---------------------|
| A: Symlinks + Explicit Reads | Low | Low | Local personal skills |
| B: Hook Injection | High | Low | Distributed plugins |
| C: Global CLAUDE.md | High | Low | Universal rules |
| D: Copy Inline | High | High | Simple scenarios |

---

## Solution A: Symlinks + Explicit Reads

**Applicable to**: Local personal skills (`~/.claude/skills/`)

### Directory Structure

```text
~/.claude/skills/
├── _shared/                          # Shared file directory
│   ├── rust-defaults.md              # Rust common rules
│   └── python-defaults.md            # Python common rules
│
├── tokio/
│   ├── SKILL.md
│   └── references/
│       └── rust-defaults.md → ../../_shared/rust-defaults.md
│
├── tokio-task/
│   ├── SKILL.md
│   └── references/
│       └── rust-defaults.md → ../../_shared/rust-defaults.md
│
└── serde/
    ├── SKILL.md
    └── references/
        └── rust-defaults.md → ../../_shared/rust-defaults.md
```

### Setup Steps

```bash
# 1. Create shared directory
mkdir -p ~/.claude/skills/_shared

# 2. Create shared rules file
cat > ~/.claude/skills/_shared/rust-defaults.md << 'EOF'
# Rust Code Generation Defaults

## Cargo.toml
- edition = "2024" (NOT 2021)
- Use latest stable crate versions

## Code Style
- Prefer explicit error handling over .unwrap()
- Use anyhow/thiserror for errors
EOF

# 3. Create symlinks for each skill
for skill in tokio tokio-task tokio-sync serde axum; do
    mkdir -p ~/.claude/skills/$skill/references
    ln -sf ../../_shared/rust-defaults.md ~/.claude/skills/$skill/references/rust-defaults.md
done
```

### Referencing in SKILL.md

```markdown
## Code Generation Rules

**IMPORTANT: Before generating code, read `./references/rust-defaults.md`**

Key rules (see rust-defaults.md for full list):

- Use edition = "2024"
- Use latest crate versions
```

### Pros and Cons

| Pros | Cons |
|------|------|
| Edit once, applies everywhere | Symlinks are not portable |
| Clear file organization | Links break when distributed to others |
| Supports multiple shared files | Requires initial setup |

---

## Solution B: Hook Injection

**Applicable to**: Distributed plugins (e.g., rust-skills)

### Principle

Inject shared rules when the user submits input via a `UserPromptSubmit` hook:

```text
User input -> Hook triggers -> Inject rules -> Claude processes
```

### Directory Structure

```text
my-plugin/
├── .claude/
│   ├── settings.json           # Hook configuration
│   └── hooks/
│       └── inject-rules.sh     # Rule injection script
└── skills/
    └── ...                     # No symlinks needed
```

### Configuration Files

**.claude/settings.json**:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "(?i)(rust|cargo|tokio|async|await)",
        "command": ".claude/hooks/inject-rules.sh"
      }
    ]
  }
}
```

**.claude/hooks/inject-rules.sh**:

```bash
#!/bin/bash
cat << 'EOF'

=== CODE GENERATION RULES ===

When generating Rust code:
- Use edition = "2024" in Cargo.toml
- Use latest stable crate versions
- Prefer explicit error handling

===

EOF
```

### Pros and Cons

| Pros | Cons |
|------|------|
| Fully portable | Injected on every request (increases tokens) |
| No file structure dependency | Requires hook support |
| Works immediately upon installation | Rules are in scripts, harder to edit |

---

## Solution C: Global CLAUDE.md

**Applicable to**: Rules universal to all projects

### File Location

```text
~/.claude/CLAUDE.md    # Global, applies to all sessions
```

### Example Content

```markdown
# Global Claude Code Rules

## Rust Defaults

- Use edition = "2024"
- Use latest crate versions

## Python Defaults

- Use Python 3.12+
- Use type hints
```

### Pros and Cons

| Pros | Cons |
|------|------|
| Simplest | Applies to all projects (may be too broad) |
| Single configuration point | Cannot differentiate by domain |
| Always in effect | May conflict with project rules |

---

## Solution D: Copy Inline

**Applicable to**: Simple scenarios, few skills

### Approach

Directly copy the same rules into each SKILL.md:

```markdown
# tokio/SKILL.md

## Code Generation Rules

- Use edition = "2024"
- Use latest crate versions

## tokio-task/SKILL.md

## Code Generation Rules

- Use edition = "2024"        # Duplicated
- Use latest crate versions # Duplicated
```

### Pros and Cons

| Pros | Cons |
|------|------|
| Most portable | Rules duplicated, hard to maintain |
| No dependencies | Updates require editing multiple places |
| Simple and direct | Easily becomes inconsistent |

---

## Recommended Combination

```text
+----------------------------------------------------------+
|                    Decision Tree                          |
+----------------------------------------------------------+

Personal use or distribution?
    |
    +-- Personal use -> Symlinks + Explicit Reads (Solution A)
    |                   Easy to maintain; edit once, applies everywhere
    |
    +-- Distribute to others -> Plugin or standalone skill?
                                |
                                +-- Plugin -> Hook Injection (Solution B)
                                |            Portable; works immediately upon installation
                                |
                                +-- Standalone skill -> Copy Inline (Solution D)
                                                       Simple, no dependencies
```

---

## Practical Examples

### Example 1: Personal tokio skills series

```bash
# Using Solution A
~/.claude/skills/
├── _shared/rust-defaults.md
├── tokio/references/rust-defaults.md -> ...
├── tokio-task/references/rust-defaults.md -> ...
└── tokio-sync/references/rust-defaults.md -> ...
```

### Example 2: rust-skills plugin

```bash
# Using Solution B
rust-skills/
├── .claude/hooks/rust-skill-eval-hook.sh  # Injects edition 2024 and other rules
└── skills/m01-ownership/SKILL.md          # No symlinks needed
```

### Example 3: Universal code style

```bash
# Using Solution C
~/.claude/CLAUDE.md  # Write universal rules; applies to all projects
```

---

## Automation Script

### Batch Create Symlinks

```bash
#!/bin/bash
# setup-skill-inheritance.sh

SHARED_DIR="$HOME/.claude/skills/_shared"
SHARED_FILE="rust-defaults.md"

# Create shared directory
mkdir -p "$SHARED_DIR"

# Create symlinks for specified skills
for skill in "$@"; do
    skill_dir="$HOME/.claude/skills/$skill"
    if [ -d "$skill_dir" ]; then
        mkdir -p "$skill_dir/references"
        ln -sf "../../_shared/$SHARED_FILE" "$skill_dir/references/$SHARED_FILE"
        echo "Done: $skill"
    else
        echo "Not found: $skill"
    fi
done
```

Usage:

```bash
./setup-skill-inheritance.sh tokio tokio-task tokio-sync serde axum
```

---

## Summary

| Your Situation | Recommended Solution |
|----------------|---------------------|
| Local personal skills | **Symlinks** (Solution A) |
| Distributed plugin | **Hook Injection** (Solution B) |
| Universal global rules | **Global CLAUDE.md** (Solution C) |
| Simple standalone skill | **Copy Inline** (Solution D) |
