# Create GitHub Repository - Step by Step Guide

## 🚀 Quick Setup Instructions

Follow these steps to create your GitHub repository and push the Virtual Prototype Creation App:

### Step 1: Create Repository on GitHub

1. **Go to GitHub**: Open [github.com](https://github.com) and sign in
2. **Create New Repository**: Click the "+" icon → "New repository"
3. **Repository Settings**:
   - **Name**: `virtual-prototype-creation-app`
   - **Description**: `Web-based virtual prototype creation app with FMI 3.0 and SSP 2.0 support for SystemC, Simulink, and Modelica IP reuse`
   - **Visibility**: Public (recommended for open source)
   - **Initialize**: Leave all checkboxes UNCHECKED (we already have code)
4. **Click "Create repository"**

### Step 2: Push Your Code

After creating the repository, GitHub will show you instructions. Use these commands in your terminal:

```bash
# Navigate to your project directory
cd /workspace/project

# Add GitHub as remote origin (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/virtual-prototype-creation-app.git

# Rename branch to main (GitHub's default)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

### Step 3: Configure Repository Settings

#### Enable GitHub Actions
1. Go to your repository → **Actions** tab
2. Click "I understand my workflows, go ahead and enable them"

#### Set Up Secrets (Required for CI/CD)
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"** and add these:

**Required Secrets:**
- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub password/token

**Optional Secrets:**
- `SLACK_WEBHOOK_URL`: For deployment notifications
- `CODECOV_TOKEN`: For code coverage reports

#### Configure Branch Protection
1. Go to **Settings** → **Branches**
2. Click **"Add rule"**
3. Branch name pattern: `main`
4. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging

### Step 4: Test Your Setup

1. **Make a small change** to test the workflow:
   ```bash
   echo "# Test" >> README.md
   git add README.md
   git commit -m "Test GitHub Actions workflow"
   git push
   ```

2. **Check Actions**: Go to the **Actions** tab to see your workflow running

### Step 5: Create Your First Release

When ready to create a release:

```bash
# Tag your current version
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

This will trigger the release workflow and create:
- GitHub release with changelog
- Docker images with version tags
- Release artifacts for multiple platforms

## 🔧 Alternative: Using GitHub CLI

If you have GitHub CLI installed:

```bash
# Login to GitHub CLI
gh auth login

# Create repository
gh repo create virtual-prototype-creation-app \
  --description "Web-based virtual prototype creation app with FMI 3.0 and SSP 2.0 support" \
  --public

# Push code
git remote add origin https://github.com/$(gh api user --jq .login)/virtual-prototype-creation-app.git
git branch -M main
git push -u origin main
```

## 📋 What Happens After Setup

Once your repository is created and pushed:

### Automatic CI/CD Pipeline
- **Every push/PR**: Runs tests, security scans, code quality checks
- **Main branch**: Builds and deploys Docker images
- **Version tags**: Creates releases with artifacts

### Weekly Maintenance
- **Dependency updates**: Automatic PRs for security updates
- **Security scanning**: Vulnerability reports and alerts

### Available Endpoints
After deployment, your app will have:
- **Frontend**: Modern React interface
- **Backend API**: FastAPI with OpenAPI docs
- **Health checks**: Monitoring endpoints
- **File management**: FMU/SSP upload/download

## 🎯 Repository Features

Your repository includes:

### GitHub Actions Workflows
- ✅ **CI/CD Pipeline**: Multi-platform testing and deployment
- ✅ **Release Automation**: Automated releases with Docker images
- ✅ **Dependency Updates**: Weekly security and dependency updates

### Docker Support
- ✅ **Multi-stage builds**: Optimized container images
- ✅ **Security hardening**: Non-root users, minimal attack surface
- ✅ **Production ready**: Health checks and monitoring

### Comprehensive Testing
- ✅ **Backend tests**: pytest with coverage reporting
- ✅ **Frontend tests**: Vitest with React Testing Library
- ✅ **Integration tests**: End-to-end API testing
- ✅ **Security tests**: Vulnerability scanning

### Documentation
- ✅ **API Documentation**: Auto-generated OpenAPI/Swagger docs
- ✅ **Deployment Guides**: Multiple cloud platform instructions
- ✅ **Architecture Docs**: Technical implementation details

## 🚨 Important Notes

1. **Docker Hub**: Create Docker Hub repositories for image pushing:
   - `your-username/virtual-prototype-backend`
   - `your-username/virtual-prototype-frontend`

2. **Secrets**: Add repository secrets before the first workflow run

3. **Branch Protection**: Enable after initial push to prevent direct pushes to main

4. **License**: Consider adding a license file (MIT recommended for open source)

## 🆘 Troubleshooting

### Common Issues:

**Authentication Error:**
```bash
# If you get authentication errors, use personal access token
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/virtual-prototype-creation-app.git
```

**Workflow Failures:**
- Check that all required secrets are set
- Verify Docker Hub repository names match your username
- Review workflow logs in the Actions tab

**Permission Errors:**
- Ensure your GitHub token has repo permissions
- Check that branch protection rules allow your workflow

## 🎉 Success!

Once completed, you'll have:
- ✅ Professional GitHub repository
- ✅ Automated CI/CD pipeline
- ✅ Security scanning and monitoring
- ✅ Production-ready deployment
- ✅ Comprehensive documentation

Your Virtual Prototype Creation App is now ready for the world! 🚀

---

**Need help?** Check the other documentation files:
- `GITHUB_SETUP.md` - Detailed GitHub configuration
- `DEPLOYMENT.md` - Production deployment options
- `README.md` - Project overview and features