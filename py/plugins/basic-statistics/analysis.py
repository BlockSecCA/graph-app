"""
Basic Graph Statistics Implementation

Calculates fundamental graph metrics including density, diameter, clustering, and connectivity statistics.
"""

import networkx as nx
from datetime import datetime
from typing import List, Dict, Any, Tuple
import statistics
from collections import Counter


class AnalysisError(Exception):
    """Base exception for analysis errors"""
    pass


class GraphValidationError(AnalysisError):
    """Graph doesn't meet plugin requirements"""
    pass


def analyze_graph(nodes: List[Dict], edges: List[Dict], parameters: Dict = None) -> Dict[str, Any]:
    """
    Calculate comprehensive basic graph statistics.
    
    Args:
        nodes: List of node dictionaries with 'id', 'label', etc.
        edges: List of edge dictionaries with 'source', 'target', 'type', 'weight'
        parameters: Analysis parameters from UI
        
    Returns:
        Structured analysis results with graph statistics
        
    Raises:
        GraphValidationError: If graph doesn't meet requirements
        AnalysisError: If analysis fails
    """
    start_time = datetime.now()
    
    # Set default parameters
    if not parameters:
        parameters = {}
    
    analysis_focus = parameters.get('analysis_focus', 'comprehensive')
    show_distribution = parameters.get('show_distribution', True)
    detailed_clustering = parameters.get('detailed_clustering', False)
    connectivity_analysis = parameters.get('connectivity_analysis', True)
    distance_analysis = parameters.get('distance_analysis', True)
    
    # Validate inputs
    if not nodes:
        raise GraphValidationError("Analysis requires at least 1 node")
    
    try:
        # Build NetworkX graph (detect if should be directed)
        is_directed = any(edge.get('type') for edge in edges) or len(edges) != len(set((e['source'], e['target']) for e in edges))
        G = nx.DiGraph() if is_directed else nx.Graph()
        
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
            
            weight = abs(edge.get('weight', 1))
            G.add_edge(edge['source'], edge['target'], weight=weight)
        
        # Create ID to label mapping for readable output
        id_to_label = {node['id']: node.get('label', node['id']) for node in nodes}
        
        # Calculate statistics based on focus
        results_data = {}
        
        # Basic metrics (always calculated)
        basic_stats = calculate_basic_metrics(G)
        results_data.update(basic_stats)
        
        if analysis_focus in ['comprehensive', 'connectivity'] and connectivity_analysis:
            connectivity_stats = calculate_connectivity_metrics(G, id_to_label)
            results_data.update(connectivity_stats)
        
        if analysis_focus in ['comprehensive', 'clustering'] or detailed_clustering:
            clustering_stats = calculate_clustering_metrics(G, id_to_label, detailed_clustering)
            results_data.update(clustering_stats)
        
        if analysis_focus in ['comprehensive', 'distance'] and distance_analysis:
            distance_stats = calculate_distance_metrics(G, id_to_label)
            results_data.update(distance_stats)
        
        if show_distribution:
            degree_stats = calculate_degree_distribution(G)
            results_data.update(degree_stats)
        
        # Calculate execution time
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds() * 1000
        
        # Build visualizations
        visualizations = []
        
        # Highlight nodes with extreme degrees
        if 'degree_stats' in results_data:
            degree_dict = dict(G.degree())
            max_degree_node = max(degree_dict, key=degree_dict.get)
            min_degree_node = min(degree_dict, key=degree_dict.get)
            
            if degree_dict[max_degree_node] > degree_dict[min_degree_node]:
                visualizations.append({
                    "type": "node_highlight",
                    "nodes": [id_to_label[max_degree_node]],
                    "color": "#d73027",
                    "title": f"Highest Degree Node ({degree_dict[max_degree_node]} connections)"
                })
        
        # Highlight isolated nodes if any
        isolated_nodes = list(nx.isolates(G))
        if isolated_nodes:
            visualizations.append({
                "type": "node_highlight", 
                "nodes": [id_to_label[node] for node in isolated_nodes],
                "color": "#636363",
                "title": f"Isolated Nodes ({len(isolated_nodes)})"
            })
        
        # Build final results
        final_results = {
            "metadata": {
                "analysis_id": "basic-statistics",
                "analysis_name": "Basic Graph Statistics",
                "timestamp": start_time.isoformat(),
                "parameters_used": parameters,
                "execution_time_ms": round(execution_time, 2),
                "graph_stats": {
                    "nodes": len(nodes),
                    "edges": len(edges),
                    "is_directed": is_directed,
                    "analysis_focus": analysis_focus,
                    "has_weights": any(edge.get('weight', 1) != 1 for edge in edges)
                }
            },
            "results": {
                "primary": {
                    "basic_metrics": results_data.get('basic_metrics', {}),
                    "connectivity_summary": results_data.get('connectivity_summary', {}),
                    "clustering_summary": results_data.get('clustering_summary', {})
                },
                "secondary": results_data,
                "visualizations": visualizations
            }
        }
        
        # Generate summary
        summary_parts = []
        if 'basic_metrics' in results_data:
            metrics = results_data['basic_metrics']
            summary_parts.append(f"{metrics.get('node_count', 0)} nodes, {metrics.get('edge_count', 0)} edges")
            if 'density' in metrics:
                summary_parts.append(f"Density: {metrics['density']:.3f}")
            if 'average_degree' in metrics:
                summary_parts.append(f"Avg degree: {metrics['average_degree']:.1f}")
        
        if 'connectivity_summary' in results_data:
            conn = results_data['connectivity_summary']
            if conn.get('is_connected') is False:
                components = conn.get('connected_components', 1)
                summary_parts.append(f"{components} components")
        
        final_results["summary"] = ". ".join(summary_parts) + "." if summary_parts else "Graph statistics calculated."
        
        return final_results
        
    except Exception as e:
        raise AnalysisError(f"Graph statistics analysis failed: {str(e)}")


