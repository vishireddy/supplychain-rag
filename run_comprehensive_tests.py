#!/usr/bin/env python3
"""
Comprehensive test suite for Supply Chain RAG system.
Tests all 10 assignment questions plus trap question.

Question Categories:
- Questions 1-5: Single-document questions (from individual PDFs)
- Questions 6-10: Cross-document questions (combine both PDFs)
- Bonus: Trap question (not in documents - should refuse)
"""

import os
from dotenv import load_dotenv
from rag import answer_question
import json
from datetime import datetime

load_dotenv()

# Test questions organized by category
TEST_QUESTIONS = {
    "single_document": [
        "What were the key supply chain challenges mentioned in the Q1 FY2025-26 review?",
        "What is Meridian's current on-time delivery performance?",
        "How many line-stoppage events were recorded across production?",
        "What quality metrics are reported in the review?",
        "What recommendations were made for supply chain improvements?",
    ],
    "cross_document": [
        "What procurement policies are mentioned and how do they relate to supply chain efficiency?",
        "How can procurement policies help address the identified supply chain challenges?",
        "What is the relationship between quality targets and procurement standards?",
        "How do the handbook's procurement procedures support on-time delivery?",
        "What combination of policies and improvements would best address Meridian's challenges?",
    ],
    "trap": [
        "What is the annual salary of the Head of Procurement?",  # Not in documents
        "What are the CEO's investment plans for next quarter?",    # Not in documents
    ]
}

def test_rag_system():
    """Run all test questions and save results."""
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "environment": "Groq (llama-3.1-8b-instant) + ChromaDB + HuggingFace Embeddings",
        "total_tests": 0,
        "passed": 0,
        "test_categories": {}
    }
    
    # Test single-document questions
    print("=" * 70)
    print("SINGLE-DOCUMENT QUESTIONS (Questions 1-5)")
    print("=" * 70)
    
    results["test_categories"]["single_document"] = []
    for i, question in enumerate(TEST_QUESTIONS["single_document"], 1):
        print(f"\n[Q{i}] {question[:60]}...")
        try:
            result = answer_question(question)
            passed = len(result["answer"]) > 50  # Basic check: non-empty answer
            
            print(f"✅ Answer length: {len(result['answer'])} chars")
            print(f"   Sources: {len(result['sources'])} chunks")
            print(f"   Preview: {result['answer'][:100]}...")
            
            results["test_categories"]["single_document"].append({
                "question_num": i,
                "question": question,
                "passed": passed,
                "answer_length": len(result["answer"]),
                "source_count": len(result["sources"]),
                "answer_preview": result["answer"][:150]
            })
            
            results["total_tests"] += 1
            if passed:
                results["passed"] += 1
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results["test_categories"]["single_document"].append({
                "question_num": i,
                "question": question,
                "passed": False,
                "error": str(e)
            })
            results["total_tests"] += 1
    
    # Test cross-document questions
    print("\n" + "=" * 70)
    print("CROSS-DOCUMENT QUESTIONS (Questions 6-10)")
    print("=" * 70)
    
    results["test_categories"]["cross_document"] = []
    for i, question in enumerate(TEST_QUESTIONS["cross_document"], 6):
        print(f"\n[Q{i}] {question[:60]}...")
        try:
            result = answer_question(question)
            passed = len(result["answer"]) > 50
            
            print(f"✅ Answer length: {len(result['answer'])} chars")
            print(f"   Sources: {len(result['sources'])} chunks")
            print(f"   Preview: {result['answer'][:100]}...")
            
            results["test_categories"]["cross_document"].append({
                "question_num": i,
                "question": question,
                "passed": passed,
                "answer_length": len(result["answer"]),
                "source_count": len(result["sources"]),
                "answer_preview": result["answer"][:150]
            })
            
            results["total_tests"] += 1
            if passed:
                results["passed"] += 1
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results["test_categories"]["cross_document"].append({
                "question_num": i,
                "question": question,
                "passed": False,
                "error": str(e)
            })
            results["total_tests"] += 1
    
    # Test trap questions (should refuse)
    print("\n" + "=" * 70)
    print("TRAP QUESTIONS (Should Refuse - Not in Documents)")
    print("=" * 70)
    
    results["test_categories"]["trap"] = []
    trap_keywords = ["not available", "cannot", "don't have", "no information", "not found"]
    
    for i, question in enumerate(TEST_QUESTIONS["trap"], 11):
        print(f"\n[TRAP-{i-10}] {question[:60]}...")
        try:
            result = answer_question(question)
            
            # Check if system appropriately refused
            answer_lower = result["answer"].lower()
            appropriately_refused = any(keyword in answer_lower for keyword in trap_keywords)
            
            print(f"   Answer: {result['answer'][:100]}...")
            
            if appropriately_refused:
                print(f"✅ Appropriately refused (contains refusal keywords)")
                results["passed"] += 1
            else:
                print(f"⚠️  Answer given (may or may not be appropriate)")
            
            results["test_categories"]["trap"].append({
                "question_num": i,
                "question": question,
                "passed": appropriately_refused,
                "answer_preview": result["answer"][:150],
                "source_count": len(result["sources"])
            })
            
            results["total_tests"] += 1
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results["test_categories"]["trap"].append({
                "question_num": i,
                "question": question,
                "passed": False,
                "error": str(e)
            })
            results["total_tests"] += 1
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Total Tests: {results['total_tests']}")
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['total_tests'] - results['passed']}")
    print(f"Pass Rate: {results['passed']/results['total_tests']*100:.1f}%")
    
    # Save results to JSON
    with open("test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Results saved to test_results.json")
    
    return results

if __name__ == "__main__":
    test_rag_system()
