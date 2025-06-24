# CLAUDE.md - Project Context & Progress

## Project Overview
**graph-app** - Electron-based causal graph editor and analysis tool
- **Repository**: https://github.com/BlockSecCA/graph-app
- **Tech Stack**: Electron v25.0.0, Node.js v20.19.2, vis-network, Pyodide
- **Purpose**: Simple interface for editing graphs and running basic causal analysis

## Current Architecture
```
main.js (Electron main process)
├── index.html (Bootstrap tabs container)
    ├── graph_editor_new.html (iframe - vis-network editor)
    └── analysis_tool.html (iframe - Pyodide Python analysis)
```

## Key Limitations Identified
1. **Isolation**: Editor and analysis run in separate iframes with no communication
2. **Hardcoded Schema**: Rigid graph structure enforced in GRAPH_SPEC.md
   - Nodes: `{id, label, type?, group?}`
   - Edges: `{source, target, type?, weight?}`
3. **No Format Support**: Only reads its own JSON format
4. **Manual Workflow**: Editor saves → Analysis loads files manually

## Current State
- ✅ App works as basic graph editor
- ✅ Analysis tool functions with Pyodide
- ❌ No integration between components
- ❌ Limited to proprietary JSON format
- ❌ No versioning for releases

## Immediate Goals
1. **Versioning & Packaging**: Set up proper versioning for executable releases
2. **Release Preparation**: Ensure app can be packaged into executable
3. **Future**: Multi-format import capabilities (GraphML, DOT, CSV, etc.)

## Technical Notes
- Uses `lib/graphUtils.js` for graph operations (hardcoded schema)
- Python analysis in `py/test_pyodide.py` 
- Sample graphs in `graphs/` directory
- Tests in `__tests__/graphUtils.test.js`

## Package.json Scripts
- `npm start` - Launch Electron app
- `npm test` - Run Jest tests
- `npm run build` - Build process
- `npm run pack` - Package app

## Development Environment
- Node.js v20.19.2 (use nvm for version management)
- Electron v25.0.0

## Next Session Context
Working on versioning and release preparation before implementing multi-format import capabilities. User wants to keep the simple, lightweight editor but extend import capabilities to read graphs from other sources/formats.