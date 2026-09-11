import os
from src.sign_generator import retrieve_signs, sequence_sign_videos

print("=== ISL Sign Generator Test ===")

# Test 1: Single target words
single_words = ["HELLO", "THANK_YOU", "WATER", "HELP", "WHERE", "GO", "YES", "NO"]
print("\n--- Test 1: Single Words Retrieval ---")
retrieved_paths = retrieve_signs(single_words)
for word, path in zip(single_words, retrieved_paths):
    print(f"{word:<12} -> {path}")

# Test 2: Short sequence "please help"
print("\n--- Test 2: Sequence 'please help' ---")
sequence_1 = ["PLEASE", "HELP"]
items_1 = sequence_sign_videos(sequence_1)
for item in items_1:
    print(f"Gloss: {item['word']:<10} | Rel: {item['relative_path']} | File Exists: {item['found']}")

# Test 3: Question sequence
print("\n--- Test 3: Question Sequence ---")
sequence_2 = ["WHERE", "YOU", "GO"]
items_2 = sequence_sign_videos(sequence_2)
for item in items_2:
    print(f"Gloss: {item['word']:<10} | Rel: {item['relative_path']} | File Exists: {item['found']}")