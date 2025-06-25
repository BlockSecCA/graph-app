"""
Basic Graph Statistics Plugin

Provides fundamental graph metrics including density, diameter, clustering, and connectivity statistics.
"""

ANALYSIS_INFO = {
    # Required fields
    "id": "basic-statistics",
    "name": "Basic Graph Statistics", 
    "description": "Fundamental graph metrics including density, diameter, clustering, and connectivity analysis",
    "version": "1.0.0",
    "author": "Graph App Team",
    
    # Optional fields
    "category": "Graph Statistics",
    "tags": ["statistics", "metrics", "density", "diameter", "clustering", "connectivity"],
    "supports_directed": True,
    "supports_weighted": True,
    
    # Parameters that can be configured by user
    "parameters": [
        {
            "id": "analysis_focus",
            "name": "Analysis Focus",
            "type": "select",
            "default": "comprehensive",
            "options": [
                {"value": "comprehensive", "label": "All Statistics"},
                {"value": "basic", "label": "Basic Metrics Only"},
                {"value": "connectivity", "label": "Connectivity Analysis"},
                {"value": "clustering", "label": "Clustering Analysis"},
                {"value": "distance", "label": "Distance Metrics"}
            ],
            "description": "Which statistical measures to calculate"
        },
        {
            "id": "show_distribution",
            "name": "Show Degree Distribution",
            "type": "boolean",
            "default": True,
            "description": "Include degree distribution analysis"
        },
        {
            "id": "detailed_clustering",
            "name": "Detailed Clustering Analysis",
            "type": "boolean",
            "default": False,
            "description": "Calculate clustering coefficient for each node"
        },
        {
            "id": "connectivity_analysis",
            "name": "Connectivity Analysis",
            "type": "boolean",
            "default": True,
            "description": "Analyze graph connectivity and components"
        },
        {
            "id": "distance_analysis",
            "name": "Distance Analysis",
            "type": "boolean",
            "default": True,
            "description": "Calculate diameter, radius, and path lengths"
        }
    ]
}

# Export the analysis function
# from .analysis import analyze_graph