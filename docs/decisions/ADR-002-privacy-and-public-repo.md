# ADR-002: Public repository, private data

**Date:** 2026-10-17 · **Status:** accepted

**Context.** The repo is a portfolio piece, but the project films a public road from the author's window.

**Decision.** The code and documentation are public. Raw video, recordings, datasets and anything revealing the location stay private (DVC remote on a private S3 bucket). Private planning notes (vacancy analysis, shopping list) are git-ignored. Only blurred, selected frames may be sent to third-party tools (Hasty). See `docs/privacy.md`.

**Consequences.** CI and pre-commit hooks block media, data and model binaries outside allowed paths. A history rewrite was needed once after private notes were committed; do not repeat it.
