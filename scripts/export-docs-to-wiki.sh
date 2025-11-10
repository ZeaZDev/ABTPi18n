#!/bin/bash

# Export Documentation to GitHub Wiki
# This script exports all documentation from the repository to the GitHub Wiki

set -e

REPO_NAME="ABTPi18n"
WIKI_URL="https://github.com/ZeaZDev/${REPO_NAME}.wiki.git"
WIKI_DIR="tmp/${REPO_NAME}.wiki"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Exporting Documentation to Wiki ===${NC}"

# Clean up old wiki clone if it exists
if [ -d "$WIKI_DIR" ]; then
    echo -e "${YELLOW}Removing old wiki clone...${NC}"
    rm -rf "$WIKI_DIR"
fi

# Create tmp directory if it doesn't exist
mkdir -p tmp

# Clone the wiki repository
echo -e "${GREEN}Cloning wiki repository...${NC}"
if ! git clone "$WIKI_URL" "$WIKI_DIR" 2>/dev/null; then
    echo -e "${RED}Failed to clone wiki repository.${NC}"
    echo -e "${YELLOW}The wiki might not be initialized yet. Please:${NC}"
    echo "1. Go to https://github.com/ZeaZDev/${REPO_NAME}/wiki"
    echo "2. Click 'Create the first page' to initialize the wiki"
    echo "3. Run this script again"
    exit 1
fi

cd "$WIKI_DIR"

# Function to convert file path to wiki page name
# Example: docs/guides/SECURITY.md -> Guides-Security
convert_to_wiki_name() {
    local filepath="$1"
    # Remove .md extension
    local name="${filepath%.md}"
    # Remove docs/ prefix
    name="${name#docs/}"
    # Remove tools/ prefix
    name="${name#tools/}"
    # Replace / with -
    name="${name//\//-}"
    # Convert to Title Case (capitalize first letter of each word)
    # Keep the original case for acronyms like README, API, etc.
    echo "$name"
}

# Function to copy and convert markdown file
copy_doc_file() {
    local src_file="$1"
    local wiki_name
    local dest_file
    
    wiki_name="$(convert_to_wiki_name "$src_file")"
    dest_file="${wiki_name}.md"
    
    echo "  Copying: $src_file -> $dest_file"
    
    # Copy the file
    cp "$REPO_ROOT/$src_file" "$dest_file"
    
    # Update internal links to work with wiki format
    # Convert [Link](../path/to/file.md) to [Link](Wiki-Page-Name)
    # This is a basic conversion - may need refinement based on actual link patterns
    sed -i 's|\](docs/|\](|g' "$dest_file"
    sed -i 's|\](tools/|\](|g' "$dest_file"
    sed -i 's|/|\-|g' "$dest_file" 2>/dev/null || true
}

# Create Home page with navigation
echo -e "${GREEN}Creating Home page...${NC}"
cat > Home.md << 'EOF'
# ABTPro i18n Wiki

Welcome to the Auto Bot Trader Pro (ABTPro) i18n documentation wiki.

## Quick Navigation

### Getting Started
- [Main README](README) - Project overview and quick start
- [Installation Guide](setup-INSTALLER_PLATFORM_REQUIREMENTS) - Platform requirements
- [GitHub Setup](setup-GITHUB-SETUP) - GitHub configuration
- [Contributing Guide](guides-CONTRIBUTING) - Development setup and workflow

### Core Documentation
- [Security Model](guides-SECURITY) - Encryption and security practices
- [Roadmap](guides-ROADMAP) - Project phases and progress
- [Release Process](guides-RELEASE) - Creating releases

### Integration & Setup
- [TradingView Integration](integrations-TRADINGVIEW_INTEGRATION) - Connect TradingView alerts
- [Google Drive Integration](integration-GOOGLE_DRIVE_INTEGRATION) - Google Drive setup
- [Google Drive Loader Guide](guides-GDRIVE_LOADER_GUIDE) - Using the GDrive loader

### Strategy Development
- [Strategy Guide](strategy-STRATEGY_GUIDE) - Creating trading strategies
- [Strategy Implementation Notes](strategy-STRATEGY_IMPLEMENTATION_NOTES) - Implementation details
- [DR/Failover Strategy](strategy-DR_FAILOVER_STRATEGY) - Disaster recovery

### Tools Documentation
- [Tools README](tools-README) - Tools overview
- [Tools Architecture](tools-ARCHITECTURE) - Architecture documentation
- [Tools Examples](tools-EXAMPLES) - Usage examples
- [Tools Summary](tools-SUMMARY) - Tools summary
- [Screenshot Tool](tools-README_SCREENSHOTS) - Automated screenshot capture

### Phase Documentation

#### Phase 1: Foundation & Security
- [Phase 1 Guide](phases-phase1-PHASE1_GUIDE)
- [Phase 1 Summary](phases-phase1-PHASE1_SUMMARY)
- [Phase 1 Implementation](phases-phase1-PHASE1_IMPLEMENTATION_SUMMARY)

#### Phase 2: Strategy Engine & Risk Management
- [Phase 2 Guide](phases-phase2-PHASE2_GUIDE)
- [Phase 2 Summary](phases-phase2-PHASE2_SUMMARY)
- [Phase 2 Implementation](phases-phase2-PHASE2_IMPLEMENTATION_SUMMARY)

