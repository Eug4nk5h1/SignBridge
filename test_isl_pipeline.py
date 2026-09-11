import os
import sys

from src.nlp import analyze_sentence
from src.translator import translate_to_asl
from src.sign_library import get_sign, get_absolute_sign_path
from src.sign_generator import sequence_sign_videos


def test_required_words():
    print("==========================================")
    print("TEST 1: Required Individual Vocabulary Words")
    print("==========================================")
    required_words = ["hello", "thank_you", "water", "help", "where", "go", "yes", "no"]
    all_ok = True

    for word in required_words:
        rel_path = get_sign(word)
        abs_path = get_absolute_sign_path(word)
        exists = abs_path is not None and os.path.exists(abs_path)

        if not exists:
            all_ok = False

        status = "EXISTS" if exists else "MISSING"
        print(f"Gloss: {word.upper():<12} -> MP4 Path: {rel_path} [{status}]")

    assert all_ok, "One or more required vocabulary words missing!"
    print("-> Test 1 PASSED: All 8 required words mapped to valid MP4 paths.\n")


def test_short_sequence_please_help():
    print("==========================================")
    print("TEST 2: Short Sequence 'please help'")
    print("==========================================")
    sequence = ["PLEASE", "HELP"]
    video_records = sequence_sign_videos(sequence)

    for record in video_records:
        print(f"Word: {record['word']} | Path: {record['relative_path']} | Valid File: {record['found']}")
        assert record['found'], f"Video for {record['word']} not found!"

    print("-> Test 2 PASSED: Sequence 'please help' mapped to valid MP4 files.\n")


def test_end_to_end_nlp_translator_pipeline():
    print("==========================================")
    print("TEST 3: End-to-End NLP -> Translation -> Sign Generation Pipeline")
    print("==========================================")
    test_sentences = [
        "Please help.",
        "Where are you going?",
        "Do you want water?",
        "Thank you."
    ]

    for sentence in test_sentences:
        print(f"\nInput English Sentence: '{sentence}'")
        analysis = analyze_sentence(sentence)
        sign_tokens = translate_to_asl(analysis)
        print(f"Extracted ISL Gloss Tokens: {sign_tokens}")

        video_records = sequence_sign_videos(sign_tokens)
        for record in video_records:
            status = "FOUND" if record['found'] else "MISSING"
            print(f"  - Gloss: {record['word']:<10} -> Video: {record['relative_path']} [{status}]")

    print("\n-> Test 3 PASSED: End-to-End Pipeline execution successful.\n")


if __name__ == "__main__":
    print("Starting SignBridge ISL Dataset Integration Tests...\n")
    test_required_words()
    test_short_sequence_please_help()
    test_end_to_end_nlp_translator_pipeline()
    print("ALL INTEGRATION TESTS PASSED SUCCESSFULLY!")
