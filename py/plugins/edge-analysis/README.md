# Edge Weight Analysis Plugin

Comprehensive analysis of edge weights, relationships, and flow patterns with rich edge visualization.

## Overview

While most network analysis focuses on nodes, edges often contain the most important information about relationships, flows, and interactions. This plugin provides deep insights into edge patterns with beautiful visual representations.

Perfect for:
- **Flow analysis** - Understanding how resources/information move
- **Relationship strength** - Identifying strong vs weak connections
- **Pattern recognition** - Spotting connection patterns and outliers
- **Quality assessment** - Evaluating connection reliability/importance

## Analysis Types

### Comprehensive (Default)
Complete edge analysis including weights, flow, relationships, and strength.

### Weight Distribution Only
- Statistical analysis of weight values
- Weight categories and distributions
- Outlier identification

### Flow Patterns Only  
- Directional flow analysis
- Source, sink, and hub identification
- Flow balance assessment

### Relationship Types Only
- Positive vs negative relationship analysis
- Relationship strength patterns
- Type-based statistics

### Connection Strength Only
- Strongest and weakest connections
- Connection importance ranking
- Critical connection identification

## Edge Coloring Methods

### By Weight Strength (Default)
- Colors represent connection strength
- **Strong connections:** Red/warm colors
- **Weak connections:** Blue/cool colors
- Immediate visual strength assessment

### By Relationship Type (+/-)
- **Green:** Positive relationships
- **Red:** Negative relationships  
- **Gray:** Neutral relationships
- Perfect for causal/influence networks

### By Flow Direction
- Colors indicate flow patterns
- Useful for directed graphs
- Helps identify flow bottlenecks

### By Edge Importance
- Colors based on criticality for network connectivity
- Highlights structurally important edges
- Useful for infrastructure analysis

## Color Schemes

### Strength (Default)
- **Blue → Red** gradient
- Professional, clear strength indication
- Good for technical analysis

### Heat Map
- **Cool → Warm** temperature-based
- Intuitive strength representation
- Great for presentations

### Traffic Light
- **Green → Yellow → Red**
- Intuitive status indication
- Perfect for operational dashboards

### Monochrome
- **Gray scale** only
- Print-friendly, professional
- Good for formal reports

### Rainbow
- **Full spectrum** colors
- Maximum visual distinction
- Great for complex patterns

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| **Analysis Focus** | Which aspect to analyze | Comprehensive |
| **Weight Categories** | Number of weight groups (3-10) | 5 |
| **Edge Coloring Method** | How to color edges | By Weight Strength |
| **Edge Width Scaling** | Scale width by weight | True |
| **Highlight Extreme Edges** | Show strongest/weakest | True |
| **Show Edge Labels** | Display weight values | False |
| **Color Scheme** | Visual color palette | Strength |

## Key Metrics

### Weight Statistics
- **Mean/Median Weight:** Central tendency
- **Weight Range:** Spread of values
- **Standard Deviation:** Variability
- **Weight Categories:** Groupings by strength

### Flow Analysis  
- **Flow Sources:** Nodes with high outflow
- **Flow Sinks:** Nodes with high inflow
- **Flow Hubs:** Nodes with high total flow
- **Net Flow:** Balance of in vs out flow

### Relationship Patterns
- **Positive/Negative Ratios:** Relationship type distribution
- **Average Strengths:** Mean strength by type
- **Type Percentages:** Composition breakdown

### Connection Strength
- **Strongest Connections:** Top weighted edges
- **Weakest Connections:** Lowest weighted edges
- **Edge Importance:** Structural significance

## Visualizations

### Edge Coloring
- Immediate visual indication of edge properties
- Customizable color schemes for different contexts
- Pattern recognition at a glance

### Edge Width Scaling
- Thicker edges = stronger connections
- Visual hierarchy of connection importance
- Easy identification of major flows

