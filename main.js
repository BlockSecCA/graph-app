// Import necessary modules from Electron
const { app, BrowserWindow, Menu, shell, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs');

// Function to log messages to the renderer process console
function logToRenderer(win, message) {
    win.webContents.executeJavaScript(`console.log(${JSON.stringify(message)});`);
}

// Function to create the main application window
function createWindow() {
    // Create a new BrowserWindow instance
    const win = new BrowserWindow({
        width: 800, // Set the width of the window
        height: 600, // Set the height of the window
        webPreferences: {
            nodeIntegration: true, // Enable Node.js integration in the renderer process
            contextIsolation: false, // Disable context isolation to allow access to require
        },
        icon: __dirname + `/assets/icon.ico`
    });

    // Load the unified interface
    win.loadFile('src/unified-interface.html');

    // Log to the renderer process console
    win.webContents.on('did-finish-load', () => {
        logToRenderer(win, "Main process started");
    });
}

// Function to open documentation files in external application
function openDocumentationFile(filename, title) {
    const filePath = path.join(__dirname, filename);
    
    // Check if file exists
    if (!fs.existsSync(filePath)) {
        console.error(`Documentation file not found: ${filename}`);
        return;
    }
    
    // Open with default application (markdown viewer, text editor, etc.)
    shell.openExternal(`file://${filePath}`).catch(error => {
        console.error(`Could not open ${title}:`, error);
        
        // Fallback: try opening with system default
        shell.openPath(filePath).catch(fallbackError => {
            console.error(`Fallback failed for ${title}:`, fallbackError);
        });
    });
}

// Create a custom menu template
const menuTemplate = [
    {
        label: 'File',
        submenu: [
            { 
                label: 'New Graph', 
                accelerator: 'F5',
                role: 'reload'
            },
            { type: 'separator' },
            { 
                label: 'Load Graph...', 
                accelerator: 'CmdOrCtrl+O',
                click: async () => {
                    const { dialog } = require('electron');
                    const win = BrowserWindow.getFocusedWindow();
                    if (win) {
                        const result = await dialog.showOpenDialog(win, {
                            properties: ['openFile'],
                            filters: [
                                { name: 'JSON Files', extensions: ['json'] },
                                { name: 'All Files', extensions: ['*'] }
                            ]
                        });
                        
                        if (!result.canceled && result.filePaths.length > 0) {
                            const filePath = result.filePaths[0];
                            const fs = require('fs');
                            try {
                                const fileContent = fs.readFileSync(filePath, 'utf8');
                                win.webContents.send('menu-load-graph-content', fileContent, path.basename(filePath));
                            } catch (error) {
                                console.error('Error reading file:', error);
                            }
                        }
                    }
                }
            },
            { 
                label: 'Save Graph...', 
                accelerator: 'CmdOrCtrl+S',
                click: () => {
                    const win = BrowserWindow.getFocusedWindow();
                    if (win) {
                        win.webContents.send('menu-save-graph');
                    }
                }
            },
            { type: 'separator' },
            { 
                label: 'Restart Application', 
                accelerator: 'CmdOrCtrl+Shift+R',
                click: () => {
                    console.log('Menu: Restart Application clicked');
                    app.relaunch();
                    app.quit();
                }
            },
            { label: 'Exit', role: 'quit' }
        ]
    },
    {
        label: 'View',
        submenu: [
            { 
                label: 'Fit Graph to View', 
                accelerator: 'CmdOrCtrl+0',
                click: () => {
                    const win = BrowserWindow.getFocusedWindow();
                    if (win) {
                        win.webContents.send('menu-fit-graph');
                    }
                }
            },
            { type: 'separator' },
            { label: 'Toggle Developer Tools', role: 'toggledevtools' }
        ]
    },
    {
        label: 'Window',
        submenu: [
            { label: 'Minimize', role: 'minimize' },
            { label: 'Close', role: 'close' }
        ]
    },
    {
        label: 'Tools',
        submenu: [
            { 
                label: 'Open Plugins Folder', 
                click: () => {
                    const pluginsDir = global.pluginsDirectory || initializePluginDirectories();
                    shell.openPath(pluginsDir);
                }
            }
        ]
    },
    {
        label: 'Help',
        submenu: [
            { 
                label: 'Help', 
                click: () => openDocumentationFile('HELP.md', 'Help')
            },
            { type: 'separator' },
            { 
                label: 'README', 
                click: () => openDocumentationFile('README.md', 'README')
            },
            { 
                label: 'Plugin Development Guide', 
                click: () => openDocumentationFile('PLUGIN.md', 'Plugin Development Guide')
            },
            { 
                label: 'Plugin Specification', 
                click: () => openDocumentationFile('PLUGIN_SPEC.md', 'Plugin Specification')
            },
            { type: 'separator' },
            { 
                label: 'Roadmap', 
                click: () => openDocumentationFile('ROADMAP.md', 'Roadmap')
            },
            { 
                label: 'Changelog', 
                click: () => openDocumentationFile('CHANGELOG.md', 'Changelog')
            }
        ]
    }
];

// Set the application menu
const menu = Menu.buildFromTemplate(menuTemplate);
Menu.setApplicationMenu(menu);

// Initialize plugin directories
function initializePluginDirectories() {
    const userDataPath = app.getPath('userData');
    const pluginsDir = path.join(userDataPath, 'plugins');
    
    // Create plugins directory if it doesn't exist
    if (!fs.existsSync(pluginsDir)) {
        fs.mkdirSync(pluginsDir, { recursive: true });
        console.log('Created user plugins directory:', pluginsDir);
    }
    
    // Copy built-in plugins to user directory (first time only)
    const builtinPluginsDir = path.join(__dirname, 'py', 'plugins');
    
    if (fs.existsSync(builtinPluginsDir)) {
        const builtinPlugins = fs.readdirSync(builtinPluginsDir);
        
        for (const pluginName of builtinPlugins) {
            const srcDir = path.join(builtinPluginsDir, pluginName);
            const destDir = path.join(pluginsDir, pluginName);
            
            // Only copy if destination doesn't exist (don't overwrite user modifications)
            if (!fs.existsSync(destDir) && fs.statSync(srcDir).isDirectory()) {
                try {
                    copyDirectory(srcDir, destDir);
                    console.log(`Copied built-in plugin: ${pluginName}`);
                } catch (error) {
                    console.error(`Failed to copy plugin ${pluginName}:`, error);
                }
            }
        }
    }
    
    // Store plugin directory path for renderer process
    global.pluginsDirectory = pluginsDir;
    
    return pluginsDir;
}

// Helper function to copy directories recursively
function copyDirectory(src, dest) {
    fs.mkdirSync(dest, { recursive: true });
    
    const entries = fs.readdirSync(src, { withFileTypes: true });
    
    for (const entry of entries) {
        const srcPath = path.join(src, entry.name);
        const destPath = path.join(dest, entry.name);
        
        if (entry.isDirectory()) {
            copyDirectory(srcPath, destPath);
        } else {
            fs.copyFileSync(srcPath, destPath);
        }
    }
}

// Add IPC handler for getting plugins directory
ipcMain.handle('get-plugins-directory', () => {
    return global.pluginsDirectory || initializePluginDirectories();
});

// Event listener for when the app is ready to create the window
app.whenReady().then(() => {
    initializePluginDirectories();
    createWindow();
});

// Event listener for when all windows are closed
app.on('window-all-closed', () => {
    // On non-macOS platforms, quit the app
    if (process.platform !== 'darwin') {
        app.quit(); // Quit the application
    }
});

// Event listener for macOS to recreate a window when the app is activated
app.on('activate', () => {
    // If there are no open windows, create a new one
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow(); // Call the function to create a new window
    }
});