def calculate_basic_metrics(G: nx.Graph) -> Dict:
    """Calculate fundamental graph metrics."""
    results = {}
    
    node_count = G.number_of_nodes()
    edge_count = G.number_of_edges()
    
    # Basic counts
    basic_metrics = {
        'node_count': node_count,
        'edge_count': edge_count,
        'is_directed': G.is_directed(),
        'is_multigraph': G.is_multigraph()
    }
    
    # Density
    if node_count > 1:
        if G.is_directed():
            max_edges = node_count * (node_count - 1)
        else:
            max_edges = node_count * (node_count - 1) / 2
        basic_metrics['density'] = round(edge_count / max_edges, 4) if max_edges > 0 else 0
    else:
        basic_metrics['density'] = 0
    
    # Degree statistics
    degrees = [d for n, d in G.degree()]
    if degrees:
        basic_metrics['average_degree'] = round(sum(degrees) / len(degrees), 2)
        basic_metrics['max_degree'] = max(degrees)
        basic_metrics['min_degree'] = min(degrees)
        basic_metrics['degree_variance'] = round(statistics.variance(degrees) if len(degrees) > 1 else 0, 4)
    
    # Self loops
    basic_metrics['self_loops'] = nx.number_of_selfloops(G)
    
    results['basic_metrics'] = basic_metrics
    return results


