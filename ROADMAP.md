# Causal Graph Tool - Roadmap

## Overview
This document outlines planned improvements to the graph editor, organized by impact and complexity. The app currently works as a basic graph editor but has significant limitations in integration, format support, and architecture.

---

## 🔥 HIGH IMPACT - User-Facing Improvements

### 1. Multi-Format Import Support
**Impact**: ⭐⭐⭐⭐⭐ | **Complexity**: ⭐⭐⭐⭐
- **Problem**: App only reads its own JSON format, limiting usefulness
- **Solution**: Add parsers for common graph formats
- **Formats to support**:
  - GraphML (XML-based, used by yEd, Gephi)
  - DOT/Graphviz (text format)
  - CSV (edge lists, adjacency matrices)
  - GEXF (XML, used by Gephi)
  - Cytoscape.js JSON
  - NetworkX JSON variants
- **Benefits**: Makes app useful for real-world data instead of just toy examples

### 2. Real-Time Editor-Analysis Integration
**Impact**: ⭐⭐⭐⭐⭐ | **Complexity**: ⭐⭐⭐
- **Problem**: Editor and analysis are isolated - no live updates
- **Current Workflow**: Edit → Save → Load in Analysis tab
- **Solution**: Shared state between editor and analysis
- **Features**:
  - Auto-analysis as you edit
  - Live influence score updates
  - Instant path highlighting
  - No file save/load needed
- **Benefits**: Seamless workflow, immediate feedback

### 3. Enhanced Graph Visualization
**Impact**: ⭐⭐⭐⭐ | **Complexity**: ⭐⭐⭐
- **Problem**: Basic vis-network styling, limited visual feedback
- **Solution**: Rich visualization features
- **Features**:
  - Node styling by type/group
  - Edge styling by weight/type
  - Influence score visualization (node size/color)
  - Path highlighting
  - Layout algorithms (force-directed, hierarchical, circular)
- **Benefits**: Better understanding of graph structure and analysis results

---

## 🔧 MEDIUM IMPACT - Architecture & UX

### 4. Flexible Schema System
**Impact**: ⭐⭐⭐⭐ | **Complexity**: ⭐⭐⭐⭐
- **Problem**: Hardcoded schema limits adaptability
- **Current Schema**: Fixed `{id, label, type, group}` for nodes, `{source, target, type, weight}` for edges
- **Solution**: Configurable field mappings
- **Features**:
  - Schema editor/configurator
  - Field mapping for imports
  - Custom properties support
  - Validation rules
- **Benefits**: Works with any graph data structure

### 5. Unified Interface Design
**Impact**: ⭐⭐⭐ | **Complexity**: ⭐⭐⭐
- **Problem**: Separate iframes create isolation and poor UX
- **Current**: Bootstrap tabs with embedded iframes
- **Solution**: Single-page application with integrated components
- **Features**:
  - Side-by-side editor and analysis
  - Shared toolbar and menus
  - Consistent styling
  - Better responsive design
- **Benefits**: Professional look, better user experience

### 6. Graph Export Capabilities
**Impact**: ⭐⭐⭐ | **Complexity**: ⭐⭐
- **Problem**: Can only save to proprietary JSON format
- **Solution**: Export to multiple formats
- **Features**:
  - Export to GraphML, DOT, CSV, PNG, SVG
  - Print-friendly layouts
  - Analysis report export
- **Benefits**: Interoperability with other tools

---

## 🛡️ MEDIUM IMPACT - Security & Architecture

### 7. Electron Security Hardening
**Impact**: ⭐⭐⭐ | **Complexity**: ⭐⭐⭐
- **Problem**: Using deprecated `nodeIntegration: true` (security risk)
- **Current**: Direct Node.js access in renderer
- **Solution**: Proper Electron security practices
- **Changes**:
  - Disable node integration
  - Enable context isolation
  - Use preload scripts for IPC
  - Content Security Policy
- **Benefits**: Secure, follows Electron best practices

### 8. Proper Project Structure
**Impact**: ⭐⭐ | **Complexity**: ⭐⭐⭐
- **Problem**: Files mixed in root directory
- **Current**: HTML files in root, no clear separation
- **Solution**: Standard Electron project structure
- **Structure**:
  ```
  src/
  ├── main/ (main process)
  ├── renderer/ (renderer files)
  └── shared/ (shared utilities)
  ```
- **Benefits**: Maintainable, scalable, professional

---

## 🔧 LOW IMPACT - Quality of Life

### 9. Enhanced Error Handling
**Impact**: ⭐⭐ | **Complexity**: ⭐⭐
- **Problem**: Poor error messages, crashes on invalid data
- **Solution**: Comprehensive error handling and validation
- **Features**:
  - Graph validation with helpful messages
  - Recovery from invalid states
  - Better debugging tools
- **Benefits**: More reliable, user-friendly

### 10. Improved Testing Coverage
**Impact**: ⭐⭐ | **Complexity**: ⭐⭐
- **Problem**: Minimal test coverage
- **Current**: Basic unit tests for graphUtils
- **Solution**: Comprehensive test suite
- **Coverage**:
  - Unit tests for all modules
  - Integration tests for workflows
  - End-to-end tests for critical paths
- **Benefits**: Reliable releases, easier refactoring

### 11. Performance Optimizations
**Impact**: ⭐⭐ | **Complexity**: ⭐⭐
- **Problem**: Potential performance issues with large graphs
- **Solution**: Optimize for large datasets
- **Features**:
  - Virtualization for large graphs
  - Lazy loading of analysis results
  - Efficient rendering algorithms
- **Benefits**: Handles real-world data sizes

---

## 🎯 RECOMMENDED IMPLEMENTATION ORDER

### Phase 1: Core Integration (Weeks 1-2)
1. **Real-Time Editor-Analysis Integration** - Biggest UX improvement
2. **Multi-Format Import Support** - Most requested feature

### Phase 2: Security & Architecture (Weeks 3-4)
3. **Electron Security Hardening** - Critical for production use
4. **Enhanced Graph Visualization** - Improves analysis understanding

### Phase 3: Polish & Extensibility (Weeks 5-6)
5. **Flexible Schema System** - Enables wider adoption
6. **Unified Interface Design** - Professional polish

### Phase 4: Quality & Export (Ongoing)
7. **Graph Export Capabilities** - Easy addition after core work
8. **Enhanced Error Handling** - Continuous improvement
9. **Performance Optimizations** - As needed
10. **Project Structure** - When refactoring anyway
11. **Testing Coverage** - Ongoing with each feature

---

## 📊 Impact Legend
- ⭐⭐⭐⭐⭐ = Game-changing feature
- ⭐⭐⭐⭐ = Major improvement
- ⭐⭐⭐ = Noticeable improvement
- ⭐⭐ = Nice to have
- ⭐ = Minor improvement

## 🔧 Complexity Legend
- ⭐⭐⭐⭐⭐ = Major rewrite required
- ⭐⭐⭐⭐ = Significant development effort
- ⭐⭐⭐ = Moderate development effort
- ⭐⭐ = Straightforward implementation
- ⭐ = Quick fix/addition