#### Phase 3: i18n Dashboard & Authentication
- [Phase 3 Guide](phases-phase3-PHASE3_GUIDE)
- [Phase 3 Summary](phases-phase3-PHASE3_SUMMARY)
- [Phase 3 Implementation](phases-phase3-PHASE3_IMPLEMENTATION_SUMMARY)

#### Phase 4: Advanced Risk & Monetization
- [Phase 4 Guide](phases-phase4-PHASE4_GUIDE)
- [Phase 4 Summary](phases-phase4-PHASE4_SUMMARY)
- [Phase 4 Implementation](phases-phase4-PHASE4_IMPLEMENTATION_SUMMARY)

#### Phase 5: Compliance & Audit
- [Phase 5 Guide](phases-phase5-PHASE5_GUIDE)
- [Phase 5 Summary](phases-phase5-PHASE5_SUMMARY)
- [Phase 5 Implementation](phases-phase5-PHASE5_IMPLEMENTATION_SUMMARY)
- [Phase 5 Quick Start](phases-phase5-PHASE5_QUICK_START)
- [Phase 5 Migration](phases-phase5-PHASE5_MIGRATION_GUIDE)

#### Phase 6: ML / Intelligence
- [Phase 6 Guide](phases-phase6-PHASE6_GUIDE)
- [Phase 6 Summary](phases-phase6-PHASE6_SUMMARY)
- [Phase 6 Implementation](phases-phase6-PHASE6_IMPLEMENTATION_SUMMARY)
- [Phase 6 Quick Start](phases-phase6-PHASE6_QUICK_START)

### Additional Resources
- [Changelog](CHANGELOG) - Version history
- [TradingView Summary](TRADINGVIEW_SUMMARY) - TradingView integration summary
- [Documentation Index](README-docs) - Complete documentation index

---

**Note:** This wiki is automatically generated from the repository documentation.
To update this wiki, modify the documentation files in the repository and run `scripts/export-docs-to-wiki.sh`.
EOF

# Copy main README
echo -e "${GREEN}Copying main README...${NC}"
cp "$REPO_ROOT/README.md" "README.md"

# Copy CHANGELOG
echo -e "${GREEN}Copying CHANGELOG...${NC}"
cp "$REPO_ROOT/CHANGELOG.md" "CHANGELOG.md"

# Copy all documentation files
echo -e "${GREEN}Copying documentation files...${NC}"

# Find and copy all .md files from docs/ directory
find "$REPO_ROOT/docs" -name "*.md" -type f | while read -r file; do
    relative_path="${file#"$REPO_ROOT"/}"
    copy_doc_file "$relative_path"
done

# Copy tools documentation
echo -e "${GREEN}Copying tools documentation...${NC}"
find "$REPO_ROOT/tools" -name "*.md" -type f | while read -r file; do
    relative_path="${file#"$REPO_ROOT"/}"
    copy_doc_file "$relative_path"
done

# Create a sidebar (if wiki supports it)
echo -e "${GREEN}Creating sidebar...${NC}"
cat > _Sidebar.md << 'EOF'
## Navigation

### Getting Started
- [Home](Home)
- [README](README)
- [Contributing](guides-CONTRIBUTING)

### Guides
- [Security](guides-SECURITY)
- [Roadmap](guides-ROADMAP)
- [Release](guides-RELEASE)

### Setup
- [GitHub Setup](setup-GITHUB-SETUP)
- [Platform Requirements](setup-INSTALLER_PLATFORM_REQUIREMENTS)

### Strategy
- [Strategy Guide](strategy-STRATEGY_GUIDE)
- [DR/Failover](strategy-DR_FAILOVER_STRATEGY)

### Integrations
- [TradingView](integrations-TRADINGVIEW_INTEGRATION)
- [Google Drive](integration-GOOGLE_DRIVE_INTEGRATION)

### Phases
- [Phase 1](phases-phase1-PHASE1_GUIDE)
- [Phase 2](phases-phase2-PHASE2_GUIDE)
- [Phase 3](phases-phase3-PHASE3_GUIDE)
- [Phase 4](phases-phase4-PHASE4_GUIDE)
- [Phase 5](phases-phase5-PHASE5_GUIDE)
- [Phase 6](phases-phase6-PHASE6_GUIDE)
EOF

# Git operations
echo -e "${GREEN}Committing changes to wiki...${NC}"
git add .
if git diff --staged --quiet; then
    echo -e "${YELLOW}No changes to commit${NC}"
else
    git commit -m "Update wiki documentation from repository ($(date '+%Y-%m-%d %H:%M:%S'))"
    echo -e "${GREEN}Pushing changes to wiki...${NC}"
    git push origin master
    echo -e "${GREEN}✓ Wiki updated successfully!${NC}"
fi

# Clean up
cd "$REPO_ROOT"
echo -e "${GREEN}Cleaning up temporary files...${NC}"
rm -rf "$WIKI_DIR"

echo -e "${GREEN}=== Documentation export complete ===${NC}"
echo -e "View the wiki at: https://github.com/ZeaZDev/${REPO_NAME}/wiki"
