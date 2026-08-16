#!/usr/bin/env python3
"""Quick test of RAG system with 3 sample questions."""

import os
from dotenv import load_dotenv
from rag import answer_question

load_dotenv()

# Test 1: Single-document question
print("🧪 Test 1: Single-Document Question")
print("-" * 60)
q1 = "What were the key supply chain challenges mentioned?"
result = answer_question(q1)
print(f"Q: {q1}")
print(f"A: {result['answer'][:250]}...")
print(f"Sources: {len(result['sources'])} chunks")
print()

# Test 2: Cross-document question
print("🧪 Test 2: Cross-Document Question")
print("-" * 60)
q2 = "What procurement policies are recommended?"
result = answer_question(q2)
print(f"Q: {q2}")
print(f"A: {result['answer'][:250]}...")
print(f"Sources: {len(result['sources'])} chunks")
print()

# Test 3: Trap question (should refuse or admit no knowledge)
print("🧪 Test 3: Trap Question (Not in Documents)")
print("-" * 60)
q3 = "What is the annual salary of the Head of Procurement?"
result = answer_question(q3)
print(f"Q: {q3}")
print(f"A: {result['answer'][:250]}...")
