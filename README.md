# Causal Graph Tool
This Electron-based application provides a simple interface for editing graphs and running basic analysis on them.

## Application Overview
- **Main Window**: `main.js` creates an 800x600 window and loads `index.html`. A menu option **"Open README"** displays this file in a new window.
- **Index Page**: `index.html` offers two Bootstrap tabs: a Graph Editor and a Graph Analysis Tool, each embedded in an `<iframe>`.
- **Graph Editor**: `graph_editor_new.html` uses `vis-network` to visualize graphs. Users can add or delete nodes and edges, save graphs as JSON, and reload saved graphs. A draggable handle allows resizing the network view.
 - **Graph Analysis**: `analysis_tool.html` loads Pyodide to run the Python script `py/test_pyodide.py`. The script converts the graph to NetworkX, computes influence scores, and finds positive or negative paths between the first and last nodes. Results appear formatted as JSON in a text area and via alerts.

Launching the app with `npm start` opens the Electron window with tabs for building and analyzing graphs.

## Getting Started
1. Install dependencies with `npm install`.
2. Start the application using `npm start`.

## Development Environment
This project was developed using **Node.js v20.19.2** together with **Electron v25.0.0**.  
Using a version manager such as [`nvm`](https://github.com/nvm-sh/nvm) makes it easy to match these versions.

## Testing
Run `npm test` to execute the Jest test suite found in the `__tests__` directory.

## Packaging
Additional scripts for building and packaging the app are defined in `package.json`:
- `npm run build`
- `npm run pack`

## Agents
For AI agents and automation guidance, see [AGENTS.md](./AGENTS.md)
