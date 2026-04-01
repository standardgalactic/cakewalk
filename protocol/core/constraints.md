# Constraints

## Constraint families

A constraint family C_t may contain any combination of:

- logical constraints
- algebraic constraints
- physical or dynamical constraints
- resource constraints
- semantic compatibility constraints
- temporal ordering constraints
- interface or typing constraints

It is useful to write

C_t = {c_t^{(1)}, ..., c_t^{(n_t)}}.

## Hard and soft constraints

Partition when useful:

C_t = C_t^{hard} ∪ C_t^{soft}.

Hard constraints define feasibility. Soft constraints induce preference, priority, or energy-like penalties.

A common formalization is a defect functional

Δ_t : Ω_t -> ℝ_{≥0},

with admissibility condition

x ∈ A_t  if and only if  Δ_t(x) = 0

for exact admissibility, or

x ∈ A_t^{ε}  if and only if  Δ_t(x) ≤ ε

for approximate admissibility.

## Structural recommendation

Whenever possible, encode constraints explicitly as:

- predicates
- equations
- inequalities
- typing rules
- interface contracts
- provenance requirements
- commutation or non-commutation rules

Avoid replacing constraints with vague style statements.

## Constraint failure

Constraint failure should be described by locating the failing object, operator, or interface rather than by saying merely that something is "wrong" or "does not work".

Preferred form:

- failing object
- violated constraint
- observable symptom
- minimal repair
