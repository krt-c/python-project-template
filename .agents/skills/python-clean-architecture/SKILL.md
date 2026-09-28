---
name: python-clean-architecture
description: Apply Clean Architecture boundaries to Python applications when domain rules, workflows, and external adapters need independent testing or substitution.
---

# Python Clean Architecture

Use this guidance when the application has meaningful policy or replaceable external dependencies. Keep small scripts and straightforward programs simple; do not add layers only to match a diagram.

## Boundaries

- **Domain** owns core rules and domain models. Keep it independent of frameworks, databases, networks, and filesystem implementations.
- **Application** owns use cases and the narrow contracts those use cases require. Depend on domain rules and contracts, not concrete infrastructure.
- **Infrastructure** implements contracts for external systems such as databases, APIs, queues, and filesystems.
- **Presentation** translates incoming and outgoing formats. Controllers, CLI commands, and UI handlers belong here and call application use cases.
- **Bootstrap** constructs concrete adapters and wires them to application and presentation components.

Dependencies point inward. Keep models and contracts separate from implementations when that improves clarity. Add an abstraction only when it protects a policy, enables a real substitution, or creates a useful test seam.

## Testing

- Test domain rules and application use cases without real external services where practical.
- Use fakes at application boundaries; test infrastructure adapters against their contracts.
- Keep integration tests for meaningful component wiring and serialization behavior.
