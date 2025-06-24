# Graph Analysis Plugin Specification

## Overview
This document defines how to create analysis plugins for the Causal Graph Tool. Plugins are Python modules that analyze graph data and return structured results for visualization.

---

## Plugin Structure

### 1. File Organization
```
py/plugins/
├── my_analysis/
│   ├── __init__.py          # Plugin metadata and exports
│   ├── analysis.py          # Main analysis function
│   ├── requirements.txt     # Python dependencies (optional)
│   ├── README.md           # Plugin documentation
│   └── tests/              # Unit tests (recommended)
│       └── test_analysis.py
```

### 2. Plugin Metadata (`__init__.py`)
```python
"""
My Custom Analysis Plugin
"""

ANALYSIS_INFO = {
    # Required fields
    "id": "my-analysis",                    # Unique identifier (kebab-case)
    "name": "My Custom Analysis",           # Display name
    "description": "Brief description of what this analysis does",
    "version": "1.0.0",                    # Semantic version
    "author": "Your Name",                  # Plugin author
    
    # Categorization
    "category": "structural",               # structural|causal|flow|custom
    "tags": ["centrality", "importance"],  # Search/filter tags
    
    # Requirements
    "min_nodes": 2,                        # Minimum nodes required
    "min_edges": 1,                        # Minimum edges required
    "supports_directed": True,             # Works with directed graphs
    "supports_undirected": True,           # Works with undirected graphs
    "supports_weighted": True,             # Uses edge weights
    
    # UI Configuration
    "parameters": [
        {
            "name": "algorithm",
            "type": "select",
            "label": "Algorithm Type",
            "description": "Choose the algorithm variant",
            "required": True,
            "default": "standard",
            "options": [
                {"value": "standard", "label": "Standard Algorithm"},
                {"value": "weighted", "label": "Weighted Algorithm"}
            ]
        },
        {
            "name": "threshold",
            "type": "number",
            "label": "Threshold Value",
            "description": "Minimum threshold for inclusion",
            "required": False,
            "default": 0.5,
            "min": 0.0,
            "max": 1.0,
            "step": 0.1
        },
        {
            "name": "source_node",
            "type": "select_node",
            "label": "Source Node",
            "description": "Starting node for analysis",
            "required": False,
            "default": "auto"  # "auto", "first", "last", or specific node ID
        }
    ]
}

# Import the main analysis function
from .analysis import analyze_graph

# Export public interface
__all__ = ['ANALYSIS_INFO', 'analyze_graph']
```

---

## Parameter Types Reference

### Basic Types
- `"number"` - Numeric input (int/float)
- `"text"` - Text input (string)
- `"boolean"` - Checkbox (true/false)
- `"select"` - Dropdown selection

### Graph-Specific Types
- `"select_node"` - Node picker dropdown
- `"select_nodes"` - Multiple node picker
- `"select_edge"` - Edge picker dropdown
- `"node_attribute"` - Select from available node attributes
- `"edge_attribute"` - Select from available edge attributes

### Parameter Properties
```python
{
    "name": "param_name",           # Parameter key (snake_case)
    "type": "number",               # Parameter type
    "label": "Display Label",       # UI label
    "description": "Help text",     # Tooltip/help text
    "required": True,               # Whether required
    "default": 0.5,                # Default value
    
    # Type-specific properties
    "min": 0,                      # number: minimum value
    "max": 100,                    # number: maximum value
    "step": 0.1,                   # number: increment step
    "options": [...],              # select: available options
    "multiple": True,              # select_nodes: allow multiple selection
}
```

---

## Main Analysis Function (`analysis.py`)

### Function Signature
```python
def analyze_graph(nodes, edges, parameters=None):
    """
    Analyze the graph and return structured results.
    
    Args:
        nodes (list): List of node dictionaries
        edges (list): List of edge dictionaries  
        parameters (dict): Analysis parameters from UI
        
    Returns:
        dict: Structured analysis results
        
    Raises:
        ValueError: If graph doesn't meet requirements
        AnalysisError: If analysis fails
    """
```

### Input Data Structures

#### Nodes Format
```python
nodes = [
    {
        "id": "A",                    # Required: unique identifier
        "label": "Node A",            # Optional: display label
        "type": "entity",             # Optional: node type
        "group": "main",              # Optional: grouping
        # ... custom attributes
    }
]
```

#### Edges Format  
```python
edges = [
    {
        "source": "A",                # Required: source node ID
        "target": "B",                # Required: target node ID
        "type": "+",                  # Optional: edge type ("+", "-", or custom)
        "weight": 1.5,                # Optional: edge weight (default: 1)
        # ... custom attributes
    }
]
```

