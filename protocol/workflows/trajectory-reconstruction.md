# Workflow: Trajectory Reconstruction

Use this workflow when the present state appears insufficient to answer a provenance-sensitive question.

## Step 1: Specify the present summary

State what is actually observed or retained as X_t.

## Step 2: Identify missing latent structure

State what parts of detailed state or history have been projected away.

## Step 3: Characterize admissible histories

Define the class of histories H compatible with X_t and the known constraints.

## Step 4: Determine identifiability

State whether reconstruction is:
- unique
- finite ambiguous
- many-to-one
- impossible without more information

## Step 5: Separate replay, audit, and reversal

Make explicit whether the task is:
- to replay from retained trace
- to audit likely prior steps
- to reverse a dynamic law

## Step 6: Recommend instrumentation

If provenance matters but is currently underdetermined, specify the minimal additional logging or state retention needed.
