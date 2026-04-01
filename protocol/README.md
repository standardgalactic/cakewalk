# Protocol Suite

This repository defines a tool-agnostic reasoning protocol for constraint-first analysis, irreversible state evolution, field-based interpretation, and structure-preserving merge.

The protocol is designed to be portable across:
- general-purpose language models
- code assistants
- local agents
- human collaborators

The central design choice is that the protocol is defined first and tool adapters are derived second.

## Directory layout

- `core/` contains the formal base assumptions.
- `mappings/` contains reusable mathematical interpretations.
- `workflows/` contains operational procedures.
- `agents/` contains role prompts for specialized analysis.
- `commands/` contains thin portable task specifications.
- `schemas/` contains machine-readable state and event schemas.
- `adapters/` contains lightweight tool-specific wrappers.
- `examples/` contains minimal worked examples.

## Central objects

The protocol repeatedly uses the following structures:

- Possibility space: Ω_t
- Constraint family: C_t
- Admissible set: A_t = Adm(Ω_t, C_t)
- History trace: H_t
- Present summary or observable state: X_t
- Invariant family: I
- Defect or entropy measure: S
- Optional field interpretation: (Φ, v, S)

## Minimal philosophy

A system is not primarily an object. It is a constrained trajectory through a structured space.

The present state is often insufficient to determine the generating history.

Reconstruction is not reversal.

Merge is not concatenation.

Interpretation should be tied to explicit state spaces, constraints, invariants, and transition operators whenever possible.
