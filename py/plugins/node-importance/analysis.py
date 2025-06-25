"""
Node Importance Ranking Implementation

Ranks nodes by importance and provides rich visual highlighting with multiple color schemes.
"""

import networkx as nx
from datetime import datetime
from typing import List, Dict, Any
import colorsys


class AnalysisError(Exception):
    """Base exception for analysis errors"""
    pass


class GraphValidationError(AnalysisError):
    """Graph doesn't meet plugin requirements"""
    pass


def analyze_graph(nodes: List[Dict], edges: List[Dict], parameters: Dict = None) -> Dict[str, Any]:
    """
    Rank nodes by importance and create rich visual highlighting.
    
    Args:
        nodes: List of node dictionaries with 'id', 'label', etc.
        edges: List of edge dictionaries with 'source', 'target', 'type', 'weight'
        parameters: Analysis parameters from UI
        
    Returns:
        Structured analysis results with importance rankings and visualizations
        
    Raises:
        GraphValidationError: If graph doesn't meet requirements
        AnalysisError: If analysis fails
    """
    start_time = datetime.now()
    
    # Set default parameters
    if not parameters:
        parameters = {}
    
    ranking_method = parameters.get('ranking_method', 'composite')
    highlight_tiers = parameters.get('highlight_tiers', 4)
    top_percent = parameters.get('top_percent', 50)
    color_scheme = parameters.get('color_scheme', 'heat')
    show_labels = parameters.get('show_labels', True)
    tier_sizing = parameters.get('tier_sizing', True)
    
    # Validate inputs
    if not nodes:
        raise GraphValidationError("Analysis requires at least 1 node")
    
    try:
        # Build NetworkX graph
        G = nx.DiGraph() if any(edge.get('type') for edge in edges) else nx.Graph()
        
        # Add nodes to the graph
        for node in nodes:
            if 'id' not in node:
                raise GraphValidationError("All nodes must have an 'id' field")
            G.add_node(
                node['id'], 
                label=node.get('label', node['id']),
                type=node.get('type', ''),
                group=node.get('group', '')
            )
        
        # Add edges with weights
        for edge in edges:
            if 'source' not in edge or 'target' not in edge:
                raise GraphValidationError("All edges must have 'source' and 'target' fields")
            
            # Validate source and target exist
            if edge['source'] not in G.nodes:
                raise GraphValidationError(f"Edge source '{edge['source']}' not found in nodes")
            if edge['target'] not in G.nodes:
                raise GraphValidationError(f"Edge target '{edge['target']}' not found in nodes")
            
            weight = abs(edge.get('weight', 1))  # Use absolute weight
            G.add_edge(edge['source'], edge['target'], weight=weight)
        
        # Create ID to label mapping for readable output
        id_to_label = {node['id']: node.get('label', node['id']) for node in nodes}
        
        # Calculate importance scores based on selected method
        importance_scores = calculate_importance_scores(G, ranking_method)
        
        # Convert to labeled results
        importance_labeled = {
            id_to_label[node_id]: score for node_id, score in importance_scores.items()
        }
        
        # Create importance ranking
        ranked_nodes = sorted(importance_labeled.items(), key=lambda x: x[1], reverse=True)
        
        # Calculate how many nodes to include in highlighting
        total_nodes = len(ranked_nodes)
        nodes_to_highlight = max(1, int(total_nodes * top_percent / 100))
        top_nodes = ranked_nodes[:nodes_to_highlight]
        
        # Create importance tiers
        tier_data = create_importance_tiers(top_nodes, highlight_tiers)
        
        # Generate colors for tiers
        tier_colors = generate_color_scheme(highlight_tiers, color_scheme)
        
        # Create visualization data
        node_colors = {}
        node_sizes = {}
        node_tiers = {}
        node_labels = {}
        
        for i, tier in enumerate(tier_data):
            color = tier_colors[i]
            base_size = 30 - (i * 4) if tier_sizing else 15  # Larger for higher tiers
            
            for node_name, score in tier['nodes']:
                node_colors[node_name] = color
                node_sizes[node_name] = max(base_size, 10)
                node_tiers[node_name] = i + 1
                
                if show_labels:
                    node_labels[node_name] = f"{node_name}\n({score:.3f})"
                else:
                    node_labels[node_name] = node_name
        
        # Add remaining nodes with default styling
        for node_name, score in ranked_nodes[nodes_to_highlight:]:
            if node_name not in node_colors:
                node_colors[node_name] = "#cccccc"  # Gray for unranked
                node_sizes[node_name] = 12
                node_tiers[node_name] = 0  # Tier 0 for unranked
                node_labels[node_name] = node_name if not show_labels else f"{node_name}\n({score:.3f})"
        
        # Calculate statistics
        stats = calculate_importance_stats(importance_labeled, tier_data)
        
        # Calculate execution time
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds() * 1000
        
        # Build visualizations
        visualizations = []
        
        # Node coloring by importance tier
        visualizations.append({
            "type": "node_color",
            "data_source": "node_colors",
            "title": f"Importance Ranking ({ranking_method.title()})",
            "color_mapping": node_colors
        })
        
        # Node sizing by importance tier
        if tier_sizing:
            visualizations.append({
                "type": "node_size",
                "data_source": "importance_scores",
                "title": "Importance Size",
                "min_size": 10,
                "max_size": 30
            })
        
        # Highlight top tier nodes
        if tier_data and tier_data[0]['nodes']:
            top_tier_nodes = [node for node, score in tier_data[0]['nodes']]
            visualizations.append({
                "type": "node_highlight",
                "nodes": top_tier_nodes,
                "color": tier_colors[0],
                "title": f"Tier 1 (Most Important)"
            })
        
        # Build results
        results = {
            "metadata": {
                "analysis_id": "node-importance",
                "analysis_name": "Node Importance Ranking",
                "timestamp": start_time.isoformat(),
                "parameters_used": parameters,
                "execution_time_ms": round(execution_time, 2),
                "graph_stats": {
                    "nodes": len(nodes),
                    "edges": len(edges),
                    "ranking_method": ranking_method,
                    "tiers_created": len(tier_data),
                    "nodes_highlighted": nodes_to_highlight
                }
            },
            "results": {
                "primary": {
                    "importance_ranking": dict(ranked_nodes[:10]),  # Top 10
                    "tier_summary": [
                        {
                            "tier": i + 1,
                            "count": len(tier['nodes']),
                            "avg_score": tier['avg_score'],
                            "color": tier_colors[i]
                        }
                        for i, tier in enumerate(tier_data)
                    ]
                },
                "secondary": {
                    "importance_scores": importance_labeled,
                    "full_ranking": ranked_nodes,
                    "tier_assignments": node_tiers,
                    "node_colors": node_colors,
                    "node_sizes": node_sizes,
                    "node_labels": node_labels,
                    "statistics": stats,
                    "tier_data": tier_data
                },
                "visualizations": visualizations
            }
        }
        
        # Generate summary
        summary_parts = []
        if ranked_nodes:
            top_node = ranked_nodes[0]
            summary_parts.append(f"Most important: {top_node[0]} ({top_node[1]:.3f})")
            summary_parts.append(f"Ranked {len(ranked_nodes)} nodes")
            summary_parts.append(f"Created {len(tier_data)} importance tiers")
            summary_parts.append(f"Method: {ranking_method.title()}")
        
        results["summary"] = ". ".join(summary_parts) + "." if summary_parts else "Importance ranking completed."
        
        return results
        
    except Exception as e:
        raise AnalysisError(f"Node importance analysis failed: {str(e)}")


