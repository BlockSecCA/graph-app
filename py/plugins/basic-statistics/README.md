# Basic Graph Statistics Plugin

Comprehensive analysis of fundamental graph metrics including density, diameter, clustering, connectivity, and degree distribution.

## Overview

This plugin provides essential statistical measures that form the foundation of graph analysis. These metrics help understand the basic structural properties, connectivity patterns, and overall characteristics of your network.

Perfect for:
- **Initial graph exploration** - Understanding basic structure
- **Comparative analysis** - Comparing different graphs or time periods  
- **Quality assessment** - Evaluating graph completeness and connectivity
- **Research foundations** - Building upon fundamental measurements

## Core Metrics

### Basic Structure
- **Node/Edge Counts** - Size of the network
- **Density** - How connected the graph is (0 = no edges, 1 = fully connected)
- **Average Degree** - Mean number of connections per node
- **Self-loops** - Nodes connected to themselves

### Connectivity Analysis
- **Connected Components** - Separate subgraphs
- **Isolated Nodes** - Nodes with no connections
- **Largest Component** - Size of main connected subgraph
- **Node/Edge Connectivity** - Minimum cuts needed to disconnect graph

### Clustering Analysis  
- **Global Clustering Coefficient** - Overall clustering tendency
- **Average Clustering Coefficient** - Mean local clustering
- **Triangle Count** - Number of 3-node complete subgraphs
- **Node-level Clustering** - Individual clustering coefficients

### Distance Metrics
- **Diameter** - Longest shortest path in the graph
- **Radius** - Minimum eccentricity  
- **Average Path Length** - Mean shortest path distance
- **Center/Periphery** - Most/least central nodes by distance

### Degree Distribution
- **Degree Range** - Min/max node degrees
- **Degree Variance** - Spread of degree values
- **Most Common Degree** - Modal degree value
- **Degree Entropy** - Diversity of degree distribution

## Analysis Focus Options

### Comprehensive (Default)
Complete statistical analysis including all metrics above.

### Basic Metrics Only
- Node/edge counts
- Density  
- Average degree
- Basic connectivity

### Connectivity Analysis
- Connected components
- Isolated nodes
- Component sizes
- Connectivity measures

### Clustering Analysis
- Clustering coefficients
- Triangle counts
- Local clustering patterns

### Distance Metrics
- Diameter and radius
- Path lengths
- Center and periphery
- Eccentricity analysis

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| **Analysis Focus** | Which metrics to calculate | Comprehensive |
| **Show Degree Distribution** | Include degree distribution analysis | True |
| **Detailed Clustering** | Calculate per-node clustering | False |
| **Connectivity Analysis** | Analyze graph connectivity | True |
| **Distance Analysis** | Calculate diameter/radius | True |

## Example Results

```json
{
  "basic_metrics": {
    "node_count": 25,
    "edge_count": 43,
    "density": 0.147,
    "average_degree": 3.44,
    "max_degree": 8,
    "min_degree": 1
  },
  "connectivity_summary": {
    "is_connected": true,
    "connected_components": 1,
    "isolated_nodes_count": 0,
    "largest_component_size": 25
  },
  "clustering_summary": {
    "global_clustering_coefficient": 0.286,
    "average_clustering_coefficient": 0.314,
    "triangle_count": 12
  },
  "distance_summary": {
    "diameter": 6,
    "radius": 3,
    "average_path_length": 2.847,
    "center_nodes": ["Node_5"],
    "periphery_nodes": ["Node_23", "Node_17"]
  }
}
```

## Use Cases

### Network Quality Assessment
- **Completeness** - Are there isolated nodes or components?
- **Connectivity** - How well-connected is the network?
- **Balance** - Even degree distribution or hub-dominated?

### Comparative Analysis
- **Before/after** - Changes in structure over time
- **Different networks** - Comparing similar systems
- **Benchmark** - Against theoretical or ideal networks

### Research Foundations
- **Small-world properties** - High clustering + short paths
- **Scale-free networks** - Power-law degree distribution  
- **Random graphs** - Compare against theoretical models

### Infrastructure Analysis
- **Robustness** - How many failures to disconnect?
- **Efficiency** - Average communication distance
- **Redundancy** - Multiple paths between nodes

### Social Network Analysis
- **Community structure** - Clustering patterns
- **Influence spread** - Path lengths and connectivity
- **Network evolution** - Changes in basic metrics

## Interpretation Guide

### Density
- **High (>0.5):** Dense, well-connected network
- **Medium (0.1-0.5):** Moderately connected
- **Low (<0.1):** Sparse network, potential connectivity issues

### Clustering Coefficient
- **High (>0.3):** Strong local clustering, community structure
- **Medium (0.1-0.3):** Moderate clustering
- **Low (<0.1):** Little clustering, more random structure

### Average Path Length
- **Short (<3):** Efficient communication, small-world
- **Medium (3-5):** Typical for many real networks
- **Long (>5):** Poor connectivity, potential bottlenecks

### Connected Components
- **1 component:** Fully connected network
- **Few components:** Mostly connected with isolated clusters
- **Many components:** Fragmented network

### Degree Distribution
- **Low variance:** Homogeneous, egalitarian network
- **High variance:** Heterogeneous, hub-dominated network
- **Power-law:** Scale-free network properties

## Best Practices

### Analysis Selection
- **Start comprehensive** for initial exploration
- **Focus on connectivity** for network reliability questions
- **Use distance metrics** for efficiency analysis
- **Detailed clustering** for community detection prep

### Interpretation
- **Compare to benchmarks** - Random graphs, theoretical models
- **Consider domain context** - What do metrics mean for your network?
- **Look for patterns** - High clustering + short paths = small-world
- **Validate with visualization** - Do statistics match visual patterns?

### Performance Notes
- **Distance metrics** are expensive for large graphs (>100 nodes)
- **Detailed clustering** adds computation for per-node analysis
- **Connectivity analysis** is efficient for most graph sizes
- **Basic metrics** are fast even for very large graphs

## Tips

- **Use basic focus** for quick overview of large graphs
- **Enable detailed clustering** to identify highly clustered nodes
- **Compare density** across different time periods
- **Watch for isolated nodes** that might indicate data quality issues
- **Low connectivity** might suggest missing edges or incomplete data
- **Very high clustering** might indicate over-connected or artificial data
- **Extreme diameter** values could indicate linear or tree-like structures

## Technical Notes

- Handles both directed and undirected graphs appropriately
- Uses largest connected component for distance calculations when graph is disconnected
- Automatically detects graph type (directed vs undirected) based on edge patterns
- Provides fallback calculations for edge cases and disconnected graphs
- Optimized algorithms for better performance on larger graphs
- Includes entropy calculations for degree distribution diversity
- Supports weighted graphs (uses edge weights where applicable)