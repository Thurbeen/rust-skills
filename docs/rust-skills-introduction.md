# Rust Skills: The Secret Weapon for More Accurate AI-Written Rust

> A Rust development assistant system built specifically for Claude Code -- through meta-question-oriented knowledge indexing, dynamically generated Skills, and precise real-time documentation retrieval, it fundamentally solves the "unreliable" problem of AI-written Rust code.

---

## 1. Origin: When AI Meets Rust

If you have ever used AI to write Rust, you have probably experienced this scenario:

> The AI confidently generates a piece of code. You eagerly press compile -- then face a screen full of red errors. Incorrect lifetimes, ownership conflicts, unsatisfied trait bounds...

**AI is reasonably reliable writing Python or JavaScript, but frequently stumbles with Rust.** This is not an illusion -- there are deep reasons behind it.

Even more frustrating is the version problem. When you ask "how to use tokio's spawn," the AI might give you a long-deprecated API. Ask "what's new in Rust 1.84," and the answer might be months out of date.

This prompted me to think about a question: **Can we build a specialized set of tools that make AI truly reliable when writing Rust?**

Rust Skills is the answer to that question.

---

## 2. Problem Analysis: Four Challenges of AI-Written Rust

### Challenge 1: Keeping the Knowledge Base Up to Date

Large language models have a training data cutoff date -- this is their Achilles' heel.

The Rust ecosystem evolves rapidly, with frequent crate version updates. The correct way to write something in the `tokio 1.0` era may be deprecated in `tokio 1.49`. When you ask about the latest version information, the model can only search its "memory," which is often outdated.

### Challenge 2: Lack of Real-Time Information Retrieval

Most AI programming assistants are "information islands":

- Cannot query crates.io for actual version numbers
- Cannot access docs.rs for accurate API documentation
- Cannot retrieve Rust version changelogs

Without tool support, AI can only rely on training data to "answer from memory."

### Challenge 3: Systematic Lack of Coding Standards

The Rust community has mature coding standard consensus: `snake_case` naming, uniform error handling patterns, specific formatting styles...

However, AI has not systematically mastered these standards. Generated code may run, but it often lacks that idiomatic Rust flavor -- it is not "Rustic" enough.

### Challenge 4: Superficial Unsafe Code Review

Unsafe Rust is a minefield that requires careful navigation. FFI bindings, raw pointer operations, memory layout control -- one wrong step can lead to memory leaks, undefined behavior (UB), or even security vulnerabilities.

Unfortunately, AI's review of unsafe code is often only surface-deep.

---

## 3. The Solution: Core Design of Rust Skills

### 3.1 Meta-Question Oriented: Making AI Think Like an Expert

The Rust Skills knowledge system is built on a core insight: **Problems in Rust development can be categorized into several "meta-questions."**

We distilled the core challenges of Rust development into 15 meta-question categories:

| Code | Meta-Question | Core Inquiry |
|:----:|---------------|-------------|
| m01 | Memory Ownership and Lifetimes | Who owns this memory? When is it freed? |
| m02 | Determinism and Flexibility of Resource Management | How to find balance between control and flexibility? |
| m06 | Error Handling Philosophy | Is this failure expected or unexpected? |
| m07 | Compile-Time Concurrency Safety Guarantees | How to let the compiler guard concurrency correctness? |
| m08 | Identifying and Crossing Safety Boundaries | Where is the boundary between safe and unsafe? |

When a user raises a question, the system automatically identifies the relevant meta-question category and invokes the corresponding specialized Skill to provide targeted help. It is like equipping the AI with an experienced Rust mentor.

### 3.2 Dynamic Skills: On-Demand Crate-Specific Knowledge Bases

**This is the most innovative design in Rust Skills.**

Facing a practical reality: the Rust ecosystem has tens of thousands of crates, and pre-building a Skill for each one is neither realistic nor necessary.

Our solution is **dynamic generation** -- creating dedicated Skills on demand based on your project's `Cargo.toml` dependencies.

Taking tokio as an example, with just one command:

```bash
cd my-async-project
/sync-crate-skills
```

