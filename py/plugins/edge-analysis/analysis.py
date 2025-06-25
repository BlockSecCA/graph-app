"""
Edge Weight Analysis Implementation

Comprehensive analysis of edge weights, relationships, and flow patterns with rich visualization.
"""

import networkx as nx
from datetime import datetime
from typing import List, Dict, Any, Tuple
import statistics


class AnalysisError(Exception):
    """Base exception for analysis errors"""
    pass


class GraphValidationError(AnalysisError):
    """Graph doesn't meet plugin requirements"""
    pass


def analyze_graph(nodes: List[Dict], edges: List[Dict], parameters: Dict = None) -> Dict[str, Any]:
    """
    Perform comprehensive edge weight analysis.
    
    Args:
        nodes: List of node dictionaries with 'id', 'label', etc.
        edges: List of edge dictionaries with 'source', 'target', 'type', 'weight'
        parameters: Analysis parameters from UI
        
    Returns:
        Structured analysis results with edge analysis and visualizations
        
    Raises:
        GraphValidationError: If graph doesn't meet requirements
        AnalysisError: If analysis fails
    """
    start_time = datetime.now()
    
    # Set default parameters
    if not parameters:
        parameters = {}
    
    analysis_focus = parameters.get('analysis_focus', 'comprehensive')
    weight_categories = parameters.get('weight_categories', 5)
    edge_coloring = parameters.get('edge_coloring', 'weight_strength')
    edge_sizing = parameters.get('edge_sizing', True)
    highlight_extremes = parameters.get('highlight_extremes', True)
    show_edge_labels = parameters.get('show_edge_labels', False)
    color_scheme = parameters.get('color_scheme', 'strength')
    
    # Validate inputs
    if not nodes:
        raise GraphValidationError("Analysis requires at least 1 node")
    
    if not edges:
        raise GraphValidationError("Edge analysis requires at least 1 edge")
    
    try:
        # Build NetworkX graph
        G = nx.DiGraph()
        
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
        
        # Add edges with weights and metadata
        edge_data = []
        for edge in edges:
            if 'source' not in edge or 'target' not in edge:
                raise GraphValidationError("All edges must have 'source' and 'target' fields")
            
            # Validate source and target exist
            if edge['source'] not in G.nodes:
                raise GraphValidationError(f"Edge source '{edge['source']}' not found in nodes")
            if edge['target'] not in G.nodes:
                raise GraphValidationError(f"Edge target '{edge['target']}' not found in nodes")
            
            weight = edge.get('weight', 1)
            edge_type = edge.get('type', '+')
            
            # Store original edge data for analysis
            edge_info = {
                'source': edge['source'],
                'target': edge['target'],
                'weight': weight,
                'type': edge_type,
                'abs_weight': abs(weight),
                'strength': abs(weight),
                'id': f"{edge['source']}-{edge['target']}"
            }
            edge_data.append(edge_info)
            
            G.add_edge(edge['source'], edge['target'], **edge_info)
        
        # Create ID to label mapping for readable output
        id_to_label = {node['id']: node.get('label', node['id']) for node in nodes}
        
        # Perform analysis based on focus
        results_data = {}
        
        if analysis_focus in ['comprehensive', 'weights']:
            weight_analysis = analyze_edge_weights(edge_data, weight_categories)
            results_data.update(weight_analysis)
        
        if analysis_focus in ['comprehensive', 'flow']:
            flow_analysis = analyze_flow_patterns(G, edge_data, id_to_label)
            results_data.update(flow_analysis)
        
        if analysis_focus in ['comprehensive', 'relationships']:
            relationship_analysis = analyze_relationships(edge_data, id_to_label)
            results_data.update(relationship_analysis)
        
        if analysis_focus in ['comprehensive', 'strength']:
            strength_analysis = analyze_connection_strength(G, edge_data, id_to_label)
            results_data.update(strength_analysis)
        
        # Create visualization data
        visualization_data = create_edge_visualizations(
            edge_data, id_to_label, edge_coloring, edge_sizing, 
            color_scheme, highlight_extremes, show_edge_labels
        )
        results_data.update(visualization_data)
        
        # Calculate execution time
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds() * 1000
        
        # Build visualizations
        visualizations = []
        
        # Edge coloring based on selected method
        if 'edge_colors' in results_data:
            visualizations.append({
                "type": "edge_color",
                "data_source": "edge_colors",
                "title": f"Edge Analysis ({edge_coloring.replace('_', ' ').title()})",
                "color_mapping": results_data['edge_colors']
            })
        
        # Edge width scaling
        if edge_sizing and 'edge_widths' in results_data:
            visualizations.append({
                "type": "edge_width", 
                "data_source": "edge_widths",
                "title": "Edge Weight Scaling",
                "min_width": 1,
                "max_width": 8
            })
        
        # Highlight extreme edges
        if highlight_extremes and 'extreme_edges' in results_data:
            if results_data['extreme_edges']['strongest']:
                visualizations.append({
                    "type": "edge_highlight",
                    "edges": results_data['extreme_edges']['strongest'],
                    "color": "#d73027",
                    "title": "Strongest Connections"
                })
        
        # Build final results
        final_results = {
            "metadata": {
                "analysis_id": "edge-analysis",
                "analysis_name": "Edge Weight Analysis",
                "timestamp": start_time.isoformat(),
                "parameters_used": parameters,
                "execution_time_ms": round(execution_time, 2),
                "graph_stats": {
                    "nodes": len(nodes),
                    "edges": len(edges),
                    "analysis_focus": analysis_focus,
                    "has_weights": any(edge.get('weight', 1) != 1 for edge in edges),
                    "has_types": any(edge.get('type') for edge in edges)
                }
            },
            "results": {
                "primary": {
                    "edge_count": len(edges),
                    "weight_statistics": results_data.get('weight_stats', {}),
                    "relationship_summary": results_data.get('relationship_summary', {}),
                    "strongest_connections": results_data.get('strongest_edges', [])[:5]
                },
                "secondary": results_data,
                "visualizations": visualizations
            }
        }
        
        # Generate summary
        summary_parts = []
        if 'weight_stats' in results_data:
            stats = results_data['weight_stats']
            summary_parts.append(f"Analyzed {len(edges)} edges")
            if 'mean_weight' in stats:
                summary_parts.append(f"Average weight: {stats['mean_weight']:.2f}")
        
        if 'relationship_summary' in results_data:
            rel_sum = results_data['relationship_summary']
            if rel_sum.get('positive_count', 0) > 0:
                summary_parts.append(f"{rel_sum['positive_count']} positive relationships")
            if rel_sum.get('negative_count', 0) > 0:
                summary_parts.append(f"{rel_sum['negative_count']} negative relationships")
        
        final_results["summary"] = ". ".join(summary_parts) + "." if summary_parts else "Edge analysis completed."
        
        return final_results
        
    except Exception as e:
        raise AnalysisError(f"Edge analysis failed: {str(e)}")


