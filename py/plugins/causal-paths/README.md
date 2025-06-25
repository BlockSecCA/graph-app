# Causal Path Analysis Plugin

This plugin analyzes causal relationships and influence pathways in directed graphs using NetworkX.

## Description

The Causal Path Analysis plugin calculates:
- **Influence Scores**: Sum of incoming edge weights for each node
- **Positive Paths**: Causal pathways using only positive (+) edges
- **Negative Paths**: Causal pathways using only negative (-) edges  
- **Mixed Paths**: Pathways combining both positive and negative edges

## Parameters

- **Source Node**: Starting node for path analysis (auto-selects first node if not specified)
- **Target Node**: Ending node for path analysis (auto-selects last node if not specified)
- **Maximum Path Length**: Maximum number of hops to consider (1-10, default: 5)

## Analysis Details

### Influence Scores
Calculated as the sum of all incoming edge weights to each node:
- Positive edges contribute positive weight
- Negative edges contribute negative weight
- Results show which nodes have the highest positive or negative influence

### Path Analysis
Finds all simple paths between source and target nodes:
- **Positive Paths**: All edges in path are positive (+)
- **Negative Paths**: All edges in path are negative (-)
- **Mixed Paths**: Combination of positive and negative edges

Paths are sorted by absolute weight (strongest influence first).

## Requirements

- **Minimum Nodes**: 1
- **Minimum Edges**: 0 (will analyze nodes even without edges)
- **Graph Type**: Directed graphs only
- **Edge Weights**: Supported and recommended

## Example Usage

1. Create a graph with nodes representing entities
2. Add directed edges with + or - types representing positive/negative influences
3. Set edge weights to represent strength of influence
4. Select source and target nodes for path analysis
5. Run analysis to see influence scores and causal pathways

## Output

The plugin returns:
- **Primary Results**: Influence scores, positive paths, negative paths
- **Secondary Results**: Detailed path information with weights and lengths
- **Visualizations**: Node sizing based on influence scores
- **Summary**: Human-readable description of findings

## Version History

- **1.0.0**: Initial release with basic causal path analysis