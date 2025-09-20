# 🔐 GitHub Secrets Configuration Guide

## 📋 Required Secrets for CI/CD Pipeline

Your CI/CD pipeline requires the following secrets to be configured in your GitHub repository:

---

## 🎯 **Required Secrets**

### 1. **DOCKER_HUB_USERNAME**
- **Purpose**: Your Docker Hub username for authentication
- **Value**: Your Docker Hub username (e.g., `rayyan9477`)

### 2. **DOCKER_HUB_ACCESS_TOKEN**
- **Purpose**: Docker Hub access token for secure authentication
- **Value**: Generated Docker Hub access token (NOT your password)

---

## 🛠️ **Step-by-Step Setup Instructions**

### **Step 1: Create Docker Hub Access Token**

1. **Go to Docker Hub**:
   - Visit: https://hub.docker.com
   - Sign in to your Docker Hub account

2. **Navigate to Security Settings**:
   - Click on your profile (top-right)
   - Select **"Account Settings"**
   - Go to **"Security"** tab

3. **Generate New Access Token**:
   - Click **"New Access Token"**
   - **Token Description**: `GitHub-Actions-CI-CD`
   - **Access Permissions**: Select **"Read, Write, Delete"**
   - Click **"Generate"**

4. **Copy the Token**:
   - ⚠️ **IMPORTANT**: Copy the token immediately!
   - You won't be able to see it again
   - Store it securely

### **Step 2: Configure GitHub Repository Secrets**

1. **Go to Your Repository**:
   - Navigate to your GitHub repository
   - Example: `https://github.com/yourusername/House-Price-Prediction-Model`

2. **Access Settings**:
   - Click the **"Settings"** tab (top navigation)
   - Scroll down to **"Security"** section in sidebar
   - Click **"Secrets and variables"**
   - Select **"Actions"**

3. **Add DOCKER_HUB_USERNAME**:
   - Click **"New repository secret"**
   - **Name**: `DOCKER_HUB_USERNAME`
   - **Secret**: Your Docker Hub username (e.g., `rayyan9477`)
   - Click **"Add secret"**

4. **Add DOCKER_HUB_ACCESS_TOKEN**:
   - Click **"New repository secret"**
   - **Name**: `DOCKER_HUB_ACCESS_TOKEN`
   - **Secret**: Paste the access token from Step 1
   - Click **"Add secret"**

---

## ✅ **Verification Steps**

### **Check Secrets Are Configured**:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. You should see:
   ```
   ✅ DOCKER_HUB_USERNAME
   ✅ DOCKER_HUB_ACCESS_TOKEN
   ```

### **Test Docker Hub Connection** (Optional):

```bash
# Test locally (optional)
echo $DOCKER_HUB_ACCESS_TOKEN | docker login -u $DOCKER_HUB_USERNAME --password-stdin
```

---

## 🔄 **How Secrets Are Used in Workflows**

### **In deploy.yml**:

```yaml
- name: Log in to Docker Hub
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKER_HUB_USERNAME }}
    password: ${{ secrets.DOCKER_HUB_ACCESS_TOKEN }}
```

### **In Docker Image Naming**:

```yaml
images: ${{ secrets.DOCKER_HUB_USERNAME }}/house-price-prediction
```

---

## 🚨 **Security Best Practices**

### **Do's**:
- ✅ Use access tokens instead of passwords
- ✅ Set minimal required permissions
- ✅ Regularly rotate access tokens
- ✅ Use descriptive names for tokens
- ✅ Monitor token usage

### **Don'ts**:
- ❌ Never commit secrets to code
- ❌ Don't share tokens in chat/email
- ❌ Don't use personal passwords
- ❌ Don't set overly broad permissions
- ❌ Don't forget to revoke unused tokens

---

## 🔧 **Troubleshooting**

### **Common Issues**:

1. **"Invalid credentials" error**:
   - ✅ Verify username is correct
   - ✅ Regenerate access token
   - ✅ Check token permissions

2. **"Repository not found" error**:
   - ✅ Verify Docker Hub username
   - ✅ Check image naming in workflow

3. **"Access denied" error**:
   - ✅ Ensure token has Write permissions
   - ✅ Check repository exists on Docker Hub

### **Debug Steps**:

1. **Check Secrets in Repository**:
   ```
   Settings → Secrets and variables → Actions
   ```

2. **Verify Token is Active**:
   - Go to Docker Hub Security settings
   - Check token last used date

3. **Test Workflow**:
   - Create a test push to trigger workflow
   - Check GitHub Actions logs for detailed errors

---

## 📊 **Expected Workflow Behavior**

### **After Secrets Configuration**:

1. **Code Quality Workflow** (dev branch):
   - ✅ Runs without secrets (uses GITHUB_TOKEN automatically)

2. **Testing Workflow** (test branch):
   - ✅ Runs without secrets (uses GITHUB_TOKEN automatically)

3. **Deployment Workflow** (master branch):
   - ✅ Authenticates with Docker Hub using secrets
   - ✅ Builds and pushes Docker image
   - ✅ Creates GitHub issue notification

---

## 🎯 **Quick Setup Checklist**

- [ ] **Docker Hub Account Created**
- [ ] **Access Token Generated** (with Read/Write/Delete permissions)
- [ ] **DOCKER_HUB_USERNAME** secret added to GitHub
- [ ] **DOCKER_HUB_ACCESS_TOKEN** secret added to GitHub
- [ ] **Secrets visible in repository settings**
- [ ] **Test workflow triggered successfully**

---

## 📝 **Example Values**

### **For User: rayyan9477**

```bash
# In GitHub Secrets:
DOCKER_HUB_USERNAME = rayyan9477
DOCKER_HUB_ACCESS_TOKEN = dckr_pat_1234567890abcdef...

# Resulting Docker Image:
rayyan9477/house-price-prediction:latest
```

---

## 🔗 **Useful Links**

- [Docker Hub Security Settings](https://hub.docker.com/settings/security)
- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Docker Login Action](https://github.com/docker/login-action)

---

## ⚡ **Quick Commands**

### **Test Docker Hub Authentication**:
```bash
# Create test token and verify
docker login -u your_username
```

### **View Repository Secrets**:
```bash
# Using GitHub CLI
gh secret list
```

### **Test Workflow Locally**:
```bash
# Act (GitHub Actions local runner)
act push
```

---

## 🎉 **Success Indicators**

Once secrets are properly configured, you should see:

1. ✅ **Green checkmarks** in GitHub Actions
2. ✅ **Docker image** appears in your Docker Hub repository
3. ✅ **GitHub issue** created with deployment notification
4. ✅ **No authentication errors** in workflow logs

---

**🔐 Your secrets are now properly configured for the CI/CD pipeline!**