def analyze_edge_weights(edge_data: List[Dict], categories: int) -> Dict:
    """Analyze weight distribution and statistics."""
    results = {}
    
    weights = [edge['weight'] for edge in edge_data]
    abs_weights = [edge['abs_weight'] for edge in edge_data]
    
    if not weights:
        return results
    
    # Basic statistics
    weight_stats = {
        'count': len(weights),
        'mean_weight': round(statistics.mean(weights), 3),
        'median_weight': round(statistics.median(weights), 3),
        'min_weight': round(min(weights), 3),
        'max_weight': round(max(weights), 3),
        'weight_range': round(max(weights) - min(weights), 3)
    }
    
    if len(weights) > 1:
        weight_stats['std_dev'] = round(statistics.stdev(weights), 3)
    
    # Weight distribution
    abs_weights.sort()
    
    # Create weight categories
    if len(abs_weights) >= categories:
        category_size = len(abs_weights) // categories
        weight_categories = []
        
        for i in range(categories):
            start_idx = i * category_size
            end_idx = (i + 1) * category_size if i < categories - 1 else len(abs_weights)
            
            category_weights = abs_weights[start_idx:end_idx]
            weight_categories.append({
                'category': i + 1,
                'min_weight': round(min(category_weights), 3),
                'max_weight': round(max(category_weights), 3),
                'count': len(category_weights),
                'avg_weight': round(sum(category_weights) / len(category_weights), 3)
            })
    else:
        weight_categories = []
    
    results.update({
        'weight_stats': weight_stats,
        'weight_categories': weight_categories,
        'weight_distribution': {
            'positive_weights': [w for w in weights if w > 0],
            'negative_weights': [w for w in weights if w < 0],
            'zero_weights': [w for w in weights if w == 0]
        }
    })
    
    return results


