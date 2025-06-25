# Plugin Development Guide

Create custom analysis plugins for the Causal Graph Tool using Python and NetworkX.

## 🚀 Quick Start

### 1. Access Plugin Directory

**Installed App:**
- Open Causal Graph Tool
- Go to **Tools → Open Plugins Folder**
- This opens your user plugin directory

**Development:**
- Navigate to `py/plugins/` in the project folder

### 2. Create Your Plugin

Create a new folder with your plugin name:
```
plugins/
└── my-awesome-analysis/
    ├── __init__.py          # Plugin configuration
    ├── analysis.py          # Your analysis code
    └── README.md           # Documentation
```

### 3. Basic Plugin Structure

**`__init__.py`** - Plugin metadata:
```python
"""
My Awesome Analysis Plugin
"""

ANALYSIS_INFO = {
    "id": "my-awesome-analysis",
    "name": "My Awesome Analysis",
    "description": "Does something amazing with graphs",
    "version": "1.0.0",
    "author": "Your Name",
    "category": "structural",
    "min_nodes": 1,
    "min_edges": 0
}

from .analysis import analyze_graph
__all__ = ['ANALYSIS_INFO', 'analyze_graph']
```

**`analysis.py`** - Your analysis logic:
```python
import networkx as nx
from datetime import datetime

def analyze_graph(nodes, edges, parameters=None):
    """
    Analyze the graph and return results.
    
    Args:
        nodes: List of node dictionaries
        edges: List of edge dictionaries
        parameters: Analysis parameters (optional)
    
    Returns:
        Dictionary with analysis results
    """
    
    # Build NetworkX graph
    G = nx.DiGraph()
    
    # Add nodes
    for node in nodes:
        G.add_node(node['id'], **node)
    
    # Add edges
    for edge in edges:
        weight = edge.get('weight', 1)
        if edge.get('type') == '-':
            weight = -weight
        G.add_edge(edge['source'], edge['target'], weight=weight)
    
    # Your analysis here
    results = {}
    for node in G.nodes():
        degree = G.degree(node)
        results[node] = degree
    
    # Return structured results
    return {
        "metadata": {
            "analysis_id": "my-awesome-analysis",
            "analysis_name": "My Awesome Analysis",
            "timestamp": datetime.now().isoformat()
        },
        "results": {
            "primary": {
                "node_scores": results
            }
        },
        "summary": f"Analyzed {len(nodes)} nodes and {len(edges)} edges."
    }
```

### 4. Test Your Plugin

1. **Restart the app** - Plugins are discovered on startup
2. **Check the dropdown** - Your plugin should appear in the analysis dropdown
3. **Create a test graph** - Add some nodes and edges
4. **Select your plugin** - Choose it from the dropdown
5. **View results** - Analysis runs automatically

## 📊 Plugin Categories

### Structural Analysis
- Node centrality measures
- Graph connectivity analysis
- Community detection
- Graph metrics

### Causal Analysis
- Causal path finding
- Influence propagation
- Mediation analysis
- Confounding detection

### Flow Analysis
- Network flow algorithms
- Bottleneck identification
- Resource allocation
- Path optimization

## 🛠 Common Patterns

### Node Centrality Analysis
```python
def analyze_graph(nodes, edges, parameters=None):
    G = nx.DiGraph()
    # ... build graph ...
    
    centrality = nx.betweenness_centrality(G)
    
    return {
        "results": {
            "primary": {
                "centrality_scores": centrality
            }
        },
        "summary": f"Calculated betweenness centrality for {len(nodes)} nodes."
    }
```

### Path Analysis
```python
def analyze_graph(nodes, edges, parameters=None):
    G = nx.DiGraph()
    # ... build graph ...
    
    # Find shortest paths
    paths = []
    for source in G.nodes():
        for target in G.nodes():
            if source != target:
                try:
                    path = nx.shortest_path(G, source, target)
                    paths.append(path)
                except nx.NetworkXNoPath:
                    pass
    
    return {
        "results": {
            "primary": {
                "shortest_paths": paths
            }
        },
        "summary": f"Found {len(paths)} shortest paths."
    }
```

