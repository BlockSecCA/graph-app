// Import necessary modules from Electron
const { app, BrowserWindow, Menu, shell } = require('electron');
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
        },
        icon: __dirname + `/assets/icon.ico`
    });

    // Load the index.html file into the window
    win.loadFile('index.html');

    // Log to the renderer process console
    win.webContents.on('did-finish-load', () => {
        logToRenderer(win, "Main process started");
    });
}

// Function to open README.md in a new window
function openReadme() {
    const readmePath = path.join(__dirname, 'README.md'); // Path to README.md
    fs.readFile(readmePath, 'utf8', (err, data) => {
        if (err) {
            console.error('Error reading README.md:', err);
            return;
        }
        const readmeWindow = new BrowserWindow({
            width: 800,
            height: 600,
            webPreferences: {
                nodeIntegration: true,
            },
            autoHideMenuBar: true, // Suppress the menu bar
            title: 'README' // Optional: Set a title for the window
        });
        // Load the README.md content as plain text
        readmeWindow.loadURL('data:text/plain;charset=utf-8,' + encodeURIComponent(data)); // Load plain text content
    });
}

// Create a custom menu template
const menuTemplate = [
    {
        label: 'File',
        submenu: [
            { label: 'Exit', role: 'quit' }
        ]
    },
    {
        label: 'View',
        submenu: [
            { label: 'Reload', role: 'reload' },
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
        label: 'Help',
        submenu: [
            { label: 'Open README', click: openReadme } // Call openReadme function
        ]
    }
];

// Set the application menu
const menu = Menu.buildFromTemplate(menuTemplate);
Menu.setApplicationMenu(menu);

// Event listener for when the app is ready to create the window
app.whenReady().then(createWindow);

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