def calculate_importance_scores(G: nx.Graph, method: str) -> Dict[str, float]:
    """Calculate importance scores using the specified method."""
    
    if method == 'degree':
        scores = nx.degree_centrality(G)
    elif method == 'betweenness':
        scores = nx.betweenness_centrality(G, weight='weight')
    elif method == 'closeness':
        try:
            scores = nx.closeness_centrality(G, distance='weight')
        except:
            scores = nx.closeness_centrality(G)
    elif method == 'pagerank':
        scores = nx.pagerank(G, weight='weight')
    elif method == 'clustering':
        scores = nx.clustering(G, weight='weight')
    elif method == 'composite':
        # Calculate multiple measures and combine
        measures = {}
        
        # Degree centrality
        measures['degree'] = nx.degree_centrality(G)
        
        # Betweenness centrality
        try:
            measures['betweenness'] = nx.betweenness_centrality(G, weight='weight')
        except:
            measures['betweenness'] = nx.betweenness_centrality(G)
        
        # Closeness centrality
        try:
            measures['closeness'] = nx.closeness_centrality(G, distance='weight')
        except:
            measures['closeness'] = nx.closeness_centrality(G)
        
        # PageRank
        try:
            measures['pagerank'] = nx.pagerank(G, weight='weight')
        except:
            measures['pagerank'] = nx.pagerank(G)
        
        # Combine scores (weighted average)
        scores = {}
        weights = {'degree': 0.3, 'betweenness': 0.3, 'closeness': 0.2, 'pagerank': 0.2}
        
        for node in G.nodes():
            combined_score = sum(
                measures[measure].get(node, 0) * weight 
                for measure, weight in weights.items()
            )
            scores[node] = combined_score
    else:
        # Default to degree centrality
        scores = nx.degree_centrality(G)
    
    return scores