#### Parameters Format
```python
parameters = {
    "algorithm": "weighted",
    "threshold": 0.7,
    "source_node": "A"
}
```

### Output Format

#### Standard Result Structure
```python
{
    "metadata": {
        "analysis_id": "my-analysis",
        "analysis_name": "My Custom Analysis",
        "timestamp": "2024-01-15T10:30:00Z",
        "parameters_used": {...},
        "execution_time_ms": 150,
        "graph_stats": {
            "nodes": 10,
            "edges": 15,
            "is_directed": True,
            "is_connected": False
        }
    },
    
    "results": {
        # Primary results (always shown)
        "primary": {
            "node_scores": {              # Node-level results
                "A": 0.85,
                "B": 0.62,
                # ...
            },
            "edge_scores": {              # Edge-level results (optional)
                "A->B": 0.75,
                # ...
            },
            "graph_metrics": {            # Graph-level results
                "overall_connectivity": 0.68,
                "clustering_coefficient": 0.43
            }
        },
        
        # Secondary results (collapsible/optional display)
        "secondary": {
            "paths": [                    # Path-based results
                {
                    "path": ["A", "B", "C"],
                    "score": 0.85,
                    "type": "positive"
                }
            ],
            "clusters": [                 # Grouping results
                {
                    "nodes": ["A", "B"],
                    "score": 0.92,
                    "label": "Cluster 1"
                }
            ]
        },
        
        # Visualization hints
        "visualizations": [
            {
                "type": "node_size",        # Visualization type
                "data_source": "node_scores", # Data to use
                "title": "Node Importance",
                "min_size": 10,
                "max_size": 30
            },
            {
                "type": "edge_color",
                "data_source": "edge_scores",
                "title": "Edge Strength", 
                "color_scale": "blue_red"
            },
            {
                "type": "node_highlight",
                "nodes": ["A", "C"],
                "color": "#ff0000",
                "title": "Key Nodes"
            }
        ]
    },
    
    # Human-readable summary
    "summary": "Analysis found 3 highly connected clusters with node A showing highest centrality (0.85)."
}
```

---

## Visualization Hints Reference

### Node Visualizations
```python
{
    "type": "node_size",
    "data_source": "node_scores",     # Key from results.primary
    "title": "Node Importance",
    "min_size": 10,                   # Minimum node size
    "max_size": 50,                   # Maximum node size
    "scale": "linear"                 # "linear" | "log" | "sqrt"
}

{
    "type": "node_color", 
    "data_source": "node_scores",
    "title": "Centrality Score",
    "color_scale": "viridis",         # "viridis" | "blue_red" | "greyscale"
    "reverse": False                  # Reverse color scale
}

{
    "type": "node_highlight",
    "nodes": ["A", "B"],              # Specific nodes to highlight
    "color": "#ff0000",               # Highlight color
    "title": "Important Nodes"
}
```

### Edge Visualizations
```python
{
    "type": "edge_width",
    "data_source": "edge_scores", 
    "title": "Connection Strength",
    "min_width": 1,
    "max_width": 8
}

{
    "type": "edge_color",
    "data_source": "edge_scores",
    "title": "Edge Weight",
    "color_scale": "blue_red"
}

{
    "type": "path_highlight",
    "paths": [["A", "B", "C"]],       # Paths to highlight
    "color": "#00ff00",
    "width": 4,
    "title": "Optimal Paths"
}
```

---

## Example Implementation

### Simple Centrality Plugin
```python
# py/plugins/centrality/__init__.py
ANALYSIS_INFO = {
    "id": "centrality",
    "name": "Node Centrality Analysis",
    "description": "Calculate node centrality measures",
    "version": "1.0.0",
    "author": "Example Author",
    "category": "structural",
    "min_nodes": 2,
    "parameters": [
        {
            "name": "measure",
            "type": "select",
            "label": "Centrality Measure",
            "required": True,
            "default": "betweenness",
            "options": [
                {"value": "betweenness", "label": "Betweenness Centrality"},
                {"value": "closeness", "label": "Closeness Centrality"},
                {"value": "degree", "label": "Degree Centrality"}
            ]
        }
    ]
}

from .analysis import analyze_graph
```

