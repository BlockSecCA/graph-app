# Changelog

All notable changes to the Causal Graph Tool will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-06-25

### 🎯 Major Changes
This is a complete architectural rewrite of the application, moving from an iframe-based design to a modern unified interface with an extensible plugin system.

### ✨ Added
- **Unified Interface**: Single-page application design replacing iframe isolation
- **Plugin Architecture**: Extensible Python-based analysis system with automatic discovery
- **Context Menu System**: Professional right-click interface for all graph operations
- **Real-time Analysis**: Automatic analysis updates as graphs are modified
- **Advanced Physics**: Interactive node positioning with collision detection
- **Rich Result Display**: Detailed analysis results with metadata and execution timing
- **User Plugin Directory**: User-serviceable plugin system in app data directory
- **Tools Menu**: Direct access to plugin folder and documentation
- **Enhanced File Operations**: Integrated File menu with keyboard shortcuts
- **Shared State Management**: Real-time synchronization between editor and analysis
- **Comprehensive Documentation**: Plugin development guide and specifications

### 🔄 Changed
- **Complete UI Redesign**: Eliminated Bootstrap tabs and iframe architecture
- **Node Creation**: Changed from form-based to context menu-based workflow
- **Edge Creation**: Moved from toolbar buttons to context menu selection
- **Graph Editing**: All operations now use right-click context menus
- **Analysis Integration**: Analysis now runs automatically on graph changes
- **File Management**: Moved file operations from toolbar to File menu
- **Graph Visualization**: Enhanced with better physics and styling

### 🗑️ Removed
- **Iframe Architecture**: Eliminated separate iframe-based components
- **Bootstrap UI**: Removed Bootstrap dependency for cleaner styling
- **Toolbar Buttons**: Replaced with context menus and menu bar operations
- **Manual Analysis Loading**: Analysis now loads automatically
- **Separate HTML Files**: Consolidated into unified interface

### 🔧 Technical Improvements
- **NetworkX Integration**: Full NetworkX support via Pyodide for sophisticated analysis
- **Plugin Discovery**: Automatic scanning and loading of user plugins
- **Error Handling**: Comprehensive error handling with graceful fallbacks
- **Cross-Platform**: Proper user data directory handling for Windows/Mac/Linux
- **Performance**: Optimized rendering and physics simulation

### 📊 Analysis Enhancements
- **Causal Path Analysis**: Advanced multi-hop pathway detection
- **Influence Scoring**: Sophisticated node influence calculations
- **Positive/Negative Paths**: Separate detection of positive and negative causal chains
- **Mixed Path Detection**: Identification of paths with both positive and negative edges
- **Execution Metadata**: Detailed timing and graph statistics
- **Result Visualization**: Rich formatting with color-coded scores

### 🛠️ Developer Experience
- **Plugin Development**: Complete framework for creating custom analysis plugins
- **Hot Reloading**: Plugins discovered automatically on app restart
- **Comprehensive API**: Full plugin specification with examples
- **Documentation**: Extensive guides for plugin development
- **Error Reporting**: Detailed error messages for plugin development

### 🚀 User Experience
- **Intuitive Interface**: Professional, clean design with logical workflows
- **Context-Sensitive Menus**: Right-click operations specific to clicked elements
- **Keyboard Shortcuts**: Standard shortcuts for common operations
- **Responsive Design**: Adaptive layout for different screen sizes
- **Immediate Feedback**: Real-time updates and visual confirmations

## [1.0.0] - 2024-XX-XX

### Initial Release
- Basic graph editor with vis-network integration
- Simple Python analysis via Pyodide
- Bootstrap-based tabbed interface
- Basic file save/load functionality
- Simple node and edge creation forms
- Basic influence score calculation
- iframe-based architecture

---

## Version Numbering

This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions  
- **PATCH** version for backwards-compatible bug fixes

## Categories

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for vulnerability fixes