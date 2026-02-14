# Meta-Cognition Example: E0382 in a Trading System

> Demonstrates how the three-layer cognitive model traces a surface error back to domain constraints, providing a deeper solution.

## User Question

> "My trading system reports E0382; the data was moved"

---

## Traditional Answer (Bad)

```text
"Use .clone() to fix it"
```

**Problem**: Only fixes the surface symptom without understanding the root cause.

---

## Meta-Cognition Tracing Process

### Step 1: Identify Entry Layer

| Signal | Entry Layer | Tracing Direction |
|--------|-------------|-------------------|
| E0382 | **Layer 1** (language mechanics) | Trace UP |

**Initial Skill**: m01-ownership

---

### Step 2: Layer 1 Analysis (m01-ownership)

**Core question**: Who should own this data?

| Error | Don't Just Say | Ask Instead |
|-------|----------------|-------------|
| E0382 | "Clone it" | **Who should own this data?** |

**Thinking prompts**:

1. What is the domain role of this data? -> "Transaction record" = Transaction Record
2. Is the ownership design intentional? -> Need to check domain constraints
3. Fix the symptom or redesign? -> Trace up to understand the reason

---

### Step 3: Trace Up to Layer 3 (domain-fintech)

**Discovered domain constraints**:

| Domain Rule | Design Constraint | Rust Implementation |
|-------------|-------------------|---------------------|
| **Audit trail** | Immutable records | Arc<T>, no modification |
| Consistency | Transaction boundaries | Clear ownership |

**Key insight**:

```text
Rule: All transactions must be immutable and traceable
Reason: Regulatory compliance, dispute resolution
Rust: Use Arc<T> for sharing, event sourcing pattern
```

---

### Step 4: Trace Down to Layer 2 Design

From domain-fintech tracing down:

```text
"Need immutable transaction records"
    -> m09-domain: Model as Value Objects
    -> m01-ownership: Use Arc for sharing immutable data
```

**Design decision**: Transaction records are **Value Objects** and should be **immutably shared**, not moved or repeatedly cloned.

---

## Meta-Cognition Answer (Good)

### Reasoning Chain

```text
+- Layer 1: E0382 = ownership error
|  Problem: value used after being moved
|      ^
+- Layer 3: Trading system domain constraints
|  Rule: Transaction records must be immutable and traceable (audit requirement)
|  Implication: Data should be shared, not moved or copied
|      v
+- Layer 2: Design pattern selection
   Solution: Use Arc<TransactionRecord> to share immutable data
```

### Recommended Fix

```rust
// Before (E0382)
fn process_transaction(record: TransactionRecord) {
    save_to_db(record);        // record moved here
    send_notification(record); // E0382: use of moved value
}

// After (Meta-Cognition Fix)
use std::sync::Arc;

fn process_transaction(record: Arc<TransactionRecord>) {
    save_to_db(Arc::clone(&record));       // Arc clone = cheap
    send_notification(Arc::clone(&record)); // Still works
    audit_log(record);                      // Last use
}
```

### Why Arc Instead of clone()?

| Approach | Cost | Semantics | Domain Fit |
|----------|------|-----------|------------|
| `.clone()` | Copies entire data | Creates independent copy | Violates single source of truth |
| `Arc<T>` | Reference count +1 | Shares the same data | Meets audit requirements |

**Reasoning**:

- `clone()` copies all the data -> wastes memory, violates "single source of truth"
- `Arc<T>` shares the same data -> meets audit requirements, all references point to the same record

### Reasoning Chain Summary

```text
E0382 -> Ask "Who should own the data?" -> Discover it's an audit record ->
Domain constraint requires immutability + traceability -> Design as Arc<T> sharing ->
Not a syntax fix, but a design improvement
```

---

## Comparison

| Criteria | Traditional Answer | Meta-Cognition |
|----------|-------------------|----------------|
| Fixes the error | Yes | Yes |
| Explains why | No | Yes |
| Considers domain | No | Yes |
| Suggests design | No | Yes |
| Prevents future issues | No | Yes |

---

## Key Learnings

### 1. Don't Stop at Layer 1

The surface error (E0382) is just a symptom. The real problem may be in the design layer or the domain layer.

### 2. Domain Constraints Drive Design

Financial domain audit requirements dictate that data must be immutable and traceable, which directly affects ownership design.

### 3. Arc vs Clone Selection

| Scenario | Choice |
|----------|--------|
| Data needs to evolve independently | `clone()` |
| Data is a shared fact | `Arc<T>` |
| Financial audit records | `Arc<T>` (single source of truth) |

---

## Related Skills

| Skill | Role |
|-------|------|
| m01-ownership | Layer 1 entry point, ownership mechanics |
| m02-resource | Arc/Rc smart pointer selection |
| m09-domain | Value Object vs Entity modeling |
| domain-fintech | Financial domain constraints |

---

## References

- `_meta/reasoning-framework.md` - Complete tracing framework
- `skills/m01-ownership/SKILL.md` - Ownership skill
- `skills/domain-fintech/SKILL.md` - Financial domain constraints
