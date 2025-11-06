#!/bin/bash
#
# Manual Changelog Generation Script
#
# This script allows you to manually generate the changelog from fragments
# for local testing before pushing to GitHub.
#
# Usage:
#   .dev/scripts/generate_changelog.sh [version]
#
# If no version is provided, it will use the version from galaxy.yml
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  ALPACA Operator Changelog Generator      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
echo ""

# Get the script directory and navigate to repo root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

echo -e "${CYAN}📂 Repository: $REPO_ROOT${NC}"
echo ""

# Get version from parameter or galaxy.yml
if [ -n "$1" ]; then
    VERSION="$1"
    echo -e "${YELLOW}📦 Using provided version: $VERSION${NC}"
else
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Error: Python 3 is required but not found.${NC}"
        exit 1
    fi
    
    VERSION=$(python3 -c "import yaml; print(yaml.safe_load(open('galaxy.yml'))['version'])")
    echo -e "${YELLOW}📦 Using version from galaxy.yml: $VERSION${NC}"
fi

echo ""

# Check if fragments exist
if [ ! -d "changelogs/fragments" ] || [ -z "$(ls -A changelogs/fragments/*.yml changelogs/fragments/*.yaml 2>/dev/null)" ]; then
    echo -e "${YELLOW}⚠️  No changelog fragments found in changelogs/fragments/${NC}"
    echo -e "${YELLOW}Nothing to generate. Create some fragment files first!${NC}"
    echo ""
    echo -e "${CYAN}Example fragment file (changelogs/fragments/my-feature.yml):${NC}"
    echo "---"
    echo "minor_changes:"
    echo '  - "Add new feature XYZ"'
    echo ""
    exit 0
fi

echo -e "${GREEN}✅ Found changelog fragments:${NC}"
ls -1 changelogs/fragments/*.yml changelogs/fragments/*.yaml 2>/dev/null | sed 's/^/   • /'
echo ""

# Install antsibull-changelog if not available
if ! command -v antsibull-changelog &> /dev/null; then
    echo -e "${YELLOW}📥 antsibull-changelog not found. Installing...${NC}"
    pip3 install antsibull-changelog
    echo ""
fi

# Navigate to changelogs directory
cd changelogs

echo -e "${BLUE}📝 Generating changelog for version $VERSION...${NC}"
echo ""
antsibull-changelog release --version "$VERSION"

# Navigate back to repo root
cd "$REPO_ROOT"

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ Changelog Generated Successfully!      ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}📄 Review the changes:${NC}"
echo "   • CHANGELOG.rst (user-facing changelog)"
echo "   • changelogs/changelog.yaml (structured changelog data)"
echo ""
echo -e "${YELLOW}🔍 Next steps:${NC}"
echo ""
echo -e "   1. Review the generated CHANGELOG.rst:"
echo -e "      ${GREEN}cat CHANGELOG.rst${NC}"
echo ""
echo -e "   2. If satisfied, commit the changes:"
echo -e "      ${GREEN}git add CHANGELOG.rst changelogs/changelog.yaml${NC}"
echo -e "      ${GREEN}git rm changelogs/fragments/*.yml${NC}"
echo -e "      ${GREEN}git commit -m 'chore: Generate changelog for version $VERSION'${NC}"
echo ""
echo -e "   3. Push to trigger CI/CD:"
echo -e "      ${GREEN}git push${NC}"
echo ""
echo -e "${BLUE}ℹ️  Note: When you push to main with fragments, the GitHub Actions${NC}"
echo -e "${BLUE}   workflow will automatically generate the changelog for you.${NC}"
echo ""

