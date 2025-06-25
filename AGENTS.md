# AGENTS.md

## Overview

This project is a professional Electron-based causal graph editor and analysis tool (v2.0). Features include:
- **Unified Interface**: Single-page application with real-time editor-analysis integration
- **Context Menu System**: Professional right-click interface for all graph operations  
- **Plugin Architecture**: Extensible Python-based analysis via Pyodide/NetworkX
- **State Management**: Event-driven coordination between all components

## Key Modules (v2.0 Architecture)

### `src/unified-interface.html`
- **Main Application Interface**: Replaces old iframe-based system
- **Graph Editor**: Uses `vis-network` with context menu operations
- **Analysis Panel**: Real-time display of plugin results
- **Modal System**: Professional dialogs for node/edge editing
- **User Operations**:
  - Right-click canvas to add nodes
  - Right-click nodes for edit/delete
  - Drag between nodes to create edges
  - Right-click edges for edit/delete
  - Automatic analysis on graph changes

### `src/shared-state.js`
- **Core State Management**: EventTarget-based coordination system
- **Graph Operations**: Comprehensive node/edge management with validation
- **Plugin Integration**: Manages plugin selection and execution
- **Network Coordination**: Controls multiple vis-network instances
- **Key Functions**:
  - `addNode()`, `addEdge()`, `deleteNode()`, `deleteEdge()`
  - `importGraph()`, `exportGraph()`
  - `setPlugin()`, `registerNetwork()`
  - Event dispatching for UI updates

### `main.js` (Electron Main Process)
- **Menu System**: File/View/Tools menus with keyboard shortcuts
- **IPC Handlers**: Native file dialogs and system integration
- **Plugin Directory**: Automatic user plugin folder setup
- **Window Management**: Professional window creation and focus handling

### `py/plugin_loader.py`
- **Plugin Discovery**: Automatic scanning of plugin directories
- **Plugin Loading**: Dynamic import and validation of plugins
- **Error Handling**: Graceful fallbacks for plugin failures

### `py/plugins/` (Plugin System)
- **User-Serviceable Directory**: Located in app data folder
- **Plugin Structure**: `__init__.py` + `analysis.py` + `README.md`
- **Example Plugin**: `causal-paths` with advanced NetworkX analysis
- **Development Framework**: Complete plugin development guide in `PLUGIN.md`

### `lib/graphUtils.js` (Legacy)
- **Compatibility Layer**: Maintained for backward compatibility
- **Pure Functions**: Graph operations without state management
- **Test Coverage**: Maintained test suite (22 tests passing)

## Test Coverage (v2.0)

### Primary Test Suite: `__tests__/shared-state.test.js`
- **21 comprehensive tests** for v2.0 architecture
- **Coverage Areas**:
  - Node/Edge Management with validation
  - Graph Import/Export with error handling
  - Event System for UI coordination
  - Plugin System integration
  - State consistency and complex operations

### Legacy Test Suite: `__tests__/graphUtils.test.js`  
- **22 tests** for backward compatibility
- **Pure function testing** of graph operations

### Test Execution
- `npm test` - Run full test suite (43 tests)
- Jest configuration with Node.js compatibility mocking

## Agent Tasks Allowed

### Documentation & Testing
- Update project documentation (`README.md`, `CLAUDE.md`, `AGENTS.md`)
- Create/enhance test coverage for new features
- Update plugin development documentation
- Maintain changelog and roadmap documentation

### Feature Development
- **Plugin Development**: Create new analysis plugins following `PLUGIN.md`
- **State Management**: Enhance `src/shared-state.js` functionality
- **UI Improvements**: Modify `src/unified-interface.html` for UX enhancements
- **Analysis Features**: Extend Python analysis capabilities with NetworkX

### Architecture Enhancements
- **Performance Optimization**: Improve large graph handling
- **Export Formats**: Add support for GraphML, DOT, CSV export (roadmap v2.1)
- **Import Capabilities**: Multi-format import system (roadmap v3.0)
- **Plugin System**: Enhanced plugin discovery and management

## Agent Constraints

### Core Stability
- **Maintain v2.0 Architecture**: Don't revert to iframe-based system
- **Preserve Plugin System**: Maintain user-serviceable plugin directory structure
- **Keep Context Menu UX**: Don't restore button-based interface without explicit request
- **JSON Format Compatibility**: Maintain GRAPH_SPEC.md compliance

### Development Guidelines
- **Test Coverage**: Always run tests before major changes (`npm test`)
- **Event System**: Use shared state management for component coordination
- **Plugin Standards**: Follow established plugin development framework
- **Documentation**: Keep technical documentation current with code changes

### Modification Priorities
1. **High Impact, Low Risk**: Plugin development, documentation, test coverage
2. **Medium Impact**: UI enhancements, export features, performance optimization  
3. **High Risk**: Core architecture changes, state management modifications
4. **Roadmap Items**: Multi-format import (v3.0), flexible schema (v3.0)

## Current Development Status

- ✅ **v2.0 Complete**: Unified interface, plugin system, comprehensive documentation
- ✅ **Test Suite**: Full coverage for v2.0 architecture (43 tests passing)
- 🚧 **Active**: Documentation maintenance and test suite refinement
- 📋 **Next**: Phase 1 roadmap items (advanced visualization, export formats)