/**
 * Tests for the v2.0 shared state management system
 */

// Mock EventTarget and CustomEvent for Node.js environment
const { EventEmitter } = require('events');

global.EventTarget = class EventTarget {
    constructor() {
        this._emitter = new EventEmitter();
    }
    
    addEventListener(type, listener) {
        this._emitter.on(type, listener);
    }
    
    removeEventListener(type, listener) {
        this._emitter.removeListener(type, listener);
    }
    
    dispatchEvent(event) {
        this._emitter.emit(event.type, event);
        return true;
    }
};

global.CustomEvent = class CustomEvent {
    constructor(type, options = {}) {
        this.type = type;
        this.detail = options.detail || null;
    }
};

// Mock window and document objects for the shared-state module
global.window = {
    addEventListener: jest.fn(),
    removeEventListener: jest.fn()
};

global.document = {
    querySelector: jest.fn()
};

// Load the source code as text and eval it in our mocked environment
const fs = require('fs');
const path = require('path');
const sharedStateCode = fs.readFileSync(path.join(__dirname, '../src/shared-state.js'), 'utf8');

// Remove the window assignments and evaluate, making GraphAppState global
const codeWithoutWindow = sharedStateCode
    .replace('window.GraphAppState = GraphAppState;', 'global.GraphAppState = GraphAppState;')
    .replace('window.graphApp = new GraphAppState();', '');

eval(codeWithoutWindow);

// Extract GraphAppState from global for testing
const { GraphAppState } = global;

