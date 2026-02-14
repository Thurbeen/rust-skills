# Rust Skills: The Secret Weapon for More Accurate AI-Written Rust

> A Rust development assistant plugin built specifically for Claude Code that significantly improves AI-written Rust code quality through meta-question orientation, dynamic Skills, and precise documentation retrieval.

## 1. Motivation: Why Does AI Need Specialized Skills for Rust?

As a Rust developer, I frequently use AI for assisted programming. However, during use, I noticed a frustrating phenomenon: **AI is fairly reliable writing other languages, but frequently stumbles with Rust**.

Compilation errors, lifetime issues, ownership confusion... AI-generated Rust code often requires extensive modification to pass compilation. Worse still, when I ask about a specific crate's usage, the AI frequently gives outdated or nonexistent APIs.

This prompted me to think: **Can we build a specialized set of Skills that make AI more precise when writing Rust?**

Rust Skills is the answer to that question.

## 2. Four Challenges of AI-Written Rust

### 2.1 Stale Model Knowledge Base

Large language models have a training data cutoff date. When you ask "What's new in Rust 1.84" or "What's the latest version of tokio," the model may return information from months or even a year ago.

The Rust ecosystem evolves rapidly, with frequent crate version updates. A correct usage pattern from the `tokio 1.0` era may be deprecated or changed in `tokio 1.49`.

### 2.2 Lack of Specialized Tool Access

Most AI programming assistants lack the ability to retrieve real-time Rust ecosystem information:

- Cannot query crates.io for the latest versions
- Cannot access docs.rs for accurate API documentation
- Cannot retrieve Rust version changelogs

The result is that AI can only rely on "memory" from training data, which is often inaccurate.

### 2.3 No Coding Standards Guidance

Rust has its own unique coding standards and best practices. Naming conventions (snake_case vs CamelCase), formatting rules, error handling patterns... all have community consensus.

However, most AI has not systematically learned these standards. Generated code may run, but it is not "Rustic" enough.

### 2.4 Missing Unsafe Standards

Unsafe Rust is an area that requires special care. FFI bindings, raw pointer operations, memory layout control... these all require strict adherence to safety standards.

An incorrect unsafe usage can lead to undefined behavior (UB), memory leaks, or even security vulnerabilities. Yet AI's review of unsafe code is often not rigorous enough.

## 3. How Rust Skills Solves These Problems

### 3.1 Core Architecture: Meta-Question Oriented

Rust Skills employs a unique **Meta-Question Oriented** knowledge indexing system that classifies core problems in Rust development into 15 meta-question categories:

| Code | Meta-Question | Core Inquiry |
|------|---------------|-------------|
| m01 | Memory Ownership and Lifetimes | Who owns this memory? When is it freed? |
| m02 | Resource Management Balance | How to balance determinism with flexibility? |
| m06 | Error Handling Philosophy | Is the failure expected or unexpected? |
| m07 | Concurrency Correctness | How to ensure concurrency safety at compile time? |
| m08 | Safety Boundaries | Where is the safety boundary? How to build a bridge? |

When a user encounters a problem, Rust Skills automatically identifies the question category and invokes the corresponding Skill to provide targeted help.

### 3.2 Dynamic Skills: On-Demand Crate Knowledge Base

This is one of the most distinctive features of Rust Skills.

**Problem**: The Rust ecosystem has tens of thousands of crates; it is impossible to pre-create a Skill for each one.

**Solution**: Dynamic Skills **generate on demand** based on dependencies in the project's `Cargo.toml`.

Taking tokio as an example:

```bash
# Enter your Rust project
cd my-async-project

# Sync all dependency Skills
/sync-crate-skills
```

The system will:

1. Parse dependencies in `Cargo.toml`
2. Generate a dedicated Skill for each dependency
3. Store them in `~/.claude/skills/`

The generated tokio Skill looks like this:

