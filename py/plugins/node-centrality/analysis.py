"""
Node Centrality Analysis Implementation

Calculates various centrality measures to identify important nodes in the graph.
"""

import networkx as nx
from datetime import datetime
from typing import List, Dict, Any


class AnalysisError(Exception):
    """Base exception for analysis errors"""
    pass


class GraphValidationError(AnalysisError):
    """Graph doesn't meet plugin requirements"""
    pass


def analyze_graph(nodes: List[Dict], edges: List[Dict], parameters: Dict = None) -> Dict[str, Any]:
    """
    Calculate centrality measures for nodes in the graph.
    
    Args:
        nodes: List of node dictionaries with 'id', 'label', etc.
        edges: List of edge dictionaries with 'source', 'target', 'type', 'weight'
        parameters: Analysis parameters from UI
        
    Returns:
        Structured analysis results with centrality scores and visualizations
        
    Raises:
        GraphValidationError: If graph doesn't meet requirements
        AnalysisError: If analysis fails
    """
    start_time = datetime.now()
    
    # Set default parameters
    if not parameters:
        parameters = {}
    
    centrality_types = parameters.get('centrality_types', ['betweenness', 'closeness', 'degree', 'eigenvector'])
    normalize = parameters.get('normalize', True)
    top_nodes = parameters.get('top_nodes', 3)
    
    # Validate inputs
    if not nodes:
        raise GraphValidationError("Analysis requires at least 1 node")
    
    if len(nodes) < 2:
        raise GraphValidationError("Centrality analysis requires at least 2 nodes")
    
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
            
            weight = abs(edge.get('weight', 1))  # Use absolute weight for centrality
            G.add_edge(edge['source'], edge['target'], weight=weight)
        
        # Create ID to label mapping for readable output
        id_to_label = {node['id']: node.get('label', node['id']) for node in nodes}
        
        # Calculate centrality measures
        centrality_results = {}
        
        if 'degree' in centrality_types:
            degree_cent = nx.degree_centrality(G)
            centrality_results['degree'] = {
                id_to_label[node]: round(score, 4) for node, score in degree_cent.items()
            }
        
        if 'betweenness' in centrality_types:
            try:
                betweenness_cent = nx.betweenness_centrality(G, normalized=normalize, weight='weight')
                centrality_results['betweenness'] = {
                    id_to_label[node]: round(score, 4) for node, score in betweenness_cent.items()
                }
            except:
                # Fallback for disconnected graphs
                betweenness_cent = nx.betweenness_centrality(G, normalized=normalize)
                centrality_results['betweenness'] = {
                    id_to_label[node]: round(score, 4) for node, score in betweenness_cent.items()
                }
        
        if 'closeness' in centrality_types:
            try:
                closeness_cent = nx.closeness_centrality(G, distance='weight')
                centrality_results['closeness'] = {
                    id_to_label[node]: round(score, 4) for node, score in closeness_cent.items()
                }
            except:
                # Fallback for disconnected graphs
                closeness_cent = nx.closeness_centrality(G)
                centrality_results['closeness'] = {
                    id_to_label[node]: round(score, 4) for node, score in closeness_cent.items()
                }
        
        if 'eigenvector' in centrality_types:
            try:
                # Convert to undirected for eigenvector centrality if directed
                G_undirected = G.to_undirected() if nx.is_directed(G) else G
                eigenvector_cent = nx.eigenvector_centrality(G_undirected, weight='weight', max_iter=1000)
                centrality_results['eigenvector'] = {
                    id_to_label[node]: round(score, 4) for node, score in eigenvector_cent.items()
                }
            except:
                # Fallback without weights or use degree centrality
                try:
                    eigenvector_cent = nx.eigenvector_centrality(G_undirected, max_iter=1000)
                    centrality_results['eigenvector'] = {
                        id_to_label[node]: round(score, 4) for node, score in eigenvector_cent.items()
                    }
                except:
                    # Use degree centrality as final fallback
                    centrality_results['eigenvector'] = centrality_results.get('degree', {})
        
        if 'pagerank' in centrality_types:
            try:
                pagerank_cent = nx.pagerank(G, weight='weight')
                centrality_results['pagerank'] = {
                    id_to_label[node]: round(score, 4) for node, score in pagerank_cent.items()
                }
            except:
                pagerank_cent = nx.pagerank(G)
                centrality_results['pagerank'] = {
                    id_to_label[node]: round(score, 4) for node, score in pagerank_cent.items()
                }
        
        # Find overall most important nodes (average across all measures)
        if centrality_results:
            # Calculate composite score
            all_nodes = set()
            for measure_scores in centrality_results.values():
                all_nodes.update(measure_scores.keys())
            
            composite_scores = {}
            for node in all_nodes:
                scores = [measure_scores.get(node, 0) for measure_scores in centrality_results.values()]
                composite_scores[node] = round(sum(scores) / len(scores), 4)
            
            # Find top nodes
            top_node_list = sorted(composite_scores.items(), key=lambda x: x[1], reverse=True)[:top_nodes]
            top_node_names = [node for node, score in top_node_list]
        else:
            composite_scores = {}
            top_node_names = []
        
        # Calculate execution time
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds() * 1000
        
        # Build results with visualizations
        visualizations = []
        
        # Add node sizing based on composite scores
        if composite_scores:
            visualizations.append({
                "type": "node_size",
                "data_source": "composite_centrality",
                "title": "Node Importance (Composite Score)",
                "min_size": 10,
                "max_size": 35
            })
        
        # Add highlighting for top nodes
        if top_node_names:
            visualizations.append({
                "type": "node_highlight",
                "nodes": top_node_names,
                "color": "#ff6b6b",
                "title": f"Top {len(top_node_names)} Most Central Nodes"
            })
        
        results = {
            "metadata": {
                "analysis_id": "node-centrality",
                "analysis_name": "Node Centrality Analysis",
                "timestamp": start_time.isoformat(),
                "parameters_used": parameters,
                "execution_time_ms": round(execution_time, 2),
                "graph_stats": {
                    "nodes": len(nodes),
                    "edges": len(edges),
                    "is_directed": nx.is_directed(G),
                    "is_connected": nx.is_connected(G) if not nx.is_directed(G) else nx.is_weakly_connected(G)
                }
            },
            "results": {
                "primary": {
                    "composite_centrality": composite_scores,
                    "top_nodes": dict(top_node_list)
                },
                "secondary": centrality_results,
                "visualizations": visualizations
            }
        }
        
        # Generate summary
        summary_parts = []
        if centrality_results:
            summary_parts.append(f"Calculated {len(centrality_types)} centrality measure(s)")
            if top_node_names:
                summary_parts.append(f"Most central node: {top_node_names[0]}")
                summary_parts.append(f"Top {len(top_node_names)} nodes highlighted")
        
        results["summary"] = ". ".join(summary_parts) + "." if summary_parts else "Centrality analysis completed."
        
        return results
        
    except Exception as e:
        raise AnalysisError(f"Node centrality analysis failed: {str(e)}")