import spacy
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import re
import os

class SpamClassifier:
    def __init__(self, model_path='models/spam_classifier.joblib'):
        self.model_path = model_path
        self.nlp = spacy.load("en_core_web_sm")
        self.pipeline = None
        self.load_model()
    
    def preprocess_text(self, text):
        """
        Preprocess text using spaCy for spam classification
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Process with spaCy
        doc = self.nlp(text)
        
        # Extract tokens, lemmatize, and filter
        tokens = []
        for token in doc:
            # Keep only alphabetic tokens, not stopwords, and length > 2
            if (token.is_alpha and 
                not token.is_stop and 
                len(token.text) > 2 and
                not token.is_punct):
                tokens.append(token.lemma_)
        
        return ' '.join(tokens)
    
    def extract_features(self, text):
        """
        Extract additional features for spam classification
        """
        features = {}
        
        # Text length
        features['text_length'] = len(text)
        
        # Number of words
        features['word_count'] = len(text.split())
        
        # Number of sentences
        doc = self.nlp(text)
        features['sentence_count'] = len(list(doc.sents))
        
        # Number of exclamation marks
        features['exclamation_count'] = text.count('!')
        
        # Number of question marks
        features['question_count'] = text.count('?')
        
        # Number of capital letters
        features['capital_count'] = sum(1 for c in text if c.isupper())
        
        # Number of numbers
        features['number_count'] = sum(1 for c in text if c.isdigit())
        
        # Check for spam indicators
        spam_words = ['free', 'money', 'cash', 'winner', 'prize', 'urgent', 'limited', 'offer', 
                     'click', 'buy', 'discount', 'sale', 'credit', 'loan', 'debt', 'investment',
                     'earn', 'income', 'million', 'dollar', 'lottery', 'casino', 'viagra', 'pills']
        
        features['spam_word_count'] = sum(1 for word in text.lower().split() if word in spam_words)
        
        return features
    
    def train(self, texts, labels):
        """
        Train the spam classifier
        """
        # Preprocess all texts
        processed_texts = [self.preprocess_text(text) for text in texts]
        
        # Create pipeline with TF-IDF and Naive Bayes
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
            ('classifier', MultinomialNB())
        ])
        
        # Train the pipeline
        self.pipeline.fit(processed_texts, labels)
        
        # Save the model
        self.save_model()
    
    def predict(self, text):
        """
        Predict if text is spam or ham
        """
        if self.pipeline is None:
            raise ValueError("Model not trained or loaded")
        
        # Preprocess the text
        processed_text = self.preprocess_text(text)
        
        # Make prediction
        prediction = self.pipeline.predict([processed_text])[0]
        probability = self.pipeline.predict_proba([processed_text])[0]
        
        # Get confidence scores
        ham_prob = probability[0] if prediction == 0 else probability[1]
        spam_prob = probability[1] if prediction == 1 else probability[0]
        
        return {
            'prediction': 'spam' if prediction == 1 else 'ham',
            'confidence': {
                'ham': float(ham_prob),
                'spam': float(spam_prob)
            },
            'features': self.extract_features(text)
        }
    
    def save_model(self):
        """
        Save the trained model
        """
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.pipeline, self.model_path)
    
    def load_model(self):
        """
        Load a trained model
        """
        try:
            if os.path.exists(self.model_path):
                self.pipeline = joblib.load(self.model_path)
                print(f"Model loaded from {self.model_path}")
            else:
                print(f"No saved model found at {self.model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.pipeline = None

# Sample training data
SAMPLE_DATA = {
    'ham': [
        "Hi John, how are you doing? Let's meet for coffee tomorrow.",
        "The meeting is scheduled for 2 PM today. Please bring your laptop.",
        "Thanks for your email. I'll get back to you soon.",
        "Can you please send me the report by Friday?",
        "I'm looking forward to our presentation next week.",
        "The project deadline has been extended to next month.",
        "Please review the attached documents and let me know your thoughts.",
        "I'll be out of office next week. Please contact Sarah for urgent matters.",
        "The quarterly results look great! Good job everyone.",
        "Don't forget to submit your timesheet by the end of the day."
    ],
    'spam': [
        "FREE MONEY! Click here to claim your $1000 prize NOW!",
        "URGENT: You've won a million dollars! Send your bank details immediately!",
        "Buy Viagra online at 50% discount! Limited time offer!",
        "Earn $5000 per week working from home! No experience needed!",
        "CONGRATULATIONS! You're our lucky winner! Claim your prize!",
        "Hot singles in your area! Click here to meet them now!",
        "Get rich quick! Invest in our amazing opportunity!",
        "FREE iPhone! Just pay shipping and handling!",
        "Lose weight fast with our miracle pills! Guaranteed results!",
        "URGENT: Your account has been suspended. Click here to verify!"
    ]
}

def create_sample_dataset():
    """
    Create a sample dataset for training
    """
    texts = []
    labels = []
    
    # Add ham samples
    for text in SAMPLE_DATA['ham']:
        texts.append(text)
        labels.append(0)  # 0 for ham
    
    # Add spam samples
    for text in SAMPLE_DATA['spam']:
        texts.append(text)
        labels.append(1)  # 1 for spam
    
    return texts, labels

if __name__ == "__main__":
    # Create and train the classifier
    classifier = SpamClassifier()
    
    # Create sample dataset
    texts, labels = create_sample_dataset()
    
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