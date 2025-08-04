from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from spam_classifier import SpamClassifier, SAMPLE_DATA
import os
import logging

app = Flask(__name__)
CORS(app)

# Configure logging for Vercel
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add caching headers for better performance
@app.after_request
def add_cache_headers(response):
    if request.path.startswith('/api/'):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    else:
        response.headers['Cache-Control'] = 'public, max-age=300'
    return response

# Initialize the spam classifier
classifier = None

def initialize_classifier():
    """Initialize the spam classifier"""
    global classifier
    try:
        classifier = SpamClassifier()
        model_path = 'models/spam_classifier.joblib'
        
        if os.path.exists(model_path):
            if classifier.load_model(model_path):
                print(f"Model loaded from {model_path}")
                return True
            else:
                print("⚠️  Failed to load model. Training new model...")
        else:
            print("⚠️  No pre-trained model found. Training new model...")
        
        # Train with sample data
        texts = SAMPLE_DATA['texts']
        labels = SAMPLE_DATA['labels']
        
        if classifier.train(texts, labels):
            classifier.save_model(model_path)
            print("✅ Model trained and saved successfully")
            return True
        else:
            print("❌ Failed to train model")
            return False
            
    except Exception as e:
        print(f"❌ Error initializing classifier: {e}")
        return False

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': classifier is not None and classifier.is_trained
    })

@app.route('/api/classify', methods=['POST'])
def classify_email():
    """Classify email text as spam or ham"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'No text provided'
            }), 400
        
        text = data['text'].strip()
        
        if not text:
            return jsonify({
                'error': 'Empty text provided'
            }), 400
        
        if classifier is None or not classifier.is_trained:
            return jsonify({
                'error': 'Model not loaded'
            }), 500
        
        # Make prediction
        result = classifier.predict(text)
        
        return jsonify({
            'success': True,
            'text': text,
            'prediction': result['prediction'],
            'confidence': result['confidence'],
            'spam_probability': result['spam_probability'],
            'ham_probability': result['ham_probability'],
            'features': result['features']
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Classification failed: {str(e)}'
        }), 500

@app.route('/api/train', methods=['POST'])
def train_model():
    """Retrain the model with new data"""
    try:
        if classifier is None:
            return jsonify({
                'error': 'Classifier not initialized'
            }), 500
        
        # Retrain with the sample data
        texts = SAMPLE_DATA['texts']
        labels = SAMPLE_DATA['labels']
        
        classifier.train(texts, labels)
        
        return jsonify({
            'success': True,
            'message': 'Model retrained successfully',
            'samples': len(texts)
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Training failed: {str(e)}'
        }), 500

@app.route('/api/examples')
def get_examples():
    """Get example texts for testing"""
    examples = {
        'ham': [
            "Hi John, how are you doing? Let's meet for coffee tomorrow.",
            "The meeting is scheduled for 2 PM today. Please bring your laptop.",
            "Thanks for your email. I'll get back to you soon.",
            "Can you please send me the report by Friday?",
            "I'm looking forward to our presentation next week."
        ],
        'spam': [
            "FREE MONEY! Click here to claim your $1000 prize NOW!",
            "URGENT: You've won a million dollars! Send your bank details immediately!",
            "Buy Viagra online at 50% discount! Limited time offer!",
            "Earn $5000 per week working from home! No experience needed!",
            "CONGRATULATIONS! You're our lucky winner! Claim your prize!"
        ]
    }
    
    return jsonify(examples)

# Initialize the classifier when the module is imported
if initialize_classifier():
    print("✅ Classifier initialized successfully")
else:
    print("❌ Failed to initialize classifier")

# Create templates directory if it doesn't exist
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)

if __name__ == '__main__':
    print("🚀 Starting Spam Classifier Web Application...")
    print("🌐 Starting web server on http://localhost:8080")
    app.run(debug=True, host='0.0.0.0', port=8080) 