import js # Import the js module to access JavaScript variables
import networkx as nx

# Convert JavaScript data to Python-native format
nodes = js.GraphData.nodes.to_py()  # Convert nodes to Python
edges = js.GraphData.edges.to_py()  # Convert edges to Python

# Print the fully converted data
print("Converted nodes:", nodes)
print("Converted edges:", edges)

# Initialize directed graph
G = nx.DiGraph()

# Add nodes to the graph
for node in nodes:
    G.add_node(node['id'], label=node['label'], type=node['type'], group=node['group'])

# Add edges with weights and types (positive/negative influences)
for edge in edges:
    weight = edge.get('weight', 1)
    if edge.get('type') == '-':
        weight = -weight  # Indicate negative influence
    G.add_edge(edge['source'], edge['target'], weight=weight)

# Calculate influence scores (sum of incoming edge weights for each node)
influence_scores = {node: sum(data['weight'] for _, node, data in G.in_edges(node, data=True)) for node in G.nodes}

# Find paths that only use positive or only negative edges
positive_paths = [path for path in nx.all_simple_paths(G, source=nodes[0]['id'], target=nodes[-1]['id'])
                  if all(G[u][v]['weight'] > 0 for u, v in zip(path, path[1:]))]
negative_paths = [path for path in nx.all_simple_paths(G, source=nodes[0]['id'], target=nodes[-1]['id'])
                  if all(G[u][v]['weight'] < 0 for u, v in zip(path, path[1:]))]

# Prepare result
result = {
    "influence_scores": influence_scores,
    "positive_paths": positive_paths,
    "negative_paths": negative_paths
}
result  # Return result for JavaScript