const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  getPluginsDirectory: () => ipcRenderer.invoke('get-plugins-directory'),
  
  // Menu event listeners
  onMenuLoadGraph: (callback) => ipcRenderer.on('menu-load-graph-content', callback),
  onMenuSaveGraph: (callback) => ipcRenderer.on('menu-save-graph', callback),
  onMenuFitGraph: (callback) => ipcRenderer.on('menu-fit-graph', callback),
  
  // Remove listeners
  removeAllListeners: (channel) => ipcRenderer.removeAllListeners(channel)
});