"""
Community Detection Analysis Implementation

Identifies groups and clusters of nodes using various community detection algorithms.
"""

import networkx as nx
from datetime import datetime
from typing import List, Dict, Any
import random


class AnalysisError(Exception):
    """Base exception for analysis errors"""
    pass


class GraphValidationError(AnalysisError):
    """Graph doesn't meet plugin requirements"""
    pass


def analyze_graph(nodes: List[Dict], edges: List[Dict], parameters: Dict = None) -> Dict[str, Any]:
    """
    Detect communities in the graph using various algorithms.
    
    Args:
        nodes: List of node dictionaries with 'id', 'label', etc.
        edges: List of edge dictionaries with 'source', 'target', 'type', 'weight'
        parameters: Analysis parameters from UI
        
    Returns:
        Structured analysis results with community assignments and visualizations
        
    Raises:
        GraphValidationError: If graph doesn't meet requirements
        AnalysisError: If analysis fails
    """
    start_time = datetime.now()
    
    # Set default parameters
    if not parameters:
        parameters = {}
    
    algorithm = parameters.get('algorithm', 'louvain')
    resolution = parameters.get('resolution', 1.0)
    color_communities = parameters.get('color_communities', True)
    show_modularity = parameters.get('show_modularity', True)
    
    # Validate inputs
    if not nodes:
        raise GraphValidationError("Analysis requires at least 1 node")
    
    if len(nodes) < 3:
        raise GraphValidationError("Community detection requires at least 3 nodes")
    
    if not edges:
        raise GraphValidationError("Community detection requires at least 1 edge")
    
    try:
        # Build NetworkX graph - use undirected for community detection
        G = nx.Graph()
        
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
        
        # Add edges with weights (ignore direction for community detection)
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
        
        # Detect communities based on selected algorithm
        communities = []
        algorithm_info = {}
        
        if algorithm == 'louvain':
            try:
                # Check if we have the community package
                import community as community_louvain
                partition = community_louvain.best_partition(G, resolution=resolution, weight='weight', random_state=42)
                
                # Convert partition to communities list
                community_dict = {}
                for node, comm_id in partition.items():
                    if comm_id not in community_dict:
                        community_dict[comm_id] = []
                    community_dict[comm_id].append(node)
                
                communities = list(community_dict.values())
                algorithm_info = {
                    "name": "Louvain",
                    "resolution": resolution,
                    "supports_weights": True
                }
            except ImportError:
                # Fallback to greedy modularity if louvain package not available
                communities = list(nx.community.greedy_modularity_communities(G, weight='weight'))
                algorithm_info = {
                    "name": "Greedy Modularity (Louvain fallback)",
                    "supports_weights": True
                }
        
        elif algorithm == 'girvan_newman':
            # Use Girvan-Newman algorithm
            communities_generator = nx.community.girvan_newman(G)
            # Get the first split (can be extended to get more levels)
            try:
                communities = next(communities_generator)
                communities = [list(community) for community in communities]
                algorithm_info = {
                    "name": "Girvan-Newman",
                    "hierarchical": True,
                    "supports_weights": False
                }
            except StopIteration:
                # No communities found, treat as single community
                communities = [list(G.nodes())]
                algorithm_info = {
                    "name": "Girvan-Newman",
                    "note": "No clear community structure found"
                }
        
        elif algorithm == 'label_propagation':
            communities = list(nx.community.label_propagation_communities(G, weight='weight'))
            communities = [list(community) for community in communities]
            algorithm_info = {
                "name": "Label Propagation",
                "supports_weights": True,
                "randomized": True
            }
        
        elif algorithm == 'greedy_modularity':
            communities = list(nx.community.greedy_modularity_communities(G, weight='weight'))
            communities = [list(community) for community in communities]
            algorithm_info = {
                "name": "Greedy Modularity",
                "supports_weights": True
            }
        
        else:
            raise AnalysisError(f"Unknown algorithm: {algorithm}")
        
        # Convert node IDs to labels for readable output
        communities_labeled = []
        for i, community in enumerate(communities):
            community_labeled = {
                "id": i,
                "name": f"Community {i+1}",
                "size": len(community),
                "nodes": [id_to_label[node_id] for node_id in community],
                "node_ids": community  # Keep IDs for visualization
            }
            communities_labeled.append(community_labeled)
        
        # Sort communities by size (largest first)
        communities_labeled.sort(key=lambda x: x['size'], reverse=True)
        
        # Recalculate IDs and names after sorting
        for i, community in enumerate(communities_labeled):
            community['id'] = i
            community['name'] = f"Community {i+1}"
        
        # Calculate modularity if requested
        modularity_score = None
        if show_modularity and len(communities) > 1:
            try:
                # Create partition dict for modularity calculation
                partition = {}
                for i, community in enumerate(communities):
                    for node in community:
                        partition[node] = i
                modularity_score = round(nx.community.modularity(G, communities, weight='weight'), 4)
            except:
                modularity_score = None
        
        # Generate community colors for visualization
        community_colors = {}
        if color_communities:
            # Use a set of distinct colors
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', 
                     '#FF9FF3', '#54A0FF', '#5F27CD', '#00D2D3', '#FF9F43',
                     '#C44569', '#F8B500', '#6C5CE7', '#A29BFE', '#FD79A8']
            
            for i, community in enumerate(communities_labeled):
                color = colors[i % len(colors)]
                for node_id in community['node_ids']:
                    community_colors[id_to_label[node_id]] = color
        
        # Calculate execution time
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds() * 1000
        
        # Build visualizations
        visualizations = []
        
        if color_communities and community_colors:
            # Create node coloring by community
            color_mapping = {}
            for community in communities_labeled:
                color = colors[community['id'] % len(colors)]
                for node_label in community['nodes']:
                    color_mapping[node_label] = color
            
            visualizations.append({
                "type": "node_color",
                "data_source": "community_colors",
                "title": f"Communities (Algorithm: {algorithm_info['name']})",
                "color_mapping": color_mapping
            })
        
        # Add node sizing based on community size
        community_sizes = {}
        for community in communities_labeled:
            for node_label in community['nodes']:
                community_sizes[node_label] = community['size']
        
        if community_sizes:
            visualizations.append({
                "type": "node_size",
                "data_source": "community_sizes",
                "title": "Community Size",
                "min_size": 12,
                "max_size": 25
            })
        
        # Build results
        results = {
            "metadata": {
                "analysis_id": "community-detection",
                "analysis_name": "Community Detection",
                "timestamp": start_time.isoformat(),
                "parameters_used": parameters,
                "execution_time_ms": round(execution_time, 2),
                "algorithm": algorithm_info,
                "graph_stats": {
                    "nodes": len(nodes),
                    "edges": len(edges),
                    "communities_found": len(communities_labeled),
                    "modularity": modularity_score
                }
            },
            "results": {
                "primary": {
                    "communities": communities_labeled,
                    "modularity": modularity_score,
                    "algorithm_used": algorithm_info['name']
                },
                "secondary": {
                    "community_colors": community_colors,
                    "community_sizes": community_sizes,
                    "largest_community": communities_labeled[0] if communities_labeled else None,
                    "smallest_community": communities_labeled[-1] if communities_labeled else None
                },
                "visualizations": visualizations
            }
        }
        
        # Generate summary
        summary_parts = []
        if communities_labeled:
            summary_parts.append(f"Found {len(communities_labeled)} communities")
            summary_parts.append(f"Largest has {communities_labeled[0]['size']} nodes")
            if modularity_score is not None:
                summary_parts.append(f"Modularity: {modularity_score}")
            summary_parts.append(f"Algorithm: {algorithm_info['name']}")
        
        results["summary"] = ". ".join(summary_parts) + "." if summary_parts else "Community detection completed."
        
        return results
        
    except Exception as e:
        raise AnalysisError(f"Community detection failed: {str(e)}")