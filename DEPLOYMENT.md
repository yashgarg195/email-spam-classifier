# Deployment Guide

## 🚀 Quick Deployment Options

### Option 1: Railway (Recommended - Free Tier)

1. **Connect your GitHub repository**
   - Go to https://railway.app/
   - Sign in with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your `email-spam-classifier` repository

2. **Configure the deployment**
   - Railway will auto-detect it's a Python app
   - Add environment variable: `PORT=8080`
   - Deploy!

3. **Access your app**
   - Railway will provide a public URL
   - Your app will be live at `https://your-app-name.railway.app`

### Option 2: Heroku

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew install heroku/brew/heroku
   
   # Or download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku app**
   ```bash
   # Login to Heroku
   heroku login
   
   # Create app
   heroku create your-spam-classifier
   
   # Add Python buildpack
   heroku buildpacks:set heroku/python
   ```

3. **Create Procfile**
   ```bash
   echo "web: python app.py" > Procfile
   ```

4. **Deploy**
   ```bash
   git add Procfile
   git commit -m "Add Procfile for Heroku deployment"
   git push heroku main
   ```

### Option 3: Docker Deployment

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   RUN python -m spacy download en_core_web_sm
   
   COPY . .
   
   RUN python train_model.py
   
   EXPOSE 8080
   
   CMD ["python", "app.py"]
   ```

2. **Build and run**
   ```bash
   # Build image
   docker build -t spam-classifier .
   
   # Run container
   docker run -p 8080:8080 spam-classifier
   ```

### Option 4: Local Network Access

To make your app accessible on your local network:

```bash
# Modify app.py to bind to all interfaces
# Change this line in app.py:
app.run(debug=True, host='0.0.0.0', port=8080)

# Then run
python app.py

# Access from other devices on your network:
# http://YOUR_COMPUTER_IP:8080
```

## 🔧 Environment Variables

For production deployment, consider setting these environment variables:

```bash
# Flask settings
export FLASK_ENV=production
export FLASK_DEBUG=0

# Port (for platforms that set their own port)
export PORT=8080

# Model path
export MODEL_PATH=models/spam_classifier.joblib
```

## 📊 Performance Optimization

For production use:

1. **Use a production WSGI server**
   ```bash
   pip install gunicorn
   
   # Run with gunicorn
   gunicorn -w 4 -b 0.0.0.0:8080 app:app
   ```

2. **Add to requirements.txt**
   ```
   gunicorn==20.1.0
   ```

3. **Update Procfile for Heroku**
   ```
   web: gunicorn app:app
   ```

## 🔒 Security Considerations

1. **Disable debug mode in production**
   ```python
   # In app.py
   app.run(debug=False, host='0.0.0.0', port=8080)
   ```

2. **Add rate limiting**
   ```bash
   pip install flask-limiter
   ```

3. **Use HTTPS in production**
   - Most cloud platforms provide this automatically
   - For local deployment, consider using a reverse proxy

## 📈 Monitoring

Add basic monitoring:

```python
# In app.py
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.before_request
def log_request():
    logger.info(f"Request: {request.method} {request.path}")
```

## 🎯 Recommended Deployment Flow

1. **Start with Railway** (easiest, free)
2. **Test thoroughly** on the deployed version
3. **Add monitoring** and logging
4. **Scale up** if needed (Heroku, AWS, etc.)

## 🚨 Troubleshooting

### Common Issues:

1. **Port already in use**
   - Change port in `app.py`
   - Use environment variable `PORT`

2. **Model not found**
   - Ensure `train_model.py` runs during deployment
   - Check model path in production

3. **Dependencies missing**
   - Verify all packages in `requirements.txt`
   - Check for platform-specific requirements

### Debug Commands:

```bash
# Check if app is running
curl http://localhost:8080/api/health

# View logs (if using gunicorn)
tail -f logs/app.log

# Check Python environment
python -c "import spacy; print(spacy.__version__)"
```

Your spam classifier is now ready for production deployment! 🌐 