### Community Detection
```python
import networkx as nx
from networkx.algorithms import community

def analyze_graph(nodes, edges, parameters=None):
    G = nx.Graph()  # Undirected for community detection
    # ... build graph ...
    
    communities = community.greedy_modularity_communities(G)
    
    community_data = []
    for i, comm in enumerate(communities):
        community_data.append({
            "id": i,
            "nodes": list(comm),
            "size": len(comm)
        })
    
    return {
        "results": {
            "primary": {
                "communities": community_data
            }
        },
        "summary": f"Detected {len(communities)} communities."
    }
```

## 🎨 Result Visualization

### Node Sizing by Score
```python
"visualizations": [
    {
        "type": "node_size",
        "data_source": "centrality_scores",
        "title": "Node Centrality",
        "min_size": 10,
        "max_size": 30
    }
]
```

### Edge Coloring by Weight
```python
"visualizations": [
    {
        "type": "edge_color",
        "data_source": "edge_weights",
        "title": "Edge Strength",
        "color_scale": "blue_red"
    }
]
```

### Highlight Important Nodes
```python
"visualizations": [
    {
        "type": "node_highlight",
        "nodes": ["node1", "node2"],
        "color": "#ff0000",
        "title": "Key Nodes"
    }
]
```

## ⚡ Advanced Features

### User Parameters
```python
ANALYSIS_INFO = {
    # ... other fields ...
    "parameters": [
        {
            "name": "threshold",
            "type": "number",
            "label": "Threshold Value",
            "default": 0.5,
            "min": 0.0,
            "max": 1.0,
            "step": 0.1
        },
        {
            "name": "algorithm",
            "type": "select",
            "label": "Algorithm",
            "default": "standard",
            "options": [
                {"value": "standard", "label": "Standard"},
                {"value": "weighted", "label": "Weighted"}
            ]
        }
    ]
}
```

### Error Handling
```python
def analyze_graph(nodes, edges, parameters=None):
    # Validate inputs
    if len(nodes) < 2:
        raise ValueError("Analysis requires at least 2 nodes")
    
    if not edges:
        raise ValueError("Analysis requires at least 1 edge")
    
    try:
        # Your analysis here
        pass
    except Exception as e:
        raise RuntimeError(f"Analysis failed: {str(e)}")
```

### Performance for Large Graphs
```python
def analyze_graph(nodes, edges, parameters=None):
    # For large graphs, consider:
    
    # 1. Sampling
    if len(nodes) > 1000:
        sample_nodes = random.sample(nodes, 1000)
    
    # 2. Approximation algorithms
    if len(nodes) > 500:
        centrality = nx.betweenness_centrality(G, k=100)  # Sample 100 nodes
    else:
        centrality = nx.betweenness_centrality(G)
    
    # 3. Progress indication (future feature)
    # progress_callback(0.5)  # 50% complete
```

## 🔍 Debugging Tips

### Console Logging
```python
def analyze_graph(nodes, edges, parameters=None):
    print(f"Analyzing graph with {len(nodes)} nodes, {len(edges)} edges")
    print(f"Parameters: {parameters}")
    
    # Your analysis...
    
    print("Analysis complete")
    return results
```

### Validate Results
```python
def analyze_graph(nodes, edges, parameters=None):
    # ... analysis ...
    
    # Validate results before returning
    assert 'metadata' in results
    assert 'results' in results
    assert 'primary' in results['results']
    
    return results
```

## 📚 Available Libraries

Your plugins have access to:
- **NetworkX**: Graph algorithms and analysis
- **NumPy**: Numerical computing
- **SciPy**: Scientific computing
- **Pandas**: Data manipulation (via Pyodide)
- **Standard Library**: All Python standard modules

## 🚀 Plugin Sharing

### Export Your Plugin
1. **Create archive**: Zip your plugin folder
2. **Include documentation**: Add README.md with usage instructions
3. **Test thoroughly**: Verify on different graph types
4. **Share**: Distribute via GitHub, email, or plugin repositories

### Import Others' Plugins
1. **Download plugin**: Get the plugin folder
2. **Extract to plugins directory**: Use Tools → Open Plugins Folder
3. **Restart app**: Plugins are discovered on startup
4. **Select and test**: Choose from dropdown and verify results

## 🆘 Need Help?

- **Complete Specification**: See [PLUGIN_SPEC.md](./PLUGIN_SPEC.md) for full technical details
- **Example Plugins**: Check `py/plugins/causal-paths/` for a complete example
- **NetworkX Documentation**: https://networkx.org/documentation/
- **Issues**: Report problems at https://github.com/BlockSecCA/graph-app/issues

---

**Happy plugin development!** 🎉