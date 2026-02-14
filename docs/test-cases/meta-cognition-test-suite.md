# Meta-Cognition Test Suite

> Designed to distinguish between "ordinary AI answers" vs "meta-cognitive traceback answers"

## Design Principles

A good test case should:

1. **An ordinary answer can "solve" the problem** - syntactically correct, compiles
2. **But the ordinary answer has hidden issues** - violates domain constraints or design principles
3. **Only understanding the domain leads to the correct recommendation**

---

## Test Case 1: Financial Precision Trap

### Problem

```text
I'm writing a payment system, and the fee calculation produces incorrect amounts:

fn calculate_fee(amount: f64, rate: f64) -> f64 {
    amount * rate
}

fn main() {
    let amount = 0.1 + 0.2;
    let fee = calculate_fee(amount, 0.03);
    println!("Fee: {}", fee);  // Outputs 0.009000000000000001 instead of 0.009
}

How do I fix this precision issue?
```

### Answer Comparison

| Level | Answer | Problem |
|-------|--------|---------|
| * Surface | `format!("{:.2}", fee)` formatted output | Only hides the problem, internally still wrong |
| ** Syntax | Use `f64::round()` to round | Cumulative errors still appear |
| *** Mechanism | Use integer cents as the unit | Viable but not professional |
| ***** Meta-cognition | **Financial systems must not use floating point; must use rust_decimal** | Understands domain constraints |

### Meta-Cognitive Traceback

```text
Layer 1: Floating point precision issue -> IEEE 754 representation limitation
    ^
Layer 3: Financial domain constraint -> Precision is a regulatory requirement, not a technical choice
    v
Layer 2: Use rust_decimal::Decimal type
```

### Correct Answer

```rust
use rust_decimal::Decimal;
use rust_decimal_macros::dec;

fn calculate_fee(amount: Decimal, rate: Decimal) -> Decimal {
    amount * rate
}

fn main() {
    let amount = dec!(0.1) + dec!(0.2);  // Exact 0.3
    let fee = calculate_fee(amount, dec!(0.03));
    println!("Fee: {}", fee);  // Exact 0.009
}
```

---

## Test Case 2: Concurrency Sharing Trap

### Problem

```text
My Web API needs to share configuration, but the compiler throws an error:

use std::rc::Rc;

struct AppConfig {
    db_url: String,
    api_key: String,
}

async fn handle_request(config: Rc<AppConfig>) {
    // Use config...
}

#[tokio::main]
async fn main() {
    let config = Rc::new(AppConfig {
        db_url: "postgres://...".into(),
        api_key: "secret".into(),
    });

    tokio::spawn(handle_request(config.clone()));  // Compile error
}

Error: `Rc<AppConfig>` cannot be sent between threads safely
How do I fix this?
```

### Answer Comparison

| Level | Answer | Problem |
|-------|--------|---------|
| * Surface | Change `Rc` to `Arc` | Correct but incomplete |
| ** Syntax | `Arc<AppConfig>` + explain Send trait | Technically correct |
| *** Mechanism | Explain Rc vs Arc differences | Still at the technical level |
| ***** Meta-cognition | **Web services are multi-threaded; config should use `&'static` or `OnceLock`; Arc is only a suboptimal solution** | Understands web domain |

### Meta-Cognitive Traceback

```text
Layer 1: Rc is not Send -> cannot cross thread boundaries
    ^
Layer 3: Web service domain constraint -> high concurrency, multi-threaded, config is immutable
    v
Layer 2: Config pattern selection:
    - OnceLock<AppConfig> (recommended, zero runtime overhead)
    - lazy_static! (classic approach)
    - Arc<AppConfig> (viable but has overhead)
```

### Correct Answer

```rust
use std::sync::OnceLock;

static CONFIG: OnceLock<AppConfig> = OnceLock::new();

fn get_config() -> &'static AppConfig {
    CONFIG.get_or_init(|| AppConfig {
        db_url: std::env::var("DATABASE_URL").unwrap(),
        api_key: std::env::var("API_KEY").unwrap(),
    })
}

async fn handle_request() {
    let config = get_config();  // Zero overhead, no clone
    // Use config...
}
```

---

## Test Case 3: Error Handling Trap

### Problem

```text
My CLI tool panics when processing files:

fn process_file(path: &str) -> String {
    let content = std::fs::read_to_string(path).unwrap();
    let config: Config = serde_json::from_str(&content).unwrap();
    config.name.to_uppercase()
}

Users report the program crashes when a file doesn't exist. How can I provide friendlier error messages?
```

