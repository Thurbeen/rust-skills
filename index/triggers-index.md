# Trigger Keywords Index

Complete mapping of keywords to skills.

---

## Error Codes → Skills

| Error Code | Description | Route To |
|------------|-------------|----------|
| E0382 | Use of moved value | m01-ownership |
| E0597 | Lifetime too short | m01-ownership |
| E0506 | Cannot assign to borrowed | m01-ownership |
| E0507 | Cannot move out of borrowed | m01-ownership |
| E0515 | Return local reference | m01-ownership |
| E0716 | Temporary value dropped | m01-ownership |
| E0106 | Missing lifetime specifier | m01-ownership |
| E0596 | Cannot borrow as mutable | m03-mutability |
| E0499 | Multiple mutable borrows | m03-mutability |
| E0502 | Borrow conflict | m03-mutability |
| E0277 | Trait bound not satisfied | m04-zero-cost / m07-concurrency |
| E0308 | Type mismatch | m04-zero-cost |
| E0599 | No method found | m04-zero-cost |
| E0038 | Trait not object-safe | m04-zero-cost |
| E0433 | Cannot find crate/module | m11-ecosystem |

---

## Keywords → Skills

### Layer 1: Language Mechanics

| Keywords | Route To |
|----------|----------|
| ownership, borrow, lifetime, move, moved value | m01-ownership |
| Box, Rc, Arc, RefCell, Cell, smart pointer | m02-resource |
| mut, mutable, interior mutability | m03-mutability |
| generic, trait, inline, monomorphization | m04-zero-cost |
| type state, phantom, newtype, PhantomData | m05-type-driven |
| Result, Option, Error, panic, ?, anyhow, thiserror | m06-error-handling |
| Send, Sync, thread, async, await, channel, tokio | m07-concurrency |
| unsafe, FFI, extern, raw pointer, transmute | unsafe-checker |

### Layer 2: Design Choices

| Keywords | Route To |
|----------|----------|
| domain model, DDD, business logic | m09-domain |
| performance, optimization, benchmark, profiling | m10-performance |
| crate, dependency, interop, ecosystem | m11-ecosystem |
| RAII, Drop, resource lifecycle | m12-lifecycle |
| domain error, retry, circuit breaker, recovery | m13-domain-error |
| mental model, how to think, learning Rust | m14-mental-model |
| anti-pattern, common mistake, pitfall, code smell | m15-anti-pattern |

### Layer 3: Domain Constraints

| Keywords | Route To |
|----------|----------|
| fintech, trading, decimal, currency, payment | domain-fintech |
| web, HTTP, REST, axum, actix, handler | domain-web |
| CLI, command line, clap, terminal | domain-cli |
| kubernetes, docker, grpc, microservice | domain-cloud-native |
| embedded, no_std, microcontroller, firmware | domain-embedded |
| ML, tensor, model, inference, ndarray | domain-ml |
| IoT, sensor, mqtt, edge | domain-iot |

---

## Query Patterns → Actions

| Pattern | Action |
|---------|--------|
| "compare" / "vs" | Enable Negotiation Protocol |
| "best practice" | Enable Negotiation Protocol |
| Domain + Error (e.g., "trading system E0382") | Enable Negotiation Protocol |
| Single error code (e.g., "E0382") | Direct lookup, no negotiation |
| Single version query (e.g., "tokio version") | Direct lookup, no negotiation |

---

## Priority Rules

When multiple skills match, use this priority:

1. **Error codes** take highest priority (direct mapping)
2. **Domain keywords** + error → load BOTH domain skill and error skill
3. **Comparison queries** → enable negotiation, load multiple skills
4. **General keywords** → route to most specific skill

### Conflict Resolution

| Conflict | Resolution |
|----------|------------|
| unsafe in m11 vs unsafe-checker | unsafe-checker (more specific) |
| error in m06 vs m13 | m06 for general, m13 for domain-specific |
| RAII in m01 vs m12 | m12 for design, m01 for implementation |

---

## Related Documents

| Document | Purpose |
|----------|---------|
| [skills-index.md](./skills-index.md) | Complete skill catalog with descriptions |
| [meta-questions.md](./meta-questions.md) | Meta-question category definitions |
| [domain-extensions.md](./domain-extensions.md) | Domain-specific code ranges |

### Framework

| File | Purpose |
|------|---------|
| [../_meta/reasoning-framework.md](../_meta/reasoning-framework.md) | How to trace through cognitive layers |
| [../_meta/negotiation-protocol.md](../_meta/negotiation-protocol.md) | When negotiation triggers |

### Router

| File | Purpose |
|------|---------|
| [../skills/rust-router/SKILL.md](../skills/rust-router/SKILL.md) | Implements these routing rules |
