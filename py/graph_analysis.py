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
    try:
        G = nx.DiGraph()
        for node in nodes:
            node_id = node.get('id')
            if node_id is None:
                raise ValueError("Node missing 'id'")
            G.add_node(
                node_id,
                label=node.get('label', node_id),
                type=node.get('type', ''),
                group=node.get('group', '')
            )

        node_ids = set(G.nodes())
        for edge in edges:
            src = edge.get('source')
            tgt = edge.get('target')
            if src is None or tgt is None:
                raise ValueError("Edge missing 'source' or 'target'")
            if src not in node_ids or tgt not in node_ids:
                raise ValueError("Edge references missing node")
            weight = edge.get('weight', 1)
            if edge.get('type') == '-':
                weight = -weight
            G.add_edge(src, tgt, weight=weight)

        id_to_label = {n['id']: n.get('label', n['id']) for n in nodes if n.get('id') is not None}

        influence_scores = {
            id_to_label.get(node, node): sum(data['weight'] for _, node, data in G.in_edges(node, data=True))
            for node in G.nodes
        }

        positive_paths = []
        negative_paths = []
        if len(nodes) >= 2:
            source = nodes[0].get('id')
            target = nodes[-1].get('id')
            try:
                if source is not None and target is not None and nx.has_path(G, source, target):
                    all_weights = [d['weight'] for _, _, d in G.edges(data=True)]
                    if all_weights and max(all_weights) > 0:
                        cutoff = len(G.nodes())
                        try:
                            for path in nx.all_simple_paths(G, source=source, target=target, cutoff=cutoff):
                                if all(G[u][v]['weight'] > 0 for u, v in zip(path, path[1:])):
                                    positive_paths.append([id_to_label.get(n, n) for n in path])
                                if all(G[u][v]['weight'] < 0 for u, v in zip(path, path[1:])):
                                    negative_paths.append([id_to_label.get(n, n) for n in path])
                        except Exception as e:
                            raise e
            except Exception as e:
                raise e

        return {
            'influence_scores': influence_scores,
            'positive_paths': positive_paths,
            'negative_paths': negative_paths,
            'error': ''
        }

    except Exception as e:
        return {
            'influence_scores': {},
            'positive_paths': [],
            'negative_paths': [],
            'error': str(e)
        }
