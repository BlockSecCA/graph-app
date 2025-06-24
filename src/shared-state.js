/**
 * Shared State Management System
 * Handles graph data, analysis results, and UI coordination
 */

class GraphAppState extends EventTarget {
    constructor() {
        super();
        
        // Core application state
        this.state = {
            // Graph data (compatible with GRAPH_SPEC.md)
            currentGraph: {
                nodes: [],
                edges: []
            },
            
            // Analysis state
            selectedPlugin: 'causal-paths',
            analysisResults: null,
            isAnalyzing: false,
            
            // UI state
            activeMode: 'editor', // 'editor' | 'analysis' | 'split'
            containerSizes: {
                editor: { width: 400, height: 300 },
                analysis: { width: 400, height: 300 }
            },
            
            // Plugin system
            availablePlugins: new Map(),
            pluginParameters: new Map()
        };
        
        // Network instances for coordination
        this.networks = {
            editor: null,
            analysis: null
        };
        
        // Resize management
        this.resizeState = {
            isResizing: false,
            activeContainer: null,
            startPos: { x: 0, y: 0 },
            startSize: { width: 0, height: 0 }
        };
        
        this.initializeEventHandlers();
    }
    
    /**
     * Update graph data and notify all subscribers
     */
    updateGraph(graphData) {
        this.state.currentGraph = {
            nodes: [...graphData.nodes],
            edges: [...graphData.edges]
        };
        
        this.dispatchEvent(new CustomEvent('graphUpdated', {
            detail: { graph: this.state.currentGraph }
        }));
        
        // Auto-trigger analysis if enabled
        this.triggerAnalysis();
    }
    
    /**
     * Add a single node and update state
     */
    addNode(node) {
        // Validate node format per GRAPH_SPEC.md
        if (!node.id) {
            throw new Error('Node must have an id');
        }
        
        // Check for duplicate IDs
        const exists = this.state.currentGraph.nodes.find(n => n.id === node.id);
        if (exists) {
            throw new Error(`Node with id '${node.id}' already exists`);
        }
        
        this.state.currentGraph.nodes.push({
            id: node.id,
            label: node.label || node.id,
            type: node.type || '',
            group: node.group || '',
            ...node
        });
        
        this.dispatchEvent(new CustomEvent('nodeAdded', {
            detail: { node, graph: this.state.currentGraph }
        }));
        
        this.triggerAnalysis();
    }
    
    /**
     * Add a single edge and update state
     */
    addEdge(edge) {
        // Validate edge format per GRAPH_SPEC.md
        if (!edge.source || !edge.target) {
            throw new Error('Edge must have source and target');
        }
        
        // Validate source and target nodes exist
        const sourceExists = this.state.currentGraph.nodes.find(n => n.id === edge.source);
        const targetExists = this.state.currentGraph.nodes.find(n => n.id === edge.target);
        
        if (!sourceExists) {
            throw new Error(`Source node '${edge.source}' does not exist`);
        }
        if (!targetExists) {
            throw new Error(`Target node '${edge.target}' does not exist`);
        }
        
        this.state.currentGraph.edges.push({
            source: edge.source,
            target: edge.target,
            type: edge.type || '+',
            weight: edge.weight || 1,
            ...edge
        });
        
        this.dispatchEvent(new CustomEvent('edgeAdded', {
            detail: { edge, graph: this.state.currentGraph }
        }));
        
        this.triggerAnalysis();
    }
    
    /**
     * Delete a node and all connected edges
     */
    deleteNode(nodeId) {
        this.state.currentGraph.nodes = this.state.currentGraph.nodes.filter(n => n.id !== nodeId);
        this.state.currentGraph.edges = this.state.currentGraph.edges.filter(
            e => e.source !== nodeId && e.target !== nodeId
        );
        
        this.dispatchEvent(new CustomEvent('nodeDeleted', {
            detail: { nodeId, graph: this.state.currentGraph }
        }));
        
        this.triggerAnalysis();
    }
    
    /**
     * Delete a specific edge
     */
    deleteEdge(source, target) {
        this.state.currentGraph.edges = this.state.currentGraph.edges.filter(
            e => !(e.source === source && e.target === target)
        );
        
        this.dispatchEvent(new CustomEvent('edgeDeleted', {
            detail: { source, target, graph: this.state.currentGraph }
        }));
        
        this.triggerAnalysis();
    }
    
    /**
     * Register a vis-network instance for coordination
     */
    registerNetwork(type, network) {
        this.networks[type] = network;
        
        // Apply current container size if available
        if (this.state.containerSizes[type]) {
            const size = this.state.containerSizes[type];
            network.setSize(`${size.width}px`, `${size.height}px`);
        }
    }
    
    /**
     * Update container size and coordinate network instances
     */
    updateContainerSize(type, width, height) {
        // Enforce minimum size constraints
        const minWidth = 150;
        const minHeight = 150;
        
        width = Math.max(width, minWidth);
        height = Math.max(height, minHeight);
        
        // Update state
        this.state.containerSizes[type] = { width, height };
        
        // Update network if registered
        if (this.networks[type]) {
            this.networks[type].setSize(`${width}px`, `${height}px`);
            this.networks[type].fit();
        }
        
        this.dispatchEvent(new CustomEvent('containerResized', {
            detail: { type, width, height }
        }));
    }
    
