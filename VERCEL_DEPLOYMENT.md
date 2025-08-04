# Vercel Deployment Guide

## 🚀 Deploy to Vercel in 3 Steps

### Step 1: Install Vercel CLI (Optional)

```bash
# Install Vercel CLI globally
npm install -g vercel

# Or use npx (no installation required)
npx vercel
```

### Step 2: Deploy from GitHub (Recommended)

1. **Go to Vercel Dashboard**
   - Visit https://vercel.com/dashboard
   - Sign in with GitHub (or create account)

2. **Import Your Repository**
   - Click "New Project"
   - Select "Import Git Repository"
   - Choose `yashgarg195/email-spam-classifier`
   - Click "Import"

3. **Configure Project**
   - **Framework Preset**: Other
   - **Root Directory**: `./` (leave as default)
   - **Build Command**: Leave empty (Vercel will auto-detect)
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements.txt && python -m spacy download en_core_web_sm && python train_model.py`

4. **Environment Variables** (Optional)
   - `PYTHONPATH`: `.`
   - `FLASK_ENV`: `production`

5. **Deploy**
   - Click "Deploy"
   - Wait for build to complete (2-3 minutes)

### Step 3: Access Your App

- Vercel will provide a URL like: `https://email-spam-classifier-xxx.vercel.app`
- Your app will be live and accessible worldwide!

## 🔧 Manual Deployment (Alternative)

If you prefer using the CLI:

```bash
# Navigate to your project directory
cd /Users/yashgarg/Documents/nlp

# Deploy to Vercel
vercel

# Follow the prompts:
# - Set up and deploy? Y
# - Which scope? [your-account]
# - Link to existing project? N
# - What's your project's name? email-spam-classifier
# - In which directory is your code located? ./
# - Want to override the settings? N
```

## 📊 Vercel Features

### ✅ **Automatic Benefits**
- **Global CDN**: Your app is served from the edge worldwide
- **HTTPS**: Automatic SSL certificates
- **Auto-scaling**: Handles traffic spikes automatically
- **Git Integration**: Automatic deployments on push
- **Preview Deployments**: Test changes before going live

### 🔄 **Continuous Deployment**
- Every push to `main` branch = automatic deployment
- Preview deployments for pull requests
- Instant rollbacks to previous versions

## 🛠️ Configuration Details

### `vercel.json` Explained
```json
{
  "version": 2,                    // Vercel platform version
  "builds": [
    {
      "src": "app.py",             // Your Flask app entry point
      "use": "@vercel/python"      // Python runtime
    }
  ],
  "routes": [
    {
      "src": "/(.*)",              // All routes
      "dest": "app.py"             // Route to Flask app
    }
  ],
  "env": {
    "PYTHONPATH": "."              // Python path configuration
  },
  "regions": ["iad1"],             // Deploy to US East (Virginia)
  "public": false                  // Private deployment
}
```

## 🚨 Important Notes for Vercel

### ⚠️ **Serverless Limitations**
- **Cold starts**: First request may be slower
- **Function timeout**: 30 seconds max (configurable)
- **Memory limits**: 1024MB per function
- **File system**: Read-only (except `/tmp`)

### 🔧 **Optimizations**
1. **Model Loading**: Model is loaded once per cold start
2. **Caching**: Consider caching predictions for repeated requests
3. **Async Processing**: Use background tasks for heavy operations

## 📈 Performance Tips

### 🚀 **Optimize for Vercel**
```python
# In app.py - Add caching headers
@app.after_request
def add_cache_headers(response):
    response.headers['Cache-Control'] = 'public, max-age=300'
    return response

# Use environment variables for configuration
import os
DEBUG = os.environ.get('FLASK_ENV') == 'development'
```

### 📊 **Monitor Performance**
- Vercel Analytics (built-in)
- Function execution times
- Cold start frequency
- Error rates

## 🔍 Troubleshooting

### Common Issues:

1. **Build Failures**
   ```bash
   # Check build logs in Vercel dashboard
   # Common fixes:
   # - Ensure all dependencies in requirements.txt
   # - Check Python version compatibility
   # - Verify spaCy model download
   ```

2. **Import Errors**
   ```bash
   # Make sure PYTHONPATH is set correctly
   # Check that all files are in the repository
   ```

3. **Model Loading Issues**
   ```bash
   # Ensure train_model.py runs during build
   # Check model file path in production
   ```

### Debug Commands:
```bash
# Test locally with Vercel dev
vercel dev

# Check deployment status
vercel ls

# View deployment logs
vercel logs [deployment-url]
```

## 🎯 Next Steps After Deployment

1. **Custom Domain** (Optional)
   - Add your domain in Vercel dashboard
   - Configure DNS settings

2. **Environment Variables**
   - Add production-specific settings
   - Configure API keys if needed

3. **Monitoring**
   - Set up Vercel Analytics
   - Monitor function performance

4. **Optimization**
   - Implement caching strategies
   - Optimize model loading

## 🌟 Vercel Advantages

- **Zero Configuration**: Works out of the box
- **Global Performance**: Edge network worldwide
- **Automatic Scaling**: Handles any traffic load
- **Git Integration**: Deploy on every push
- **Free Tier**: Generous limits for personal projects
- **Professional Features**: Teams, analytics, monitoring

Your spam classifier will be live globally in minutes! 🌍 