def analyze_flow_patterns(G: nx.DiGraph, edge_data: List[Dict], id_to_label: Dict) -> Dict:
    """Analyze directional flow patterns in the graph."""
    results = {}
    
    # Calculate flow statistics
    in_degrees = dict(G.in_degree(weight='weight'))
    out_degrees = dict(G.out_degree(weight='weight'))
    
    # Find flow sources (high out-degree, low in-degree)
    # Find flow sinks (high in-degree, low out-degree)
    # Find flow hubs (high both in and out degree)
    
    flow_nodes = {}
    for node_id in G.nodes():
        in_flow = in_degrees.get(node_id, 0)
        out_flow = out_degrees.get(node_id, 0)
        net_flow = out_flow - in_flow
        
        node_label = id_to_label[node_id]
        flow_nodes[node_label] = {
            'in_flow': round(in_flow, 3),
            'out_flow': round(out_flow, 3),
            'net_flow': round(net_flow, 3),
            'total_flow': round(in_flow + out_flow, 3)
        }
    
    # Classify nodes by flow pattern
    sources = [(node, data) for node, data in flow_nodes.items() if data['net_flow'] > 0.5]
    sinks = [(node, data) for node, data in flow_nodes.items() if data['net_flow'] < -0.5]
    hubs = [(node, data) for node, data in flow_nodes.items() if data['total_flow'] > statistics.mean([d['total_flow'] for d in flow_nodes.values()]) if flow_nodes]
    
    sources.sort(key=lambda x: x[1]['net_flow'], reverse=True)
    sinks.sort(key=lambda x: x[1]['net_flow'])
    hubs.sort(key=lambda x: x[1]['total_flow'], reverse=True)
    
    results.update({
        'flow_analysis': {
            'node_flows': flow_nodes,
            'flow_sources': [node for node, data in sources[:5]],
            'flow_sinks': [node for node, data in sinks[:5]],
            'flow_hubs': [node for node, data in hubs[:5]]
        }
    })
    
    return results


def analyze_relationships(edge_data: List[Dict], id_to_label: Dict) -> Dict:
    """Analyze relationship types and patterns."""
    results = {}
    
    # Count relationship types
    positive_edges = [edge for edge in edge_data if edge['type'] == '+']
    negative_edges = [edge for edge in edge_data if edge['type'] == '-']
    neutral_edges = [edge for edge in edge_data if edge['type'] not in ['+', '-']]
    
    relationship_summary = {
        'total_edges': len(edge_data),
        'positive_count': len(positive_edges),
        'negative_count': len(negative_edges),
        'neutral_count': len(neutral_edges),
        'positive_percentage': round(len(positive_edges) / len(edge_data) * 100, 1) if edge_data else 0,
        'negative_percentage': round(len(negative_edges) / len(edge_data) * 100, 1) if edge_data else 0
    }
    
    # Analyze relationship strengths
    if positive_edges:
        pos_weights = [edge['abs_weight'] for edge in positive_edges]
        relationship_summary['avg_positive_strength'] = round(statistics.mean(pos_weights), 3)
        relationship_summary['max_positive_strength'] = round(max(pos_weights), 3)
    
    if negative_edges:
        neg_weights = [edge['abs_weight'] for edge in negative_edges]
        relationship_summary['avg_negative_strength'] = round(statistics.mean(neg_weights), 3)
        relationship_summary['max_negative_strength'] = round(max(neg_weights), 3)
    
    results.update({
        'relationship_summary': relationship_summary,
        'relationship_details': {
            'positive_edges': [(f"{id_to_label[e['source']]} → {id_to_label[e['target']]}", e['weight']) for e in positive_edges],
            'negative_edges': [(f"{id_to_label[e['source']]} → {id_to_label[e['target']]}", e['weight']) for e in negative_edges]
        }
    })
    
    return results


def analyze_connection_strength(G: nx.DiGraph, edge_data: List[Dict], id_to_label: Dict) -> Dict:
    """Analyze connection strength and importance."""
    results = {}
    
    # Sort edges by absolute weight
    sorted_edges = sorted(edge_data, key=lambda x: x['abs_weight'], reverse=True)
    
    # Find strongest and weakest edges
    strongest_edges = sorted_edges[:5]
    weakest_edges = sorted_edges[-5:]
    
    # Create readable edge descriptions
    strongest_descriptions = []
    for edge in strongest_edges:
        source_label = id_to_label[edge['source']]
        target_label = id_to_label[edge['target']]
        edge_desc = f"{source_label} → {target_label}"
        strongest_descriptions.append((edge_desc, edge['weight']))
    
    weakest_descriptions = []
    for edge in weakest_edges:
        source_label = id_to_label[edge['source']]
        target_label = id_to_label[edge['target']]
        edge_desc = f"{source_label} → {target_label}"
        weakest_descriptions.append((edge_desc, edge['weight']))
    
    # Calculate edge importance (could be based on betweenness, etc.)
    edge_importance = {}
    for edge in edge_data:
        importance_score = edge['abs_weight']  # Simple importance = weight
        edge_key = f"{id_to_label[edge['source']]} → {id_to_label[edge['target']]}"
        edge_importance[edge_key] = round(importance_score, 3)
    
    results.update({
        'strength_analysis': {
            'strongest_edges': strongest_descriptions,
            'weakest_edges': weakest_descriptions,
            'edge_importance': edge_importance
        }
    })
    
    return results


