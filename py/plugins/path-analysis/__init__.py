"""
Advanced Path Analysis Plugin

Analyzes paths between nodes including shortest paths, all paths, critical paths, and path efficiency.
"""

ANALYSIS_INFO = {
    # Required fields
    "id": "path-analysis",
    "name": "Advanced Path Analysis", 
    "description": "Comprehensive path analysis including shortest paths, path efficiency, and bottleneck identification",
    "version": "1.0.0",
    "author": "Graph App Team",
    
    # Optional fields
    "category": "Path Analysis",
    "tags": ["paths", "shortest", "efficiency", "bottlenecks", "connectivity"],
    "supports_directed": True,
    "supports_weighted": True,
    
    # Parameters that can be configured by user
    "parameters": [
        {
            "id": "source_node",
            "name": "Source Node",
            "type": "node_select",
            "default": "auto",
            "description": "Starting node for path analysis (auto = first node)"
        },
        {
            "id": "target_node", 
            "name": "Target Node",
            "type": "node_select", 
            "default": "auto",
            "description": "Ending node for path analysis (auto = last node)"
        },
        {
            "id": "analysis_type",
            "name": "Analysis Type",
            "type": "select",
            "default": "comprehensive",
            "options": [
                {"value": "comprehensive", "label": "Comprehensive (All Analysis)"},
                {"value": "shortest_only", "label": "Shortest Paths Only"},
                {"value": "all_paths", "label": "All Simple Paths"},
                {"value": "efficiency", "label": "Path Efficiency"},
                {"value": "bottlenecks", "label": "Bottleneck Analysis"}
            ],
            "description": "Type of path analysis to perform"
        },
        {
            "id": "max_path_length",
            "name": "Maximum Path Length",
            "type": "number",
            "default": 6,
            "min": 2,
            "max": 15,
            "description": "Maximum number of hops in paths to consider"
        },
        {
            "id": "path_limit",
            "name": "Path Limit",
            "type": "number", 
            "default": 20,
            "min": 5,
            "max": 100,
            "description": "Maximum number of paths to analyze (for performance)"
        },
        {
            "id": "highlight_critical",
            "name": "Highlight Critical Paths",
            "type": "boolean",
            "default": True,
            "description": "Highlight the most important paths in visualization"
        }
    ]
}

# Export the analysis function
# from .analysis import analyze_graph