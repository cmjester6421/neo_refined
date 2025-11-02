#!/usr/bin/env python3
"""
NEO with Gemini AI - Quick Demo
Demonstrates the integration of Google Gemini AI with NEO
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.ai_engine import NEOAIEngine

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def demo_basic_query():
    """Demo: Basic AI query"""
    print_header("🤖 Demo 1: Basic AI Query")
    
    engine = NEOAIEngine(use_gemini=True)
    
    if not engine.is_gemini_available():
        print("❌ Gemini not available. Please check your API key.")
        return
    
    print("\nQuery: What is machine learning?")
    print("-" * 70)
    
    response = engine.generate_response(
        "Explain machine learning in 3 sentences for a beginner.",
        temperature=0.7,
        max_tokens=500
    )
    
    print(response)

def demo_code_analysis():
    """Demo: AI-powered code analysis"""
    print_header("💻 Demo 2: Code Analysis with AI")
    
    engine = NEOAIEngine(use_gemini=True)
    
    if not engine.is_gemini_available():
        print("❌ Gemini not available.")
        return
    
    code = """
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    left = [x for x in arr[1:] if x < pivot]
    right = [x for x in arr[1:] if x >= pivot]
    return quicksort(left) + [pivot] + quicksort(right)
"""
    
    print("\nAnalyzing this code:")
    print("-" * 70)
    print(code)
    print("-" * 70)
    
    analysis = engine.analyze_code_with_ai(code, "python")
    
    if "error" in analysis:
        print(f"Error: {analysis['error']}")
    else:
        print("\n📊 Analysis Results:")
        import json
        print(json.dumps(analysis, indent=2))

def demo_problem_solving():
    """Demo: Problem solving with reasoning"""
    print_header("🧠 Demo 3: Problem Solving with AI Reasoning")
    
    engine = NEOAIEngine(use_gemini=True)
    
    if not engine.is_gemini_available():
        print("❌ Gemini not available.")
        return
    
    problem = "How do I implement a cache with LRU eviction policy?"
    
    print(f"\nProblem: {problem}")
    print("-" * 70)
    
    solution = engine.solve_with_ai(
        problem,
        context="I'm building a web application that needs caching"
    )
    
    print(solution)

def demo_chat():
    """Demo: Interactive chat"""
    print_header("💬 Demo 4: Chat Conversation")
    
    engine = NEOAIEngine(use_gemini=True)
    
    if not engine.is_gemini_available():
        print("❌ Gemini not available.")
        return
    
    messages = [
        "What are microservices?",
        "What are the benefits?",
        "What are common challenges?"
    ]
    
    context = []
    
    for i, msg in enumerate(messages, 1):
        print(f"\n[Message {i}] You: {msg}")
        print("-" * 70)
        
        response = engine.chat_with_gemini(msg, context)
        print(f"NEO: {response[:300]}...")
        
        # Update context
        context.append({"role": "user", "content": msg})
        context.append({"role": "assistant", "content": response})

def demo_translation():
    """Demo: Translation"""
    print_header("🌍 Demo 5: Multi-language Translation")
    
    engine = NEOAIEngine(use_gemini=True)
    
    if not engine.is_gemini_available():
        print("❌ Gemini not available.")
        return
    
    text = "Artificial intelligence is transforming the world."
    languages = ["Spanish", "French", "Japanese"]
    
    print(f"\nOriginal: {text}")
    print("-" * 70)
    
    for lang in languages:
        translation = engine.translate_with_ai(text, lang)
        print(f"{lang}: {translation}")

def demo_summarization():
    """Demo: Text summarization"""
    print_header("📝 Demo 6: Text Summarization")
    
    engine = NEOAIEngine(use_gemini=True)
    
    if not engine.is_gemini_available():
        print("❌ Gemini not available.")
        return
    
    long_text = """
    Quantum computing is a revolutionary technology that leverages the principles 
    of quantum mechanics to process information in fundamentally different ways 
    compared to classical computers. Unlike classical bits that can only be in 
    states of 0 or 1, quantum bits (qubits) can exist in superposition, meaning 
    they can be in multiple states simultaneously. This property, along with 
    quantum entanglement, allows quantum computers to explore many possible 
    solutions to a problem at once, potentially solving certain types of problems 
    exponentially faster than classical computers. Key applications include 
    cryptography, drug discovery, financial modeling, and optimization problems. 
    However, quantum computers are still in early stages of development and face 
    significant challenges including maintaining qubit coherence, error correction, 
    and scaling up the number of qubits.
    """
    
    print("\nLong text (150+ words):")
    print("-" * 70)
    print(long_text.strip())
    print("\n" + "-" * 70)
    
    summary = engine.summarize_with_ai(long_text, max_length=50)
    
    print(f"\nSummary (50 words): {summary}")

def main():
    """Run all demos"""
    print("\n" + "🔹" * 35)
    print("  NEO with Google Gemini AI - Interactive Demo")
    print("🔹" * 35)
    
    demos = [
        ("Basic AI Query", demo_basic_query),
        ("Code Analysis", demo_code_analysis),
        ("Problem Solving", demo_problem_solving),
        ("Chat Conversation", demo_chat),
        ("Translation", demo_translation),
        ("Summarization", demo_summarization),
    ]
    
    print("\nAvailable Demos:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"  {i}. {name}")
    print("  0. Run all demos")
    print("  q. Quit")
    
    while True:
        choice = input("\nSelect demo (0-6, q): ").strip().lower()
        
        if choice == 'q':
            print("\n👋 Goodbye!")
            break
        
        if choice == '0':
            # Run all demos
            for name, demo_func in demos:
                try:
                    demo_func()
                    input("\n⏎ Press Enter to continue...")
                except KeyboardInterrupt:
                    print("\n\nDemo interrupted.")
                    break
                except Exception as e:
                    print(f"\n❌ Error in {name}: {e}")
            break
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(demos):
                name, demo_func = demos[idx]
                try:
                    demo_func()
                except Exception as e:
                    print(f"\n❌ Error: {e}")
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Invalid input. Enter a number or 'q'.")
    
    print("\n" + "=" * 70)
    print("  Thank you for trying NEO with Gemini AI!")
    print("  For more info: docs/GEMINI_GUIDE.md")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
