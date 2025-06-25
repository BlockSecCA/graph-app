"""
Community Detection Plugin

Identifies groups and clusters of nodes that are more connected to each other than to the rest of the graph.
"""

ANALYSIS_INFO = {
    # Required fields
    "id": "community-detection",
    "name": "Community Detection", 
    "description": "Identify clusters and communities of closely connected nodes using multiple algorithms",
    "version": "1.0.0",
    "author": "Graph App Team",
    
    # Optional fields
    "category": "Network Analysis",
    "tags": ["community", "clustering", "groups", "modularity"],
    "supports_directed": True,
    "supports_weighted": True,
    
    # Parameters that can be configured by user
    "parameters": [
        {
            "id": "algorithm",
            "name": "Detection Algorithm",
            "type": "select",
            "default": "louvain",
            "options": [
                {"value": "louvain", "label": "Louvain (Fast, Good Quality)"},
                {"value": "girvan_newman", "label": "Girvan-Newman (Hierarchical)"},
                {"value": "label_propagation", "label": "Label Propagation (Very Fast)"},
                {"value": "greedy_modularity", "label": "Greedy Modularity (Good Balance)"}
            ],
            "description": "Algorithm to use for community detection"
        },
        {
            "id": "resolution",
            "name": "Resolution Parameter",
            "type": "number",
            "default": 1.0,
            "min": 0.1,
            "max": 3.0,
            "step": 0.1,
            "description": "Higher values create smaller communities (Louvain only)"
        },
        {
            "id": "color_communities",
            "name": "Color Communities",
            "type": "boolean",
            "default": True,
            "description": "Color nodes by their community membership"
        },
        {
            "id": "show_modularity",
            "name": "Calculate Modularity",
            "type": "boolean", 
            "default": True,
            "description": "Calculate modularity score (quality of community structure)"
        }
    ]
}

# Export the analysis function
from .analysis import analyze_graph