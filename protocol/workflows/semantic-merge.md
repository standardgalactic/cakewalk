# Workflow: Semantic Merge

## Step 1: Extract structure from each side

For each artifact A and B, identify:
- principal claims
- invariants
- operator behavior
- type/interface commitments
- naming conventions
- provenance-sensitive assumptions

## Step 2: Distinguish shallow from deep conflict

Separate:
- notation conflicts
- naming conflicts
- ordering conflicts
- implementation conflicts
- true ontological contradictions

## Step 3: Identify the shared backbone

Construct the strongest shared substructure that both sides preserve.

## Step 4: Measure drift

Estimate where merging would destroy:
- invariants
- claims
- interfaces
- provenance

## Step 5: Produce a merged artifact or layered split

If a clean merge exists, construct it. If not, preserve both sides and make the obstruction explicit.

## Output contract

Return:
- shared structure
- real conflicts
- safe merge strategy
- merged result or explicit non-merge explanation
