---
name: python-solid-principles
description: Apply SOLID principles pragmatically when designing or reviewing non-trivial Python functions, classes, contracts, and adapters.
---

# SOLID Principles for Python

Use SOLID as a set of design checks, not as a reason to add abstractions to simple code.

- **Single Responsibility:** Keep each module, class, and function cohesive, with one primary reason to change.
- **Open/Closed:** Use composition or a narrow contract when real variants are expected; avoid speculative extension points.
- **Liskov Substitution:** Keep implementations and test fakes consistent with their contract, including return and error behavior.
- **Interface Segregation:** Give each consumer the smallest contract it needs.
- **Dependency Inversion:** Make high-level policy depend on stable abstractions rather than low-level implementation details. Wire concrete dependencies at the application entry point.

Prefer clear functions and simple composition over patterns for their own sake. Use a design pattern only when it makes a real responsibility, substitution, or workflow easier to understand.
