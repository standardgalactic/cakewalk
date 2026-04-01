# Workflow: Constraint Analysis

Given an artifact, system, note, code path, or theory fragment, perform the following procedure.

## Step 1: Define the possibility space

Specify Ω. If Ω is too large or implicit, state the working approximation.

## Step 2: Identify the constraint family

List the active constraints C. Distinguish hard constraints from soft constraints if useful.

## Step 3: Characterize the admissible set

State A = Adm(Ω, C). If exact characterization is impossible, state a useful approximation.

## Step 4: Determine residual ambiguity

Describe whether the admissible region is:
- singleton or effectively unique
- finite but ambiguous
- continuous family
- path-dependent
- observationally degenerate

## Step 5: Identify invariants and failure modes

State what is supposed to remain preserved and name the most likely constraint violations.

## Step 6: Propose minimal repairs

Prefer the smallest change that eliminates the structural defect without destroying preserved invariants.

## Output contract

The final answer should separate:
- given information
- inferred structure
- unconstrained degrees of freedom
- repair recommendations
