# Documentation Cache Specification

> Local caching mechanism for agent-fetched documentation results

## Cache Goals

- Reduce redundant network requests
- Speed up response times
- Offline availability (within cache validity period)

## Cache Location

### Priority

1. **Skill references directory** (if the skill exists)

   ```text
   ~/.claude/skills/{crate}/references/{item}.md
   ```

2. **Global cache directory** (fallback)

   ```text
   ~/.claude/cache/rust-docs/{source}/{path}.json
   ```

### Path Mapping

| Document Type | Cache Path |
|---------------|------------|
| docs.rs crate | `~/.claude/cache/rust-docs/docs.rs/{crate}/{item}.json` |
| std library | `~/.claude/cache/rust-docs/std/{module}/{item}.json` |
| releases.rs | `~/.claude/cache/rust-docs/releases.rs/{version}.json` |
| lib.rs | `~/.claude/cache/rust-docs/lib.rs/{crate}.json` |
| clippy | `~/.claude/cache/rust-docs/clippy/{lint}.json` |

## Cache Format

### JSON Structure

```json
{
  "meta": {
    "url": "https://doc.rust-lang.org/std/marker/trait.Send.html",
    "fetched_at": "2025-01-16T23:30:00Z",
    "expires_at": "2025-01-23T23:30:00Z",
    "source": "agent-browser",
    "version": "1"
  },
  "content": {
    "title": "std::marker::Send",
    "signature": "pub unsafe auto trait Send { }",
    "description": "Types that can be transferred across thread boundaries...",
    "sections": {
      "implementors": "...",
      "examples": "..."
    }
  }
}
```

### Markdown Format (for references/)

````markdown
---
url: https://doc.rust-lang.org/std/marker/trait.Send.html
fetched_at: 2025-01-16T23:30:00Z
expires_at: 2025-01-23T23:30:00Z
source: agent-browser
---

# std::marker::Send

**Signature:**

```rust
pub unsafe auto trait Send { }
```
````

**Description:**
Types that can be transferred across thread boundaries...

```text

## Expiration Times

| Document Type | Default Expiration | Notes |
|---------------|-------------------|-------|
| std library | 30 days | Stable, rarely changes |
| crate docs (stable) | 7 days | Versions may update |
| releases.rs | Never expires | Historical versions are immutable |
| lib.rs (crate info) | 1 day | Version info changes frequently |
| clippy lints | 14 days | Updates with each Rust release |

## Agent Workflow

### 1. Check Cache

```

1. Build cache path
2. Check if file exists
3. Check if expired (expires_at < now)
4. If valid, return cached content

```text

### 2. Fetch and Cache

```

1. Fetch using actionbook + agent-browser
2. Parse content
3. Generate cache file (JSON or Markdown)
4. Save to the corresponding path
5. Return content

```text

### 3. Force Refresh

Users can request a force refresh:
```

"refresh Send trait docs"
"refresh tokio::spawn docs"

```text

## Cache Management Commands

### /rust-skills:cache-status

Display cache status:
```

Rust Docs Cache Status:

- std library: 45 items, 12MB
- docs.rs: 128 items, 34MB
- releases.rs: 15 items, 2MB
- Total: 188 items, 48MB

Expired: 23 items

```text

### /rust-skills:cache-clean

Clean expired or all cache:
```

/rust-skills:cache-clean # Clean expired
/rust-skills:cache-clean --all    # Clean all
/rust-skills:cache-clean tokio    # Clean specific crate

```text

## Implementation Location

| File | Responsibility |
|------|----------------|
| `agents/docs-cache.md` | General instructions for cache checking and saving |
| `agents/docs-researcher.md` | Updated: added caching logic |
| `agents/std-docs-researcher.md` | Updated: added caching logic |
| `commands/cache-status.md` | Cache status command |
| `commands/cache-clean.md` | Cache cleanup command |
