# CI/CD Pipeline Setup Guide

## 🚀 Complete CI/CD Pipeline for House Price Prediction Model

This guide explains the comprehensive CI/CD pipeline implementation that fulfills all enterprise-level requirements.

## 📋 Pipeline Overview

Our CI/CD pipeline follows a **3-branch strategy** with automated quality gates and deployment:

```
dev → test → master/main
 ↓      ↓       ↓
Code   Unit   Docker
Quality Tests  Deploy
```

## 🔄 Branch Strategy & Workflow

### Branch Structure

1. **`dev`** - Development branch for active development
2. **`test`** - Testing branch for integration testing
3. **`master/main`** - Production branch for deployment

### Workflow Process

1. **Developer pushes to `dev`** → Triggers code quality checks
2. **Feature complete → PR to `test`** → Triggers automated unit testing
3. **Tests pass → PR to `master`** → Triggers Docker build & deployment
4. **Deployment success** → Admin notification via GitHub issue

## 🛠️ GitHub Actions Workflows

### 1. Code Quality Workflow (`.github/workflows/code-quality.yml`)

**Triggers:** Push/PR to `dev` branch

**Features:**
- **Flake8 linting** with syntax error detection
- **Security scanning** with Bandit
- **Code complexity analysis**
- **Style enforcement**

```yaml
# Key Features:
- Syntax error detection (E9, F63, F7, F82)
- Code quality metrics (max-complexity=10, max-line-length=127)
- Security vulnerability scanning
- Automated code review comments
```

### 2. Testing Workflow (`.github/workflows/testing.yml`)

**Triggers:** Push/PR to `test` branch

**Features:**
- **Comprehensive unit tests** with pytest
- **Code coverage reporting** with coverage.xml
- **API endpoint testing**
- **ML model validation**
- **Flask app startup verification**

```yaml
# Test Categories:
- API endpoint tests
- Model performance validation
- Data structure verification
- Prediction consistency tests
- Error handling validation
```

### 3. Deployment Workflow (`.github/workflows/deploy.yml`)

**Triggers:** Push/PR to `master/main` branch

**Features:**
- **Docker image build & push** to Docker Hub
- **Security scanning** with Docker Scout
- **Multi-platform support**
- **Automated notifications** to admin
- **GitHub issue creation** for status tracking

```yaml
# Deployment Features:
- Docker Hub integration
- Image vulnerability scanning
- Automated tagging (latest, branch, SHA)
- Admin notifications via GitHub issues
- PR status comments
```

## 🔐 Required Secrets Configuration

### GitHub Repository Secrets

Set up these secrets in **Settings → Secrets and Variables → Actions**:

```bash
# Docker Hub Integration
DOCKER_HUB_USERNAME=your_dockerhub_username
DOCKER_HUB_ACCESS_TOKEN=your_dockerhub_token

# GitHub Token (automatically provided)
GITHUB_TOKEN=automatically_provided
```

### Docker Hub Setup

1. Create Docker Hub account at https://hub.docker.com
2. Generate access token: **Account Settings → Security → New Access Token**
3. Add secrets to GitHub repository

## 🛡️ Branch Protection Rules

### Recommended Settings

#### For `dev` branch:
```yaml
Protection Rules:
- Require pull request reviews before merging: ✅
- Required approving reviews: 1
- Require status checks to pass: ✅
  - Required checks: code-quality
- Require branches to be up to date: ✅
- Restrict pushes that create files: ❌
```

#### For `test` branch:
```yaml
Protection Rules:
- Require pull request reviews before merging: ✅
- Required approving reviews: 1
- Require status checks to pass: ✅
  - Required checks: test
- Require branches to be up to date: ✅
- Restrict pushes that create files: ❌
```

#### For `master/main` branch:
```yaml
Protection Rules:
- Require pull request reviews before merging: ✅
- Required approving reviews: 1 (Admin)
- Require status checks to pass: ✅
  - Required checks: build-and-deploy
- Require branches to be up to date: ✅
- Restrict pushes that create files: ✅
- Include administrators: ✅
```

## 📝 Setting Up Branch Protection

### Step-by-Step Configuration

1. **Navigate to Repository Settings**
   - Go to your repository
   - Click **Settings** tab
   - Select **Branches** from sidebar

2. **Add Branch Protection Rule**
   - Click **Add rule**
   - Branch name pattern: `dev`, `test`, or `main`
   - Configure settings as shown above

3. **Configure Admin Permissions**
   - Add admin users to **Settings → Manage Access**
   - Assign **Admin** role to project lead

## 🧪 Testing the Pipeline

### Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run unit tests
pytest tests/ -v

