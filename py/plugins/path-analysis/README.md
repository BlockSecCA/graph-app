# Advanced Path Analysis Plugin

Comprehensive analysis of paths between nodes including shortest paths, path efficiency, and bottleneck identification.

## Overview

Path analysis is fundamental to understanding how information, resources, or influence flow through networks. This plugin provides comprehensive insights into:

- **Connectivity:** How nodes are connected and reachable
- **Efficiency:** How efficiently information can flow
- **Bottlenecks:** Which nodes/edges are critical for connectivity
- **Redundancy:** Alternative paths and backup routes

## Analysis Types

### Comprehensive (Default)
Performs all analyses below for complete insight into network paths.

### Shortest Paths Only
- Finds the most direct route between source and target
- Calculates minimum distance/cost
- Useful for optimization and routing problems

### All Simple Paths  
- Discovers all possible routes (no cycles)
- Analyzes path diversity and redundancy
- Identifies alternative routes

### Path Efficiency
- Measures how efficiently the network connects nodes
- Calculates global connectivity metrics
- Assesses network resilience

### Bottleneck Analysis
- Identifies critical nodes and edges
- Finds single points of failure
- Highlights infrastructure vulnerabilities

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| **Source Node** | Starting point for analysis | Auto (first node) |
| **Target Node** | Ending point for analysis | Auto (last node) |
| **Analysis Type** | Which type of analysis to perform | Comprehensive |
| **Maximum Path Length** | Longest paths to consider (hops) | 6 |
| **Path Limit** | Maximum paths to analyze | 20 |
| **Highlight Critical Paths** | Show important paths visually | True |

## Key Metrics

### Distance & Length
- **Shortest Distance:** Minimum weighted path cost
- **Path Length:** Number of hops/edges in path
- **Average Path Length:** Mean steps between nodes

### Efficiency Measures
- **Global Efficiency (0-1):** Overall network connectivity
  - **1.0:** Fully connected, direct paths everywhere
  - **0.5:** Moderately connected
  - **0.0:** Completely disconnected
- **Path Efficiency:** How close paths are to optimal

### Bottleneck Scores
- **Node Betweenness:** How often node lies on shortest paths
- **Edge Criticality:** How important each edge is for connectivity
- **Critical Nodes:** Nodes with highest bottleneck scores

## Visualizations

### Node Highlighting
- **Red nodes:** Critical bottleneck nodes
- Shows which nodes are most important for connectivity

### Node Sizing
- Size based on betweenness centrality
- Larger nodes = more critical for paths

### Edge Coloring  
- Colors based on edge criticality
- Red edges = critical for connectivity
- Yellow edges = moderately important

## Example Results

```json
{
  "shortest_path": ["Start", "Hub", "End"],
  "shortest_distance": 2.5,
  "total_paths": 3,
  "avg_path_efficiency": 0.75,
  "critical_nodes": ["Hub", "Gateway"],
  "node_betweenness": {
    "Hub": 0.8,
    "Gateway": 0.6,
    "Start": 0.0,
    "End": 0.0
  }
}
```

## Use Cases

### Network Infrastructure
- Identify critical routers/switches
- Plan redundant connections
- Optimize data flow paths
- Assess network resilience

### Supply Chain Analysis
- Find shortest delivery routes
- Identify critical suppliers/distributors
- Plan backup supply paths
- Optimize logistics networks

### Social Network Analysis
- Trace information spread paths
- Identify influential connectors
- Find communication bottlenecks
- Analyze relationship paths

### Process Flow Analysis
- Optimize business process paths
- Identify process bottlenecks
- Find critical approval points
- Design efficient workflows

### Transportation Networks
- Find optimal travel routes
- Identify traffic bottlenecks
- Plan alternative routes
- Assess transportation resilience

## Interpretation Guide

### High Efficiency (>0.7)
- Well-connected network
- Multiple alternative paths
- Low risk of disconnection
- Fast information flow

### Moderate Efficiency (0.3-0.7)
- Adequately connected
- Some bottlenecks present
- Moderate redundancy
- Average connectivity

### Low Efficiency (<0.3)
- Poorly connected network
- High dependency on few nodes/edges
- Risk of disconnection
- Slow information flow

### Critical Nodes
- **High betweenness (>0.5):** Major bottlenecks
- **Medium betweenness (0.1-0.5):** Important connectors
- **Low betweenness (<0.1):** Peripheral nodes

## Tips

- **Use comprehensive analysis** to get complete picture
- **Check efficiency scores** to assess overall connectivity health
- **Identify critical nodes** to prioritize protection/redundancy
- **Analyze multiple source-target pairs** for complete coverage
- **Consider path limits** for large networks to maintain performance
- **Look for single points of failure** in critical infrastructure

## Technical Notes

- Uses NetworkX shortest path algorithms (Dijkstra's algorithm)
- Handles weighted and unweighted graphs
- Converts edge weights to distances (absolute values)
- Limits path enumeration for performance on large graphs
- Handles disconnected graphs gracefully
- Calculates efficiency using global efficiency metric