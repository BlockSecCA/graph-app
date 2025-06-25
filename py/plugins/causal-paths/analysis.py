"""
Causal Path Analysis Implementation

This module implements causal relationship analysis using NetworkX.
It calculates influence scores and identifies positive/negative causal pathways.
"""

import networkx as nx
from datetime import datetime
from typing import List, Dict, Any, Tuple


class AnalysisError(Exception):
    """Base exception for analysis errors"""
    pass


class GraphValidationError(AnalysisError):
    """Graph doesn't meet plugin requirements"""
    pass


def analyze_graph(nodes: List[Dict], edges: List[Dict], parameters: Dict = None) -> Dict[str, Any]:
    """
    Analyze causal relationships in the graph.
    
    Args:
        nodes: List of node dictionaries with 'id', 'label', etc.
        edges: List of edge dictionaries with 'source', 'target', 'type', 'weight'
        parameters: Analysis parameters from UI
        
    Returns:
        Structured analysis results following plugin spec
        
    Raises:
        GraphValidationError: If graph doesn't meet requirements
        AnalysisError: If analysis fails
    """
    start_time = datetime.now()
    
    # Set default parameters
    if not parameters:
        parameters = {}
    
    max_path_length = parameters.get('max_path_length', 5)
    source_node_param = parameters.get('source_node', 'auto')
    target_node_param = parameters.get('target_node', 'auto')
    
    # Validate inputs
    if not nodes:
        raise GraphValidationError("Analysis requires at least 1 node")
    
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
        
        # Add edges with weights and types
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
            
            # Convert negative edges to negative weights
            if edge_type == '-':
                weight = -abs(weight)
            else:
                weight = abs(weight)
                
            G.add_edge(edge['source'], edge['target'], weight=weight, type=edge_type)
        
        # Create ID to label mapping for readable output
        id_to_label = {node['id']: node.get('label', node['id']) for node in nodes}
        
        # Calculate influence scores (sum of incoming edge weights for each node)
        influence_scores = {}
        for node_id in G.nodes:
            score = sum(data['weight'] for _, target, data in G.in_edges(node_id, data=True))
            influence_scores[id_to_label[node_id]] = round(score, 3)
        
        # Determine source and target for path analysis
        node_ids = [node['id'] for node in nodes]
        
        if source_node_param == 'auto':
            source_node = node_ids[0] if node_ids else None
        else:
            source_node = source_node_param if source_node_param in node_ids else node_ids[0]
            
        if target_node_param == 'auto':
            target_node = node_ids[-1] if len(node_ids) > 1 else node_ids[0]
        else:
            target_node = target_node_param if target_node_param in node_ids else node_ids[-1]
        
        # Find causal paths
        positive_paths = []
        negative_paths = []
        mixed_paths = []
        
        if source_node and target_node and source_node != target_node:
            try:
                # Find all simple paths up to max_path_length
                all_paths = list(nx.all_simple_paths(
                    G, 
                    source=source_node, 
                    target=target_node, 
                    cutoff=max_path_length
                ))
                
                for path in all_paths:
                    # Analyze path edges to determine if positive, negative, or mixed
                    path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
                    edge_types = [G[u][v]['type'] for u, v in path_edges]
                    
                    # Convert to readable path
                    readable_path = [id_to_label[node_id] for node_id in path]
                    
                    # Calculate path weight (product for causal chains)
                    path_weight = 1
                    for u, v in path_edges:
                        path_weight *= G[u][v]['weight']
                    
                    path_info = {
                        'path': readable_path,
                        'weight': round(path_weight, 3),
                        'length': len(path) - 1
                    }
                    
                    # Classify path type
                    if all(t == '+' for t in edge_types):
                        positive_paths.append(path_info)
                    elif all(t == '-' for t in edge_types):
                        negative_paths.append(path_info)
                    else:
                        mixed_paths.append(path_info)
                        
            except nx.NetworkXNoPath:
                # No path exists between source and target
                pass
            except Exception as e:
                # Path finding failed, but continue with other analysis
                print(f"Path analysis warning: {e}")
        
        # Sort paths by weight (strongest first)
        positive_paths.sort(key=lambda x: abs(x['weight']), reverse=True)
        negative_paths.sort(key=lambda x: abs(x['weight']), reverse=True)
        mixed_paths.sort(key=lambda x: abs(x['weight']), reverse=True)
        
        # Calculate execution time
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds() * 1000
        
        # Build results
        results = {
            "metadata": {
                "analysis_id": "causal-paths",
                "analysis_name": "Causal Path Analysis",
                "timestamp": start_time.isoformat(),
                "parameters_used": parameters,
                "execution_time_ms": round(execution_time, 2),
                "graph_stats": {
                    "nodes": len(nodes),
                    "edges": len(edges),
                    "is_directed": True,
                    "is_connected": nx.is_weakly_connected(G) if G.nodes else False
                }
            },
            "results": {
                "primary": {
                    "influence_scores": influence_scores,
                    "positive_paths": [p['path'] for p in positive_paths],
                    "negative_paths": [p['path'] for p in negative_paths]
                },
                "secondary": {
                    "detailed_positive_paths": positive_paths,
                    "detailed_negative_paths": negative_paths,
                    "mixed_paths": mixed_paths,
                    "path_analysis_source": id_to_label.get(source_node, source_node),
                    "path_analysis_target": id_to_label.get(target_node, target_node)
                },
                "visualizations": [
                    {
                        "type": "node_size",
                        "data_source": "influence_scores",
                        "title": "Node Influence",
                        "min_size": 10,
                        "max_size": 30
                    }
                ]
            }
        }
        
        # Generate summary
        summary_parts = []
        if influence_scores:
            max_influence = max(influence_scores.items(), key=lambda x: abs(x[1]))
            summary_parts.append(f"Highest influence: {max_influence[0]} ({max_influence[1]})")
        
        summary_parts.append(f"Found {len(positive_paths)} positive path(s)")
        summary_parts.append(f"{len(negative_paths)} negative path(s)")
        
        if mixed_paths:
            summary_parts.append(f"{len(mixed_paths)} mixed path(s)")
            
        results["summary"] = ". ".join(summary_parts) + "."
        
        return results
        
    except Exception as e:
        raise AnalysisError(f"Causal path analysis failed: {str(e)}")