    /**
     * Initialize resize handling for containers
     */
    initializeResizer(containerElement, resizerElement, type) {
        const self = this;
        
        resizerElement.addEventListener('mousedown', function(e) {
            self.resizeState.isResizing = true;
            self.resizeState.activeContainer = type;
            self.resizeState.startPos = { x: e.clientX, y: e.clientY };
            
            const rect = containerElement.getBoundingClientRect();
            self.resizeState.startSize = { 
                width: rect.width, 
                height: rect.height 
            };
            
            // Add global event listeners
            window.addEventListener('mousemove', self.handleResize.bind(self));
            window.addEventListener('mouseup', self.stopResize.bind(self));
            
            e.preventDefault();
        });
    }
    
    /**
     * Handle resize drag events
     */
    handleResize(e) {
        if (!this.resizeState.isResizing) return;
        
        const type = this.resizeState.activeContainer;
        const container = document.querySelector(`[data-container-type="${type}"]`);
        
        if (!container) return;
        
        const deltaX = e.clientX - this.resizeState.startPos.x;
        const deltaY = e.clientY - this.resizeState.startPos.y;
        
        const newWidth = this.resizeState.startSize.width + deltaX;
        const newHeight = this.resizeState.startSize.height + deltaY;
        
        // Update container and network
        container.style.width = `${newWidth}px`;
        container.style.height = `${newHeight}px`;
        
        this.updateContainerSize(type, newWidth, newHeight);
    }
    
    /**
     * Stop resize operation
     */
    stopResize() {
        this.resizeState.isResizing = false;
        this.resizeState.activeContainer = null;
        
        // Remove global event listeners
        window.removeEventListener('mousemove', this.handleResize.bind(this));
        window.removeEventListener('mouseup', this.stopResize.bind(this));
    }
    
    /**
     * Set active analysis plugin
     */
    setPlugin(pluginId, parameters = {}) {
        this.state.selectedPlugin = pluginId;
        this.state.pluginParameters.set(pluginId, parameters);
        
        this.dispatchEvent(new CustomEvent('pluginChanged', {
            detail: { pluginId, parameters }
        }));
        
        this.triggerAnalysis();
    }
    
    /**
     * Trigger analysis with current plugin (debounced)
     */
    triggerAnalysis() {
        // Clear existing timeout
        if (this.analysisTimeout) {
            clearTimeout(this.analysisTimeout);
        }
        
        // Debounce analysis calls (300ms delay)
        this.analysisTimeout = setTimeout(() => {
            this.runAnalysis();
        }, 300);
    }
    
    /**
     * Run analysis with current graph and plugin
     */
    async runAnalysis() {
        if (this.state.currentGraph.nodes.length === 0) {
            return; // No graph to analyze
        }
        
        this.state.isAnalyzing = true;
        this.dispatchEvent(new CustomEvent('analysisStarted'));
        
        try {
            const plugin = this.state.availablePlugins.get(this.state.selectedPlugin);
            if (!plugin) {
                throw new Error(`Plugin '${this.state.selectedPlugin}' not found`);
            }
            
            const parameters = this.state.pluginParameters.get(this.state.selectedPlugin) || {};
            
            // Run analysis (this will be implemented when we add plugin system)
            const results = await plugin.analyze(this.state.currentGraph, parameters);
            
            this.state.analysisResults = results;
            this.state.isAnalyzing = false;
            
            this.dispatchEvent(new CustomEvent('analysisCompleted', {
                detail: { results }
            }));
            
        } catch (error) {
            this.state.isAnalyzing = false;
            this.dispatchEvent(new CustomEvent('analysisError', {
                detail: { error: error.message }
            }));
        }
    }
    
    /**
     * Export current graph as JSON
     */
    exportGraph() {
        return JSON.stringify(this.state.currentGraph, null, 2);
    }
    
    /**
     * Import graph from JSON
     */
    importGraph(jsonString) {
        try {
            const graphData = JSON.parse(jsonString);
            
            // Validate format per GRAPH_SPEC.md
            if (!graphData.nodes || !Array.isArray(graphData.nodes)) {
                throw new Error('Invalid graph format: missing nodes array');
            }
            if (!graphData.edges || !Array.isArray(graphData.edges)) {
                throw new Error('Invalid graph format: missing edges array');
            }
            
            // Validate node IDs are unique
            const nodeIds = graphData.nodes.map(n => n.id);
            const uniqueIds = new Set(nodeIds);
            if (nodeIds.length !== uniqueIds.size) {
                throw new Error('Invalid graph: duplicate node IDs found');
            }
            
            // Validate edge references
            for (const edge of graphData.edges) {
                if (!nodeIds.includes(edge.source)) {
                    throw new Error(`Invalid edge: source node '${edge.source}' not found`);
                }
                if (!nodeIds.includes(edge.target)) {
                    throw new Error(`Invalid edge: target node '${edge.target}' not found`);
                }
            }
            
            this.updateGraph(graphData);
            
        } catch (error) {
            throw new Error(`Failed to import graph: ${error.message}`);
        }
    }
    
    /**
     * Initialize event handlers for cleanup
     */
    initializeEventHandlers() {
        // Cleanup resize state if window loses focus
        window.addEventListener('blur', () => {
            if (this.resizeState.isResizing) {
                this.stopResize();
            }
        });
    }
    
    /**
     * Get current state (read-only)
     */
    getState() {
        return JSON.parse(JSON.stringify(this.state));
    }
}

// Export for use in modules
window.GraphAppState = GraphAppState;

// Create global instance
window.graphApp = new GraphAppState();