def calculate_connectivity_metrics(G: nx.Graph, id_to_label: Dict) -> Dict:
    """Calculate connectivity and component analysis."""
    results = {}
    
    connectivity_summary = {}
    
    # Check if graph is connected
    if G.is_directed():
        is_connected = nx.is_strongly_connected(G)
        is_weakly_connected = nx.is_weakly_connected(G)
        components = list(nx.strongly_connected_components(G))
        weak_components = list(nx.weakly_connected_components(G))
        
        connectivity_summary.update({
            'is_strongly_connected': is_connected,
            'is_weakly_connected': is_weakly_connected,
            'strongly_connected_components': len(components),
            'weakly_connected_components': len(weak_components)
        })
        
        # Largest components
        if components:
            largest_scc = max(components, key=len)
            connectivity_summary['largest_scc_size'] = len(largest_scc)
            connectivity_summary['largest_scc_nodes'] = [id_to_label[node] for node in list(largest_scc)[:5]]
        
        if weak_components:
            largest_wcc = max(weak_components, key=len)
            connectivity_summary['largest_wcc_size'] = len(largest_wcc)
    else:
        is_connected = nx.is_connected(G)
        components = list(nx.connected_components(G))
        
        connectivity_summary.update({
            'is_connected': is_connected,
            'connected_components': len(components)
        })
        
        # Largest component
        if components:
            largest_component = max(components, key=len)
            connectivity_summary['largest_component_size'] = len(largest_component)
            connectivity_summary['largest_component_nodes'] = [id_to_label[node] for node in list(largest_component)[:5]]
    
    # Isolated nodes
    isolated_nodes = list(nx.isolates(G))
    connectivity_summary['isolated_nodes_count'] = len(isolated_nodes)
    if isolated_nodes:
        connectivity_summary['isolated_nodes'] = [id_to_label[node] for node in isolated_nodes[:10]]
    
    # Node connectivity (for small graphs)
    if G.number_of_nodes() <= 50:  # Only for smaller graphs due to computational cost
        try:
            if not G.is_directed():
                connectivity_summary['node_connectivity'] = nx.node_connectivity(G)
                connectivity_summary['edge_connectivity'] = nx.edge_connectivity(G)
        except:
            pass  # Skip if too expensive
    
    results['connectivity_summary'] = connectivity_summary
    return results


def calculate_clustering_metrics(G: nx.Graph, id_to_label: Dict, detailed: bool = False) -> Dict:
    """Calculate clustering coefficient and related metrics."""
    results = {}
    
    clustering_summary = {}
    
    # Global clustering coefficient
    try:
        if G.is_directed():
            # For directed graphs, use the undirected version
            G_undirected = G.to_undirected()
            global_clustering = nx.transitivity(G_undirected)
            avg_clustering = nx.average_clustering(G_undirected)
        else:
            global_clustering = nx.transitivity(G)
            avg_clustering = nx.average_clustering(G)
        
        clustering_summary['global_clustering_coefficient'] = round(global_clustering, 4)
        clustering_summary['average_clustering_coefficient'] = round(avg_clustering, 4)
        
    except Exception:
        clustering_summary['global_clustering_coefficient'] = 0
        clustering_summary['average_clustering_coefficient'] = 0
    
    # Detailed node clustering
    if detailed:
        try:
            if G.is_directed():
                node_clustering = nx.clustering(G.to_undirected())
            else:
                node_clustering = nx.clustering(G)
            
            # Convert to labeled format
            labeled_clustering = {
                id_to_label[node]: round(coeff, 4) 
                for node, coeff in node_clustering.items()
            }
            
            # Find nodes with highest clustering
            sorted_clustering = sorted(labeled_clustering.items(), key=lambda x: x[1], reverse=True)
            clustering_summary['highest_clustering_nodes'] = sorted_clustering[:5]
            clustering_summary['node_clustering_coefficients'] = labeled_clustering
            
        except Exception:
            pass
    
    # Triangles count
    try:
        if not G.is_directed():
            triangles = nx.triangles(G)
            total_triangles = sum(triangles.values()) // 3  # Each triangle counted 3 times
            clustering_summary['triangle_count'] = total_triangles
            
            if triangles:
                max_triangles_node = max(triangles, key=triangles.get)
                clustering_summary['max_triangles_node'] = id_to_label[max_triangles_node]
                clustering_summary['max_triangles_count'] = triangles[max_triangles_node]
    except Exception:
        pass
    
    results['clustering_summary'] = clustering_summary
    return results


