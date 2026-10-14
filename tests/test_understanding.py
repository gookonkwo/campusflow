"""Tests for the understanding check's scoring and input retry."""

import unittest

from campusflow.understanding_check import score_answers, run_understanding_check


class UnderstandingCheckTests(unittest.TestCase):
    def test_correct_answers_score_six(self):
        self.assertEqual(score_answers(["B", "C", "B", "C", "C", "B"]), 6)

    def test_wrong_answers_score_zero(self):
        self.assertEqual(score_answers(["A"] * 6), 0)

    def test_invalid_answer_list_is_rejected(self):
        with self.assertRaises(ValueError):
            score_answers(["B", "C"])
        with self.assertRaises(ValueError):
            score_answers(["B", "C", "B", "C", "C", "X"])

    def test_invalid_choice_retries_without_extra_score(self):
        inputs = iter(["X", "", "B", "C", "B", "C", "C", "B",
                       "Unassigned tickets cannot start.",
                       "Zero total cannot be divided."])
        output = []
        result = run_understanding_check(
            input_fn=lambda prompt: next(inputs), output_fn=output.append)
        self.assertEqual(result["score"], 6)
        self.assertEqual(len(result["answers"]), 6)
        self.assertEqual(len(result["explanations"]), 2)
        self.assertEqual(output.count("Please enter A, B, C or D."), 2)


if __name__ == "__main__":
    unittest.main()