```python
# py/plugins/centrality/analysis.py
import networkx as nx
from datetime import datetime

def analyze_graph(nodes, edges, parameters=None):
    if not parameters:
        parameters = {}
        
    measure = parameters.get("measure", "betweenness")
    
    # Build NetworkX graph
    G = nx.Graph()  # or DiGraph() for directed
    
    for node in nodes:
        G.add_node(node['id'], **node)
    
    for edge in edges:
        weight = edge.get('weight', 1)
        G.add_edge(edge['source'], edge['target'], weight=weight)
    
    # Calculate centrality
    if measure == "betweenness":
        centrality = nx.betweenness_centrality(G)
    elif measure == "closeness":
        centrality = nx.closeness_centrality(G)
    elif measure == "degree":
        centrality = nx.degree_centrality(G)
    else:
        raise ValueError(f"Unknown measure: {measure}")
    
    # Convert to display labels
    id_to_label = {n['id']: n.get('label', n['id']) for n in nodes}
    labeled_centrality = {
        id_to_label[node_id]: score 
        for node_id, score in centrality.items()
    }
    
    return {
        "metadata": {
            "analysis_id": "centrality",
            "analysis_name": "Node Centrality Analysis",
            "timestamp": datetime.now().isoformat(),
            "parameters_used": parameters,
            "graph_stats": {
                "nodes": len(nodes),
                "edges": len(edges)
            }
        },
        "results": {
            "primary": {
                "node_scores": labeled_centrality
            },
            "visualizations": [
                {
                    "type": "node_size",
                    "data_source": "node_scores",
                    "title": f"{measure.title()} Centrality",
                    "min_size": 10,
                    "max_size": 30
                }
            ]
        },
        "summary": f"Calculated {measure} centrality for {len(nodes)} nodes. "
                  f"Highest scoring node: {max(labeled_centrality, key=labeled_centrality.get)}"
    }
```

---

## Error Handling

### Custom Exceptions
```python
class AnalysisError(Exception):
    """Base exception for analysis errors"""
    pass

class GraphValidationError(AnalysisError):
    """Graph doesn't meet plugin requirements"""
    pass

class ParameterError(AnalysisError):
    """Invalid parameters provided"""
    pass
```

### Error Handling Pattern
```python
def analyze_graph(nodes, edges, parameters=None):
    # Validate inputs
    if len(nodes) < 2:
        raise GraphValidationError("Analysis requires at least 2 nodes")
    
    if not edges:
        raise GraphValidationError("Analysis requires at least 1 edge")
    
    # Validate parameters
    if parameters and 'threshold' in parameters:
        threshold = parameters['threshold']
        if not 0 <= threshold <= 1:
            raise ParameterError("Threshold must be between 0 and 1")
    
    try:
        # Perform analysis
        result = do_analysis(nodes, edges, parameters)
        return result
    except Exception as e:
        raise AnalysisError(f"Analysis failed: {str(e)}")
```

---

## Testing Guidelines

### Required Tests
```python
# py/plugins/my_analysis/tests/test_analysis.py
import pytest
from ..analysis import analyze_graph
from ..analysis import GraphValidationError, ParameterError

def test_basic_analysis():
    """Test basic functionality with minimal graph"""
    nodes = [
        {'id': 'A', 'label': 'Node A'},
        {'id': 'B', 'label': 'Node B'}
    ]
    edges = [
        {'source': 'A', 'target': 'B', 'weight': 1}
    ]
    
    result = analyze_graph(nodes, edges)
    
    assert 'metadata' in result
    assert 'results' in result
    assert 'primary' in result['results']

def test_parameter_validation():
    """Test parameter validation"""
    nodes = [{'id': 'A'}, {'id': 'B'}]
    edges = [{'source': 'A', 'target': 'B'}]
    
    with pytest.raises(ParameterError):
        analyze_graph(nodes, edges, {'threshold': 2.0})  # Invalid threshold

def test_empty_graph():
    """Test error handling for empty graph"""
    with pytest.raises(GraphValidationError):
        analyze_graph([], [])
```

---

## Plugin Installation

### Manual Installation
1. Create plugin directory in `py/plugins/`
2. Add plugin files following the structure above
3. Plugin will be auto-discovered on next app restart

### Plugin Registry (Future)
- Plugins could be distributed as packages
- Central registry for sharing community plugins
- Automatic dependency installation

---

## Best Practices

### Performance
- Use efficient algorithms for large graphs
- Consider memory usage with large datasets
- Add progress indicators for long-running analysis
- Cache expensive computations when possible

### User Experience
- Provide clear parameter descriptions
- Use sensible default values
- Include helpful error messages
- Generate meaningful summaries

### Code Quality
- Include comprehensive tests
- Document complex algorithms
- Follow Python coding standards
- Handle edge cases gracefully

### Visualization
- Provide meaningful visualization hints
- Use appropriate scales and colors
- Consider colorblind accessibility
- Test with various graph sizes

---

This specification provides everything needed to create robust, user-friendly analysis plugins for the Causal Graph Tool.