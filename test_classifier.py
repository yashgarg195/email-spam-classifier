#!/usr/bin/env python3
"""
Test script for the spam classifier
"""

from spam_classifier import SpamClassifier
import json

def test_classifier():
    """Test the spam classifier with various examples"""
    print("🧪 Testing Spam Classifier...")
    print("=" * 50)
    
    # Initialize classifier
    try:
        classifier = SpamClassifier()
        if classifier.pipeline is None:
            print("❌ Model not loaded. Please run train_model.py first.")
            return False
        print("✅ Classifier initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize classifier: {e}")
        return False
    
    # Test cases
    test_cases = [
        {
            "text": "Hi John, how are you doing? Let's meet for coffee tomorrow.",
            "expected": "ham",
            "description": "Normal business email"
        },
        {
            "text": "FREE MONEY! Click here to claim your $1000 prize NOW!",
            "expected": "spam",
            "description": "Obvious spam with money offer"
        },
        {
            "text": "The meeting is scheduled for 2 PM today. Please bring your laptop.",
            "expected": "ham",
            "description": "Professional meeting email"
        },
        {
            "text": "URGENT: You've won a million dollars! Send your bank details immediately!",
            "expected": "spam",
            "description": "Urgent money scam"
        },
        {
            "text": "Thanks for your email. I'll get back to you soon.",
            "expected": "ham",
            "description": "Polite response email"
        },
        {
            "text": "Buy Viagra online at 50% discount! Limited time offer!",
            "expected": "spam",
            "description": "Pharmaceutical spam"
        }
    ]
    
    correct_predictions = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test_case['description']}")
        print(f"Text: {test_case['text'][:50]}...")
        
        try:
            result = classifier.predict(test_case['text'])
            prediction = result['prediction']
            confidence = result['confidence']
            
            print(f"Prediction: {prediction}")
            print(f"Confidence: Ham: {confidence['ham']:.3f}, Spam: {confidence['spam']:.3f}")
            
            if prediction == test_case['expected']:
                print("✅ CORRECT")
                correct_predictions += 1
            else:
                print("❌ INCORRECT")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {correct_predictions}/{total_tests} correct")
    accuracy = (correct_predictions / total_tests) * 100
    print(f"Accuracy: {accuracy:.1f}%")
    
    if accuracy >= 80:
        print("🎉 Excellent! The classifier is working well.")
        return True
    elif accuracy >= 60:
        print("⚠️  Good, but there's room for improvement.")
        return True
    else:
        print("❌ The classifier needs improvement.")
        return False

def test_api_endpoints():
    """Test the API endpoints"""
    print("\n🌐 Testing API endpoints...")
    print("=" * 50)
    
    try:
        import requests
        import time
        
        # Start the server in background (this would need to be done manually)
        print("⚠️  Note: Make sure the Flask server is running (python app.py)")
        print("Testing API endpoints...")
        
        base_url = "http://localhost:8080"
        
        # Test health endpoint
        try:
            response = requests.get(f"{base_url}/api/health", timeout=5)
            if response.status_code == 200:
                print("✅ Health endpoint working")
            else:
                print("❌ Health endpoint failed")
        except:
            print("❌ Health endpoint not accessible")
        
        # Test examples endpoint
        try:
            response = requests.get(f"{base_url}/api/examples", timeout=5)
            if response.status_code == 200:
                examples = response.json()
                print(f"✅ Examples endpoint working ({len(examples['ham'])} ham, {len(examples['spam'])} spam examples)")
            else:
                print("❌ Examples endpoint failed")
        except:
            print("❌ Examples endpoint not accessible")
        
        # Test classification endpoint
        test_text = "Hi, can we schedule a meeting?"
        try:
            response = requests.post(
                f"{base_url}/api/classify",
                json={"text": test_text},
                timeout=5
            )
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Classification endpoint working (prediction: {result['prediction']})")
            else:
                print("❌ Classification endpoint failed")
        except:
            print("❌ Classification endpoint not accessible")
            
    except ImportError:
        print("⚠️  requests library not available. Install with: pip install requests")

if __name__ == "__main__":
    print("🚀 Running Spam Classifier Tests...")
    
    # Test the classifier
    classifier_works = test_classifier()
    
    # Test API endpoints
    test_api_endpoints()
    
    print("\n" + "=" * 50)
    if classifier_works:
        print("🎉 All tests completed successfully!")
    else:
        print("⚠️  Some tests failed. Please check the setup.")
    
    print("\nTo run the web application:")
    print("  python app.py")
    print("Then visit: http://localhost:8080") 