# Ontology

## Primitive stance

A system is modeled as a constrained evolution of possibilities rather than as a static object with intrinsic narrative properties.

At each time t, define a protocol state as the tuple

Y_t = (Ω_t, C_t, A_t, H_t, X_t, I),

where:

- Ω_t is the live possibility space at time t.
- C_t is the active constraint family at time t.
- A_t = Adm(Ω_t, C_t) ⊆ Ω_t is the admissible set.
- H_t is the append-only history trace.
- X_t is an observable or compressed present-state summary.
- I is the family of invariants expected to persist under admissible evolution.

## Admissibility

The admissible set is induced by a constraint operator

Adm : 𝒫(Ω) × 𝒞 → 𝒫(Ω),

so that A_t = Adm(Ω_t, C_t).

The protocol treats admissibility as primary. Narrative interpretation is secondary and must not substitute for constraint specification.

## Evolution

A general step consists of three layers:

1. Constraint update:
   C_t -> C_{t+1}

2. Admissible-space update:
   Ω_t -> Ω_{t+1}
   A_t -> A_{t+1}

3. History extension:
   H_{t+1} = H_t ⊕ e_{t+1}

for some event e_{t+1}.

The symbol ⊕ denotes append-only extension. No right inverse is assumed.

## Present-state compression

The present state X_t is generally a many-to-one image of the deeper state:

X_t = π(Ω_t, C_t, H_t),

for some projection or compression map π.

In general, π is not injective. Therefore X_t alone need not determine H_t.

## Identity

Identity is historical rather than purely extensional. Two present states may be observationally equivalent while differing in provenance. When provenance matters semantically, H_t must be preserved explicitly or through sufficient statistics.
