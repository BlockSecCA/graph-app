## Graph Specification for Analysis

### Node Requirements
* Each node **must** include:
  * `id`: unique string identifier
* Optional (but preferred) fields:
  * `label`: string
  * `type`: string
  * `group`: string

### Edge Requirements
* Each edge **must** include:
  * `source`: string, matching a `node.id`
  * `target`: string, matching a `node.id`
* Optional (with defaults):
  * `type`: `"+"` or `"-"` (default is `"+"`)
  * `weight`: numeric (default is `1`)

### Graph-Level Structural Constraints
* Node IDs must be **unique**.
* All edges must reference valid node IDs.
* Graph must contain at least **2 nodes** and **1 edge** to be meaningful for analysis.
* Edge weights must be valid numbers.

### Example of a broken graph
{
  "nodes": [
    { "id": "1", "label": "Node 1" },
    { "id": "1", "label": "Duplicate ID" },       // Duplicate ID
    { "label": "Missing ID" },                    // Missing 'id'
    { "id": "4" }                                 // No label (ok if optional, bad if required)
  ],
  "edges": [
    { "source": "1", "target": "2" },             // Target "2" doesn’t exist
    { "source": "1" },                            // Missing 'target'
    { "target": "4" },                            // Missing 'source'
    { "source": "999", "target": "1" },           // Source does not exist
    { "source": "1", "target": "4", "weight": "a" }, // Non-numeric weight
    { "source": "1", "target": "1" }              // Self-loop (maybe allowed, but worth warning)
  ]
}

---

## Semantic Guidelines for Causal Analysis (Optional, but recommended)
* **Directed Acyclic Graphs (DAGs)** are assumed by most causal path logic.
* Cycles are allowed but may limit or distort interpretation.
* Negative weights are allowed, but if **all paths** are negative, a warning should be raised.
* Self-loops (`source == target`) are allowed but generally **ignored** or **warned against**.
* All weights of 0 provide no influence and should trigger a warning.
* Disconnected graphs (unreachable nodes) can be analyzed, but some nodes will not appear in paths or influence scoring.

---

## Edge Cases That Should Trigger Warnings (Not Errors)
* All edges negative or zero-weight
* Only one node (trivial graph)
* Graph contains cycles (if DAG expected)
* No path exists from first node to last node
* Node labels missing (makes output hard to interpret)
* Self-loops

## Output from a Graph Validator Should Include:
* `errors`: list of fatal issues (block analysis)
* `warnings`: list of advisory issues (analysis may proceed)
* `metadata`: optional stats (e.g., number of nodes/edges, is DAG, has cycles, etc.)
