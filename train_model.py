#!/usr/bin/env python3
"""
Training script for the Email Spam Classifier
"""

import os
from spam_classifier import SpamClassifier, SAMPLE_DATA

def main():
    print("🚀 Training Email Spam Classifier...")
    print("=" * 50)
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Initialize classifier
    classifier = SpamClassifier()
    
    # Get training data
    texts = SAMPLE_DATA['texts']
    labels = SAMPLE_DATA['labels']
    
    print(f"📊 Training with {len(texts)} samples:")
    print(f"   - Spam samples: {sum(labels)}")
    print(f"   - Ham samples: {len(labels) - sum(labels)}")
    
    # Train the model
    print("\n🔄 Training model...")
    success = classifier.train(texts, labels)
    
    if success:
        print("✅ Model training completed successfully!")
        
        # Save the model
        model_path = 'models/spam_classifier.joblib'
        classifier.save_model(model_path)
        print(f"💾 Model saved to: {model_path}")
        
        # Test the model
        print("\n🧪 Testing model with sample texts...")
        test_texts = [
            "URGENT: Claim your free iPhone now!",
            "Hi, can you send me the meeting notes?",
            "FREE MONEY! Click here to win $1000!",
            "Thanks for your help with the project."
        ]
        
        for text in test_texts:
            result = classifier.predict(text)
            print(f"Text: '{text[:50]}...'")
            print(f"  Prediction: {result['prediction']}")
            print(f"  Confidence: {result['confidence']:.2%}")
            print(f"  Spam probability: {result['spam_probability']:.2%}")
            print()
        
        print("🎉 Training and testing completed successfully!")
        return True
    else:
        print("❌ Model training failed!")
        return False

if __name__ == "__main__":
    main() 