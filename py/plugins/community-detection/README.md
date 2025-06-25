# Community Detection Plugin

Identify clusters and communities of nodes that are more connected to each other than to the rest of the graph.

## Overview

Community detection reveals the modular structure of networks by finding groups of nodes that are densely connected internally but sparsely connected to other groups. This is useful for:

- **Social networks:** Finding friend groups, professional circles
- **Biological networks:** Identifying functional modules, protein complexes  
- **Information networks:** Discovering topic clusters, research areas
- **Infrastructure:** Finding network segments, organizational units

## Algorithms

### Louvain (Default)
- **Speed:** Fast  
- **Quality:** High
- **Best for:** General purpose, large networks
- **Features:** Supports weights, resolution parameter
- **Output:** Hierarchical communities with high modularity

### Girvan-Newman  
- **Speed:** Slow
- **Quality:** High theoretical foundation
- **Best for:** Small networks, understanding community structure
- **Features:** Hierarchical, edge betweenness based
- **Output:** Binary splits creating hierarchical communities

### Label Propagation
- **Speed:** Very fast
- **Quality:** Good
- **Best for:** Large networks, quick analysis
- **Features:** Randomized, supports weights
- **Output:** Non-deterministic communities

### Greedy Modularity
- **Speed:** Fast
- **Quality:** Good balance
- **Best for:** Medium networks, reliable results
- **Features:** Deterministic, supports weights
- **Output:** Communities optimizing modularity

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| **Detection Algorithm** | Which algorithm to use | Louvain |
| **Resolution Parameter** | Controls community size (Louvain only) | 1.0 |
| **Color Communities** | Color nodes by community membership | True |
| **Calculate Modularity** | Show modularity quality score | True |

### Resolution Parameter
- **Higher values (1.5-3.0):** Smaller, more focused communities
- **Default (1.0):** Balanced community sizes
- **Lower values (0.1-0.8):** Larger, more inclusive communities

## Visualizations

### Node Coloring
- Each community gets a distinct color
- Makes community structure visually apparent
- Up to 15 distinct colors supported

### Node Sizing  
- Nodes sized by their community size
- Larger nodes = member of larger community
- Helps identify major vs minor communities

## Quality Metrics

### Modularity Score
- **Range:** -1 to +1
- **Good:** > 0.3
- **Excellent:** > 0.5  
- **Interpretation:** How well-separated communities are

## Example Results

```json
{
  "communities": [
    {
      "id": 0,
      "name": "Community 1", 
      "size": 5,
      "nodes": ["CEO", "VP_Sales", "Manager_A", "Sales_Rep_1", "Sales_Rep_2"]
    },
    {
      "id": 1,
      "name": "Community 2",
      "size": 4, 
      "nodes": ["CTO", "Dev_Lead", "Developer_1", "Developer_2"]
    }
  ],
  "modularity": 0.42,
  "algorithm_used": "Louvain"
}
```

## Use Cases

### Social Network Analysis
- Identify friend groups in social media
- Find professional circles in LinkedIn networks
- Detect echo chambers in communication networks

### Organizational Analysis  
- Discover informal teams in company hierarchies
- Identify departmental boundaries
- Find cross-functional collaboration patterns

### Biological Networks
- Identify functional modules in protein interaction networks
- Find metabolic pathways in biochemical networks
- Discover gene regulatory modules

### Information Networks
- Cluster research papers by topic
- Group web pages by subject matter
- Identify knowledge domains in citation networks

## Tips

- **Try multiple algorithms** to compare results
- **Louvain is usually the best starting point** for most networks
- **Adjust resolution** if communities seem too large or small
- **Check modularity score** to validate community quality
- **Use Girvan-Newman** for small networks where you want to understand the hierarchical structure
- **Label Propagation** is great for very large networks where speed matters

## Technical Notes

- Converts directed graphs to undirected for analysis
- Uses absolute edge weights (ignores negative signs)
- Handles disconnected graphs gracefully
- Sorts communities by size (largest first)
- Falls back to greedy modularity if Louvain package unavailable