def create_edge_visualizations(edge_data: List[Dict], id_to_label: Dict, coloring_method: str, 
                             sizing: bool, color_scheme: str, highlight_extremes: bool, 
                             show_labels: bool) -> Dict:
    """Create visualization data for edges."""
    results = {}
    
    # Generate edge colors based on method
    edge_colors = {}
    edge_widths = {}
    edge_labels = {}
    
    # Get weight range for normalization
    weights = [edge['abs_weight'] for edge in edge_data]
    if weights:
        min_weight = min(weights)
        max_weight = max(weights)
        weight_range = max_weight - min_weight if max_weight > min_weight else 1
    else:
        min_weight = max_weight = weight_range = 0
    
    # Color scheme definitions
    if color_scheme == 'strength':
        color_map = ['#2166ac', '#4393c3', '#92c5de', '#f7f7f7', '#fddbc7', '#f4a582', '#d6604d', '#b2182b']
    elif color_scheme == 'heat':
        color_map = ['#313695', '#4575b4', '#74add1', '#abd9e9', '#fee090', '#fdae61', '#f46d43', '#d73027']
    elif color_scheme == 'traffic':
        color_map = ['#2166ac', '#5aae61', '#a6d96a', '#ffffbf', '#fdae61', '#f46d43', '#d73027', '#a50026']
    elif color_scheme == 'monochrome':
        color_map = ['#f7f7f7', '#d9d9d9', '#bdbdbd', '#969696', '#737373', '#525252', '#252525', '#000000']
    else:  # rainbow
        color_map = ['#9e0142', '#d53e4f', '#f46d43', '#fdae61', '#fee08b', '#e6f598', '#abdda4', '#66c2a5']
    
    for edge in edge_data:
        source_label = id_to_label[edge['source']]
        target_label = id_to_label[edge['target']]
        edge_key = f"{source_label} → {target_label}"
        
        # Determine color based on method
        if coloring_method == 'weight_strength':
            # Color by absolute weight strength
            if weight_range > 0:
                normalized = (edge['abs_weight'] - min_weight) / weight_range
            else:
                normalized = 0.5
            color_idx = int(normalized * (len(color_map) - 1))
            edge_colors[edge_key] = color_map[color_idx]
            
        elif coloring_method == 'relationship_type':
            # Color by positive/negative type
            if edge['type'] == '+':
                edge_colors[edge_key] = '#27ae60'  # Green for positive
            elif edge['type'] == '-':
                edge_colors[edge_key] = '#e74c3c'  # Red for negative
            else:
                edge_colors[edge_key] = '#95a5a6'  # Gray for neutral
                
        elif coloring_method == 'flow_direction':
            # Could implement based on in/out degree of nodes
            edge_colors[edge_key] = color_map[len(color_map) // 2]  # Default middle color
            
        else:
            # Default coloring
            edge_colors[edge_key] = '#95a5a6'
        
        # Set edge width based on weight
        if sizing:
            if weight_range > 0:
                normalized_width = (edge['abs_weight'] - min_weight) / weight_range
            else:
                normalized_width = 0.5
            width = 1 + (normalized_width * 7)  # 1-8 range
            edge_widths[edge_key] = round(width, 1)
        else:
            edge_widths[edge_key] = 2
        
        # Set edge labels
        if show_labels:
            edge_labels[edge_key] = str(edge['weight'])
        else:
            edge_labels[edge_key] = ""
    
    # Find extreme edges for highlighting
    extreme_edges = {'strongest': [], 'weakest': []}
    if highlight_extremes and edge_data:
        sorted_by_weight = sorted(edge_data, key=lambda x: x['abs_weight'], reverse=True)
        
        # Top 3 strongest
        for edge in sorted_by_weight[:3]:
            source_label = id_to_label[edge['source']]
            target_label = id_to_label[edge['target']]
            extreme_edges['strongest'].append(f"{source_label} → {target_label}")
        
        # Bottom 3 weakest (if different from strongest)
        for edge in sorted_by_weight[-3:]:
            source_label = id_to_label[edge['source']]
            target_label = id_to_label[edge['target']]
            edge_key = f"{source_label} → {target_label}"
            if edge_key not in extreme_edges['strongest']:
                extreme_edges['weakest'].append(edge_key)
    
    results.update({
        'edge_colors': edge_colors,
        'edge_widths': edge_widths,
        'edge_labels': edge_labels,
        'extreme_edges': extreme_edges
    })
    
    return results