# History Mapping

## Historical state

When present state is not semantically sufficient, represent the system using

(Ω_t, H_t),

where Ω_t is the live possibility set and H_t is append-only history.

## Event semantics

An event e may:
- refine Ω_t
- remove possibilities
- add metadata
- record refusal
- commit a selection
- introduce or update constraints

The crucial point is that two events with similar immediate effects on Ω_t may differ in H_t and therefore differ semantically.

## Provenance-sensitive equivalence

Define two states as observationally equivalent if they induce the same X_t, but historically equivalent only if they also preserve the relevant class of trace information.

Observational equivalence does not imply historical equivalence.
