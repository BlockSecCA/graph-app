"""
Advanced Path Analysis Implementation

Comprehensive analysis of paths between nodes including efficiency, bottlenecks, and criticality.
"""

import networkx as nx
from datetime import datetime
from typing import List, Dict, Any, Tuple
import heapq


class AnalysisError(Exception):
    """Base exception for analysis errors"""
    pass


class GraphValidationError(AnalysisError):
    """Graph doesn't meet plugin requirements"""
    pass


def analyze_graph(nodes: List[Dict], edges: List[Dict], parameters: Dict = None) -> Dict[str, Any]:
    """
    Perform comprehensive path analysis on the graph.
    
    Args:
        nodes: List of node dictionaries with 'id', 'label', etc.
        edges: List of edge dictionaries with 'source', 'target', 'type', 'weight'
        parameters: Analysis parameters from UI
        
    Returns:
        Structured analysis results with path information and visualizations
        
    Raises:
        GraphValidationError: If graph doesn't meet requirements
        AnalysisError: If analysis fails
    """
    start_time = datetime.now()
    
    # Set default parameters
    if not parameters:
        parameters = {}
    
    source_node_param = parameters.get('source_node', 'auto')
    target_node_param = parameters.get('target_node', 'auto')
    analysis_type = parameters.get('analysis_type', 'comprehensive')
    max_path_length = parameters.get('max_path_length', 6)
    path_limit = parameters.get('path_limit', 20)
    highlight_critical = parameters.get('highlight_critical', True)
    
    # Validate inputs
    if not nodes:
        raise GraphValidationError("Analysis requires at least 1 node")
    
    if len(nodes) < 2:
        raise GraphValidationError("Path analysis requires at least 2 nodes")
    
    try:
        # Build NetworkX directed graph
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
        
        # Add edges with weights
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
            
            # For path analysis, use absolute weights as distances
            distance = abs(weight) if weight != 0 else 1
            G.add_edge(edge['source'], edge['target'], weight=distance, type=edge_type, original_weight=weight)
        
        # Create ID to label mapping for readable output
        id_to_label = {node['id']: node.get('label', node['id']) for node in nodes}
        
        # Determine source and target nodes
        node_ids = [node['id'] for node in nodes]
        
        if source_node_param == 'auto' or source_node_param not in node_ids:
            source_node = node_ids[0] if node_ids else None
        else:
            source_node = source_node_param
            
        if target_node_param == 'auto' or target_node_param not in node_ids:
            target_node = node_ids[-1] if len(node_ids) > 1 else (node_ids[0] if node_ids else None)
        else:
            target_node = target_node_param
        
        if source_node == target_node:
            # Find a different target if source and target are the same
            for node_id in node_ids:
                if node_id != source_node:
                    target_node = node_id
                    break
        
        # Initialize results structure
        results_data = {
            "source_node": id_to_label.get(source_node, source_node),
            "target_node": id_to_label.get(target_node, target_node),
            "source_id": source_node,
            "target_id": target_node
        }
        
        # Perform different types of analysis based on type parameter
        if analysis_type in ['comprehensive', 'shortest_only']:
            shortest_paths_data = analyze_shortest_paths(G, source_node, target_node, id_to_label)
            results_data.update(shortest_paths_data)
        
        if analysis_type in ['comprehensive', 'all_paths']:
            all_paths_data = analyze_all_paths(G, source_node, target_node, max_path_length, path_limit, id_to_label)
            results_data.update(all_paths_data)
        
        if analysis_type in ['comprehensive', 'efficiency']:
            efficiency_data = analyze_path_efficiency(G, id_to_label)
            results_data.update(efficiency_data)
        
        if analysis_type in ['comprehensive', 'bottlenecks']:
            bottleneck_data = analyze_bottlenecks(G, id_to_label)
            results_data.update(bottleneck_data)
        
        # Calculate execution time
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds() * 1000
        
        # Build visualizations
        visualizations = []
        
        # Highlight critical paths if requested
        if highlight_critical and 'critical_nodes' in results_data:
            visualizations.append({
                "type": "node_highlight",
                "nodes": results_data['critical_nodes'],
                "color": "#e74c3c",
                "title": "Critical Path Nodes"
            })
        
        # Size nodes by betweenness (bottleneck importance)
        if 'node_betweenness' in results_data:
            visualizations.append({
                "type": "node_size",
                "data_source": "node_betweenness",
                "title": "Path Bottlenecks",
                "min_size": 10,
                "max_size": 30
            })
        
        # Color edges by their importance in paths
        if 'edge_criticality' in results_data:
            visualizations.append({
                "type": "edge_color",
                "data_source": "edge_criticality", 
                "title": "Edge Importance in Paths",
                "color_scale": "yellow_red"
            })
        
        # Build final results
        final_results = {
            "metadata": {
                "analysis_id": "path-analysis",
                "analysis_name": "Advanced Path Analysis",
                "timestamp": start_time.isoformat(),
                "parameters_used": parameters,
                "execution_time_ms": round(execution_time, 2),
                "graph_stats": {
                    "nodes": len(nodes),
                    "edges": len(edges),
                    "is_directed": True,
                    "is_connected": nx.is_weakly_connected(G) if G.nodes else False,
                    "analysis_type": analysis_type
                }
            },
            "results": {
                "primary": {
                    "source_target": {
                        "source": results_data.get("source_node"),
                        "target": results_data.get("target_node")
                    },
                    "shortest_path": results_data.get("shortest_path"),
                    "shortest_distance": results_data.get("shortest_distance"),
                    "path_count": results_data.get("total_paths", 0)
                },
                "secondary": results_data,
                "visualizations": visualizations
            }
        }
        
        # Generate summary
        summary_parts = []
        if 'shortest_distance' in results_data:
            shortest_dist = results_data['shortest_distance']
            if shortest_dist is not None:
                summary_parts.append(f"Shortest path: {shortest_dist:.1f} steps")
            else:
                summary_parts.append("Shortest path: No path found")
        
        if 'total_paths' in results_data:
            summary_parts.append(f"Found {results_data['total_paths']} paths")
        
        if 'avg_path_efficiency' in results_data:
            efficiency = results_data['avg_path_efficiency']
            if efficiency is not None:
                summary_parts.append(f"Average efficiency: {efficiency:.2f}")
            else:
                summary_parts.append("Average efficiency: N/A")
        
        if 'critical_nodes' in results_data:
            critical_count = len(results_data['critical_nodes'])
            summary_parts.append(f"{critical_count} critical nodes identified")
        
        final_results["summary"] = ". ".join(summary_parts) + "." if summary_parts else "Path analysis completed."
        
        return final_results
        
    except Exception as e:
        raise AnalysisError(f"Path analysis failed: {str(e)}")


