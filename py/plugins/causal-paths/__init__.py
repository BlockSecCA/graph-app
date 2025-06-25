"""
Causal Path Analysis Plugin

Analyzes causal relationships and influence paths in directed graphs.
Calculates influence scores and identifies positive/negative causal pathways.
"""

ANALYSIS_INFO = {
    # Required fields
    "id": "causal-paths",
    "name": "Causal Path Analysis", 
    "description": "Analyze causal relationships, influence scores, and positive/negative pathways in graphs",
    "version": "1.0.0",
    "author": "Graph App Team",
    
    # Categorization
    "category": "causal",
    "tags": ["causal", "influence", "paths", "networkx"],
    
    # Requirements
    "min_nodes": 1,
    "min_edges": 0,
    "supports_directed": True,
    "supports_undirected": False,
    "supports_weighted": True,
    
    # UI Configuration
    "parameters": [
        {
            "name": "source_node",
            "type": "select_node",
            "label": "Source Node (for paths)",
            "description": "Starting node for path analysis (auto-selects first node if not specified)",
            "required": False,
            "default": "auto"
        },
        {
            "name": "target_node", 
            "type": "select_node",
            "label": "Target Node (for paths)",
            "description": "Ending node for path analysis (auto-selects last node if not specified)",
            "required": False,
            "default": "auto"
        },
        {
            "name": "max_path_length",
            "type": "number",
            "label": "Maximum Path Length",
            "description": "Maximum number of hops to consider in path analysis",
            "required": False,
            "default": 5,
            "min": 1,
            "max": 10,
            "step": 1
        }
    ]
}

# Import the main analysis function
# from .analysis import analyze_graph

# Export public interface
__all__ = ['ANALYSIS_INFO', 'analyze_graph']