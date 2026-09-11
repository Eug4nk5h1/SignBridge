import os
from src.sign_library import get_sign, get_absolute_sign_path

target_test_words = [
    "hello",
    "thank_you",
    "water",
    "help",
    "where",
    "go",
    "yes",
    "no",
    "please",
    "brother",
    "school"
]

print("=== ISL Sign Library Lookup Test ===")
all_passed = True

for word in target_test_words:
    rel_path = get_sign(word)
    abs_path = get_absolute_sign_path(word)
    exists = abs_path is not None and os.path.exists(abs_path)

    if not exists:
        all_passed = False

    status = "OK" if exists else "MISSING"
    print(f"Word: {word:<12} -> RelPath: {str(rel_path):<40} [File Exists: {status}]")

print("\nSign Library Test Result:", "PASSED" if all_passed else "FAILED")