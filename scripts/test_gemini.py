#!/usr/bin/env python3
"""
Quick test script to verify Gemini AI integration
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_gemini_installation():
    """Test if Gemini package is installed"""
    print("🧪 Testing Gemini Installation...")
    try:
        import google.generativeai as genai
        print("✅ google-generativeai package installed")
        return True
    except ImportError as e:
        print(f"❌ google-generativeai not installed: {e}")
        print("   Run: pip install google-generativeai")
        return False

def test_api_key():
    """Test if API key is configured"""
    print("\n🔑 Testing API Key Configuration...")
    
    # Load .env if exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key and api_key != "your_gemini_api_key_here":
        print(f"✅ API key configured (starts with: {api_key[:10]}...)")
        return True
    else:
        print("❌ GEMINI_API_KEY not found or not set")
        print("   1. Get API key: https://makersuite.google.com/app/apikey")
        print("   2. Add to .env: GEMINI_API_KEY=your_key_here")
        return False

def test_gemini_integration():
    """Test the Gemini integration module"""
    print("\n🤖 Testing Gemini Integration Module...")
    try:
        from src.core.gemini_integration import GeminiIntegration
        print("✅ Gemini integration module loads successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import GeminiIntegration: {e}")
        return False
    except Exception as e:
        print(f"⚠️  Module loaded but with error: {e}")
        return False

def test_ai_engine():
    """Test AI engine with Gemini"""
    print("\n🧠 Testing AI Engine with Gemini...")
    try:
        from src.core.ai_engine import NEOAIEngine
        
        # Try to initialize with Gemini disabled first
        engine = NEOAIEngine(use_gemini=False)
        print("✅ AI Engine initialized (Gemini disabled)")
        
        # Try with Gemini enabled
        if os.getenv("GEMINI_API_KEY"):
            engine = NEOAIEngine(use_gemini=True)
            if engine.is_gemini_available():
                print("✅ AI Engine initialized with Gemini enabled")
                return True
            else:
                print("⚠️  AI Engine initialized but Gemini not available")
                return False
        else:
            print("⚠️  Skipping Gemini test (no API key)")
            return False
            
    except Exception as e:
        print(f"❌ AI Engine initialization failed: {e}")
        return False

def test_simple_query():
    """Test a simple Gemini query"""
    print("\n💬 Testing Simple Gemini Query...")
    
    if not os.getenv("GEMINI_API_KEY"):
        print("⏭️  Skipping (no API key)")
        return False
    
    try:
        from src.core.gemini_integration import GeminiIntegration
        
        print("   Sending test query to Gemini...")
        gemini = GeminiIntegration(model_name="gemini-2.0-flash")
        response = gemini.generate_text(
            "Say 'Hello from NEO!' in exactly 5 words",
            temperature=0.3,
            max_tokens=50
        )
        
        print(f"   Response: {response.text}")
        print("✅ Gemini query successful!")
        return True
        
    except Exception as e:
        print(f"❌ Query failed: {e}")
        if "API_KEY" in str(e).upper():
            print("   Check your API key is valid")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🔹 NEO Gemini Integration Test Suite")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Package Installation", test_gemini_installation()))
    results.append(("API Key Configuration", test_api_key()))
    results.append(("Integration Module", test_gemini_integration()))
    results.append(("AI Engine", test_ai_engine()))
    results.append(("Simple Query", test_simple_query()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Gemini is ready to use.")
        print("\nTry it out:")
        print("  python -m src.main")
        print("  You: /ai What is artificial intelligence?")
    elif passed >= 3:
        print("\n⚠️  Basic setup complete but some features unavailable.")
        print("Check the failed tests above for details.")
    else:
        print("\n❌ Setup incomplete. Please fix the errors above.")
        print("\nQuick fix:")
        print("  ./scripts/setup_gemini.sh")
    
    print("=" * 60)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
