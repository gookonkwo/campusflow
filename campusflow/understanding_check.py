"""Six-question Engineering Understanding Check.

Question data is separate from scoring and input/output.
"""

QUESTIONS = (
    ("T001 is open and unassigned. Move to in_progress?",
     ("Accept", "Reject and preserve all data", "Resolve automatically", "Remove ticket"), "B"),
    ("Zero tickets: what resolution percentage?",
     ("Crash", "100%", "0%", "Divide by one without explanation"), "C"),
    ("Search wifi + Network + open: which tickets match?",
     ("Any filter", "All supplied filters", "All network", "All open"), "B"),
    ("Add note to a resolved ticket?",
     ("Append anyway", "Delete old notes", "Reject until reopened", "Change status silently"), "C"),
    ("JSON has duplicate ticket IDs. What should loading do?",
     ("Keep both", "Replace memory", "Reject without changing memory", "Rename IDs silently"), "C"),
    ("PR changes validation without negative tests?",
     ("Approve", "Request tests and reasoning", "Merge", "Ask AI to approve"), "B"),
)


def score_answers(answers, questions=QUESTIONS):
    """Score first submitted valid choices; never grade explanations automatically."""
    if len(answers) != len(questions):
        raise ValueError("One answer is required for each question")
    if any(not isinstance(answer, str) or answer.upper() not in "ABCD"
           or len(answer) != 1 for answer in answers):
        raise ValueError("Answers must be A, B, C or D")
    return sum(answer.upper() == question[2] for answer, question in zip(answers, questions))


def run_understanding_check(input_fn=input, output_fn=print):
    """Ask six questions; retry invalid choices; collect two explanations."""
    answers = []
    for number, (scenario, options, _) in enumerate(QUESTIONS, 1):
        output_fn(f"Q{number}. {scenario}")
        for letter, option in zip("ABCD", options):
            output_fn(f"{letter}. {option}")
        while True:
            try:
                answer = input_fn("Answer (A/B/C/D): ").strip().upper()
            except (EOFError, KeyboardInterrupt):
                output_fn("Understanding check cancelled.")
                return None
            if answer in ("A", "B", "C", "D"):
                answers.append(answer)
                break
            output_fn("Please enter A, B, C or D.")
    score = score_answers(answers)
    output_fn(f"Final score: {score}/6")
    explanations = []
    for number in (1, 2):
        try:
            explanation = input_fn(f"Explain your answer to Q{number}: ").strip()
        except (EOFError, KeyboardInterrupt):
            output_fn("Explanation collection cancelled.")
            return {"score": score, "answers": answers, "explanations": explanations}
        explanations.append(explanation)
    output_fn("Discuss your explanations with your mentor; they are not auto-graded.")
    return {"score": score, "answers": answers, "explanations": explanations}
