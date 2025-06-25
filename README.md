# Causal Graph Tool v2.0

A professional Electron-based application for creating, editing, and analyzing causal graphs with an extensible plugin system.

## ✨ Features

### 🎨 **Unified Graph Editor**
- **Intuitive Interface**: Single unified view combining editing and analysis
- **Context Menu Operations**: Right-click to add nodes, edit properties, or delete elements
- **Real-time Physics**: Interactive node positioning with collision detection
- **Professional Styling**: Clean, modern interface with responsive design

### 🔗 **Smart Edge Management**
- **Visual Connections**: Directed edges with positive (+) and negative (-) influence types
- **Weighted Relationships**: Configurable edge weights for influence strength
- **Context Menus**: Right-click nodes and edges for quick editing and deletion

### 📊 **Advanced Analysis**
- **Plugin Architecture**: Extensible analysis system with Python-powered plugins
- **Real-time Updates**: Analysis automatically updates as you modify the graph
- **Rich Results**: Detailed influence scores, causal paths, and execution metadata
- **NetworkX Integration**: Sophisticated graph algorithms using industry-standard library

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
4. **Analyze Graph**: Analysis runs automatically, or click "Analyze" button
5. **Save/Load**: Use File menu for graph persistence

## 📁 File Operations

- **File → New Graph** (F5): Create a new empty graph (reloads application)
- **File → Load Graph** (Ctrl+O): Load graph from JSON file
- **File → Save Graph** (Ctrl+S): Save current graph as JSON
- **View → Fit Graph** (Ctrl+0): Center and fit graph to view

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

## 🆕 What's New in v2.0

- **🎯 Unified Interface**: Complete redesign eliminating iframe isolation
- **🔌 Plugin System**: Extensible analysis framework with Python integration
- **🎨 Context Menus**: Professional editing interface with right-click operations
- **📊 Enhanced Analysis**: Real-time analysis with rich result visualization
- **⚡ Improved Performance**: Better physics simulation and responsive design
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

**Causal Graph Tool v2.0** - Professional graph analysis made simple.