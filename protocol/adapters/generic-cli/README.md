# Generic CLI Adapter

This adapter is for local or custom agents.

Recommended pattern:

1. Load core files first.
2. Load one or more workflow files depending on the task.
3. Optionally load one agent role file.
4. Execute the requested task.
5. Emit structured output aligned with the relevant command or schema file.
