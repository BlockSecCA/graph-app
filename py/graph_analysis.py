import networkx as nx


def analyze_graph(nodes, edges):
    """Analyze directed graph and return influence scores and paths.

    Parameters
    ----------
    nodes : list of dict
        Each node dict should contain an 'id' and optionally 'label', 'type', and 'group'.
    edges : list of dict
        Each edge dict should contain 'source', 'target', and optionally 'type' and 'weight'.

    Returns
    -------
    dict
        Dictionary with keys 'influence_scores', 'positive_paths', 'negative_paths'.
    """
    G = nx.DiGraph()
    for node in nodes:
        G.add_node(
            node['id'],
            label=node.get('label', node['id']),
            type=node.get('type', ''),
            group=node.get('group', '')
        )

    for edge in edges:
        weight = edge.get('weight', 1)
        if edge.get('type') == '-':
            weight = -weight
        G.add_edge(edge['source'], edge['target'], weight=weight)

    id_to_label = {n['id']: n.get('label', n['id']) for n in nodes}

    influence_scores = {
        id_to_label[node]: sum(data['weight'] for _, node, data in G.in_edges(node, data=True))
        for node in G.nodes
    }

    positive_paths = []
    negative_paths = []
    if nodes:
        source = nodes[0]['id']
        target = nodes[-1]['id']
        for path in nx.all_simple_paths(G, source=source, target=target):
            if all(G[u][v]['weight'] > 0 for u, v in zip(path, path[1:])):
                positive_paths.append([id_to_label[n] for n in path])
            if all(G[u][v]['weight'] < 0 for u, v in zip(path, path[1:])):
                negative_paths.append([id_to_label[n] for n in path])

    return {
        'influence_scores': influence_scores,
        'positive_paths': positive_paths,
        'negative_paths': negative_paths
    }
