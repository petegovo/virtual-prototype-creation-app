#!/bin/bash

# GitHub Repository Setup Script
# This script helps you set up the Virtual Prototype Creation App on GitHub

set -e

echo "🚀 Virtual Prototype Creation App - GitHub Setup"
echo "================================================"

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d ".github" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Get GitHub username
read -p "Enter your GitHub username: " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ Error: GitHub username is required"
    exit 1
fi

echo ""
echo "📋 Setup Summary:"
echo "- Repository: virtual-prototype-creation-app"
echo "- GitHub User: $GITHUB_USERNAME"
echo "- Repository URL: https://github.com/$GITHUB_USERNAME/virtual-prototype-creation-app"
echo ""

read -p "Continue with setup? (y/N): " CONFIRM
if [[ ! $CONFIRM =~ ^[Yy]$ ]]; then
    echo "Setup cancelled."
    exit 0
fi

echo ""
echo "🔧 Setting up Git repository..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
    git config user.name "$(git config --global user.name || echo 'Your Name')"
    git config user.email "$(git config --global user.email || echo 'your.email@example.com')"
fi

# Check if we have commits
if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
    echo "Creating initial commit..."
    git add .
    git commit -m "Initial commit: Virtual Prototype Creation App with FMI 3.0 and SSP 2.0 support"
fi

# Set up remote
REPO_URL="https://github.com/$GITHUB_USERNAME/virtual-prototype-creation-app.git"

if git remote get-url origin >/dev/null 2>&1; then
    echo "Updating existing remote origin..."
    git remote set-url origin "$REPO_URL"
else
    echo "Adding remote origin..."
    git remote add origin "$REPO_URL"
fi

# Rename branch to main
echo "Setting up main branch..."
git branch -M main

echo ""
echo "✅ Git setup complete!"
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Create the repository on GitHub:"
echo "   - Go to: https://github.com/new"
echo "   - Repository name: virtual-prototype-creation-app"
echo "   - Description: Web-based virtual prototype creation app with FMI 3.0 and SSP 2.0 support"
echo "   - Make it Public"
echo "   - DON'T initialize with README, .gitignore, or license (we already have these)"
echo "   - Click 'Create repository'"
echo ""
echo "2. Push your code:"
echo "   git push -u origin main"
echo ""
echo "3. Set up repository secrets (for CI/CD):"
echo "   - Go to: https://github.com/$GITHUB_USERNAME/virtual-prototype-creation-app/settings/secrets/actions"
echo "   - Add: DOCKER_USERNAME (your Docker Hub username)"
echo "   - Add: DOCKER_PASSWORD (your Docker Hub password/token)"
echo ""
echo "4. Enable GitHub Actions:"
echo "   - Go to: https://github.com/$GITHUB_USERNAME/virtual-prototype-creation-app/actions"
echo "   - Click 'I understand my workflows, go ahead and enable them'"
echo ""
echo "🎉 Your repository is ready to push!"
echo ""
echo "Run this command when the GitHub repository is created:"
echo "git push -u origin main"
echo ""
echo "📚 For more details, see:"
echo "- CREATE_GITHUB_REPO.md - Step-by-step instructions"
echo "- GITHUB_SETUP.md - Detailed configuration guide"
echo "- DEPLOYMENT.md - Production deployment options"