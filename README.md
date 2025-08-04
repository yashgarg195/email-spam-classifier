# Email Spam/Ham Filter using spaCy

A machine learning application that uses spaCy for natural language processing to classify emails as spam or ham (legitimate).

## Features

- spaCy-based text preprocessing and feature extraction
- Machine learning classifier for spam/ham classification
- Simple web interface for testing
- RESTful API for integration
- Pre-trained model included

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Download spaCy model:
```bash
python -m spacy download en_core_web_sm
```

3. Train the model (optional - pre-trained model included):
```bash
python train_model.py
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and go to `http://localhost:8080`

## Usage

1. Enter email text in the web interface
2. Click "Classify" to get spam/ham prediction
3. View confidence scores and classification details

## API Endpoints

- `POST /api/classify` - Classify email text
- `GET /api/health` - Health check

## Project Structure

```
├── app.py                 # Flask web application
├── spam_classifier.py     # spaCy-based classifier
├── train_model.py         # Model training script
├── data/                  # Training data
├── models/                # Saved models
├── static/                # Frontend assets
└── templates/             # HTML templates
```