def calculate_distance_metrics(G: nx.Graph, id_to_label: Dict) -> Dict:
    """Calculate distance-based metrics like diameter and radius."""
    results = {}
    
    distance_summary = {}
    
    # Only calculate for connected components
    if G.is_directed():
        if nx.is_strongly_connected(G):
            components = [G]
        else:
            # Use largest strongly connected component
            sccs = list(nx.strongly_connected_components(G))
            if sccs:
                largest_scc = max(sccs, key=len)
                components = [G.subgraph(largest_scc)]
            else:
                components = []
    else:
        if nx.is_connected(G):
            components = [G]
        else:
            # Use largest connected component
            ccs = list(nx.connected_components(G))
            if ccs:
                largest_cc = max(ccs, key=len)
                components = [G.subgraph(largest_cc)]
            else:
                components = []
    
    for i, component in enumerate(components):
        if component.number_of_nodes() <= 1:
            continue
            
        try:
            # Diameter and radius
            if component.number_of_nodes() <= 100:  # Only for reasonably sized components
                if G.is_directed():
                    # For directed graphs, we need shortest path lengths
                    path_lengths = dict(nx.all_pairs_shortest_path_length(component))
                    all_distances = []
                    for source_distances in path_lengths.values():
                        all_distances.extend(source_distances.values())
                    
                    if all_distances:
                        diameter = max(all_distances)
                        avg_path_length = sum(all_distances) / len(all_distances)
                        distance_summary['diameter'] = diameter
                        distance_summary['average_path_length'] = round(avg_path_length, 3)
                else:
                    diameter = nx.diameter(component)
                    radius = nx.radius(component)
                    avg_path_length = nx.average_shortest_path_length(component)
                    
                    distance_summary['diameter'] = diameter
                    distance_summary['radius'] = radius
                    distance_summary['average_path_length'] = round(avg_path_length, 3)
                
                # Eccentricity
                eccentricity = nx.eccentricity(component)
                center = nx.center(component)
                periphery = nx.periphery(component)
                
                distance_summary['center_nodes'] = [id_to_label[node] for node in center]
                distance_summary['periphery_nodes'] = [id_to_label[node] for node in periphery]
                distance_summary['center_count'] = len(center)
                distance_summary['periphery_count'] = len(periphery)
                
        except Exception as e:
            # Handle cases where calculation fails
            distance_summary['calculation_error'] = f"Distance metrics unavailable: {str(e)[:50]}"
    
    results['distance_summary'] = distance_summary
    return results


def calculate_degree_distribution(G: nx.Graph) -> Dict:
    """Calculate degree distribution statistics."""
    results = {}
    
    degrees = [d for n, d in G.degree()]
    
    if not degrees:
        return results
    
    degree_counter = Counter(degrees)
    degree_distribution = dict(degree_counter)
    
    degree_stats = {
        'degree_distribution': degree_distribution,
        'unique_degrees': len(degree_distribution),
        'most_common_degree': degree_counter.most_common(1)[0] if degree_counter else (0, 0),
        'degree_entropy': calculate_entropy(list(degree_counter.values())) if degree_counter else 0
    }
    
    # Degree distribution statistics
    degree_stats.update({
        'min_degree': min(degrees),
        'max_degree': max(degrees),
        'median_degree': statistics.median(degrees),
        'degree_std_dev': round(statistics.stdev(degrees) if len(degrees) > 1 else 0, 3)
    })
    
    results['degree_stats'] = degree_stats
    return results


def calculate_entropy(values: List[int]) -> float:
    """Calculate Shannon entropy of a distribution."""
    import math
    
    total = sum(values)
    if total == 0:
        return 0
    
    entropy = 0
    for value in values:
        if value > 0:
            p = value / total
            entropy -= p * math.log2(p)
    
    return round(entropy, 4)