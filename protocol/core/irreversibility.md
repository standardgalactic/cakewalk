# Irreversibility

## Default axiom

Irreversibility is the default temporal orientation.

History evolves by append-only extension

H_{t+1} = H_t ⊕ e_{t+1},

and no rollback operator R satisfying

R(H_t ⊕ e_{t+1}) = H_t

is assumed unless explicitly defined and justified.

## Reconstruction versus reversal

Reconstruction attempts to infer prior states or events from present observables and retained trace data.

Reversal would require a genuine inverse dynamics or inverse operator.

These are not the same.

If π is a compression map from deeper state to present summary X_t, then reconstructing H_t from X_t requires either:
- injectivity properties of π on the relevant class, or
- additional retained information.

Absent these, provenance is underdetermined.

## Practical consequences

For protocol design:

- prefer append-only logs over destructive replacement
- separate current state from historical trace
- treat provenance-sensitive semantics as first-class
- distinguish replay, audit, and reverse execution

## Mathematical note

If T is the transition operator on detailed states, reversibility would require existence of T^{-1} on the relevant image. The protocol does not assume this. Many real operations are instead better treated as semigroup actions than as group actions.