```yaml
name: tokio
description: |
  CRITICAL: Use for tokio async runtime questions. Triggers on:
  tokio, spawn, spawn_blocking, select!, join!, try_join!,
  mpsc, oneshot, broadcast, watch, channel, Mutex, RwLock,
  timeout, sleep, interval, Duration, async I/O,
  async runtime, spawn usage, tokio examples, tokio tutorial
```

When you ask "how to use tokio spawn," this Skill will be automatically triggered, and the AI will provide an accurate answer based on the latest tokio documentation.

**Advantages of Dynamic Skills**:

- **Version tracking**: Records crate version to ensure documentation timeliness
- **On-demand loading**: Only generates what you need, no wasted resources
- **Updatable**: Refresh anytime via `/update-crate-skill tokio`
- **Workspace support**: Automatically handles multi-crate Cargo Workspace projects

### 3.3 Coding Standards Skill: Distilled Essence of 500+ Rules

Rust Skills integrates 500+ coding rules from the [Rust Coding Guidelines (Chinese Edition)](https://rust-coding-guidelines.github.io/rust-coding-guidelines-zh/) with intelligent compression:

- **P Rules (Prescribed)**: ~80 core rules that must be followed
- **G Rules (Guidance)**: Recommended rules, compressed into summaries

Rules are classified by impact level:

| Category | Impact Level | Example Rule |
|----------|-------------|-------------|
| Memory & Ownership | CRITICAL | P.MEM.LFT.01: Lifetime naming conventions |
| Concurrency & Async | CRITICAL | P.MTH.LCK.01: Deadlock prevention |
| Error Handling | HIGH | P.ERR.02: Use expect instead of unwrap |
| Code Style | MEDIUM | P.NAM.05: Getter methods should not use get_ prefix |

Query any rule via the `/guideline` command:

```bash
/guideline P.NAM.05    # View specific rule
/guideline naming      # Search for naming-related rules
```

### 3.4 Unsafe Checker: Safety Guardian with 40+ Rules

Given the special nature of Unsafe Rust, we extracted it into a standalone `unsafe-checker` Skill:

- **General principles**: When unsafe should actually be used
- **Safe abstractions**: How to build safe API wrappers
- **Raw pointer operations**: Correct usage of NonNull, PhantomData
- **FFI interop**: 18 C/Rust interop rules
- **Checklists**: Pre-write and code review checklists

```rust
// SAFETY: We checked above that index < len, so this is safe
unsafe { slice.get_unchecked(index) }
```

Every `unsafe` block should have a `// SAFETY:` comment -- this is the first thing the unsafe-checker checks.

### 3.5 Clippy Integration: Dynamically Fetch Latest Lint Information

Through the `clippy-researcher` Agent, Rust Skills can:

- Retrieve the latest Clippy lint list
- Map lints to coding standard rules
- Provide fix suggestions

```bash
/guideline --clippy needless_clone
```

## 4. Actionbook: The Core Engine for Precise Documentation Retrieval

**This is the most powerful secret weapon of Rust Skills.**

### 4.1 Problem: AI's Difficulty Retrieving Web Documentation

When AI needs to query docs.rs or crates.io information, the traditional approach is:

1. Fetch the entire HTML page
2. Parse the DOM structure
3. Extract the needed information

Problems with this approach:

- **Slow**: Requires downloading the entire page
- **Unstable**: Website structure changes can break parsing
- **Inaccurate**: May extract irrelevant content

### 4.2 Solution: Pre-Computed Action Manuals

[Actionbook](https://github.com/actionbook/actionbook) is a pre-computed website action manual database containing:

- Page descriptions and function explanations
- DOM structure analysis
- Precise CSS/XPath selectors
- Element types and allowed operations

**Workflow**:

```text
User asks about the latest version of tokio
    |
search_actions("crates.io tokio")
    |
Get pre-computed selectors
    |
agent-browser precisely extracts the version number
    |
Returns: tokio 1.49.0
```

### 4.3 Why Actionbook Is So Powerful

1. **Precise extraction**: Uses pre-computed selectors to directly fetch target data
2. **Efficient and stable**: No need to parse entire pages; fast and not affected by page changes
3. **Structured output**: Returns formatted data, not raw HTML

It is like equipping AI with a "website user manual" -- it knows where to find the needed information, which button to click, which element to extract.

### 4.4 Supported Websites

Actionbook currently supports key Rust ecosystem websites:

| Website | Purpose |
|---------|---------|
| crates.io | Crate versions, download counts, dependencies |
| lib.rs | Detailed crate information, categories |
| docs.rs | API documentation, type definitions |
| releases.rs | Rust version changelogs |

**Strongly recommended**: If you are building any AI Agent that requires browser automation, Actionbook is an essential tool. It will fundamentally change how you retrieve web data.

## 5. Installation and Usage

### 5.1 Installation

```bash
# Clone the repository
git clone https://github.com/ZhangHanDong/rust-skills.git

# Start Claude Code with the plugin
claude --plugin-dir /path/to/rust-skills
```

### 5.2 Configure Permissions

To support background Agent execution, configure permissions:

```bash
mkdir -p .claude
cat >> .claude/settings.local.json << 'EOF'
{
  "permissions": {
    "allow": [
      "Bash(agent-browser *)"
    ]
  }
}
EOF
```

### 5.3 Common Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/rust-features [version]` | Get Rust version features | `/rust-features 1.84` |
| `/crate-info <crate>` | Get crate information | `/crate-info tokio` |
| `/guideline <rule>` | Query coding standards | `/guideline P.NAM.05` |
| `/docs <crate> [item]` | Get API documentation | `/docs tokio spawn` |
| `/sync-crate-skills` | Sync Cargo.toml dependency Skills | - |
| `/unsafe-check [file]` | Check unsafe code | `/unsafe-check src/lib.rs` |

### 5.4 Usage Examples

**Example 1: Query tokio latest version and basic usage**

```text
User: What is the latest version of tokio? How to use spawn?

Claude:
1. Triggers tokio Skill
2. Calls crate-researcher Agent to get version
3. Reads local references/task.md documentation
4. Returns version information and spawn usage examples
```

**Example 2: Check unsafe code**

```text
User: Help me check if this unsafe code has problems

unsafe {
    let ptr = data.as_ptr();
    *ptr.add(index)
}

Claude:
1. Triggers unsafe-checker Skill
2. Checks for SAFETY comment - missing
3. Checks bounds verification - missing
4. Provides fix suggestions and correct examples
```

**Example 3: Sync project dependency Skills**

```bash
# Enter project directory
cd my-rust-project

# Sync Skills
/sync-crate-skills

# Output:
# Found 15 dependencies
# Creating skills for: tokio, serde, axum, sqlx, ...
# Skills synced successfully
```

## 6. Summary and Call to Action

Rust Skills is an open-source project aimed at helping AI better understand and write Rust code. It achieves this through:

- **Meta-question-oriented** knowledge indexing
- **Dynamically generated** Crate Skills
- **Precise retrieval** via Actionbook integration
- **Strict standards** for coding and unsafe code review

These significantly improve the accuracy and quality of AI-written Rust code.

### Future Plans

- [ ] More domain Skills (WebAssembly, embedded, etc.)
- [ ] IDE integration (VSCode, IntelliJ)
- [ ] Automated testing and verification
- [ ] Community-contributed Crate Skills

### Contributing

We welcome contributions in any form:

- **Submit Issues**: Report problems or make suggestions
- **Contribute Skills**: Write dedicated Skills for commonly used crates
- **Improve Documentation**: Enhance instructions and examples
- **Share Experiences**: Share your usage experiences in the community

**Repository URL**: [https://github.com/ZhangHanDong/rust-skills](https://github.com/ZhangHanDong/rust-skills)

Let's work together to make AI-written Rust more accurate!

---

*Author's note: This article was written with AI assistance*
