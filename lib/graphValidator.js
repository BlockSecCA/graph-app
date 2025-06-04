function validateGraph(graph) {
    const errors = [];
    const warnings = [];

    if (!graph || typeof graph !== 'object') {
        return { errors: ['Graph data must be an object'], warnings };
    }

    const nodes = Array.isArray(graph.nodes) ? graph.nodes : [];
    const edges = Array.isArray(graph.edges) ? graph.edges : [];

    const nodeIds = new Set();

    nodes.forEach((node, index) => {
        if (!node || typeof node !== 'object') {
            errors.push(`Node at index ${index} is invalid`);
            return;
        }
        if (!node.id) {
            errors.push(`Node at index ${index} missing id`);
            return;
        }
        if (nodeIds.has(node.id)) {
            errors.push(`Duplicate node id "${node.id}"`);
        } else {
            nodeIds.add(node.id);
        }
    });

    if (nodes.length < 2) {
        errors.push('Graph must contain at least 2 nodes');
    }
    if (edges.length < 1) {
        errors.push('Graph must contain at least 1 edge');
    }

    const validNodeIds = new Set(nodes.map(n => n.id));

    edges.forEach((edge, index) => {
        if (!edge || typeof edge !== 'object') {
            errors.push(`Edge at index ${index} is invalid`);
            return;
        }
        const { source, target } = edge;
        if (!source || !target) {
            errors.push(`Edge at index ${index} missing source or target`);
        } else {
            if (!validNodeIds.has(source) || !validNodeIds.has(target)) {
                errors.push(`Edge from ${source} to ${target} references missing node`);
            }
        }

        if (edge.weight === undefined) {
            warnings.push(`Edge from ${source} to ${target} missing weight; defaulting to 1`);
            edge.weight = 1;
        } else if (isNaN(edge.weight)) {
            errors.push(`Edge from ${source} to ${target} has non-numeric weight`);
        }

        if (edge.type === undefined) {
            warnings.push(`Edge from ${source} to ${target} missing type; defaulting to '+'`);
            edge.type = '+';
        }
    });

    return { errors, warnings };
}

module.exports = { validateGraph };
