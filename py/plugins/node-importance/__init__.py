"""
Node Importance Ranking Plugin

Ranks nodes by various importance criteria and provides rich visual highlighting.
"""

ANALYSIS_INFO = {
    # Required fields
    "id": "node-importance",
    "name": "Node Importance Ranking", 
    "description": "Rank and highlight nodes by importance using multiple criteria with rich color-coding",
    "version": "1.0.0",
    "author": "Graph App Team",
    
    # Optional fields
    "category": "Visual Analysis",
    "tags": ["importance", "ranking", "highlighting", "visualization", "tiers"],
    "supports_directed": True,
    "supports_weighted": True,
    
    # Parameters that can be configured by user
    "parameters": [
        {
            "id": "ranking_method",
            "name": "Ranking Method",
            "type": "select",
            "default": "composite",
            "options": [
                {"value": "composite", "label": "Composite Score (Multiple Factors)"},
                {"value": "degree", "label": "Degree (Connections)"},
                {"value": "betweenness", "label": "Betweenness (Bottlenecks)"},
                {"value": "closeness", "label": "Closeness (Reach)"},
                {"value": "pagerank", "label": "PageRank (Authority)"},
                {"value": "clustering", "label": "Clustering (Local Density)"}
            ],
            "description": "Method to determine node importance"
        },
        {
            "id": "highlight_tiers",
            "name": "Importance Tiers",
            "type": "number",
            "default": 4,
            "min": 2,
            "max": 8,
            "description": "Number of importance tiers to create"
        },
        {
            "id": "top_percent",
            "name": "Top Percent to Highlight",
            "type": "number",
            "default": 50,
            "min": 10,
            "max": 100,
            "description": "Percentage of nodes to include in importance ranking"
        },
        {
            "id": "color_scheme",
            "name": "Color Scheme",
            "type": "select",
            "default": "heat",
            "options": [
                {"value": "heat", "label": "Heat (Red-Orange-Yellow)"},
                {"value": "cool", "label": "Cool (Blue-Cyan-Green)"},
                {"value": "traffic", "label": "Traffic Light (Red-Yellow-Green)"},
                {"value": "rainbow", "label": "Rainbow (Full Spectrum)"},
                {"value": "monochrome", "label": "Monochrome (Blue Shades)"}
            ],
            "description": "Color scheme for importance visualization"
        },
        {
            "id": "show_labels",
            "name": "Show Importance Labels",
            "type": "boolean",
            "default": True,
            "description": "Show importance scores as node labels"
        },
        {
            "id": "tier_sizing",
            "name": "Size by Importance",
            "type": "boolean",
            "default": True,
            "description": "Scale node size based on importance tier"
        }
    ]
}

# Export the analysis function
# from .analysis import analyze_graph