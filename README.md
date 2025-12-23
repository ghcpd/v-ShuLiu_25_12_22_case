# user_display — High-performance user display module

This project refactors an unreliable baseline into a modular, concurrent, and fault-tolerant package.

Highlights:
- O(1) ID lookup via `UserStore`
- Formatters: compact, JSON, table
- Extensible filters & plugin registration
- Soft validation and repair
- Optional parallel filtering
- Structured logging and simple metrics

Usage examples and tests are under `tests/`. Run `./run_tests.ps1` on Windows.

