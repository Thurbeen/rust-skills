# Layer 2 Skills Test Scenarios

> Layer 2: Design Choices

## m05-type-driven

| Query | Expected Skill | Expected Elements |
|-------|----------------|-------------------|
| `newtype pattern` | m05-type-driven | wrapper, type safety |
| `PhantomData usage` | m05-type-driven | marker, lifetime |
| `type state pattern` | m05-type-driven | state machine, compile-time |
| `zero-sized type ZST` | m05-type-driven | zero-sized, marker |

### Test Commands

```bash
claude -p "newtype pattern"
claude -p "PhantomData usage"
```

---

## m09-domain

| Query | Expected Skill | Expected Elements |
|-------|----------------|-------------------|
| `DDD in Rust` | m09-domain | aggregate, entity |
| `domain model design` | m09-domain | value object, repository |
| `domain modeling` | m09-domain | bounded context |
| `aggregate root` | m09-domain | invariant, consistency |

### Test Commands

```bash
claude -p "DDD in Rust"
claude -p "domain modeling"
```

---

## m10-performance

| Query | Expected Skill | Expected Elements |
|-------|----------------|-------------------|
| `Rust performance optimization` | m10-performance | profiling, bottleneck |
| `how to write benchmarks` | m10-performance | criterion, bench |
| `criterion usage` | m10-performance | black_box, throughput |
| `zero copy` | m10-performance | Cow, bytes |

### Test Commands

```bash
claude -p "Rust performance optimization"
claude -p "how to write benchmarks"
```

---

## m11-ecosystem

| Query | Expected Skill | Expected Elements |
|-------|----------------|-------------------|
| `recommend a crate` | m11-ecosystem | crates.io, popularity |
| `dependency selection` | m11-ecosystem | maintenance, features |
| `Cargo.toml dependency management` | m11-ecosystem | version, workspace |
| `feature flags usage` | m11-ecosystem | optional, cfg |

### Test Commands

```bash
claude -p "recommend a crate"
claude -p "feature flags usage"
```

---

## m12-lifecycle

| Query | Expected Skill | Expected Elements |
|-------|----------------|-------------------|
| `RAII pattern` | m12-lifecycle | Drop, scope |
| `Drop trait implementation` | m12-lifecycle | destructor, cleanup |
| `resource release order` | m12-lifecycle | drop order, field |
| `scopeguard usage` | m12-lifecycle | defer, guard |

### Test Commands

```bash
claude -p "RAII pattern"
claude -p "Drop trait implementation"
```

---

## m13-domain-error

| Query | Expected Skill | Expected Elements |
|-------|----------------|-------------------|
| `retry strategy` | m13-domain-error | backoff, exponential |
| `circuit breaker implementation` | m13-domain-error | state, threshold |
| `error recovery patterns` | m13-domain-error | fallback, graceful |
| `error classification handling` | m13-domain-error | transient, permanent |

### Test Commands

```bash
claude -p "retry strategy"
claude -p "circuit breaker implementation"
```

---

## m14-mental-model

| Query | Expected Skill | Expected Elements |
|-------|----------------|-------------------|
| `how to learn Rust` | m14-mental-model | ownership, mindset |
| `Rust way of thinking` | m14-mental-model | borrow checker, mental model |
| `transitioning from Java to Rust` | m14-mental-model | comparison, transition |
| `why is Rust designed this way` | m14-mental-model | rationale, philosophy |

### Test Commands

```bash
claude -p "how to learn Rust"
claude -p "Rust way of thinking"
```

---

## m15-anti-pattern

| Query | Expected Skill | Expected Elements |
|-------|----------------|-------------------|
| `common Rust mistakes` | m15-anti-pattern | pitfall, mistake |
| `code smell Rust` | m15-anti-pattern | refactor, improve |
| `Rust anti-patterns` | m15-anti-pattern | avoid, better |
| `clone overuse` | m15-anti-pattern | unnecessary, performance |

### Test Commands

```bash
claude -p "common Rust mistakes"
claude -p "clone overuse"
```

---

## Validation Checklist

- [ ] All Layer 2 skills trigger correctly
- [ ] Design-related queries route properly
- [ ] All trigger keywords work
- [ ] No conflicts with Layer 1 skills
