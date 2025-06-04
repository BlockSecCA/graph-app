const { validateGraph } = require('../lib/graphValidator');

describe('validateGraph', () => {
  test('catches missing node id', () => {
    const graph = { nodes: [{ label: 'A' }], edges: [] };
    const result = validateGraph(graph);
    expect(result.errors.some(e => e.includes('missing id'))).toBe(true);
  });

  test('catches duplicate node ids', () => {
    const graph = { nodes: [{ id: 'a' }, { id: 'a' }], edges: [] };
    const result = validateGraph(graph);
    expect(result.errors).toContain('Duplicate node id "a"');
  });

  test('catches invalid edge references', () => {
    const graph = { nodes: [{ id: 'a' }, { id: 'b' }], edges: [{ source: 'a', target: 'c' }] };
    const result = validateGraph(graph);
    expect(result.errors.some(e => e.includes('references missing node'))).toBe(true);
  });

  test('warns about missing weight defaults', () => {
    const graph = { nodes: [{ id: 'a' }, { id: 'b' }], edges: [{ source: 'a', target: 'b' }] };
    const result = validateGraph(graph);
    expect(result.warnings.some(w => w.includes('missing weight'))).toBe(true);
    expect(graph.edges[0].weight).toBe(1);
  });

  test('catches insufficient node or edge counts', () => {
    const graph = { nodes: [{ id: 'a' }], edges: [] };
    const result = validateGraph(graph);
    expect(result.errors.some(e => e.includes('at least'))).toBe(true);
  });
});
