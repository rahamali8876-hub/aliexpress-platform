# ADR: Explicit Aggregate Identity

## Decision

All aggregates must be constructed with an explicit `aggregate_id`
via keyword-only arguments.

## Rationale

- Prevents hidden contracts
- Ensures domain event correctness
- Enforces DDD aggregate invariants

## Consequences

- Slightly more verbose constructors
- Stronger guarantees across domains
