#!/bin/bash

# Vercel Deployment Script for Email Spam Classifier
# This script automates the deployment process to Vercel

echo "🚀 Deploying Email Spam Classifier to Vercel..."
echo "================================================"

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Check if we're in the right directory
if [ ! -f "app.py" ] || [ ! -f "vercel.json" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    echo "   Expected files: app.py, vercel.json"
    exit 1
fi

echo "✅ Project structure verified"
echo "📁 Current directory: $(pwd)"
echo "📄 Found files: app.py, vercel.json"

# Deploy to Vercel
echo ""
echo "🌐 Deploying to Vercel..."
echo "   This will open your browser for authentication if needed"
echo ""

vercel --prod

echo ""
echo "🎉 Deployment completed!"
echo "📊 Check your Vercel dashboard for the live URL"
echo "🔗 Your app should be accessible at: https://[project-name].vercel.app"
echo ""
echo "💡 Tips:"
echo "   - First request may be slower (cold start)"
echo "   - Model will be loaded automatically"
echo "   - All API endpoints are available"
echo ""
echo "📚 For more info, see: VERCEL_DEPLOYMENT.md" 