The system will automatically:

1. Parse all dependencies in `Cargo.toml`
2. Generate a dedicated Skill with the latest documentation for each crate
3. Store them in the local `~/.claude/skills/` directory

Generated Skills are automatically triggered. When you ask "how to use tokio spawn," the AI will provide an accurate answer based on the latest tokio 1.49 documentation, rather than outdated "memory."

**Unique advantages of Dynamic Skills**:

| Feature | Description |
|---------|-------------|
| Version tracking | Each Skill records its corresponding crate version to ensure timeliness |
| On-demand loading | Only generates what the project actually depends on, no wasted resources |
| One-click updates | `/update-crate-skill tokio` to refresh anytime |
| Workspace support | Automatically handles complex Cargo Workspace dependency relationships |

### 3.3 Coding Standards Skill: Distilled Essence of 500+ Rules

We integrated 500+ rules from the [Rust Coding Guidelines (Chinese Edition)](https://rust-coding-guidelines.github.io/rust-coding-guidelines-zh/) with intelligent layering:

- **P Rules (Prescribed)**: ~80 core rules that must be followed
- **G Rules (Guidance)**: Recommended rules, compressed into searchable summaries

Rules are carefully classified by impact level:

| Category | Level | Typical Rule |
|----------|:-----:|-------------|
| Memory & Ownership | CRITICAL | P.MEM.LFT.01: Lifetime parameter naming conventions |
| Concurrency & Async | CRITICAL | P.MTH.LCK.01: Deadlock prevention strategies |
| Error Handling | HIGH | P.ERR.02: Prefer `expect` over `unwrap` |
| Code Style | MEDIUM | P.NAM.05: Getter methods should not use `get_` prefix |

Query any rule quickly via the `/guideline` command:

```bash
/guideline P.NAM.05     # View specific rule details
/guideline naming       # Fuzzy search for naming-related rules
```

### 3.4 Unsafe Checker: Safety Barrier Built on 40+ Rules

Given the special importance of Unsafe Rust, we extracted it into a standalone `unsafe-checker` Skill, covering:

- **Admission principles**: When unsafe is truly needed
- **Safe abstractions**: How to wrap unsafe internals in a safe shell
- **Pointer operations**: Correct usage of `NonNull`, `PhantomData`
- **FFI interop**: 18 C/Rust cross-language calling rules
- **Checklists**: Pre-write self-check + code review checklists

A fundamental principle: **Every `unsafe` block must have a `// SAFETY:` comment**.

```rust
// SAFETY: We verified above that index < len, so this access is guaranteed to be in bounds
unsafe { slice.get_unchecked(index) }
```

This is the first checkpoint of the unsafe-checker.

### 3.5 Deep Clippy Integration: Always Get the Latest Lints

Through the `clippy-researcher` Agent, the system can:

- Retrieve the latest Clippy lint list in real time
- Intelligently map lints to corresponding coding standard rules
- Provide targeted fix suggestions

```bash
/guideline --clippy needless_clone
```

---

## 4. Actionbook: The Core Engine for Precise Documentation Retrieval

**If there is one single most powerful capability to pick from Rust Skills, it would be Actionbook.**

### The Limitations of Traditional Approaches

When AI needs to query docs.rs or crates.io, the conventional approach is: fetch the entire HTML -> parse the DOM -> extract information.

This path is fraught with problems:

- **Inefficient**: Downloading and parsing entire pages is time-consuming
- **Fragile**: Minor website structure changes can break parsing
- **Noisy**: Easily mixes in irrelevant content

### Actionbook's Approach

[Actionbook](https://github.com/actionbook/actionbook) takes a smarter approach: **pre-computation**.

It pre-analyzes target websites and generates structured "action manuals" containing:

- Page function descriptions
- DOM structure analysis
- Precise CSS/XPath selectors
- Element types and executable actions

**Actual workflow**:

```text
User: "What is the latest version of tokio?"
          |
search_actions("crates.io tokio")
          |
Get pre-computed precise selectors
          |
agent-browser pinpoints the version number
          |
Returns: tokio 1.49.0
```

### Why Actionbook Is a Game-Changer

| Advantage | Description |
|-----------|-------------|
| Precise | Pre-computed selectors go straight to the target, no searching required |
| Efficient | No need to download and parse entire pages; much faster response times |
| Robust | Not affected by page detail changes |
| Structured | Outputs formatted data, not raw HTML |

In simple terms, Actionbook is like equipping AI with a "website operation manual" -- where the needed information is, which button to click, which element to extract -- all crystal clear.

### Supported Rust Ecosystem Websites

| Website | Retrieved Content |
|---------|-------------------|
| crates.io | Version numbers, download counts, dependencies |
| lib.rs | Crate details, category information |
| docs.rs | API documentation, type definitions |
| releases.rs | Rust version changelogs |

> **Strongly recommended**: If you are building any AI Agent that needs web data retrieval, Actionbook is a game-changing tool.

---

## 5. Quick Start

### 5.1 Installation

```bash
# Clone the repository
git clone https://github.com/ZhangHanDong/rust-skills.git

# Start Claude Code in plugin mode
claude --plugin-dir /path/to/rust-skills
```

### 5.2 Configure Permissions

To support background Agent execution, add permission configuration:

```bash
mkdir -p .claude
cat >> .claude/settings.local.json << 'EOF'
{
  "permissions": {
    "allow": ["Bash(agent-browser *)"]
  }
}
EOF
```

### 5.3 Core Command Quick Reference

| Command | Function | Example |
|---------|----------|---------|
| `/rust-features [ver]` | Query Rust version features | `/rust-features 1.84` |
| `/crate-info <name>` | Get crate information | `/crate-info tokio` |
| `/guideline <rule>` | Query coding standards | `/guideline P.NAM.05` |
| `/docs <crate> [item]` | Get API documentation | `/docs tokio spawn` |
| `/sync-crate-skills` | Sync project dependency Skills | - |
| `/unsafe-check [file]` | Review unsafe code | `/unsafe-check src/lib.rs` |

### 5.4 Practical Scenarios

**Scenario 1: Query crate version and usage**

```text
User: What is the latest version of tokio? How to use spawn?

Bot processing:
   1. Triggers tokio Skill
   2. crate-researcher Agent retrieves version -> 1.49.0
   3. Reads local references/task.md
   4. Returns version + complete spawn usage example
```

**Scenario 2: Unsafe code review**

```text
User: Help me check this code:
   unsafe {
       let ptr = data.as_ptr();
       *ptr.add(index)
   }

Bot result:
   - Missing SAFETY comment
   - No index bounds verification
   -> Provides fix suggestions and correct examples
```

**Scenario 3: One-click project dependency sync**

```bash
cd my-rust-project
/sync-crate-skills

# Output:
# Found 15 dependencies
# Creating Skills: tokio, serde, axum, sqlx...
# Sync complete
```

---

## 6. Closing Thoughts

Rust Skills is an open-source project dedicated to fundamentally improving the experience of AI-written Rust code.

It achieves this through four core capabilities:

- **Meta-question-oriented** knowledge indexing system
- **On-demand generated** dynamic Crate Skills
- **Actionbook-driven** precise documentation retrieval
- **Systematic** coding standards and unsafe code review

### Roadmap

- [ ] Expand domain Skills (WebAssembly, embedded development, etc.)
- [ ] IDE integration support (VSCode, IntelliJ)
- [ ] Automated quality verification
- [ ] Community-contributed Crate Skills ecosystem

### Join Us

We welcome all forms of participation:

- **Issue feedback**: Report problems, make suggestions
- **Skill contributions**: Write dedicated Skills for commonly used crates
- **Documentation improvements**: Improve instructions, add examples
- **Experience sharing**: Share your usage insights in the community

**Project URL**: [https://github.com/ZhangHanDong/rust-skills](https://github.com/ZhangHanDong/rust-skills)

---

**Let's work together to make AI-written Rust truly reliable.**

---

*This article was polished with the assistance of the Rust Skills writing-assistant Skill.*
