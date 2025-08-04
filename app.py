from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from spam_classifier import SpamClassifier
import os

app = Flask(__name__)
CORS(app)

# Initialize the spam classifier
classifier = None

def initialize_classifier():
    """Initialize the spam classifier"""
    global classifier
    try:
        classifier = SpamClassifier()
        if classifier.pipeline is None:
            print("No trained model found. Training a new model...")
            from spam_classifier import create_sample_dataset
            texts, labels = create_sample_dataset()
            classifier.train(texts, labels)
        return True
    except Exception as e:
        print(f"Error initializing classifier: {e}")
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
        'model_loaded': classifier is not None and classifier.pipeline is not None
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
        
        if classifier is None or classifier.pipeline is None:
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
        
        # For now, we'll retrain with the sample data
        # In a real application, you'd accept training data from the request
        from spam_classifier import create_sample_dataset
        texts, labels = create_sample_dataset()
        
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

if __name__ == '__main__':
    print("🚀 Starting Spam Classifier Web Application...")
    
    # Initialize the classifier
    if initialize_classifier():
        print("✅ Classifier initialized successfully")
    else:
        print("❌ Failed to initialize classifier")
    
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("🌐 Starting web server on http://localhost:8080")
    app.run(debug=True, host='0.0.0.0', port=8080) 