def analyze_shortest_paths(G: nx.DiGraph, source: str, target: str, id_to_label: Dict) -> Dict:
    """Analyze shortest paths between source and target."""
    results = {}
    
    try:
        # Calculate shortest path
        shortest_path = nx.shortest_path(G, source, target, weight='weight')
        shortest_distance = nx.shortest_path_length(G, source, target, weight='weight')
        
        # Convert to readable labels
        shortest_path_labeled = [id_to_label[node_id] for node_id in shortest_path]
        
        results.update({
            "shortest_path": shortest_path_labeled,
            "shortest_path_ids": shortest_path,
            "shortest_distance": round(shortest_distance, 2),
            "shortest_path_length": len(shortest_path) - 1
        })
        
    except nx.NetworkXNoPath:
        results.update({
            "shortest_path": None,
            "shortest_distance": None,
            "shortest_path_length": 0
        })
    
    return results


def analyze_all_paths(G: nx.DiGraph, source: str, target: str, max_length: int, limit: int, id_to_label: Dict) -> Dict:
    """Analyze all simple paths between source and target."""
    results = {}
    
    try:
        # Find all simple paths
        all_paths = list(nx.all_simple_paths(G, source, target, cutoff=max_length))
        
        # Limit number of paths for performance
        if len(all_paths) > limit:
            all_paths = all_paths[:limit]
        
        # Calculate path weights and lengths
        path_details = []
        for path in all_paths:
            path_labeled = [id_to_label[node_id] for node_id in path]
            
            # Calculate path weight
            path_weight = 0
            for i in range(len(path) - 1):
                edge_data = G[path[i]][path[i+1]]
                path_weight += edge_data['weight']
            
            path_details.append({
                "path": path_labeled,
                "path_ids": path,
                "weight": round(path_weight, 2),
                "length": len(path) - 1
            })
        
        # Sort by weight (shortest first)
        path_details.sort(key=lambda x: x['weight'])
        
        results.update({
            "all_paths": path_details,
            "total_paths": len(path_details),
            "avg_path_length": round(sum(p['length'] for p in path_details) / len(path_details), 2) if path_details else 0,
            "avg_path_weight": round(sum(p['weight'] for p in path_details) / len(path_details), 2) if path_details else 0
        })
        
    except nx.NetworkXNoPath:
        results.update({
            "all_paths": [],
            "total_paths": 0,
            "avg_path_length": 0,
            "avg_path_weight": 0
        })
    
    return results


