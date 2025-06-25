# CLAUDE.md - Project Context & Progress

## Project Overview
**graph-app** - Professional Electron-based causal graph editor and analysis tool
- **Repository**: https://github.com/BlockSecCA/graph-app
- **Version**: 2.1.3 (Restored default vis-network navigation behavior)
- **Tech Stack**: Electron v25.0.0, Node.js v20.19.2, vis-network, Pyodide, NetworkX
- **Purpose**: Modern unified interface for graph editing with extensible Python-based analysis

## Current Architecture (v2.0)
```
main.js (Electron main process)
├── File/View/Tools menu system with IPC handlers
└── src/unified-interface.html (Single-page unified interface)
    ├── Graph Editor (vis-network with context menus)
    ├── Analysis Panel (real-time results display)
    ├── Plugin System (Python/Pyodide integration)
    └── Shared State Management (src/shared-state.js)
```

## Major v2.0 Improvements ✅
1. **Unified Interface**: Eliminated iframe isolation, single-page design
2. **Real-time Integration**: Editor and analysis work together automatically  
3. **Context Menu System**: Professional right-click interface (no more buttons)
4. **Plugin Architecture**: Extensible Python-based analysis with NetworkX
5. **Shared State Management**: Event-driven coordination between components
6. **Enhanced Physics**: Interactive node positioning without graph constraints
7. **User Plugin Directory**: User-serviceable plugin system in app data folder
8. **Proper Versioning**: Semantic versioning and comprehensive release management

## Current State (v2.1)
- ✅ Unified interface with real-time editor-analysis integration
- ✅ Professional context menu-based workflow
- ✅ Extensible plugin system with Python/NetworkX
- ✅ **Advanced visualization preferences** (node sizing, arrow scaling, layout control)
- ✅ **Persistent user preferences** (localStorage-based)
- ✅ **Real-time visualization updates** (automatic preference application)
- ✅ Comprehensive documentation and release management
- ✅ Full test coverage for new architecture
- ❌ Still limited to proprietary JSON format (roadmap: v3.0)
- ❌ Fixed schema system (roadmap: v3.0)

## Next Priorities (Post v2.1)
1. **Phase 1 (v2.1)**: ✅ Advanced visualization options **COMPLETE**
2. **Phase 2 (v2.2)**: Export formats and performance optimization
3. **Phase 3 (v2.3)**: Expanded plugin ecosystem and community features
4. **Phase 4 (v3.0)**: Multi-format import and flexible schema system

## Technical Architecture Notes

