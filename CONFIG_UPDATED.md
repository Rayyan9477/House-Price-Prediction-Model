# Updated Configuration Details

## Email and Docker Configuration

### Email Notifications
- **Recipient Email**: i222489@nu.edu.pk
- **Configured in**: `.github/workflows/deploy.yml`
- **Triggers**: On successful/failed deployments to master branch

### Docker Hub Configuration
- **Username**: rayyan9477
- **Repository**: house-price-prediction
- **Image Tags**: latest, branch-specific, SHA-based

## Required GitHub Secrets

Set these secrets in your GitHub repository (Settings → Secrets and variables → Actions):

| Secret Name | Value | Description |
|-------------|--------|-------------|
| `DOCKER_HUB_USERNAME` | `rayyan9477` | Docker Hub username |
| `DOCKER_HUB_ACCESS_TOKEN` | `<your-token>` | Docker Hub access token |
| `EMAIL_USERNAME` | `<your-gmail>` | Gmail address for sending notifications |
| `EMAIL_PASSWORD` | `<app-password>` | Gmail app-specific password |

## How to Get Docker Hub Access Token

1. Go to [Docker Hub](https://hub.docker.com)
2. Login with username: `rayyan9477`
3. Go to Account Settings → Security
4. Click "New Access Token"
5. Give it a name (e.g., "GitHub Actions")
6. Copy the token and add it to GitHub secrets

## How to Get Gmail App Password

1. Enable 2-Factor Authentication on your Google account
2. Go to Google Account → Security → App passwords
3. Generate a new app password for "Mail"
4. Use this password in the `EMAIL_PASSWORD` secret

## Testing the Pipeline

Once secrets are configured:

```bash
# 1. Make changes in dev branch
git checkout dev
git add .
git commit -m "feat: test pipeline"
git push origin dev

# 2. Create PR from dev → test
# 3. Create PR from test → master
# 4. Watch notifications arrive at i222489@nu.edu.pk
```

## Email Notification Format

The email will include:
- Repository: House-Price-Prediction-Model
- Branch: master
- Commit SHA
- Build Status: success/failure
- Workflow URL for detailed logs
- Timestamp of deployment

## Docker Image Access

After successful deployment:
```bash
docker pull rayyan9477/house-price-prediction:latest
docker run -p 5000:5000 rayyan9477/house-price-prediction:latest
```

Access the API at: http://localhost:5000