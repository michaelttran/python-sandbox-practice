# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A personal Python sandbox for practicing data structures/algorithms and low-level system design. No build system, no dependencies, no test framework — just plain Python files run directly.

## Running code

```bash
python data-structures/<file>.py
python low-level-design/<file>.py
```

Files that have a `main()` guarded by `if __name__ == "__main__"` can be run directly. Stub files (comment-only) are placeholders for future implementations.

## Structure

- `data-structures/` — LeetCode-style problem stubs and implementations, organized by pattern (hashmaps, linked lists, sliding window, stacks/queues, trees/graphs)
- `low-level-design/` — OOP design pattern implementations with a requirements analysis block at the top of each file

## Conventions

**Low-level design files** follow a consistent structure:
1. A docstring block with problem statement, clarifying questions, requirements, and entity/class design decisions
2. A "cut from plan" section noting what was explicitly scoped out
3. The implementation
4. A `main()` function demonstrating usage with happy path and error cases

**Design patterns used:** Factory pattern with a dict registry (not if/elif chains), ABCs for interfaces, `Enum` for channel/type constants.

**Data structure files** start as comment stubs listing the target problems (e.g., `# Two Sum, Group Anagrams`) and get filled in as problems are solved.