### Core Files
- **src/unified-interface.html**: Main application interface
- **src/shared-state.js**: State management and event coordination
- **main.js**: Electron main process with menu system and IPC
- **py/plugin_loader.py**: Plugin discovery and loading system
- **py/plugins/**: User-serviceable plugin directory structure

### Plugin System
- **Discovery**: Automatic plugin scanning on startup
- **Integration**: Python/Pyodide with full NetworkX support
- **User Directory**: Cross-platform app data folder for user plugins
- **Development**: Complete plugin development framework and documentation

### State Management
- **Event-Driven**: EventTarget-based communication
- **Real-time Updates**: Automatic analysis on graph changes
- **Network Coordination**: Unified control of vis-network instances
- **Validation**: Comprehensive input validation per GRAPH_SPEC.md

### Testing
- **New Tests**: Comprehensive test suite for v2.0 architecture (21 tests)
- **Legacy Tests**: Maintained compatibility tests for graphUtils (22 tests)
- **Coverage**: Node/edge management, import/export, events, plugin system
- **Command**: `npm test` runs full test suite (43 tests passing)

## Package.json Scripts
- `npm start` - Launch Electron app
- `npm test` - Run Jest tests (43 tests for v2.0 + legacy)
- `npm run build` - Build process
- `npm run pack` - Package app for distribution
- `npm run lint` - Code linting (check if available)
- `npm run typecheck` - Type checking (check if available)

## Development Environment
- Node.js v20.19.2 (use nvm for version management)
- Electron v25.0.0
- Jest for testing
- NetworkX integration via Pyodide

## Current Session Context
**Plugin System Breakthrough**: Resolved critical Pyodide vs Electron `require()` conflict that was preventing plugin loading. Implemented revolutionary fetch-based plugin system that loads Python analysis code via HTTP, bypassing filesystem isolation. All 7 plugins now fully functional with NetworkX, SciPy, and NumPy support. Key achievements:

- ✅ **Plugin Loading**: Fetch-based system loads all 7 plugins without IPC dependency
- ✅ **File Operations**: Toolbar buttons replace non-functional menu items (require() conflict)
- ✅ **Unicode Support**: Base64 encoding handles any Unicode characters in plugin code
- ✅ **Scientific Stack**: Full Pyodide integration with NetworkX, SciPy, NumPy packages
- ✅ **Error Handling**: Comprehensive debugging and graceful fallbacks
- ✅ **Template System**: Plugin development template remains clean and user-friendly

**Status**: 🎉 **v2.1.3 COMPLETE** - Graph navigation fully restored by reverting to vis-network defaults. Analysis of old working app revealed that explicit interaction configuration was interfering with built-in zoom/pan behavior. Navigation now works identically to original v1.0 app. Visualization preferences system remains fully functional. Addresses GitHub issues #39, #40, and #41 completely.

## v2.1.0 New Features ✅
- ✅ **Visualization Preferences Panel**: Collapsible UI in graph editor header
- ✅ **Node Size Control**: Manual sizing (8-32px) with auto-size based on connections
- ✅ **Arrow Scale Control**: Adjustable arrow sizes (0.5-2.5x) with value-based scaling
- ✅ **Physics Layout Control**: Tight/Normal/Loose presets with custom spring length
- ✅ **Persistent Preferences**: localStorage-based settings that survive app restarts
- ✅ **Real-time Updates**: Automatic preference application on graph changes
- ✅ **Backward Compatibility**: Defaults match previous v2.0.x behavior

## v2.1.1 Bug Fixes & Enhancements ✅
- ✅ **Fixed Slider Bugs**: Node size and arrow scale sliders now work after toggling auto-modes
- ✅ **Reset to Defaults**: Red button to restore original v2.0 settings instantly
- ✅ **Unified Arrow Scaling**: Head and body now scale together as single element
- ✅ **Skinny Arrow Option**: Checkbox for thinner arrow style override
- ✅ **Robust State Management**: Proper individual property resets when switching modes

## v2.1.2 Navigation & Interaction Fixes ✅
- ✅ **Scroll Wheel Zoom**: Restored full zoom functionality with mouse wheel
- ✅ **Pan/Drag on Empty Space**: Fixed click-and-drag navigation on canvas
- ✅ **Hover Sensitivity**: Reduced unintended graph movement on mouse hover
- ✅ **Node Dragging**: Maintained individual node positioning capability
- ✅ **Interaction Optimization**: Enhanced tooltip delays and navigation controls

## v2.1.3 Navigation Restoration ✅
- ✅ **Root Cause Analysis**: Compared current app with old working v1.0 configuration
- ✅ **Default Behavior Restored**: Removed explicit interaction config to use vis-network defaults
- ✅ **Scroll Wheel Zoom**: Now works identically to original working app
- ✅ **Pan/Drag Navigation**: Canvas panning restored to original functionality  
- ✅ **Minimal Configuration**: Applied "less is more" principle from old working app
- ✅ **Compatibility Maintained**: All visualization preferences still functional

## v2.1 Series Complete ✅
The visualization enhancement vision is now fully realized:
- ✅ **User-Controlled Visualization**: Professional preference system
- ✅ **Large Graph Support**: Physics presets for better large graph layouts
- ✅ **Value-Based Scaling**: Arrows and nodes can reflect data importance
- ✅ **Persistent Experience**: Settings remembered across sessions
- ✅ **Non-Intrusive UI**: Clean collapsible panel design

Ready for **Phase 2** development (export formats, performance) or **Phase 3** (expanded plugins, community features).