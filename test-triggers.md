# Rust Skills Trigger Test Checklist

> Run these queries in a project that has rust-skills installed, and verify the correct skill is triggered.

## How to Test

1. Go to a Rust project directory with rust-skills plugin installed
2. Run each query below with `claude -p "query"`
3. Check if the expected skill is triggered (shown in Claude Code status line)

---

## Layer 1: Language Mechanics

## Ownership (m01-ownership)

| Query | Expected Skill |
|-------|----------------|
| `how to fix E0382` | m01-ownership |
| `value moved after use` | m01-ownership |
| `borrowed value does not live long enough` | m01-ownership |
| `how to fix borrow errors` | m01-ownership |
| `lifetime annotation` | m01-ownership |
| `E0597 lifetime too short` | m01-ownership |

## Resource (m02-resource)

| Query | Expected Skill |
|-------|----------------|
| `difference between Arc and Rc` | m02-resource |
| `Box vs Rc vs Arc` | m02-resource |
| `smart pointer selection` | m02-resource |
| `shared ownership` | m02-resource |

## Mutability (m03-mutability)

| Query | Expected Skill |
|-------|----------------|
| `E0499 multiple mutable borrows` | m03-mutability |
| `E0502 borrow conflict` | m03-mutability |
| `E0596 cannot borrow as mutable` | m03-mutability |
| `Cell vs RefCell` | m03-mutability |
| `interior mutability` | m03-mutability |

## Zero-Cost (m04-zero-cost)

| Query | Expected Skill |
|-------|----------------|
| `E0277 trait bound not satisfied` | m04-zero-cost |
| `generic vs trait object` | m04-zero-cost |
| `monomorphization` | m04-zero-cost |
| `E0308 type mismatch` | m04-zero-cost |
| `E0282 type annotations needed` | m04-zero-cost |

## Type-Driven (m05-type-driven)

| Query | Expected Skill |
|-------|----------------|
| `newtype pattern` | m05-type-driven |
| `PhantomData usage` | m05-type-driven |
| `type state pattern` | m05-type-driven |
| `zero-sized type ZST` | m05-type-driven |
| `marker trait` | m05-type-driven |

## Error Handling (m06-error-handling)

| Query | Expected Skill |
|-------|----------------|
| `when to use panic` | m06-error-handling |
| `Result vs Option` | m06-error-handling |
| `how to use thiserror` | m06-error-handling |
| `anyhow vs eyre` | m06-error-handling |
| `error propagation` | m06-error-handling |

## Concurrency (m07-concurrency)

| Query | Expected Skill |
|-------|----------------|
| `cannot be sent between threads` | m07-concurrency |
| `how to use async await` | m07-concurrency |
| `Send Sync trait` | m07-concurrency |
| `how to avoid deadlock` | m07-concurrency |
| `how to share data between threads` | m07-concurrency |

---

## Layer 2: Design Choices

## Domain Modeling (m09-domain)

| Query | Expected Skill |
|-------|----------------|
| `DDD in Rust` | m09-domain |
| `domain model design` | m09-domain |
| `aggregate root` | m09-domain |
| `value object vs entity` | m09-domain |
| `domain modeling` | m09-domain |

## Performance (m10-performance)

| Query | Expected Skill |
|-------|----------------|
| `Rust performance optimization` | m10-performance |
| `how to write benchmarks` | m10-performance |
| `criterion usage` | m10-performance |
| `cache locality` | m10-performance |
| `zero copy` | m10-performance |

## Ecosystem (m11-ecosystem)

| Query | Expected Skill |
|-------|----------------|
| `recommend a crate` | m11-ecosystem |
| `dependency selection` | m11-ecosystem |
| `crate comparison` | m11-ecosystem |
| `Cargo.toml dependency management` | m11-ecosystem |
| `feature flags usage` | m11-ecosystem |

## Lifecycle (m12-lifecycle)

| Query | Expected Skill |
|-------|----------------|
| `RAII pattern` | m12-lifecycle |
| `Drop trait implementation` | m12-lifecycle |
| `resource release order` | m12-lifecycle |
| `scopeguard usage` | m12-lifecycle |
| `destructor` | m12-lifecycle |