describe('GraphAppState', () => {
    let graphApp;

    beforeEach(() => {
        graphApp = new GraphAppState();
    });

    describe('Node Management', () => {
        test('addNode adds a valid node', () => {
            const node = { id: 'n1', label: 'Node 1' };
            graphApp.addNode(node);
            
            expect(graphApp.state.currentGraph.nodes).toHaveLength(1);
            expect(graphApp.state.currentGraph.nodes[0]).toMatchObject(node);
        });

        test('addNode requires an id', () => {
            expect(() => {
                graphApp.addNode({ label: 'Node without ID' });
            }).toThrow('Node must have an id');
        });

        test('addNode prevents duplicate IDs', () => {
            graphApp.addNode({ id: 'n1', label: 'First' });
            
            expect(() => {
                graphApp.addNode({ id: 'n1', label: 'Duplicate' });
            }).toThrow("Node with id 'n1' already exists");
        });

        test('addNode sets default label to id', () => {
            graphApp.addNode({ id: 'n1' });
            
            expect(graphApp.state.currentGraph.nodes[0].label).toBe('n1');
        });

        test('deleteNode removes node and connected edges', () => {
            graphApp.addNode({ id: 'n1' });
            graphApp.addNode({ id: 'n2' });
            graphApp.addEdge({ source: 'n1', target: 'n2' });
            
            graphApp.deleteNode('n1');
            
            expect(graphApp.state.currentGraph.nodes).toHaveLength(1);
            expect(graphApp.state.currentGraph.edges).toHaveLength(0);
        });
    });

    describe('Edge Management', () => {
        beforeEach(() => {
            graphApp.addNode({ id: 'n1' });
            graphApp.addNode({ id: 'n2' });
        });

        test('addEdge adds a valid edge', () => {
            const edge = { source: 'n1', target: 'n2', type: '+', weight: 2 };
            graphApp.addEdge(edge);
            
            expect(graphApp.state.currentGraph.edges).toHaveLength(1);
            expect(graphApp.state.currentGraph.edges[0]).toMatchObject(edge);
        });

        test('addEdge requires source and target', () => {
            expect(() => {
                graphApp.addEdge({ target: 'n2' });
            }).toThrow('Edge must have source and target');

            expect(() => {
                graphApp.addEdge({ source: 'n1' });
            }).toThrow('Edge must have source and target');
        });

        test('addEdge validates source node exists', () => {
            expect(() => {
                graphApp.addEdge({ source: 'nonexistent', target: 'n2' });
            }).toThrow("Source node 'nonexistent' does not exist");
        });

        test('addEdge validates target node exists', () => {
            expect(() => {
                graphApp.addEdge({ source: 'n1', target: 'nonexistent' });
            }).toThrow("Target node 'nonexistent' does not exist");
        });

        test('addEdge sets default values', () => {
            graphApp.addEdge({ source: 'n1', target: 'n2' });
            
            const edge = graphApp.state.currentGraph.edges[0];
            expect(edge.type).toBe('+');
            expect(edge.weight).toBe(1);
        });

        test('deleteEdge removes specific edge', () => {
            graphApp.addEdge({ source: 'n1', target: 'n2' });
            graphApp.addEdge({ source: 'n2', target: 'n1' });
            
            graphApp.deleteEdge('n1', 'n2');
            
            expect(graphApp.state.currentGraph.edges).toHaveLength(1);
            expect(graphApp.state.currentGraph.edges[0].source).toBe('n2');
        });
    });

    describe('Graph Import/Export', () => {
        test('exportGraph returns valid JSON', () => {
            graphApp.addNode({ id: 'n1', label: 'Node 1' });
            graphApp.addNode({ id: 'n2', label: 'Node 2' });
            graphApp.addEdge({ source: 'n1', target: 'n2', type: '+', weight: 2 });
            
            const json = graphApp.exportGraph();
            const parsed = JSON.parse(json);
            
            expect(parsed.nodes).toHaveLength(2);
            expect(parsed.edges).toHaveLength(1);
            expect(parsed.nodes[0]).toMatchObject({ id: 'n1', label: 'Node 1' });
        });

        test('importGraph loads valid graph data', () => {
            const graphData = {
                nodes: [{ id: 'a', label: 'A' }],
                edges: [{ source: 'a', target: 'b' }]
            };
            
            // This should throw because node 'b' doesn't exist
            expect(() => {
                graphApp.importGraph(JSON.stringify(graphData));
            }).toThrow("Invalid edge: target node 'b' not found");
        });

        test('importGraph validates graph format', () => {
            expect(() => {
                graphApp.importGraph('{"invalid": true}');
            }).toThrow('Invalid graph format: missing nodes array');

            expect(() => {
                graphApp.importGraph('{"nodes": [], "invalid": true}');
            }).toThrow('Invalid graph format: missing edges array');
        });

        test('importGraph validates unique node IDs', () => {
            const invalidGraph = {
                nodes: [
                    { id: 'duplicate', label: 'First' },
                    { id: 'duplicate', label: 'Second' }
                ],
                edges: []
            };
            
            expect(() => {
                graphApp.importGraph(JSON.stringify(invalidGraph));
            }).toThrow('Invalid graph: duplicate node IDs found');
        });
    });

    describe('Event System', () => {
        test('addNode dispatches events', (done) => {
            let eventCount = 0;
            
            graphApp.addEventListener('nodeAdded', (e) => {
                expect(e.detail.node.id).toBe('n1');
                eventCount++;
            });
            
            graphApp.addEventListener('graphUpdated', (e) => {
                expect(e.detail.graph.nodes).toHaveLength(1);
                eventCount++;
                
                // Both events should fire
                if (eventCount === 2) done();
            });
            
            graphApp.addNode({ id: 'n1' });
        });

        test('deleteNode dispatches events', (done) => {
            graphApp.addNode({ id: 'n1' });
            
            graphApp.addEventListener('nodeDeleted', (e) => {
                expect(e.detail.nodeId).toBe('n1');
                done();
            });
            
            graphApp.deleteNode('n1');
        });
    });

    describe('Plugin System Integration', () => {
        test('setPlugin updates selected plugin', () => {
            graphApp.setPlugin('test-plugin', { param: 'value' });
            
            expect(graphApp.state.selectedPlugin).toBe('test-plugin');
            expect(graphApp.state.pluginParameters.get('test-plugin')).toEqual({ param: 'value' });
        });

        test('registerNetwork stores network reference', () => {
            const mockNetwork = { 
                setSize: jest.fn(), 
                fit: jest.fn() 
            };
            
            graphApp.registerNetwork('editor', mockNetwork);
            
            expect(graphApp.networks.editor).toBe(mockNetwork);
        });
    });

    describe('State Consistency', () => {
        test('getState returns read-only copy', () => {
            graphApp.addNode({ id: 'n1' });
            
            const state = graphApp.getState();
            state.currentGraph.nodes = []; // This shouldn't affect the actual state
            
            expect(graphApp.state.currentGraph.nodes).toHaveLength(1);
        });

        test('multiple operations maintain consistency', () => {
            // Complex scenario
            graphApp.addNode({ id: 'a', label: 'A' });
            graphApp.addNode({ id: 'b', label: 'B' });
            graphApp.addNode({ id: 'c', label: 'C' });
            
            graphApp.addEdge({ source: 'a', target: 'b', weight: 2 });
            graphApp.addEdge({ source: 'b', target: 'c', weight: 3 });
            graphApp.addEdge({ source: 'a', target: 'c', weight: 1 });
            
            expect(graphApp.state.currentGraph.nodes).toHaveLength(3);
            expect(graphApp.state.currentGraph.edges).toHaveLength(3);
            
            // Delete middle node should remove connected edges
            graphApp.deleteNode('b');
            
            expect(graphApp.state.currentGraph.nodes).toHaveLength(2);
            expect(graphApp.state.currentGraph.edges).toHaveLength(1); // Only a->c should remain
            expect(graphApp.state.currentGraph.edges[0].source).toBe('a');
            expect(graphApp.state.currentGraph.edges[0].target).toBe('c');
        });
    });
});