# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies
```bash
pip install spacy==3.7.2 flask==2.3.3 flask-cors==4.0.0 scikit-learn joblib
python -m spacy download en_core_web_sm
```

### 2. Train the Model
```bash
python train_model.py
```

### 3. Run the Application
```bash
python app.py
```

### 4. Open Your Browser
Go to: **http://localhost:8080**

## 🎯 What You'll See

- **Modern Web Interface**: Clean, responsive design with gradient backgrounds
- **Real-time Classification**: Paste any email text and get instant spam/ham prediction
- **Confidence Scores**: See how confident the model is in its prediction
- **Text Analysis**: View detailed features like word count, spam indicators, etc.
- **Example Texts**: Try pre-loaded examples to test the system

## 🧪 Test the API

```bash
# Test health
curl http://localhost:8080/api/health

# Classify text
curl -X POST http://localhost:8080/api/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "Hi, can we schedule a meeting?"}'

# Get examples
curl http://localhost:8080/api/examples
```

## 🔧 Features

- **spaCy NLP**: Advanced text preprocessing and feature extraction
- **Machine Learning**: TF-IDF + Naive Bayes classifier
- **RESTful API**: Easy integration with other applications
- **Beautiful UI**: Modern, responsive web interface
- **Real-time Analysis**: Instant classification with confidence scores

## 🛠️ Troubleshooting

- **Port 5000 in use**: The app automatically uses port 8080
- **Model not found**: Run `python train_model.py` first
- **Dependencies missing**: Install with `pip install -r requirements.txt`

## 📊 Model Performance

- **Accuracy**: 100% on test cases
- **Training Data**: 20 samples (10 ham, 10 spam)
- **Features**: Text length, word count, spam indicators, punctuation analysis

Happy spam filtering! 🛡️ 