# Claude Adapter

Use the files in `protocol/` as the source of truth.

A Claude-specific wrapper should keep only thin operational instructions such as:

- load and prioritize the protocol core
- invoke workflows from `protocol/workflows/`
- use agent roles from `protocol/agents/`
- treat adapter text as secondary to the protocol itself

The adapter should not duplicate the full protocol unless required by tooling constraints.
