import re
import string
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpamClassifier:
    def __init__(self):
        self.pipeline = None
        self.is_trained = False
        
    def preprocess_text(self, text):
        """
        Basic text preprocessing without spaCy
        """
        if not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove numbers
        text = re.sub(r'\d+', '', text)
        
        return text
    
    def extract_features(self, texts):
        """
        Extract features using TF-IDF vectorization
        """
        if isinstance(texts, str):
            texts = [texts]
        
        # Preprocess all texts
        processed_texts = [self.preprocess_text(text) for text in texts]
        
        return processed_texts
    
    def train(self, texts, labels):
        """
        Train the spam classifier
        """
        logger.info("Starting model training...")
        
        # Preprocess texts
        processed_texts = self.extract_features(texts)
        
        # Create pipeline
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=5000,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.95
            )),
            ('classifier', MultinomialNB(alpha=1.0))
        ])
        
        # Train the model
        self.pipeline.fit(processed_texts, labels)
        self.is_trained = True
        
        logger.info("Model training completed!")
        return True
    
    def predict(self, text):
        """
        Predict if text is spam or ham
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Preprocess the text
        processed_text = self.preprocess_text(text)
        
        # Make prediction
        prediction = self.pipeline.predict([processed_text])[0]
        probability = self.pipeline.predict_proba([processed_text])[0]
        
        return {
            'prediction': 'spam' if prediction == 1 else 'ham',
            'confidence': float(max(probability)),
            'spam_probability': float(probability[1]),
            'ham_probability': float(probability[0])
        }
    
    def save_model(self, filepath):
        """
        Save the trained model
        """
        if not self.is_trained:
            raise ValueError("No trained model to save")
        
        joblib.dump(self.pipeline, filepath)
        logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """
        Load a trained model
        """
        try:
            self.pipeline = joblib.load(filepath)
            self.is_trained = True
            logger.info(f"Model loaded from {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False

# Sample training data
SAMPLE_DATA = {
    'texts': [
        # Spam examples
        "URGENT: You have won a $1000 gift card! Click here to claim now!",
        "FREE VIAGRA NOW!!! Limited time offer, act fast!",
        "CONGRATULATIONS! You've been selected for a free iPhone!",
        "Make money fast! Work from home and earn $5000 per week!",
        "LOSE WEIGHT FAST! Try our miracle diet pill today!",
        "FREE CREDIT REPORT! Check your score now!",
        "WIN A FREE VACATION! Enter our sweepstakes now!",
        "MAKE MONEY ONLINE! Join our affiliate program!",
        "FREE SAMPLE! Try our new product today!",
        "URGENT: Your account has been suspended. Click here to verify!",
        
        # Ham examples
        "Hi John, can you send me the meeting notes from yesterday?",
        "Thanks for your help with the project. It looks great!",
        "Don't forget about the team lunch tomorrow at 12 PM.",
        "I'll be working from home today due to the weather.",
        "Please review the attached document and let me know your thoughts.",
        "The presentation went well. Thanks for your support!",
        "Can we schedule a call to discuss the new requirements?",
        "I've updated the spreadsheet with the latest data.",
        "Happy birthday! Hope you have a wonderful day!",
        "Let me know if you need any clarification on the report."
    ],
    'labels': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}

if __name__ == "__main__":
    # Create and train the classifier
    classifier = SpamClassifier()
    
    # Create sample dataset
    texts = SAMPLE_DATA['texts']
    labels = SAMPLE_DATA['labels']
    
    # Train the model
    print("Training spam classifier...")
    classifier.train(texts, labels)
    print("Training completed!")
    
    # Test the model
    test_texts = [
        "Hi, can we schedule a meeting for tomorrow?",
        "FREE MONEY! Click here to claim your prize!",
        "Please send me the quarterly report.",
        "URGENT: You've won a million dollars!"
    ]
    
    print("\nTesting the model:")
    for text in test_texts:
        result = classifier.predict(text)
        print(f"Text: {text[:50]}...")
        print(f"Prediction: {result['prediction']}")
        print(f"Confidence: {result['confidence']}")
        print("-" * 50) 