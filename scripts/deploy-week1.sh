#!/bin/bash
# Week 1 Deployment Script
# Moves blog-new → blog and prepares for git deployment

set -e  # Exit on error

echo "============================================================"
echo "  Week 1 SEO Deployment Script"
echo "============================================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to confirm action
confirm() {
    read -p "$1 (yes/no): " response
    case "$response" in
        [yY][eE][sS]|[yY]) 
            return 0
            ;;
        *)
            echo "Aborted."
            return 1
            ;;
    esac
}

# CleverDogMethod
echo -e "${YELLOW}🐕 CleverDogMethod Deployment${NC}"
echo "=================================================="

if [ -d "/root/.openclaw/workspace/dog-training-landing/blog-new" ]; then
    echo ""
    echo "Current structure:"
    echo "  blog/     → Old structure"
    echo "  blog-new/ → New SEO structure"
    echo ""
    
    if confirm "Deploy CleverDogMethod? This will replace blog/ with blog-new/"; then
        cd /root/.openclaw/workspace/dog-training-landing
        
        # Backup old blog
        if [ -d "blog" ]; then
            echo "Creating backup: blog-old-backup..."
            mv blog blog-old-backup
            echo -e "${GREEN}✅${NC} Backup created"
        fi
        
        # Move blog-new to blog
        echo "Moving blog-new → blog..."
        mv blog-new blog
        echo -e "${GREEN}✅${NC} Directory moved"
        
        # Check git status
        echo ""
        echo "Git status:"
        git status --short blog/ _redirects sitemap.xml || true
        
        echo ""
        echo -e "${GREEN}✅ CleverDogMethod ready for deployment${NC}"
        echo ""
        echo "To deploy:"
        echo "  cd /root/.openclaw/workspace/dog-training-landing"
        echo "  git add blog/ _redirects sitemap.xml"
        echo "  git commit -m 'Week 1: Blog SEO restructure'"
        echo "  git push origin main"
    else
        echo "Skipped CleverDogMethod"
    fi
else
    echo -e "${RED}⚠️  blog-new directory not found${NC}"
fi

echo ""
echo "------------------------------------------------------------"
echo ""

# AI Automation Blog
echo -e "${YELLOW}🤖 AI Automation Blog Deployment${NC}"
echo "=================================================="

if [ -d "/root/.openclaw/workspace/ai-automation-blog/blog-new" ]; then
    echo ""
    echo "Current structure:"
    echo "  blog/posts/ → Old structure"
    echo "  blog-new/   → New SEO structure"
    echo ""
    
    if confirm "Deploy AI Automation Blog? This will replace blog/ with blog-new/"; then
        cd /root/.openclaw/workspace/ai-automation-blog
        
        # Backup old blog posts
        if [ -d "blog/posts" ]; then
            echo "Creating backup: blog/posts-backup-$(date +%Y%m%d)..."
            mv blog/posts blog/posts-backup-$(date +%Y%m%d)
            echo -e "${GREEN}✅${NC} Backup created"
        fi
        
        # Remove old blog directory and move blog-new
        echo "Replacing blog/ with blog-new/..."
        rm -rf blog
        mv blog-new blog
        echo -e "${GREEN}✅${NC} Directory moved"
        
        # Check git status
        echo ""
        echo "Git status:"
        git status --short blog/ _redirects sitemap.xml || true
        
        echo ""
        echo -e "${GREEN}✅ AI Automation Blog ready for deployment${NC}"
        echo ""
        echo "To deploy:"
        echo "  cd /root/.openclaw/workspace/ai-automation-blog"
        echo "  git add blog/ _redirects sitemap.xml"
        echo "  git commit -m 'Week 1: Blog SEO restructure'"
        echo "  git push origin main"
    else
        echo "Skipped AI Automation Blog"
    fi
else
    echo -e "${RED}⚠️  blog-new directory not found${NC}"
fi

echo ""
echo "============================================================"
echo -e "  ${GREEN}✅ Deployment preparation complete${NC}"
echo "============================================================"
echo ""
echo "Next steps:"
echo "  1. Review changes with 'git diff'"
echo "  2. Commit and push both blogs"
echo "  3. Test redirects after deployment"
echo "  4. Submit sitemaps to Search Console"
echo ""
