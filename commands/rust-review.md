# /rust-review

Lightweight Rust code review using clippy.

## Usage

```text
/rust-review [path]
```

## Parameters

- `path` (optional): Path to file or directory to review. Defaults to current directory.

## What It Does

Runs `cargo clippy` for code review:

| Check Type | Description |
|------------|-------------|
| `clippy::correctness` | Clearly incorrect code |
| `clippy::suspicious` | Suspicious code |
| `clippy::complexity` | Overly complex code |
| `clippy::perf` | Performance issues |
| `clippy::style` | Style issues |

## Workflow

1. **Read code** - Analyze target files/directories
2. **Run clippy** - `cargo clippy --message-format=json`
3. **Analyze results** - Categorize by severity
4. **Provide fix suggestions** - Code examples

## Example Output

```text
Rust Code Review: src/lib.rs

Running clippy...

═══════════════════════════════════════════
Results: 3 issues found
═══════════════════════════════════════════

ERROR (1):
  src/lib.rs:42 [clippy::unwrap_used]
    → unwrap() called on Result
    → Fix: Use ? operator or handle error explicitly

WARNING (2):
  src/lib.rs:15 [clippy::needless_clone]
    → Clone is not needed here
    → Fix: Remove .clone()

  src/lib.rs:28 [clippy::manual_map]
    → Use Option::map instead of match
    → Fix: x.map(|v| v + 1)

═══════════════════════════════════════════
```

## Clippy Configuration

Projects can configure clippy via `clippy.toml` or `Cargo.toml`:

```toml
# Cargo.toml
[lints.clippy]
unwrap_used = "deny"
expect_used = "warn"
```

## NOT Included

The following checks are **not** in the scope of `/rust-review`:

| Check | Reason | Alternative |
|-------|--------|-------------|
| `cargo fmt` | Not supported by all projects | Run manually |
| `miri` | Too heavy, requires nightly | `/audit safety` |
| `cargo audit` | Security audit scenario | `/audit security` |
| `lockbud` | Dedicated concurrency audit | `/audit concurrency` |

## Related Commands

- `/audit` - Heavy-weight security audit (using os-checker)
- `/unsafe-check` - Focused unsafe code checking
- `/guideline` - Query coding guidelines
