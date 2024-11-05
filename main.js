// Import necessary modules from Electron
const { app, BrowserWindow } = require('electron');
const path = require('path');

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
        // icon: 'assets/icon.ico' // Use a direct path to the icon
    });

    // Load the index.html file into the window
    win.loadFile('index.html');
}

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
