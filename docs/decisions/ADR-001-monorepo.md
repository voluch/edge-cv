# ADR-001: One monorepo with a folder per task

**Date:** 2026-10-17 · **Status:** accepted

**Context.** The first plan used about ten repositories plus a Claude Code plugin. For a single developer this meant cross-repo version tags, release-based artifact passing, ten CI setups and agents that only see one piece.

**Decision.** One repository, `edge-cv`, with a top-level folder per task and shared code in `common/`. One `.claude/` at the root; nested `CLAUDE.md` files per folder; CI with path filters.

**Consequences.** Atomic cross-component changes, one CI, one issue tracker. A component that grows strong enough to stand alone (likely the C++ tracker) can be split out later with `git filter-repo` or `git subtree split`.