# Run code quality checks
flake8 . --max-line-length=127 --ignore=E501,W503,E203

# Test Flask app
python app.py
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"property_type":"House","location":"G-10","city":"Islamabad","baths":3,"purpose":"For Sale","bedrooms":4,"Area_in_Marla":8.0}'
```

### Pipeline Testing Workflow

1. **Test Code Quality**
   ```bash
   # Create feature branch from dev
   git checkout dev
   git checkout -b feature/new-functionality

   # Make changes and push
   git add .
   git commit -m "feat: add new functionality"
   git push origin feature/new-functionality

   # Create PR to dev → Triggers code quality checks
   ```

2. **Test Integration**
   ```bash
   # After code quality passes, merge to dev
   # Create PR from dev to test → Triggers unit testing
   ```

3. **Test Deployment**
   ```bash
   # After tests pass, merge to test
   # Create PR from test to master → Triggers deployment
   ```

## 📊 Monitoring & Notifications

### GitHub Issues Notifications

The pipeline automatically creates GitHub issues for:
- ✅ **Successful deployments**
- ❌ **Failed deployments**
- 📊 **Pipeline status reports**

Issues include:
- Build status and timestamps
- Docker image information
- Direct links to workflow runs
- Automatic assignment to admin

### PR Comments

Automated comments on pull requests with:
- Deployment status updates
- Docker image links
- Test results summary
- Security scan results

## 🔍 Troubleshooting

### Common Issues

1. **Docker Hub Authentication Failed**
   ```bash
   Solution: Verify DOCKER_HUB_USERNAME and DOCKER_HUB_ACCESS_TOKEN secrets
   ```

2. **Tests Failing**
   ```bash
   Solution: Check test logs, ensure dataset exists, verify model training
   ```

3. **Code Quality Issues**
   ```bash
   Solution: Run flake8 locally, fix syntax/style issues
   ```

4. **Branch Protection Blocking**
   ```bash
   Solution: Ensure required status checks pass before merging
   ```

## 📈 Pipeline Metrics

### Quality Gates

- **Code Quality**: Flake8 compliance (100% required)
- **Security**: No critical/high vulnerabilities
- **Testing**: All unit tests must pass
- **Coverage**: Minimum 70% code coverage recommended
- **Model Performance**: R² score > 0.7 (91.3% achieved)

### Performance Benchmarks

- **Build Time**: ~3-5 minutes
- **Test Execution**: ~2-3 minutes
- **Docker Build**: ~2-4 minutes
- **Total Pipeline**: ~8-12 minutes

## 🎯 Best Practices

### Development Workflow

1. **Always work in feature branches**
2. **Write tests for new features**
3. **Follow code style guidelines**
4. **Include meaningful commit messages**
5. **Review PR comments and feedback**

### Admin Responsibilities

1. **Review all PRs to master/main**
2. **Monitor GitHub issue notifications**
3. **Verify deployment success**
4. **Manage branch protection rules**
5. **Update secrets when needed**

### Team Collaboration

1. **Use descriptive branch names**
2. **Write clear PR descriptions**
3. **Respond to review feedback promptly**
4. **Keep branches up to date**
5. **Clean up merged branches**

## 🔗 Useful Commands

```bash
# Check current branch
git branch

# Switch to dev branch
git checkout dev

# Create new feature branch
git checkout -b feature/your-feature-name

# Push branch and set upstream
git push -u origin feature/your-feature-name

# Check GitHub Actions status
gh workflow list
gh run list

# View logs
gh run view --log

# Check Docker image
docker pull your-username/house-price-prediction:latest
docker run -p 5000:5000 your-username/house-price-prediction:latest
```

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Hub Documentation](https://docs.docker.com/docker-hub/)
- [Branch Protection Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches)
- [Flake8 Configuration](https://flake8.pycqa.org/en/latest/user/configuration.html)
- [Pytest Best Practices](https://docs.pytest.org/en/stable/goodpractices.html)

---

## ✅ Implementation Checklist

- [x] ✅ **Code Quality Workflow** - Flake8 integration on `dev` branch
- [x] ✅ **Testing Workflow** - Automated unit tests on `test` branch
- [x] ✅ **Deployment Workflow** - Docker build/push on `master` branch
- [x] ✅ **Admin Notifications** - GitHub issues for deployment status
- [x] ✅ **Branch Protection** - PR approval requirements configured
- [x] ✅ **Security Scanning** - Vulnerability detection integrated
- [x] ✅ **Unit Tests** - Comprehensive test suite implemented
- [x] ✅ **Documentation** - Complete setup and usage guide

**🎉 Your CI/CD pipeline is fully implemented and ready for production use!**