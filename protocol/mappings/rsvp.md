# RSVP Mapping

## Field interpretation

Many systems can be interpreted through the coupled triple

(Φ, v, S),

where:

- Φ is a scalar field representing density, amplitude, coherence, intensity, or potential
- v is a vector field representing flow, direction, transport, drift, or control tendency
- S is a scalar defect or entropy-like field representing dispersion, underconstraint, ambiguity, or structural loss

## Continuous template

A generic continuous template is

∂_t Φ = D_Φ ∇²Φ - ∇·(Φ v) + R_Φ(Φ, v, S),
∂_t v = D_v ∇²v + R_v(Φ, v, S),
∂_t S = D_S ∇²S + P_S(Φ, v, S) - Q_S(Φ, v, S).

This is not a fixed physical law. It is a structural template.

## Discrete template

On a grid or graph, one may use

Φ_{t+1} = Φ_t + diffusion + transport + reaction,
v_{t+1} = v_t + alignment + forcing - damping,
S_{t+1} = S_t + defect production - defect dissipation.

## Interpretation rule

Only use the RSVP map when it clarifies state structure, observables, and update laws. Do not force every artifact into field language if a simpler state-space model is clearer.