def analyze_path_efficiency(G: nx.DiGraph, id_to_label: Dict) -> Dict:
    """Analyze overall path efficiency in the graph."""
    results = {}
    
    try:
        # Calculate average shortest path length
        if nx.is_connected(G.to_undirected()):
            avg_shortest_path = nx.average_shortest_path_length(G, weight='weight')
            efficiency = nx.global_efficiency(G)
        else:
            # For disconnected graphs, calculate for largest component
            largest_cc = max(nx.weakly_connected_components(G), key=len)
            subgraph = G.subgraph(largest_cc)
            avg_shortest_path = nx.average_shortest_path_length(subgraph, weight='weight')
            efficiency = nx.global_efficiency(subgraph)
        
        results.update({
            "avg_shortest_path_length": round(avg_shortest_path, 2),
            "global_efficiency": round(efficiency, 4),
            "avg_path_efficiency": round(efficiency, 4)
        })
        
    except:
        results.update({
            "avg_shortest_path_length": None,
            "global_efficiency": None,
            "avg_path_efficiency": None
        })
    
    return results


def analyze_bottlenecks(G: nx.DiGraph, id_to_label: Dict) -> Dict:
    """Identify bottleneck nodes and edges in paths."""
    results = {}
    
    try:
        # Calculate betweenness centrality for nodes (bottleneck detection)
        node_betweenness = nx.betweenness_centrality(G, weight='weight')
        node_betweenness_labeled = {
            id_to_label[node_id]: round(score, 4) for node_id, score in node_betweenness.items()
        }
        
        # Calculate edge betweenness centrality  
        edge_betweenness = nx.edge_betweenness_centrality(G, weight='weight')
        
        # Convert edge betweenness to criticality scores
        edge_criticality = {}
        for (u, v), score in edge_betweenness.items():
            edge_key = f"{id_to_label[u]} → {id_to_label[v]}"
            edge_criticality[edge_key] = round(score, 4)
        
        # Identify critical nodes (top 25% by betweenness)
        if node_betweenness_labeled:
            sorted_nodes = sorted(node_betweenness_labeled.items(), key=lambda x: x[1], reverse=True)
            critical_threshold = len(sorted_nodes) // 4 if len(sorted_nodes) >= 4 else 1
            critical_nodes = [node for node, score in sorted_nodes[:critical_threshold] if score > 0]
        else:
            critical_nodes = []
        
        results.update({
            "node_betweenness": node_betweenness_labeled,
            "edge_criticality": edge_criticality,
            "critical_nodes": critical_nodes,
            "bottleneck_count": len([score for score in node_betweenness_labeled.values() if score > 0.1])
        })
        
    except:
        results.update({
            "node_betweenness": {},
            "edge_criticality": {},
            "critical_nodes": [],
            "bottleneck_count": 0
        })
    
    return results