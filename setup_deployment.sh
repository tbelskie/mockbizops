#!/bin/bash

# Deployment Setup Script for Car Repair Shop API

echo "========================================"
echo "Car Repair Shop API - Deployment Setup"
echo "========================================"
echo ""

# Generate secure keys
echo "Generating secure keys..."
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
ADMIN_KEY=$(python3 -c "import uuid; print(str(uuid.uuid4()))")

echo ""
echo "✓ Generated secure keys"
echo ""
echo "Add these to your deployment environment variables:"
echo ""
echo "SECRET_KEY=$SECRET_KEY"
echo "ADMIN_API_KEY=$ADMIN_KEY"
echo ""
echo "========================================"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    echo "✓ Git initialized"
else
    echo "✓ Git already initialized"
fi

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo ""
    echo "You have uncommitted changes. Ready to commit?"
    echo ""
    echo "Run these commands to push to GitHub:"
    echo ""
    echo "  git add ."
    echo "  git commit -m \"Initial commit: Car Repair Shop Mock API\""
    echo "  git remote add origin https://github.com/YOUR_USERNAME/car-repair-api.git"
    echo "  git branch -M main"
    echo "  git push -u origin main"
    echo ""
else
    echo "✓ No uncommitted changes"
fi

echo "========================================"
echo "Next Steps:"
echo "========================================"
echo ""
echo "1. Create a GitHub repository:"
echo "   → Go to https://github.com/new"
echo "   → Name it 'car-repair-api'"
echo "   → Make it public or private"
echo ""
echo "2. Push your code (if not already):"
echo "   → See commands above"
echo ""
echo "3. Deploy to Railway (recommended):"
echo "   → Visit https://railway.app"
echo "   → Sign up with GitHub"
echo "   → New Project → Deploy from GitHub repo"
echo "   → Select your repository"
echo "   → Add PostgreSQL database"
echo "   → Set environment variables (shown above)"
echo "   → Deploy!"
echo ""
echo "4. Seed the database:"
echo "   → railway run python -m app.seed_data"
echo ""
echo "5. Your API will be live at:"
echo "   → https://your-app.railway.app/docs"
echo ""
echo "========================================"
echo "For detailed instructions, see DEPLOYMENT.md"
echo "========================================"
