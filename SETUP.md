# House Price Prediction CI/CD Pipeline Setup Guide

## Overview
This guide explains how to set up the complete CI/CD pipeline for the House Price Prediction project.

## Prerequisites
1. GitHub account with repository access
2. Docker Hub account
3. Email account with app-specific password (for Gmail)

## Setup Instructions

### 1. GitHub Repository Configuration

#### Branch Protection Rules
Set up branch protection for `main` and `test` branches:

1. Go to Settings → Branches
2. Add rule for `main` branch:
   - Require pull request reviews before merging
   - Require status checks to pass before merging
   - Require conversation resolution before merging
   - Restrict pushes that create files larger than 100MB

3. Add rule for `test` branch:
   - Require status checks to pass before merging
   - Require review from code owners

#### Required Secrets
Configure the following secrets in Settings → Secrets and variables → Actions:

| Secret Name | Description | How to Get |
|-------------|-------------|------------|
| `DOCKER_HUB_USERNAME` | Your Docker Hub username | Your Docker Hub account username |
| `DOCKER_HUB_ACCESS_TOKEN` | Docker Hub access token | Generate in Docker Hub → Account Settings → Security |
| `EMAIL_USERNAME` | SMTP email address | Your Gmail address |
| `EMAIL_PASSWORD` | App-specific password | Generate in Google Account → Security → App passwords |

### 2. Docker Hub Setup

1. Create Docker Hub account at https://hub.docker.com
2. Create a new repository named `house-price-prediction`
3. Generate access token:
   - Go to Account Settings → Security
   - Click "New Access Token"
   - Give it a descriptive name
   - Copy the token (save it for GitHub secrets)

### 3. Email Configuration

#### For Gmail:
1. Enable 2-factor authentication
2. Go to Google Account → Security → App passwords
3. Generate an app password for "Mail"
4. Use this password in the `EMAIL_PASSWORD` secret

### 4. Local Development Setup

```bash
# Clone repository
git clone https://github.com/Rayyan9477/House-Price-Prediction-Model.git
cd House-Price-Prediction-Model

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests locally
pytest tests/ -v

# Run the application
python app.py
```

### 5. Workflow Testing

#### Testing Code Quality Workflow:
```bash
git checkout dev
# Make some changes
git add .
git commit -m "test: trigger code quality checks"
git push origin dev
```

#### Testing Full Pipeline:
```bash
# 1. Create feature branch
git checkout dev
git checkout -b feature/test-pipeline

# 2. Make changes and push to dev
git add .
git commit -m "feat: test complete pipeline"
git push origin feature/test-pipeline

# 3. Create PR to dev (triggers code quality)
# 4. Merge to dev, then create PR to test (triggers testing)
# 5. Merge to test, then create PR to main (triggers deployment)
```

## Workflow Details

### Code Quality Workflow (`code-quality.yml`)
- **Triggers**: Push/PR to `dev` branch
- **Actions**:
  - Python syntax validation
  - flake8 linting
  - Security scanning with bandit
  - Code complexity analysis

### Testing Workflow (`testing.yml`)
- **Triggers**: Push/PR to `test` branch
- **Actions**:
  - Unit test execution
  - Code coverage reporting
  - API endpoint validation
  - Flask startup testing

### Deployment Workflow (`deploy.yml`)
- **Triggers**: Push/PR to `main` branch
- **Actions**:
  - Docker image build
  - Push to Docker Hub
  - Container security scan
  - Email notification

## Troubleshooting

### Common Issues

#### 1. Workflow Permissions
If workflows fail with permission errors:
- Go to Settings → Actions → General
- Set "Workflow permissions" to "Read and write permissions"

#### 2. Docker Hub Push Fails
- Verify `DOCKER_HUB_USERNAME` and `DOCKER_HUB_ACCESS_TOKEN` are correct
- Ensure Docker Hub repository exists and is public

#### 3. Email Notifications Not Working
- Verify Gmail app password is correct
- Check that 2FA is enabled on Google account
- Ensure EMAIL_USERNAME and EMAIL_PASSWORD secrets are set

#### 4. Tests Failing
- Check that all dependencies are in requirements.txt
- Verify dataset file `House_dataset.csv` is committed
- Run tests locally first: `pytest tests/ -v`

### Monitoring and Maintenance

#### Viewing Workflow Status
- Go to Actions tab in GitHub repository
- Click on specific workflow runs to see detailed logs
- Check for failed steps and error messages

#### Updating Dependencies
```bash
# Update requirements.txt with new versions
pip freeze > requirements.txt

# Test locally before committing
pytest tests/
python app.py
```

#### Monitoring Docker Images
- Check Docker Hub for successful pushes
- Monitor image size and security vulnerabilities
- Set up automated vulnerability scanning

## Best Practices

1. **Always test locally** before pushing to dev
2. **Write tests** for new features
3. **Keep commits small** and focused
4. **Use descriptive commit messages**
5. **Review code** before merging PRs
6. **Monitor workflow execution** regularly
7. **Update dependencies** regularly
8. **Document changes** in README

## Support

For issues with the CI/CD pipeline:
1. Check workflow logs in GitHub Actions
2. Verify all secrets are configured correctly
3. Test individual components locally
4. Contact repository maintainers

## Security Considerations

1. **Never commit secrets** to the repository
2. **Use app-specific passwords** for email
3. **Regularly rotate access tokens**
4. **Monitor for security vulnerabilities**
5. **Keep dependencies updated**
6. **Review third-party actions** before use