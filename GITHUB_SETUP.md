# GitHub Repository Setup Guide

This guide will help you create a GitHub repository for the Virtual Prototype Creation App and set up CI/CD automation.

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in to your account
2. Click the "+" icon in the top right corner and select "New repository"
3. Fill in the repository details:
   - **Repository name**: `virtual-prototype-creation-app`
   - **Description**: `Web-based virtual prototype creation app with FMI 3.0 and SSP 2.0 support for SystemC, Simulink, and Modelica IP reuse`
   - **Visibility**: Public (recommended) or Private
   - **Initialize repository**: Leave unchecked (we already have code)
   - **Add .gitignore**: None (we already have one)
   - **Choose a license**: MIT License (recommended)

4. Click "Create repository"

## Step 2: Push Code to GitHub

After creating the repository, you'll see instructions on GitHub. Run these commands in your project directory:

```bash
# Add the GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/virtual-prototype-creation-app.git

# Rename the default branch to main (if needed)
git branch -M main

# Push the code to GitHub
git push -u origin main
```

## Step 3: Configure Repository Settings

### Enable GitHub Actions
1. Go to your repository on GitHub
2. Click on the "Actions" tab
3. GitHub Actions should be enabled by default for public repositories
4. If prompted, click "I understand my workflows, go ahead and enable them"

### Set up Repository Secrets (for CI/CD)

Go to your repository → Settings → Secrets and variables → Actions, and add these secrets:

#### Required Secrets:
- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub password or access token
- `SLACK_WEBHOOK_URL`: (Optional) Slack webhook URL for deployment notifications

#### Optional Secrets for Enhanced Features:
- `CODECOV_TOKEN`: For code coverage reporting
- `SONAR_TOKEN`: For SonarCloud code quality analysis

### Configure Branch Protection Rules

1. Go to Settings → Branches
2. Click "Add rule"
3. Branch name pattern: `main`
4. Enable these options:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - ✅ Require conversation resolution before merging
   - ✅ Restrict pushes that create files larger than 100MB

### Set up Repository Topics

1. Go to your repository main page
2. Click the gear icon next to "About"
3. Add these topics: `fmi`, `ssp`, `systemc`, `simulink`, `modelica`, `virtual-prototype`, `simulation`, `fastapi`, `react`, `typescript`

## Step 4: Test GitHub Actions

1. Make a small change to any file (e.g., update README.md)
2. Commit and push the change:
   ```bash
   git add .
   git commit -m "Test GitHub Actions workflow"
   git push
   ```
3. Go to the Actions tab in your GitHub repository
4. You should see the CI/CD workflow running

## Step 5: Set up Docker Hub (Optional)

If you want to use the Docker build and push functionality:

1. Create a Docker Hub account at [hub.docker.com](https://hub.docker.com)
2. Create two repositories:
   - `virtual-prototype-backend`
   - `virtual-prototype-frontend`
3. Generate an access token in Docker Hub settings
4. Add the Docker Hub credentials to GitHub Secrets (as mentioned in Step 3)

## Available Workflows

The repository includes these GitHub Actions workflows:

### 1. CI/CD Pipeline (`.github/workflows/ci.yml`)
- **Triggers**: Push to main/develop, Pull requests
- **Jobs**:
  - Backend tests (Python 3.8-3.11)
  - Frontend tests (Node.js 18.x, 20.x)
  - Integration tests
  - Security scanning
  - Code quality checks
  - Build and deploy (main branch only)

### 2. Release Workflow (`.github/workflows/release.yml`)
- **Triggers**: Git tags starting with 'v' (e.g., v1.0.0)
- **Jobs**:
  - Create GitHub release
  - Build release artifacts for multiple platforms
  - Build and push Docker images with version tags

### 3. Dependency Updates (`.github/workflows/dependency-update.yml`)
- **Triggers**: Weekly schedule (Mondays at 9 AM UTC), Manual trigger
- **Jobs**:
  - Update Python dependencies
  - Update Node.js dependencies
  - Security audit
  - Create pull requests for updates

## Creating Your First Release

To create a release:

1. Tag your commit:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

2. The release workflow will automatically:
   - Create a GitHub release
   - Build artifacts for different platforms
   - Build and push Docker images

## Monitoring and Maintenance

### GitHub Actions Usage
- Monitor your GitHub Actions usage in Settings → Billing
- Public repositories get unlimited GitHub Actions minutes
- Private repositories have monthly limits

### Security Alerts
- Enable Dependabot alerts in Settings → Security & analysis
- Review and address security vulnerabilities promptly

### Code Quality
- Set up branch protection rules to require status checks
- Use pull request reviews for code quality
- Monitor test coverage and code quality metrics

## Troubleshooting

### Common Issues:

1. **Workflow fails due to missing secrets**
   - Check that all required secrets are set in repository settings
   - Verify secret names match exactly what's used in workflows

2. **Docker build fails**
   - Ensure Docker Hub credentials are correct
   - Check that repository names exist in Docker Hub

3. **Tests fail**
   - Review test logs in the Actions tab
   - Ensure all dependencies are properly specified

4. **Permission errors**
   - Check that the GITHUB_TOKEN has necessary permissions
   - For organization repositories, verify organization settings

## Next Steps

After setting up the repository:

1. **Development Workflow**:
   - Create feature branches for new development
   - Use pull requests for code review
   - Merge to main after CI passes

2. **Deployment**:
   - Set up staging and production environments
   - Configure deployment targets in the CI/CD workflow
   - Set up monitoring and logging

3. **Community**:
   - Add contributing guidelines
   - Set up issue templates
   - Create a code of conduct

4. **Documentation**:
   - Keep README.md updated
   - Add API documentation
   - Create user guides and tutorials

## Support

If you encounter issues:
- Check the GitHub Actions logs for detailed error messages
- Review the workflow files for configuration issues
- Consult GitHub Actions documentation
- Open an issue in the repository for help

---

**Note**: This setup provides a production-ready CI/CD pipeline with comprehensive testing, security scanning, and automated deployments. Customize the workflows according to your specific needs and infrastructure requirements.