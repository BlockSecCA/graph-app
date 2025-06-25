"""
Node Centrality Analysis Plugin

Calculates multiple centrality measures to identify important nodes in the graph.
"""

ANALYSIS_INFO = {
    # Required fields
    "id": "node-centrality",
    "name": "Node Centrality Analysis", 
    "description": "Calculate centrality measures to identify important nodes (betweenness, closeness, degree, eigenvector)",
    "version": "1.0.0",
    "author": "Graph App Team",
    
    # Optional fields
    "category": "Network Analysis",
    "tags": ["centrality", "importance", "nodes", "analysis"],
    "supports_directed": True,
    "supports_weighted": True,
    
    # Parameters that can be configured by user
    "parameters": [
        {
            "id": "centrality_types",
            "name": "Centrality Measures",
            "type": "multiselect",
            "default": ["betweenness", "closeness", "degree", "eigenvector"],
            "options": [
                {"value": "betweenness", "label": "Betweenness Centrality"},
                {"value": "closeness", "label": "Closeness Centrality"}, 
                {"value": "degree", "label": "Degree Centrality"},
                {"value": "eigenvector", "label": "Eigenvector Centrality"},
                {"value": "pagerank", "label": "PageRank"}
            ],
            "description": "Select which centrality measures to calculate"
        },
        {
            "id": "normalize",
            "name": "Normalize Values",
            "type": "boolean",
            "default": True,
            "description": "Normalize centrality values to 0-1 range"
        },
        {
            "id": "top_nodes",
            "name": "Highlight Top Nodes",
            "type": "number",
            "default": 3,
            "min": 1,
            "max": 20,
            "description": "Number of top nodes to highlight in visualization"
        }
    ]
}

# Export the analysis function
from .analysis import analyze_graph