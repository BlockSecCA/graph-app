
# Git Commands
# 1. Commit current code and push to GitHub (main branch)
git add .
git commit -m "Your commit message here"
git push origin main

# 2. Start a branch for a given file or files
git checkout -b feature-branch-name

# 3. Commit the branch and push to GitHub
git add .
git commit -m "Description of changes made in feature-branch-name"
git push origin feature-branch-name

# 4. Merge the branch with main and commit and push to GitHub
git checkout main
git merge feature-branch-name
git push origin main

# 5. Delete the branch that is no longer needed
git branch -d feature-branch-name
git push origin --delete feature-branch-name

# 6. Check the status of the project
git status

---

# Electron Commands
# 1. Start the Electron application
npm start

# 2. Build the Electron application
npm run build   

# 3. Package the Electron application (Windows, Needs Local Administrator Priviledges)
npm run build
npm run pack

# Locating the packaged application
cd dist/MyApp-win32-x64/

