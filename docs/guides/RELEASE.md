# Release Process

This document describes how to create and publish a new release of the Auto Bot Trader Pro i18n platform.

## Overview

The project uses semantic versioning (MAJOR.MINOR.PATCH) and publishes Docker images to GitHub Container Registry (ghcr.io).

## Creating a New Release

### Method 1: Using the Release Script (Recommended)

The easiest way to create a release is using the provided `release.sh` script:

1. **Update CHANGELOG.md**
   - Add a new version section at the top
   - Document all changes, additions, fixes, and security updates
   - Follow the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format

2. **Commit and Push Changes**
   ```bash
   git add CHANGELOG.md
   git commit -m "chore: prepare release v1.0.0"
   git push origin main
   ```

3. **Run the Release Script**
   ```bash
   ./release.sh 1.0.0
   ```
   The script will:
   - Verify you're on the correct branch
   - Check that CHANGELOG.md is updated
   - Create an annotated git tag
   - Prompt you to push the tag to GitHub
   - Display instructions for monitoring the release workflow

4. **Automated Workflow**
   - The `release.yml` workflow will automatically:
     - Create a GitHub release with changelog notes
     - Build Docker images for frontend and backend
     - Tag images with version numbers
     - Push images to ghcr.io

### Method 2: Manual Tag

1. **Update CHANGELOG.md**
   - Add a new version section at the top
   - Document all changes, additions, fixes, and security updates
   - Follow the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format

2. **Commit and Push Changes**
   ```bash
   git add CHANGELOG.md
   git commit -m "chore: prepare release v1.0.0"
   git push origin main
   ```

3. **Create and Push a Version Tag**
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

4. **Automated Workflow**
   - The `release.yml` workflow will automatically:
     - Create a GitHub release with changelog notes
     - Build Docker images for frontend and backend
     - Tag images with version numbers
     - Push images to ghcr.io

### Method 3: Manual Workflow Dispatch

1. **Update CHANGELOG.md** (same as Method 1)

2. **Trigger Workflow Manually**
   - Go to Actions → Release and Publish
   - Click "Run workflow"
   - Enter the version number (e.g., 1.0.0)
   - Click "Run workflow"

## Published Artifacts

After a successful release, the following Docker images are published:

- `ghcr.io/<owner>/abtpi18n-frontend:latest`
- `ghcr.io/<owner>/abtpi18n-frontend:1.0.0`
- `ghcr.io/<owner>/abtpi18n-frontend:1.0`
- `ghcr.io/<owner>/abtpi18n-frontend:1`
- `ghcr.io/<owner>/abtpi18n-backend:latest`
- `ghcr.io/<owner>/abtpi18n-backend:1.0.0`
- `ghcr.io/<owner>/abtpi18n-backend:1.0`
- `ghcr.io/<owner>/abtpi18n-backend:1`

## Using Published Images

### Pull Images

```bash
# Pull latest version
docker pull ghcr.io/<owner>/abtpi18n-frontend:latest
docker pull ghcr.io/<owner>/abtpi18n-backend:latest

# Pull specific version
docker pull ghcr.io/<owner>/abtpi18n-frontend:1.0.0
docker pull ghcr.io/<owner>/abtpi18n-backend:1.0.0
```

### Update docker-compose.yml

Instead of building locally, you can use published images:

```yaml
services:
  frontend:
    image: ghcr.io/<owner>/abtpi18n-frontend:1.0.0
    # Remove 'build' section
    container_name: abt_frontend
    restart: unless-stopped
    # ... rest of config

  backend:
    image: ghcr.io/<owner>/abtpi18n-backend:1.0.0
    # Remove 'build' section
    container_name: abt_backend
    restart: unless-stopped
    # ... rest of config

  worker:
    image: ghcr.io/<owner>/abtpi18n-backend:1.0.0
    # Remove 'build' section
    container_name: abt_worker
    restart: unless-stopped
    command: ["python", "worker.py"]
    # ... rest of config
```

## Versioning Guidelines

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (1.0.0 → 2.0.0): Breaking changes, incompatible API changes
- **MINOR** (1.0.0 → 1.1.0): New features, backward-compatible
- **PATCH** (1.0.0 → 1.0.1): Bug fixes, backward-compatible

## Rollback

If a release has issues:

1. **Revert to Previous Version**
   ```bash
   docker-compose down
   # Update docker-compose.yml to use previous version
   docker-compose up -d
   ```

2. **Create Hotfix Release**
   - Fix the issue in code
   - Update CHANGELOG.md
   - Create a new patch version tag (e.g., v1.0.1)

## Security Considerations

- All Docker images are scanned during build
- Security scanning runs via CodeQL, Bandit, and Semgrep
- Review security alerts before releasing
- Document security fixes in CHANGELOG.md

## CI/CD Pipeline

The release workflow includes:

1. **Create Release** job:
   - Extracts version from tag
   - Reads changelog for release notes
   - Creates GitHub release

2. **Build and Push Images** job:
   - Builds Docker images for frontend and backend
   - Tags with semantic versions
   - Pushes to GitHub Container Registry
   - Uses build cache for efficiency

## Troubleshooting

### Workflow Fails
- Check GitHub Actions logs
- Ensure GITHUB_TOKEN has packages:write permission
- Verify Dockerfiles are valid

### Image Pull Fails
- Authenticate with ghcr.io: `echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin`
- Ensure repository visibility matches your needs (public/private)

### Version Tag Already Exists
- Delete local tag: `git tag -d v1.0.0`
- Delete remote tag: `git push origin :refs/tags/v1.0.0`
- Create new tag with correct version
