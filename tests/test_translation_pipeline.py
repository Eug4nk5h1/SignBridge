"""Regression tests for the supported SignBridge gloss pipeline."""
import unittest

from src.concept_mapper import catalog_summary, resolve_sign_sequence
from src.nlp import analyze_sentence
from src.sign_generator import sequence_sign_videos
from src.translator import translate_to_asl


class TranslationPipelineTests(unittest.TestCase):
    def translate(self, sentence):
        analysis = analyze_sentence(sentence)
        return analysis, translate_to_asl(analysis)

    def test_documented_examples(self):
        examples = {
            "Hello": ["HELLO"],
            "My friend is coming today": ["I", "FRIEND", "COME", "TODAY"],
            "Your friend is coming today": ["YOU", "FRIEND", "COME", "TODAY"],
            "Is your friend coming today?": ["YOU", "FRIEND", "COME", "TODAY", "QUESTION"],
            "Where is your friend going?": ["WHERE", "YOU", "FRIEND", "GO"],
            "I am going to college": ["I", "GO", "COLLEGE"],
            "I love my family": ["I", "LOVE", "I", "FAMILY"],
            "I want to study today": ["I", "WANT", "STUDY", "TODAY"],
        }
        for sentence, expected in examples.items():
            with self.subTest(sentence=sentence):
                _, actual = self.translate(sentence)
                self.assertEqual(actual, expected)

    def test_wh_question_is_classified_and_preserved(self):
        analysis, glosses = self.translate("Where is your friend going?")
        self.assertEqual(analysis["sentence_type"], "QUESTION")
        self.assertEqual(analysis["question_type"], "WHERE")
        self.assertEqual(glosses[0], "WHERE")

    def test_yes_no_question_is_marked(self):
        analysis, glosses = self.translate("Is your friend coming today?")
        self.assertEqual(analysis["sentence_type"], "QUESTION")
        self.assertEqual(glosses[-1], "QUESTION")

    def test_negation_is_preserved(self):
        _, glosses = self.translate("I do not like this")
        self.assertIn("NO", glosses)

    def test_unknown_word_is_not_silently_dropped(self):
        _, glosses = self.translate("I like zorb")
        self.assertIn("ZORB", glosses)
        resolved = resolve_sign_sequence(glosses)
        zorb = next(item for item in resolved if item["gloss"] == "ZORB")
        self.assertEqual(zorb["status"], "unresolved")
        self.assertFalse(zorb["found"])

    def test_concept_and_sign_ids_resolve_to_real_assets(self):
        rows = resolve_sign_sequence(["HELLO", "FRIEND", "GO"])
        self.assertTrue(all(row["concept_id"] for row in rows))
        self.assertTrue(all(row["sign_id"] for row in rows))
        self.assertTrue(all(row["found"] for row in rows))

    def test_video_sequence_keeps_requested_order(self):
        rows = sequence_sign_videos(["I", "GO", "COLLEGE"])
        self.assertEqual([row["word"] for row in rows], ["I", "GO", "COLLEGE"])
        self.assertTrue(all(row["found"] for row in rows))

    def test_catalog_is_asl_scoped_and_populated(self):
        summary = catalog_summary()
        self.assertEqual(summary["languages"], ["ASL"])
        self.assertGreaterEqual(summary["concept_count"], 45)


if __name__ == "__main__":
    unittest.main()
