// generateManifests.js

const fs = require('fs');
const path = require('path');

const eidolonAppsDir = path.join(__dirname, 'app', 'eidolon-apps');
const manifestsData = {};

// Read the subdirectories in the eidolon-apps directory
const appDirs = fs.readdirSync(eidolonAppsDir, { withFileTypes: true })
  .filter(dirent => dirent.isDirectory())
  .map(dirent => dirent.name);

// Iterate over each app directory
appDirs.forEach(appDir => {
  const manifestPath = path.join(eidolonAppsDir, appDir, 'manifest.json');

  // Check if the manifest.json file exists
  if (fs.existsSync(manifestPath)) {
    // Read the contents of the manifest.json file
    const manifestContent = fs.readFileSync(manifestPath, 'utf8');

    // Parse the JSON content
    const manifest = JSON.parse(manifestContent);

    // Add the manifest to the manifestsData object with the app directory name as the key
    manifestsData[appDir] = manifest;
  }
});

// Write the combined manifests data to a JSON file
const manifestsFilePath = path.join(__dirname, 'eidolon-apps.json');
fs.writeFileSync(manifestsFilePath, JSON.stringify(manifestsData, null, 2));

console.log('Manifests combined successfully.');
