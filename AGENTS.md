# AGENTS.md

## Overview

This project is an Electron-based visual graph editor and causal analysis tool. It includes:
- A `vis-network`-based graph editor
- A Bootstrap UI rendered in `index.html`
- A Python-based analysis engine executed via Pyodide in-browser

## Key Modules

### `graph_editor_new.html`
- Uses `vis-network` to visualize graphs.
- Interacts with `graphUtils` functions via DOM and JS.
- Users can:
  - Add/delete nodes and edges
  - Save/load graph as JSON
  - Resize graph area

### `analysis_tool.html`
- Loads `py/test_pyodide.py` into Pyodide.
- Performs causal analysis using `networkx`.
- Outputs:
  - Influence scores
  - Positive/negative paths

### `lib/graphUtils.js`
- Pure logic for graph editing and serialization
- Testable via Jest
- Functions:
  - `addNode`, `addEdge`, `deleteNode`, `deleteEdge`
  - `saveGraph`, `loadGraph`

## Test Coverage

- Tests in `__tests__/graphUtils.test.js`
- Run using `npm test` or `npx jest`

## Agent Tasks Allowed

- Update documentation (`README.md`, `AGENTS.md`)
- Add/refactor pure JS logic in `lib/graphUtils.js`
- Generate or update test cases
- Suggest UI or UX improvements non-destructively
- Refactor analysis logic with Pyodide if requested

## Agent Constraints

- Avoid modifying:
  - `main.js` unless adding UI features
  - Pyodide Python code unless analysis goals change
- Do not change HTML unless explicitly scoped
- Maintain backward compatibility with JSON graph format
