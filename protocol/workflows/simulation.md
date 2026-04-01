# Workflow: Simulation Construction

## Step 1: Define state variables

Use a small explicit state vector or field set.

## Step 2: Define admissibility and boundary conditions

State what counts as valid initialization and valid evolution.

## Step 3: Choose dynamics

Use either:
- discrete update laws
- ODE/PDE laws
- graph-based propagation laws

## Step 4: Define observables

Select a small set of measurable quantities such as:
- coherence
- divergence
- defect
- ambiguity
- conservation error

## Step 5: State failure modes

Name numerical instability, drift, nonphysical values, or invariant violation.

## Step 6: Produce the smallest runnable scaffold

Prefer minimal working code over large architecture.
