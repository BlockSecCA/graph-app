function addNode(graph, id, label) {
    if (!id) throw new Error('id required');
    if (!label) label = id;
    graph.nodes.push({ id, label });
    return graph;
}

function addEdge(graph, source, target, type = '', weight = 1) {
    if (!source || !target) throw new Error('source and target required');
    if (isNaN(weight)) weight = 1;
    graph.edges.push({ source, target, type, weight });
    return graph;
}

function deleteNode(graph, nodeId) {
    if (!nodeId) throw new Error('nodeId required');
    graph.nodes = graph.nodes.filter(n => n.id !== nodeId);
    graph.edges = graph.edges.filter(e => e.source !== nodeId && e.target !== nodeId);
    return graph;
}

function deleteEdge(graph, source, target) {
    if (!source || !target) throw new Error('source and target required');
    graph.edges = graph.edges.filter(e => e.source !== source || e.target !== target);
    return graph;
}

function saveGraph(graph) {
    return JSON.stringify(graph, null, 2);
}

function loadGraph(jsonStr) {
    const data = JSON.parse(jsonStr);
    return {
        nodes: data.nodes || [],
        edges: data.edges || []
    };
}

module.exports = {
    addNode,
    addEdge,
    deleteNode,
    deleteEdge,
    saveGraph,
    loadGraph
};
