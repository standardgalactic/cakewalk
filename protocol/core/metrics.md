# Metrics and Defect Functionals

## Effective ambiguity

When the admissible set has a meaningful measure μ, define effective ambiguity by

S_eff(t) = log μ(A_t).

This is not necessarily thermodynamic entropy. It is a structural ambiguity measure over remaining admissible degrees of freedom.

Smaller S_eff indicates stronger determination.

## Defect functional

Let Δ_t : Ω_t -> ℝ_{≥0} measure deviation from admissibility. Then:

- exact admissibility: Δ_t(x) = 0
- approximate admissibility: Δ_t(x) ≤ ε
- optimization-oriented selection: choose x minimizing Δ_t(x)

## Invariant drift

If I_t = (I_t^{(1)}, ..., I_t^{(k)}) is an invariant monitor, define drift under a step by

D_I(t) = Σ_j d_j(I_{t+1}^{(j)}, I_t^{(j)}),

for suitable component metrics d_j.

This is useful in merge, refactor, and theory-extension tasks.

## Provenance loss

If π is a projection from detailed state to summary, define provenance loss informally by the size or measure of fibers

π^{-1}(X_t).

Large fibers indicate many histories or detailed states compatible with the same present summary.