## Domain Error (m13-domain-error)

| Query | Expected Skill |
|-------|----------------|
| `retry strategy` | m13-domain-error |
| `circuit breaker implementation` | m13-domain-error |
| `error recovery patterns` | m13-domain-error |
| `backoff retry` | m13-domain-error |
| `error classification handling` | m13-domain-error |

## Mental Model (m14-mental-model)

| Query | Expected Skill |
|-------|----------------|
| `how to learn Rust` | m14-mental-model |
| `Rust way of thinking` | m14-mental-model |
| `transitioning from Java to Rust` | m14-mental-model |
| `ownership mental model` | m14-mental-model |
| `why is Rust designed this way` | m14-mental-model |

## Anti-Pattern (m15-anti-pattern)

| Query | Expected Skill |
|-------|----------------|
| `common Rust mistakes` | m15-anti-pattern |
| `code smell Rust` | m15-anti-pattern |
| `Rust anti-patterns` | m15-anti-pattern |
| `don't write Rust like this` | m15-anti-pattern |
| `clone overuse` | m15-anti-pattern |

---

## Core Skills

## Unsafe (unsafe-checker)

| Query | Expected Skill |
|-------|----------------|
| `how to write unsafe code` | unsafe-checker |
| `FFI bindings` | unsafe-checker |
| `SAFETY comment` | unsafe-checker |
| `raw pointer` | unsafe-checker |
| `how to call C functions` | unsafe-checker |

## Version/Crate (rust-learner)

| Query | Expected Skill |
|-------|----------------|
| `tokio latest version` | rust-learner |
| `what's new in Rust 1.85` | rust-learner |
| `serde docs` | rust-learner |
| `crate info` | rust-learner |

## Code Style (coding-guidelines)

| Query | Expected Skill |
|-------|----------------|
| `Rust naming conventions` | coding-guidelines |
| `clippy warning` | coding-guidelines |
| `rustfmt configuration` | coding-guidelines |
| `P.NAM.01` | coding-guidelines |

## Router (rust-router)

| Query | Expected Skill |
|-------|----------------|
| `analyze the intent of this question` | rust-router |
| `intent analysis` | rust-router |
| `what type of Rust question is this` | rust-router |

## Layer 3: Domain Constraints

## Domains

| Query | Expected Skill |
|-------|----------------|
| `kubernetes operator in Rust` | domain-cloud-native |
| `decimal precision calculation` | domain-fintech |
| `machine learning tensor` | domain-ml |
| `IoT sensor` | domain-iot |
| `axum web server` | domain-web |
| `clap CLI argument` | domain-cli |
| `no_std embedded` | domain-embedded |

---

## Quick Test Commands

```bash
# Layer 1: Language Mechanics
claude -p "how to fix E0382"              # m01-ownership
claude -p "E0499 multiple mutable borrows" # m03-mutability
claude -p "newtype pattern"              # m05-type-driven
claude -p "Send Sync trait"              # m07-concurrency

# Layer 2: Design Choices
claude -p "DDD in Rust"                  # m09-domain
claude -p "how to write benchmarks"      # m10-performance
claude -p "recommend a crate"            # m11-ecosystem
claude -p "RAII pattern"                 # m12-lifecycle
claude -p "circuit breaker implementation" # m13-domain-error
claude -p "how to learn Rust"            # m14-mental-model
claude -p "common Rust mistakes"         # m15-anti-pattern

# Core Skills
claude -p "how to write unsafe code"     # unsafe-checker
claude -p "tokio latest version"         # rust-learner
claude -p "Rust naming conventions"      # coding-guidelines

# Layer 3: Domains
claude -p "axum web server"              # domain-web
claude -p "decimal precision calculation" # domain-fintech
```

## Expected Behavior

When a skill triggers correctly, you should see:

1. The skill name in Claude Code's status line
2. Response content that matches the skill's expertise
3. References to patterns/rules from that skill

## Troubleshooting

If skills don't trigger:

1. Ensure rust-skills plugin is installed: `claude /plugins`
2. Check plugin path is correct
3. Verify SKILL.md files have `description:` field with keywords
4. Try more specific keywords from the skill description
