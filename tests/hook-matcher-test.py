#!/usr/bin/env python3
"""
TDD tests for rust-skills hook matcher
Run: python3 tests/hook-matcher-test.py
"""

import re
import json
import sys
from pathlib import Path

# Load matcher from hooks.json
hooks_path = Path(__file__).parent.parent / "hooks" / "hooks.json"
with open(hooks_path) as f:
    hooks_config = json.load(f)

MATCHER = hooks_config["hooks"]["UserPromptSubmit"][0]["matcher"]

print(f"=== Hook Matcher TDD Tests ===")
print(f"Matcher loaded from: {hooks_path}\n")

# Test cases: (input, should_match, expected_match_word)
test_cases = [
    # Rust technical questions - should match
    ("payment system precision issue", True, "payment"),
    ("How to fix E0382 error", True, "E0382"),
    ("rust ownership problem", True, "rust"),
    ("how to use tokio", True, "how to"),
    ("why lifetime error", True, "why"),
    ("help me write an async function", True, "help me"),
    ("what is best practice", True, "best practice"),
    ("value moved error", True, "value moved"),
    ("how to use this function", True, "how to"),
    ("explain this code", True, "explain"),
    ("cargo build error", True, "cargo"),
    ("how to use async await", True, "async"),
    ("what is Send Sync trait", True, "Send"),
    ("borrow checker error", True, "borrow"),
    ("type mismatch how to fix", True, "type"),

    # Edge cases - may match but acceptable
    ("what is the weather today", True, "what"),
    ("help me book a ticket", True, "help me"),

    # Pure non-technical questions - should not match without keywords
    ("what time is the meeting tomorrow", False, None),
    ("what to eat for dinner", False, None),
]

passed = 0
failed = 0

for text, should_match, expected_word in test_cases:
    match = re.search(MATCHER, text)
    matched = match is not None

    if matched == should_match:
        passed += 1
        if matched:
            print(f"✅ PASS: '{text}' -> matched '{match.group()}'")
        else:
            print(f"✅ PASS: '{text}' -> no match (expected)")
    else:
        failed += 1
        if matched:
            print(f"❌ FAIL: '{text}' -> matched '{match.group()}' (should NOT match)")
        else:
            print(f"❌ FAIL: '{text}' -> no match (should match '{expected_word}')")

print(f"\n=== Summary ===")
print(f"Passed: {passed}/{len(test_cases)}")
print(f"Failed: {failed}/{len(test_cases)}")

if failed > 0:
    sys.exit(1)
