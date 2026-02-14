# /audit

Heavy-weight security and safety audit using os-checker tools.

## Usage

```text
/audit [mode]
```

## Parameters

- `mode` (optional): Audit mode
  - `security` - Security vulnerability audit (default)
  - `safety` - Unsafe code safety audit
  - `concurrency` - Concurrency issue audit
  - `full` - Full audit (all checkers)

## When to Use

| Scenario | Recommendation |
|----------|----------------|
| Daily development | Use `/rust-review` (clippy) |
| PR review | Use `/rust-review` |
| **Pre-release** | `/audit security` |
| **Unsafe code review** | `/audit safety` |
| **Concurrency code review** | `/audit concurrency` |
| **Security-critical projects** | `/audit full` |

## Audit Modes

### Security (Default)

Checks for known security vulnerabilities:

| Tool | What It Checks |
|------|----------------|
| `cargo audit` | CVEs in dependencies |
| `geiger` | Unsafe code exposure statistics |

```bash
cargo audit
cargo geiger
```

### Safety

Checks unsafe code correctness:

| Tool | What It Checks |
|------|----------------|
| `miri` | Undefined Behavior |
| `rudra` | Memory safety issues |
| `geiger` | Unsafe statistics |

```bash
cargo +nightly miri test
# rudra requires separate installation
```

**Note**: Requires nightly toolchain

### Concurrency

Checks for concurrency issues:

| Tool | What It Checks |
|------|----------------|
| `lockbud` | Deadlock detection |
| `atomvchecker` | Atomicity violations |

### Full

Runs all available checkers (slowest).

## Integration with os-checker Skills

The following skills are referenced during audit:

| Skill | Purpose |
|-------|---------|
| `os-checker-checkers` | Understand each tool's capabilities |
| `os-checker-cli` | os-checker command usage |
| `os-checker-diagnostics` | Interpret audit results |
| `os-checker-setup` | Install checking tools |

## Issue Prioritization

| Priority | Diagnostic Type | Action |
|----------|-----------------|--------|
| Critical | `Miri`, `Rudra`, `Audit`, `Cargo` | Fix immediately |
| High | `Lockbud(Probably)`, `Semver Violation` | Should fix |
| Medium | `Lockbud(Possibly)`, `Atomvchecker` | Needs review |
| Low | `Geiger`, `Outdated` | Informational |

## Example Output

```text
Security Audit Report
═══════════════════════════════════════════

[1/2] cargo audit
  ✗ 2 vulnerabilities found

  CRITICAL:
    RUSTSEC-2024-0001: Memory corruption in foo v1.2.3
    → Upgrade to foo v1.2.4

  HIGH:
    RUSTSEC-2024-0002: DoS vulnerability in bar v2.0.0
    → Upgrade to bar v2.0.1

[2/2] cargo geiger
  Unsafe usage in dependencies:
    ├── libc: 127 unsafe blocks
    ├── tokio: 45 unsafe blocks
    └── your-crate: 3 unsafe blocks

═══════════════════════════════════════════
Recommended Actions:
1. Update foo to v1.2.4 (CRITICAL)
2. Update bar to v2.0.1 (HIGH)
3. Review unsafe usage with /unsafe-check
```

## Tool Installation

```bash
# Security
cargo install cargo-audit

# Safety (needs nightly)
rustup +nightly component add miri

# Geiger
cargo install cargo-geiger

# Full os-checker suite
cargo install os-checker
```

## Batch Audit (Multiple Repos)

Use os-checker for batch auditing:

```bash
# Create configuration
cat > audit-config.json << 'EOF'
{
  "org/repo1": {},
  "org/repo2": {},
  "org/repo3": {}
}
EOF

# Batch run
os-checker run --config audit-config.json --emit results.json
```

## Related Commands

- `/rust-review` - Lightweight daily review (clippy)
- `/unsafe-check` - Unsafe code static analysis
- `/unsafe-review` - Interactive unsafe review