def create_importance_tiers(ranked_nodes: List[tuple], num_tiers: int) -> List[Dict]:
    """Create importance tiers from ranked nodes."""
    
    if not ranked_nodes or num_tiers <= 0:
        return []
    
    tier_size = max(1, len(ranked_nodes) // num_tiers)
    tiers = []
    
    for i in range(num_tiers):
        start_idx = i * tier_size
        # For the last tier, include any remaining nodes
        end_idx = (i + 1) * tier_size if i < num_tiers - 1 else len(ranked_nodes)
        
        tier_nodes = ranked_nodes[start_idx:end_idx]
        
        if tier_nodes:
            avg_score = sum(score for node, score in tier_nodes) / len(tier_nodes)
            min_score = min(score for node, score in tier_nodes)
            max_score = max(score for node, score in tier_nodes)
            
            tiers.append({
                'tier': i + 1,
                'nodes': tier_nodes,
                'count': len(tier_nodes),
                'avg_score': round(avg_score, 4),
                'min_score': round(min_score, 4),
                'max_score': round(max_score, 4)
            })
    
    return tiers


def generate_color_scheme(num_colors: int, scheme: str) -> List[str]:
    """Generate a list of colors for the specified scheme."""
    
    colors = []
    
    if scheme == 'heat':
        # Red to yellow heat map
        base_colors = ['#d73027', '#f46d43', '#fdae61', '#fee08b', '#e6f598', '#abdda4', '#66c2a5', '#3288bd']
    elif scheme == 'cool':
        # Blue to green cool map
        base_colors = ['#2166ac', '#4393c3', '#92c5de', '#d1e5f0', '#f7f7f7', '#fddbc7', '#f4a582', '#d6604d']
    elif scheme == 'traffic':
        # Traffic light colors
        base_colors = ['#d73027', '#fc8d59', '#fee08b', '#d9ef8b', '#91bfdb', '#4575b4', '#313695', '#2166ac']
    elif scheme == 'rainbow':
        # Full spectrum
        for i in range(num_colors):
            hue = i / max(1, num_colors - 1)  # 0 to 1
            rgb = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
            hex_color = '#{:02x}{:02x}{:02x}'.format(
                int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
            )
            colors.append(hex_color)
        return colors
    elif scheme == 'monochrome':
        # Blue monochrome
        base_colors = ['#08519c', '#2171b5', '#4292c6', '#6baed6', '#9ecae1', '#c6dbef', '#deebf7', '#f7fbff']
    else:
        # Default heat
        base_colors = ['#d73027', '#f46d43', '#fdae61', '#fee08b', '#e6f598', '#abdda4', '#66c2a5', '#3288bd']
    
    # Select colors from base palette
    if num_colors <= len(base_colors):
        colors = base_colors[:num_colors]
    else:
        # Repeat/interpolate if we need more colors
        colors = base_colors * (num_colors // len(base_colors) + 1)
        colors = colors[:num_colors]
    
    return colors


def calculate_importance_stats(importance_scores: Dict[str, float], tier_data: List[Dict]) -> Dict:
    """Calculate statistics about importance distribution."""
    
    scores = list(importance_scores.values())
    
    if not scores:
        return {}
    
    stats = {
        'total_nodes': len(scores),
        'mean_score': round(sum(scores) / len(scores), 4),
        'max_score': round(max(scores), 4),
        'min_score': round(min(scores), 4),
        'score_range': round(max(scores) - min(scores), 4),
        'tiers_created': len(tier_data)
    }
    
    # Calculate standard deviation
    mean = stats['mean_score']
    variance = sum((score - mean) ** 2 for score in scores) / len(scores)
    stats['std_deviation'] = round(variance ** 0.5, 4)
    
    return stats