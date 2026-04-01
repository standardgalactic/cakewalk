# State Model

## Canonical schema

The canonical protocol state is

Y_t = (Ω_t, C_t, A_t, H_t, X_t, I_t, M_t),

where:

- Ω_t is the possibility space
- C_t is the active constraint family
- A_t is the admissible set
- H_t is the append-only history
- X_t is the observable or compressed state
- I_t is the active invariant monitor
- M_t is optional metadata, including confidence, source, or scope

## Derived quantities

Typical derived quantities include:

- admissible cardinality or measure: μ(A_t)
- effective ambiguity: S_eff(t) = log μ(A_t), where appropriate
- defect: Δ_t(x)
- confidence or epistemic weight: w_t
- conserved monitor values: I_t(x)

## Transition form

A generic transition step can be written as

Y_{t+1} = 𝒯_t(Y_t, u_t),

where u_t is an external intervention, observation, or operator request.

Expanded form:

Ω_{t+1} = U_Ω(Ω_t, C_t, u_t)
C_{t+1} = U_C(C_t, u_t)
A_{t+1} = Adm(Ω_{t+1}, C_{t+1})
H_{t+1} = H_t ⊕ e_{t+1}
X_{t+1} = π(Ω_{t+1}, C_{t+1}, H_{t+1})
I_{t+1} = U_I(I_t, Y_t, u_t)

## Design guidance

The protocol prefers explicit state tuples over hidden process state. If an implementation stores only X_t and omits H_t, then it should be understood that provenance-sensitive questions may become unanswerable.
