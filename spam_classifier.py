import re
import string
import json
import os

class SpamClassifier:
    def __init__(self):
        self.spam_keywords = [
            'free', 'money', 'cash', 'winner', 'prize', 'urgent', 'limited', 'offer',
            'click', 'buy', 'discount', 'sale', 'credit', 'loan', 'debt', 'investment',
            'earn', 'income', 'million', 'dollar', 'lottery', 'casino', 'viagra', 'pills',
            'weight loss', 'diet', 'miracle', 'guaranteed', 'act now', 'limited time',
            'exclusive', 'secret', 'amazing', 'incredible', 'shocking', 'revealed',
            'bank account', 'social security', 'password', 'verify', 'confirm',
            'suspended', 'blocked', 'expired', 'renew', 'update', 'claim'
        ]
        
        self.ham_keywords = [
            'meeting', 'project', 'report', 'schedule', 'deadline', 'team',
            'work', 'office', 'business', 'client', 'customer', 'service',
            'help', 'support', 'question', 'answer', 'information', 'data',
            'document', 'file', 'attachment', 'review', 'feedback', 'thanks',
            'appreciate', 'coffee', 'lunch', 'dinner', 'birthday', 'congratulations'
        ]
        
        self.is_trained = True  # Rule-based doesn't need training
    
    def preprocess_text(self, text):
        """Basic text preprocessing"""
        if not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_features(self, text):
        """Extract features for classification"""
        processed_text = self.preprocess_text(text)
        words = processed_text.split()
        
        features = {
            'text_length': len(text),
            'word_count': len(words),
            'spam_keyword_count': 0,
            'ham_keyword_count': 0,
            'exclamation_count': text.count('!'),
            'question_count': text.count('?'),
            'capital_count': sum(1 for c in text if c.isupper()),
            'number_count': sum(1 for c in text if c.isdigit()),
            'url_count': len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)),
            'email_count': len(re.findall(r'\S+@\S+', text))
        }
        
        # Count spam and ham keywords
        for word in words:
            if word in self.spam_keywords:
                features['spam_keyword_count'] += 1
            if word in self.ham_keywords:
                features['ham_keyword_count'] += 1
        
        return features
    
    def calculate_spam_score(self, features):
        """Calculate spam probability based on features"""
        score = 0.0
        
        # Spam indicators (positive score)
        score += features['spam_keyword_count'] * 0.3
        score += features['exclamation_count'] * 0.1
        score += features['capital_count'] / max(features['text_length'], 1) * 0.2
        score += features['url_count'] * 0.2
        score += features['email_count'] * 0.1
        
        # Ham indicators (negative score)
        score -= features['ham_keyword_count'] * 0.2
        score -= features['question_count'] * 0.05
        
        # Normalize score to 0-1 range
        spam_probability = min(max(score, 0.0), 1.0)
        
        return spam_probability
    
    def predict(self, text):
        """Predict if text is spam or ham"""
        features = self.extract_features(text)
        spam_probability = self.calculate_spam_score(features)
        
        # Determine prediction based on threshold
        prediction = 'spam' if spam_probability > 0.5 else 'ham'
        
        # Calculate confidence based on how far from threshold
        confidence = abs(spam_probability - 0.5) * 2  # Scale to 0-1
        
        return {
            'prediction': prediction,
            'confidence': confidence,
            'spam_probability': spam_probability,
            'ham_probability': 1.0 - spam_probability,
            'features': features
        }
    
    def train(self, texts, labels):
        """Placeholder for compatibility - rule-based doesn't need training"""
        return True
    
    def save_model(self, filepath):
        """Save the classifier configuration"""
        config = {
            'spam_keywords': self.spam_keywords,
            'ham_keywords': self.ham_keywords
        }
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2)
    
    def load_model(self, filepath):
        """Load the classifier configuration"""
        try:
            with open(filepath, 'r') as f:
                config = json.load(f)
            
            self.spam_keywords = config.get('spam_keywords', self.spam_keywords)
            self.ham_keywords = config.get('ham_keywords', self.ham_keywords)
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False

# Sample training data (for compatibility)
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