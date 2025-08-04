#!/usr/bin/env python3
"""
Training script for the spam classifier
"""

from spam_classifier import SpamClassifier, create_sample_dataset
import os

def main():
    print("🚀 Starting spam classifier training...")
    
    # Create the classifier
    classifier = SpamClassifier()
    
    # Create sample dataset
    print("📊 Creating training dataset...")
    texts, labels = create_sample_dataset()
    
    print(f"📈 Dataset size: {len(texts)} samples")
    print(f"📈 Ham samples: {labels.count(0)}")
    print(f"📈 Spam samples: {labels.count(1)}")
    
    # Train the model
    print("🤖 Training the model...")
    classifier.train(texts, labels)
    
    print("✅ Training completed!")
    print(f"💾 Model saved to: {classifier.model_path}")
    
    # Test the model
    print("\n🧪 Testing the model...")
    test_cases = [
        ("Hi, can we schedule a meeting for tomorrow?", "Expected: ham"),
        ("FREE MONEY! Click here to claim your prize!", "Expected: spam"),
        ("Please send me the quarterly report.", "Expected: ham"),
        ("URGENT: You've won a million dollars!", "Expected: spam"),
        ("The project deadline has been extended.", "Expected: ham"),
        ("Buy Viagra online at 50% discount!", "Expected: spam")
    ]
    
    for text, expected in test_cases:
        result = classifier.predict(text)
        print(f"Text: {text[:40]}...")
        print(f"Prediction: {result['prediction']} ({expected})")
        print(f"Confidence: Ham: {result['confidence']['ham']:.3f}, Spam: {result['confidence']['spam']:.3f}")
        print("-" * 60)
    
    print("🎉 Model training and testing completed successfully!")

if __name__ == "__main__":
    main() 