### Extreme Edge Highlighting
- **Red highlighting:** Strongest connections
- **Blue highlighting:** Weakest connections (optional)
- Focus attention on outliers

### Edge Labels (Optional)
- Display actual weight values
- Useful for detailed analysis
- Can be toggled for clean presentations

## Example Results

```json
{
  "weight_statistics": {
    "mean_weight": 2.45,
    "max_weight": 8.2,
    "min_weight": 0.1,
    "std_dev": 1.87
  },
  "relationship_summary": {
    "positive_count": 15,
    "negative_count": 3,
    "positive_percentage": 83.3,
    "avg_positive_strength": 2.8
  },
  "strongest_connections": [
    ["CEO → Board", 8.2],
    ["Manager → Team", 6.7],
    ["Sales → Revenue", 5.9]
  ]
}
```

## Use Cases

### Business Process Analysis
- **Workflow strength:** Identify strong vs weak process links
- **Bottleneck detection:** Find process constraints
- **Efficiency analysis:** Optimize process flows

### Social Network Analysis
- **Relationship strength:** Strong vs weak social ties
- **Influence patterns:** How influence spreads
- **Community connections:** Inter-group relationship strength

### Infrastructure Analysis
- **Connection capacity:** Network link strengths
- **Critical paths:** Most important connections
- **Redundancy analysis:** Backup connection assessment

### Supply Chain Management
- **Supplier relationships:** Strength of supplier connections
- **Flow analysis:** Material/information flows
- **Risk assessment:** Critical supplier dependencies

### Financial Networks
- **Transaction volumes:** Money flow patterns
- **Relationship strength:** Business relationship assessment
- **Risk connections:** Financial risk propagation paths

## Interpretation Guide

### Strong Connections (High Weights)
- **Critical relationships** requiring protection
- **High-capacity flows** or important interactions
- **Primary pathways** for information/resources
- **Key dependencies** in the system

### Weak Connections (Low Weights)
- **Secondary relationships** or backup paths
- **Developing relationships** that might grow
- **Inefficient connections** needing attention
- **Redundant pathways** that could be optimized

### Flow Patterns
- **Sources (High Outflow):** Information/resource providers
- **Sinks (High Inflow):** Information/resource consumers  
- **Hubs (High Both):** Central processing/distribution points
- **Balanced Nodes:** Equal in/out flow

### Relationship Types
- **Positive Relationships:** Reinforcing, supportive connections
- **Negative Relationships:** Inhibiting, opposing connections
- **Mixed Networks:** Complex interaction patterns

## Best Practices

### Parameter Selection
- **Start with comprehensive analysis** for overview
- **Use weight strength coloring** for general analysis
- **Enable edge width scaling** for clear visual hierarchy
- **Show extreme highlighting** to spot outliers
- **Consider relationship type coloring** for causal networks

### Visual Settings
- **Strength color scheme** for technical analysis
- **Heat map colors** for presentations  
- **Traffic light colors** for operational dashboards
- **Disable edge labels** for clean visualizations
- **Enable labels** for detailed analysis sessions

### Analysis Focus
- **Weight distribution** to understand value patterns
- **Flow patterns** for directional networks
- **Relationship types** for causal/influence analysis
- **Connection strength** for critical path analysis

## Tips

- **Combine with node analysis** for complete picture
- **Use different color schemes** to highlight different aspects
- **Pay attention to extreme edges** - they often reveal key insights
- **Consider flow balance** in directed networks
- **Look for weight patterns** that might indicate data quality issues
- **Use edge width scaling** to quickly identify major connections
- **Toggle labels on/off** depending on analysis vs presentation needs

## Technical Notes

- Handles both directed and undirected graphs
- Supports positive, negative, and zero weights
- Automatically normalizes weights for visualization
- Creates distinct visual categories for weight ranges
- Calculates comprehensive flow statistics for directed graphs
- Provides fallback analysis for edge-sparse networks
- Optimized color schemes for visual accessibility