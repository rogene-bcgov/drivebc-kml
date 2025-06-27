#!/bin/bash

# DriveBC KML Service Setup Script
# This script helps you set up the service on GitHub

echo "🚗 DriveBC KML Service Setup"
echo "=============================="

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ This is not a git repository. Please run 'git init' first."
    exit 1
fi

echo "✅ Git repository detected"

# Check if GitHub remote exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "⚠️  No GitHub remote found. Please add your GitHub repository as origin:"
    echo "   git remote add origin https://github.com/yourusername/yourrepo.git"
    echo ""
fi

# Test the service script
echo "🧪 Testing service script..."
if python drivebc_service.py; then
    echo "✅ Service script working correctly"
else
    echo "❌ Service script failed. Please check your internet connection and try again."
    exit 1
fi

# Check if KML file was created
if [ -f "drivebc_events.kml" ]; then
    echo "✅ KML file generated successfully"
else
    echo "❌ KML file not found"
    exit 1
fi

# Add files to git
echo "📦 Adding files to git..."
git add .
git add drivebc_events.kml

# Commit files
echo "💾 Committing initial setup..."
git commit -m "Initial setup of DriveBC KML service

- Added automated service script
- Added GitHub Actions workflow
- Added web interface
- Generated initial KML file"

echo ""
echo "🚀 Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Push to GitHub: git push origin main"
echo "2. Enable GitHub Pages in repository settings"
echo "3. Enable GitHub Actions in repository settings"
echo "4. Your service will be available at:"
echo "   https://yourusername.github.io/yourrepo/"
echo ""
echo "The KML file will auto-update every 30 minutes!"
