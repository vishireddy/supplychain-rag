#!/usr/bin/env python3
"""
Complete test suite: All 10 assignment questions
"""
from rag import answer_question
import json
from datetime import datetime

# All 10 assignment questions
questions = [
    # Q1-4: Single-document questions
    ("Q1", "Which supplier had the highest spend in Q1, and what was its on-time delivery percentage?", "Single-doc (Review)"),
    ("Q2", "How many line stoppages happened in Q1, what was the total downtime, and what caused them?", "Single-doc (Review)"),
    ("Q3", "What is the approval authority for a purchase order worth ₹1.4 crore?", "Single-doc (Handbook)"),
    ("Q4", "What are the four supplier classification categories, and what qualifies a supplier as Critical?", "Single-doc (Handbook)"),
    
    # Q5-9: Cross-document questions
    ("Q5", "Kaveri Metals recorded 88.1% on-time delivery and 1,150 defects per million in Q1. Which policy clauses does this trigger, and what exactly must the buyer do?", "Cross-doc"),
    ("Q6", "The microcontroller supplier is single-source. What does the sourcing policy require in this situation, and what is the company already doing about it?", "Cross-doc"),
    ("Q7", "Microcontrollers are imported with a 46-day lead time. Using the safety-stock policy, how many days of stock should be held for this part?", "Cross-doc"),
    ("Q8", "Trident Circuit Boards had a defect rate of 640 parts per million. What is the cost consequence under the policy?", "Cross-doc"),
    ("Q9", "Which suppliers would fall below the B rating band on on-time delivery alone, and what is the escalation path for them?", "Cross-doc"),
    
    # Q10: Trap question
    ("Q10", "What is the annual salary of the Head of Procurement?", "Trap (should refuse)"),
]

def run_tests():
    print("\n" + "="*90)
    print("🧪 SUPPLY CHAIN RAG - COMPREHENSIVE TEST SUITE (10 QUESTIONS)")
    print("="*90 + "\n")
    
    results = []
    
    for q_id, question, category in questions:
        print(f"[{q_id}] {category}")
        print(f"❓ {question}")
        print("-" * 90)
        
        try:
            result = answer_question(question)
            answer = result.get('answer', 'No answer')
            sources = result.get('sources', [])
            
            # Truncate long answers for display
            display_answer = answer if len(answer) < 200 else answer[:200] + "..."
            print(f"✅ Answer: {display_answer}")
            
            if sources:
                print(f"📄 Sources: {len(sources)} chunks retrieved")
                for src in sources[:2]:
                    print(f"   • {src.get('file', 'Unknown')}, Page {src.get('page', 'Unknown')}")
                if len(sources) > 2:
                    print(f"   ... and {len(sources)-2} more chunks")
            
            results.append({
                "question_id": q_id,
                "category": category,
                "question": question,
                "answer": answer,
                "sources": sources,
                "status": "✅ Answered"
            })
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results.append({
                "question_id": q_id,
                "category": category,
                "question": question,
                "error": str(e),
                "status": "❌ Error"
            })
        
        print()
    
    # Summary
    print("="*90)
    print("📊 TEST SUMMARY")
    print("="*90)
    answered = sum(1 for r in results if r.get('status', '').startswith('✅'))
    print(f"✅ Passed: {answered}/{len(results)}")
    print(f"Single-doc (Q1-4): {sum(1 for r in results if 'Single-doc' in r.get('category', ''))}/4")
    print(f"Cross-doc (Q5-9): {sum(1 for r in results if 'Cross-doc' in r.get('category', ''))}/5")
    print(f"Trap test (Q10): {'✅ REFUSED (correct!)' if 'not available' in results[-1].get('answer', '').lower() else '❌ Did not refuse'}")
    print("="*90 + "\n")
    
    # Save results
    with open('test_results_full.json', 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_questions": len(results),
            "passed": answered,
            "results": results
        }, f, indent=2)
    
    print("✅ Results saved to test_results_full.json\n")
    return results

if __name__ == "__main__":
    run_tests()
