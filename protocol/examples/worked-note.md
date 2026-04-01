# Worked Note

Suppose two implementations produce the same current summary X_t but one retains explicit trace data and the other does not.

Under the protocol, these are not automatically equivalent.

Let π be the summary projection from detailed state to present summary. If π is many-to-one, then the implementation that discards trace data destroys information about the fiber π^{-1}(X_t). If future tasks depend on provenance, replay, or audit, then the two implementations differ materially even when present outputs match.

This is the sort of difference that should be treated as a deep semantic merge conflict rather than as a style difference.
