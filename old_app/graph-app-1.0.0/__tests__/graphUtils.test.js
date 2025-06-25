const { addNode, addEdge, deleteNode, deleteEdge, saveGraph, loadGraph } = require('../lib/graphUtils');

describe('graphUtils', () => {
  let graph;
  beforeEach(() => {
    graph = { nodes: [], edges: [] };
  });

  test('addNode adds a node with default label', () => {
    addNode(graph, 'n1');
    expect(graph.nodes).toEqual([{ id: 'n1', label: 'n1' }]);
  });

  test('addEdge adds an edge with defaults', () => {
    addEdge(graph, 'n1', 'n2');
    expect(graph.edges).toEqual([{ source: 'n1', target: 'n2', type: '', weight: 1 }]);
  });

  test('addNode without id throws', () => {
    expect(() => addNode(graph)).toThrow();
  });

  test('addEdge defaults weight to 1 when NaN', () => {
    addEdge(graph, 'n1', 'n2', '', NaN);
    expect(graph.edges).toEqual([{ source: 'n1', target: 'n2', type: '', weight: 1 }]);
  });

  test('addEdge requires source and target', () => {
    expect(() => addEdge(graph, null, 'n2')).toThrow();
    expect(() => addEdge(graph, 'n1')).toThrow();
  });

  test('deleteNode removes node and connected edges', () => {
    addNode(graph, 'n1');
    addNode(graph, 'n2');
    addEdge(graph, 'n1', 'n2');
    deleteNode(graph, 'n1');
    expect(graph.nodes).toEqual([{ id: 'n2', label: 'n2' }]);
    expect(graph.edges).toEqual([]);
  });

  test('deleteNode ignores missing id', () => {
    addNode(graph, 'n1');
    const snapshot = JSON.parse(JSON.stringify(graph));
    deleteNode(graph, 'missing');
    expect(graph).toEqual(snapshot);
  });

  test('deleteEdge removes specific edge', () => {
    addEdge(graph, 'n1', 'n2');
    addEdge(graph, 'n1', 'n3');
    deleteEdge(graph, 'n1', 'n2');
    expect(graph.edges).toEqual([{ source: 'n1', target: 'n3', type: '', weight: 1 }]);
  });

  test('saveGraph serializes graph to JSON', () => {
    addNode(graph, 'n1');
    const json = saveGraph(graph);
    expect(JSON.parse(json)).toEqual({ nodes: [{ id: 'n1', label: 'n1' }], edges: [] });
  });

  test('saveGraph includes edges', () => {
    addNode(graph, 'n1');
    addNode(graph, 'n2');
    addEdge(graph, 'n1', 'n2', 'arrow', 2);
    const json = saveGraph(graph);
    expect(JSON.parse(json)).toEqual({
      nodes: [
        { id: 'n1', label: 'n1' },
        { id: 'n2', label: 'n2' }
      ],
      edges: [
        { source: 'n1', target: 'n2', type: 'arrow', weight: 2 }
      ]
    });
  });

  test('loadGraph parses JSON to graph object', () => {
    const jsonStr = '{"nodes":[{"id":"a"}],"edges":[]}';
    const data = loadGraph(jsonStr);
    expect(data).toEqual({ nodes: [{ id: 'a' }], edges: [] });
  });
});
