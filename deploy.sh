#!/bin/bash

# Digital Contact Cards - One-Click Deployment Script
# This script automates the entire workflow from CSV data to live website + Apple Wallet passes

set -e  # Exit on any error

echo "🚀 Digital Contact Cards - Automated Deployment"
echo "================================================"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository. Please run this script from the project root."
    exit 1
fi

# Check if required files exist
if [ ! -f "team_data.csv" ]; then
    echo "❌ Error: team_data.csv not found. Please create your team data file."
    exit 1
fi

if [ ! -f "scripts/generate_site.py" ]; then
    echo "❌ Error: scripts/generate_site.py not found. Please ensure all project files are present."
    exit 1
fi

echo ""
echo "Step 1: Generating website and Apple Wallet passes from CSV data..."
echo "──────────────────────────────────────────────────────────────────"

# Generate the website and wallet passes
python3 scripts/generate_site.py

# Check if generation was successful
if [ $? -ne 0 ]; then
    echo "❌ Website generation failed. Please check the error messages above."
    exit 1
fi

echo ""
echo "Step 2: Committing changes to main branch..."
echo "──────────────────────────────────────────────"

# Add all changes to git
git add .

# Check if there are any changes to commit
if git diff --staged --quiet; then
    echo "ℹ️  No changes detected. The website is already up to date."
else
    # Commit the changes
    git commit -m "Update team data and regenerate site + wallet passes - $(date '+%Y-%m-%d %H:%M:%S')"
    echo "✅ Changes committed successfully"
fi

# Push to main branch
echo "📤 Pushing changes to main branch..."
git push origin main

if [ $? -ne 0 ]; then
    echo "❌ Failed to push to main branch. Please check your git configuration and network connection."
    exit 1
fi

echo ""
echo "Step 3: Deploying website and wallet passes to GitHub Pages..."
echo "──────────────────────────────────────────────────────────────"

# Robust deployment method: Delete and recreate gh-pages branch
# This approach prevents "non-fast-forward" errors that occur when using git subtree
# on subsequent runs. By deleting and recreating the gh-pages branch each time,
# we ensure consistent, idempotent deployments.

echo "🗑️  Cleaning up remote gh-pages branch..."
# Delete remote gh-pages branch (ignore errors if branch doesn't exist)
git push origin --delete gh-pages 2>/dev/null || echo "   Remote gh-pages branch not found (this is normal for first deployment)"

echo "🔄 Creating fresh deployment branch..."
# Delete local gh-pages branch if it exists
git branch -D gh-pages 2>/dev/null || true

# Create new orphan branch for deployment
git checkout --orphan gh-pages

echo "📦 Staging output files for deployment..."
# Add all files from the output directory as root-level files
git --work-tree=output add --all

# Commit the deployment
echo "💾 Committing deployment..."
git commit -m "Deploy website + wallet passes - $(date '+%Y-%m-%d %H:%M:%S')"

echo "🚀 Pushing to GitHub Pages..."
# Push the new gh-pages branch
git push origin gh-pages

echo "🔙 Returning to main branch..."
# Return to main branch
git checkout main --force

echo "✅ Robust deployment completed successfully!"

echo ""
echo "🎉 Deployment Complete!"
echo "════════════════════════"

# Get the GitHub Pages URL from git remote
REPO_URL=$(git remote get-url origin)
if [[ $REPO_URL == *"github.com"* ]]; then
    if [[ $REPO_URL == https* ]]; then
        # HTTPS URL format
        GITHUB_URL=${REPO_URL#https://github.com/}
        GITHUB_URL=${GITHUB_URL%.git}
    else
        # SSH URL format
        GITHUB_URL=${REPO_URL#git@github.com:}
        GITHUB_URL=${GITHUB_URL%.git}
    fi
    
    IFS='/' read -r USERNAME REPO <<< "$GITHUB_URL"
    PAGES_URL="https://${USERNAME}.github.io/${REPO}/"
    
    echo "🌐 Your website will be available at:"
    echo "   $PAGES_URL"
    echo ""
    echo "📋 Individual contact cards:"
    echo "   ${PAGES_URL}html/[name].html"
    echo ""
    echo "📱 VCF downloads available at:"
    echo "   ${PAGES_URL}vcf/[name].vcf"
    echo ""
    echo "🍎 Apple Wallet passes available at:"
    echo "   ${PAGES_URL}passes/[name].pkpass"
else
    echo "🌐 Your website will be available on GitHub Pages"
    echo "   (Unable to determine URL automatically)"
fi

echo ""
echo "⏱️  Note: It may take 1-2 minutes for changes to appear on the live site."
echo "💡 Tip: Use Ctrl+F5 (or Cmd+Shift+R on Mac) to force refresh your browser."
echo ""
echo "📱 Apple Wallet Testing:"
echo "   • Download .pkpass files on iOS device to add to Wallet"
echo "   • Scan QR codes in Wallet passes to test contact links"

echo ""
echo "✅ All done! Your digital contact cards and wallet passes are now live." 