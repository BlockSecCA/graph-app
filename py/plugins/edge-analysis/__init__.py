"""
Edge Weight Analysis Plugin

Analyzes edge weights, relationships, and flow patterns with rich edge visualization.
"""

ANALYSIS_INFO = {
    # Required fields
    "id": "edge-analysis",
    "name": "Edge Weight Analysis", 
    "description": "Comprehensive analysis of edge weights, relationships, and flow patterns with edge coloring",
    "version": "1.0.0",
    "author": "Graph App Team",
    
    # Optional fields
    "category": "Edge Analysis",
    "tags": ["edges", "weights", "relationships", "flow", "connections"],
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
                {"value": "comprehensive", "label": "Comprehensive Edge Analysis"},
                {"value": "weights", "label": "Weight Distribution Only"},
                {"value": "flow", "label": "Flow Patterns Only"},
                {"value": "relationships", "label": "Relationship Types Only"},
                {"value": "strength", "label": "Connection Strength Only"}
            ],
            "description": "Aspect of edges to focus analysis on"
        },
        {
            "id": "weight_categories",
            "name": "Weight Categories",
            "type": "number",
            "default": 5,
            "min": 3,
            "max": 10,
            "description": "Number of weight categories for visualization"
        },
        {
            "id": "edge_coloring",
            "name": "Edge Coloring Method",
            "type": "select",
            "default": "weight_strength",
            "options": [
                {"value": "weight_strength", "label": "By Weight Strength"},
                {"value": "relationship_type", "label": "By Relationship Type (+/-)"},
                {"value": "flow_direction", "label": "By Flow Direction"},
                {"value": "importance", "label": "By Edge Importance"},
                {"value": "categories", "label": "By Weight Categories"}
            ],
            "description": "Method for coloring edges"
        },
        {
            "id": "edge_sizing",
            "name": "Edge Width Scaling",
            "type": "boolean",
            "default": True,
            "description": "Scale edge width based on weight strength"
        },
        {
            "id": "highlight_extremes",
            "name": "Highlight Extreme Edges",
            "type": "boolean",
            "default": True,
            "description": "Highlight strongest and weakest edges"
        },
        {
            "id": "show_edge_labels",
            "name": "Show Edge Labels",
            "type": "boolean",
            "default": False,
            "description": "Display weight values as edge labels"
        },
        {
            "id": "color_scheme",
            "name": "Color Scheme",
            "type": "select",
            "default": "strength",
            "options": [
                {"value": "strength", "label": "Strength (Blue-Red)"},
                {"value": "heat", "label": "Heat Map (Cool-Warm)"},
                {"value": "traffic", "label": "Traffic Light (Green-Red)"},
                {"value": "monochrome", "label": "Monochrome (Gray Scale)"},
                {"value": "rainbow", "label": "Rainbow (Full Spectrum)"}
            ],
            "description": "Color scheme for edge visualization"
        }
    ]
}

# Export the analysis function
from .analysis import analyze_graph