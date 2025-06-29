# Causal Graph Tool v2.2.1

[![Status](https://img.shields.io/badge/Status-Tool-blue?style=for-the-badge)](https://github.com/BlockSecCA/graph-app)
[![Electron](https://img.shields.io/badge/Electron-2B2E3A?style=for-the-badge&logo=electron&logoColor=white)](https://www.electronjs.org/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=node.js&logoColor=white)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pyodide](https://img.shields.io/badge/Pyodide-FFD43B?style=for-the-badge&logo=python&logoColor=white)](https://pyodide.org/)
[![NetworkX](https://img.shields.io/badge/NetworkX-000000?style=for-the-badge&logo=python&logoColor=white)](https://networkx.org/)
[![Vis-network](https://img.shields.io/badge/Vis--network-4285F4?style=for-the-badge&logo=google-chrome&logoColor=white)](https://visjs.github.io/vis-network/docs/network/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

A professional Electron-based application for creating, editing, and analyzing causal graphs with an extensible plugin system and advanced visualization controls.

## ✨ Features

### 🎨 **Advanced Graph Editor**
- **Intuitive Interface**: Single unified view combining editing and analysis
- **Context Menu Operations**: Right-click to add nodes, edit properties, or delete elements
- **Visualization Preferences**: Comprehensive controls for node sizing, arrow scaling, and layout
- **Performance Optimized**: Smooth navigation for graphs of any size with intelligent physics management
- **Professional Styling**: Clean, modern interface with responsive design

### 🔗 **Smart Edge Management**
- **Visual Connections**: Directed edges with positive (+) and negative (-) influence types
- **Weighted Relationships**: Configurable edge weights for influence strength
- **Advanced Arrow Controls**: Adjustable arrow scaling with value-based sizing and skinny arrow options
- **Context Menus**: Right-click nodes and edges for quick editing and deletion

### 📊 **Advanced Analysis**
- **Plugin Architecture**: Extensible analysis system with Python-powered plugins
- **Real-time Updates**: Analysis automatically updates as you modify the graph
- **Rich Results**: Detailed influence scores, causal paths, and execution metadata
- **NetworkX Integration**: Sophisticated graph algorithms using industry-standard library

### 🎛️ **Visualization Preferences**
- **Node Controls**: Manual sizing (8-32px) with auto-size based on connection count
- **Arrow Scaling**: Adjustable arrow sizes (0.5-2.5x) with value-based proportional scaling
- **Physics Management**: Tight/Normal/Loose layout presets with custom spring length
- **Performance Settings**: Auto-disable physics for large graphs (>50 nodes) with manual override
- **Skinny Arrows**: Optional thin arrow style for cleaner dense graph visualization
- **Reset Controls**: One-click return to default settings with "Stabilize & Disable" optimization

### 🔌 **Plugin System**
- **User-Serviceable**: Add custom analysis plugins in the user data directory
- **Built-in Analytics**: Causal path analysis with positive/negative pathway detection
- **Easy Access**: Tools menu provides direct access to plugin folder
- **Extensible**: Full plugin development framework with comprehensive documentation

## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/BlockSecCA/graph-app.git
cd graph-app

# Install dependencies
npm install

# Start the application
npm start
```

### Basic Usage

1. **Create Nodes**: Right-click on empty space → "Add Node"
2. **Connect Nodes**: Right-click on empty space → "Add Edge" → Select source and target
3. **Edit Elements**: Right-click on nodes/edges for edit/delete options
4. **Customize Visualization**: Click "⚙️ Visualization" button to adjust node sizes, arrows, and performance
5. **Analyze Graph**: Select plugin from dropdown and click "Run Analysis"
6. **Save/Load**: Use toolbar buttons for graph persistence

## 📁 File Operations

- **📂 Load Graph** (toolbar button): Load graph from JSON file using file browser
- **💾 Save Graph** (toolbar button): Save current graph as JSON file 
- **File → New Graph** (F5): Create a new empty graph (reloads application)
- **File → Restart Application** (Ctrl+Shift+R): Restart the application

## 🔌 Plugin Development

The application supports custom analysis plugins written in Python. See [PLUGIN.md](./PLUGIN.md) for complete development guide.

### Quick Plugin Overview

Plugins are Python modules located in:
- **Development**: `py/plugins/`
- **Installed App**: User data directory (accessible via Tools → Open Plugins Folder)

Example plugin structure:
```
plugins/
├── my-analysis/
│   ├── __init__.py          # Plugin metadata
│   ├── analysis.py          # Main analysis function  
│   └── README.md           # Documentation
```

## 🏗 Architecture

### Modern Unified Design
- **Single-Page Application**: No more iframe isolation
- **Shared State Management**: Real-time synchronization between editor and analysis
- **Event-Driven**: Reactive updates using custom event system
- **Plugin Integration**: Dynamic plugin discovery and execution

### Technology Stack
- **Frontend**: Electron, vis-network, HTML5/CSS3/JavaScript
- **Backend**: Node.js, Python integration via Pyodide
- **Analysis**: NetworkX, custom plugin architecture
- **Build**: electron-builder for cross-platform packaging

## 🔧 Development

### Requirements
- **Node.js**: v20.19.2 or higher
- **npm**: Latest version
- **Python**: Integrated via Pyodide (no local Python required)

### Development Commands
```bash
npm start           # Start development server
npm test            # Run test suite
npm run build       # Build for production
npm run pack        # Package for current platform
npm run build:all   # Build for all platforms
```

### Project Structure
```
causal-graph-tool/
├── src/
│   ├── unified-interface.html    # Main application interface
│   └── shared-state.js          # State management system
├── py/
│   ├── plugins/                 # Built-in analysis plugins
│   └── plugin_loader.py         # Plugin discovery system
├── main.js                      # Electron main process
├── package.json                 # Project configuration
└── docs/                        # Documentation
    ├── PLUGIN.md               # Plugin development guide
    ├── CHANGELOG.md            # Version history
    └── ROADMAP.md              # Future plans
```

## 📦 Building & Distribution

### Windows
```bash
npm run build:win
```

### macOS
```bash
npm run build:mac
```

### Linux
```bash
npm run build:linux
```

### All Platforms
```bash
npm run build:all
```

## 🆕 What's New in v2.2

### v2.2.1 - Navigation & Performance
- **⚡ Large Graph Performance**: Automatic physics optimization for graphs >50 nodes
- **🎛️ Visualization Preferences**: Comprehensive controls for node sizing, arrow scaling, and layout
- **📊 Performance Monitoring**: Real-time feedback on graph performance with color-coded status
- **🔧 Manual Controls**: Physics engine toggle with "Stabilize & Disable" optimization
- **🎯 Navigation Restored**: Smooth zoom and pan for all graph sizes

### v2.1 - Visualization Controls  
- **📐 Node Size Control**: Manual sizing (8-32px) with auto-size based on connections
- **🏹 Arrow Scaling**: Adjustable arrows (0.5-2.5x) with value-based proportional scaling
- **⚙️ Physics Presets**: Tight/Normal/Loose layout options with custom spring length
- **💾 Persistent Preferences**: Settings saved across app sessions
- **🔄 Reset to Defaults**: One-click restoration of original settings

### v2.0 - Foundation
- **🎯 Unified Interface**: Complete redesign eliminating iframe isolation
- **🔌 Plugin System**: Extensible analysis framework with Python integration
- **🎨 Context Menus**: Professional editing interface with right-click operations
- **📊 Enhanced Analysis**: Real-time analysis with rich result visualization
- **🛠 User-Serviceable**: Plugin development and customization capabilities

## 📚 Documentation

- **[Plugin Development Guide](./PLUGIN.md)** - Complete guide for creating analysis plugins
- **[Change Log](./CHANGELOG.md)** - Version history and updates
- **[Roadmap](./ROADMAP.md)** - Future development plans
- **[Graph Specification](./GRAPH_SPEC.md)** - Data format documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Repository**: https://github.com/BlockSecCA/graph-app
- **Issues**: https://github.com/BlockSecCA/graph-app/issues
- **Plugin Documentation**: [PLUGIN_SPEC.md](./PLUGIN_SPEC.md)

---

**Causal Graph Tool v2.2.1** - Professional graph analysis with advanced visualization and performance optimization.