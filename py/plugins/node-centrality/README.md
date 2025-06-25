# Node Centrality Analysis Plugin

Calculate multiple centrality measures to identify the most important nodes in your graph.

## Overview

This plugin analyzes node importance using various centrality algorithms from network theory. It helps identify:
- **Hub nodes** (highly connected)
- **Bridge nodes** (connect different parts of the graph)  
- **Influential nodes** (have high impact on information flow)

## Centrality Measures

### Degree Centrality
- **What it measures:** How many connections a node has
- **Best for:** Finding highly connected nodes
- **Interpretation:** Higher values = more direct connections

### Betweenness Centrality  
- **What it measures:** How often a node lies on shortest paths between other nodes
- **Best for:** Finding bridge/bottleneck nodes
- **Interpretation:** Higher values = more control over information flow

### Closeness Centrality
- **What it measures:** How close a node is to all other nodes
- **Best for:** Finding nodes that can quickly reach others
- **Interpretation:** Higher values = shorter average distance to other nodes

### Eigenvector Centrality
- **What it measures:** Connection to other important nodes
- **Best for:** Finding nodes connected to other influential nodes  
- **Interpretation:** Higher values = connected to other central nodes

### PageRank
- **What it measures:** Importance based on incoming connections (like Google's algorithm)
- **Best for:** Ranking nodes by overall influence
- **Interpretation:** Higher values = more authoritative/important

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| **Centrality Measures** | Select which measures to calculate | All measures |
| **Normalize Values** | Scale values to 0-1 range | True |
| **Highlight Top Nodes** | Number of most central nodes to highlight | 3 |

## Visualizations

### Node Sizing
- Nodes are sized based on their **composite centrality score**
- Larger nodes = higher overall importance
- Combines all selected centrality measures

### Node Highlighting
- Top N most central nodes are highlighted in red
- Makes it easy to spot the most important nodes at a glance

## Example Results

```json
{
  "composite_centrality": {
    "CEO": 0.85,
    "Manager": 0.62, 
    "Developer": 0.41
  },
  "betweenness": {
    "CEO": 0.67,
    "Manager": 0.33,
    "Developer": 0.15
  },
  "degree": {
    "CEO": 0.8,
    "Manager": 0.6,
    "Developer": 0.4
  }
}
```

## Use Cases

- **Organizational Analysis:** Find key people in company hierarchies
- **Social Network Analysis:** Identify influential individuals
- **Infrastructure Analysis:** Locate critical network nodes
- **Knowledge Networks:** Find central concepts or topics
- **Dependency Analysis:** Identify critical components

## Tips

- **Use multiple measures** to get a complete picture of node importance
- **Betweenness centrality** is great for finding bottlenecks
- **Degree centrality** is simple but effective for finding hubs
- **PageRank** works well for directed graphs (like web links, citations)
- **Enable normalization** to compare scores across different centrality measures

## Technical Notes

- Handles both directed and undirected graphs
- Automatically falls back for disconnected graphs
- Uses NetworkX algorithms for accurate calculations
- Composite scores are averaged across all selected measures