### Answer Comparison

| Level | Answer | Problem |
|-------|--------|---------|
| * Surface | Use `expect("file not found")` | Still panics |
| ** Syntax | Return `Result<String, Box<dyn Error>>` | Technically correct but not professional |
| *** Mechanism | Use `anyhow` or `thiserror` | Better but doesn't consider the CLI scenario |
| ***** Meta-cognition | **CLI tools should: 1) use anyhow to simplify errors 2) handle errors uniformly in main 3) return correct exit codes 4) use miette for pretty output** | Understands CLI domain |

### Meta-Cognitive Traceback

```text
Layer 1: unwrap() panic -> needs error propagation
    ^
Layer 3: CLI domain constraint -> user experience, exit codes, scriptability
    v
Layer 2: CLI error handling patterns:
    - anyhow::Result to simplify error chains
    - main() -> Result<(), anyhow::Error>
    - Or use miette for pretty error display
```

### Correct Answer

```rust
use anyhow::{Context, Result};

fn process_file(path: &str) -> Result<String> {
    let content = std::fs::read_to_string(path)
        .with_context(|| format!("Failed to read file: {}", path))?;

    let config: Config = serde_json::from_str(&content)
        .with_context(|| format!("Failed to parse config file: {}", path))?;

    Ok(config.name.to_uppercase())
}

fn main() -> Result<()> {
    let result = process_file("config.json")?;
    println!("{}", result);
    Ok(())
}

// Or use miette for prettier error output
```

---

## Test Case 4: Async Blocking Trap

### Problem

```text
My API is slow when processing large files, and other requests get blocked:

async fn upload_handler(data: Vec<u8>) -> Result<String, Error> {
    // Compress file
    let compressed = compress(&data);  // This is a CPU-intensive operation

    // Calculate hash
    let hash = sha256(&compressed);    // This is also CPU-intensive

    // Save to storage
    storage.save(&hash, &compressed).await?;

    Ok(hash)
}

Why are other requests being blocked? How do I fix this?
```

### Answer Comparison

| Level | Answer | Problem |
|-------|--------|---------|
| * Surface | Add `.await` | Fundamentally misunderstands the problem |
| ** Syntax | Use `tokio::spawn` for parallel processing | Still blocks the thread |
| *** Mechanism | Use `spawn_blocking` | Correct but incomplete |
| ***** Meta-cognition | **Understand the tokio runtime model: CPU-intensive tasks must use spawn_blocking, or use a rayon thread pool, and consider backpressure control** | Understands the async domain |

### Meta-Cognitive Traceback

```text
Layer 1: Synchronous blocking inside an async function -> blocks the tokio worker
    ^
Layer 3: Web service domain constraint -> high concurrency, low latency, must not block the event loop
    v
Layer 2: Async architecture patterns:
    - CPU-intensive -> spawn_blocking or rayon
    - I/O-intensive -> keep async
    - Mixed -> separate concerns
```

### Correct Answer

```rust
async fn upload_handler(data: Vec<u8>) -> Result<String, Error> {
    // Move CPU-intensive operations to blocking thread pool
    let (compressed, hash) = tokio::task::spawn_blocking(move || {
        let compressed = compress(&data);
        let hash = sha256(&compressed);
        (compressed, hash)
    }).await?;

    // Keep I/O operations async
    storage.save(&hash, &compressed).await?;

    Ok(hash)
}
```

---

## Testing Method

### 1. With Plain Claude

Paste the problem code directly, observe at which level the answer stops.

### 2. With Claude + rust-skills

Same problem, you should see:

- Explicit layer traceback (Layer 1 -> 3 -> 2)
- Domain constraint identification
- Not just a "compiles fine" solution

### 3. Scoring Criteria

| Dimension | Ordinary Answer | Meta-Cognitive Answer |
|-----------|-----------------|----------------------|
| Fix the error | Yes | Yes |
| Explain the mechanism | Maybe | Yes |
| Identify domain constraints | No | Yes |
| Provide best practices | No | Yes |
| Explain why it's best | No | Yes |
| Mention related crates | Maybe | Yes (with version) |

---

## Quick Test Template

Copy the following to test directly:

```text
I'm developing a payment system, and I found a precision issue when calculating fees:

let amount = 0.1 + 0.2;
let fee = amount * 0.03;
println!("Fee: {}", fee);  // Outputs 0.009000000000000001

How do I fix this?
```

**Expected difference**:

- Ordinary: "Use round() or format the output"
- Meta-cognitive: "Financial systems must not use f64; must use rust_decimal -- this is a regulatory requirement"
