# CampusFlow Next — Baseline Check

## Repository and audited baseline
- Repository: https://github.com/gookonkwo/campusflow
- Baseline commit on `main`: `53e51b8d83c0cd29ffbbee70a99054c2c9bac9b3`
- Engineer A issue: https://github.com/gookonkwo/campusflow/issues/3
- Engineer A feature branch: `feat/3-validation-and-notes`
- Existing app command (per README): `python3 main.py`
- Existing automated test command: `python -m unittest discover -s tests -v`
- GitHub Actions config: `.github/workflows/tests.yml`, Python 3.9, runs the above unittest command on push and pull request.
- Baseline GitHub Actions run: https://github.com/gookonkwo/campusflow/actions/runs/38586451753
- Verified result: **PASS**. The workflow finished successfully, including the Python unittest step.
- Baseline GitHub Actions job log: **Ran 27 tests in 0.019s**, followed by **OK** (Python 3.9). The full verbose output is available in the linked Actions run. A separate fresh-clone local run has not been performed.

## Three required manual input checks — interactive verification pending
The following are proposed reproducible inputs and expected results, not observed interactive manual test outcomes. Equivalent scripted CLI scenarios have been added in `tests/test_cli_scenarios_a.py` and passed in the Engineer A CI run linked below. Those automated results must not be represented as interactive manual execution.

1. **Priority precedence**: Create ticket title "Wi-Fi outage", category Network, urgency high, affected users 10. Expected calculated priority: critical.
2. **Unassigned ticket protection**: Create an open ticket without an assignee; attempt to change status to in_progress. Expected: action rejected; original ticket collection remains unchanged.
3. **Workflow and resolved protection**: Create a ticket; assign "Operator A"; change open → in_progress → resolved; attempt to reassign while resolved; then reopen resolved → open. Expected: legal transitions succeed, reassignment while resolved fails without changing data.

Record actual CLI command/inputs, observed output, and pass/fail for each case when run against the baseline.

## Existing codebase observations (not newly reproduced bugs)
- `campusflow/tickets.py`: ticket creation, normalized category/urgency validation, strictly positive integer affected-users validation (excluding booleans), ID generation, priority calculation, ticket lookup.
- `campusflow/workflow.py`: assignment, controlled status changes, OPEN-only work queue ordered by priority then numeric ID.
- `campusflow/storage.py`: JSON list load/save, collection validation, malformed JSON rejection, temporary-file + replace save.
- `campusflow/reports.py`: basic totals by status and priority.
- `main.py`: interactive ticket lifecycle CLI.
- `tests/`: existing regression tests.

## Challenge-driven improvement gaps and audit framing
The CampusFlow Next uploaded guide describes preliminary progressing-band audit feedback, **not proof of a reproduced defect**. Missing requested features in the baseline are:
- Structured follow-up notes with per-ticket N001-style IDs, validation, resolved-ticket protections, and persistence.
- Case-insensitive title search with combined optional category/status/priority filters (Engineer B).
- Category totals, unresolved/resolved metrics, safe zero-ticket resolution percentage (Engineer B).
- CLI note entry/view and six-question Engineering Understanding Check (Engineer B).
- Explicit test/documentation evidence for collection-wide unchanged state on invalid operations, invalid-load protection, and ticket/note ID continuity (Engineer A).

Existing checks for unassigned status transitions, nonpositive affected-users, and atomic saving should be preserved and regression-tested rather than labelled broken without reproduction.

## Engineer A scope and integration contract
- A1–A6: baseline, status and validation safety, notes domain API, invalid JSON rejection, restart ID continuity.
- Agreed API with Engineer B: `add_note(tickets, ticket_id, author, message)`, returning the created note dictionary and raising `ValueError` for invalid business requests.
- Maintain JSON list format and existing original feature behavior; coordinate before changing shared function contracts.
- Run original + new tests on the feature branch, document learning with independently verified experiments, and open a PR for reciprocal review before merge.

## Remaining evidence required
- Execute and record the three baseline CLI input scenarios.
- Baseline CI log count captured: 27 tests passed; Engineer A latest CI log count captured: 47 tests passed. A separate fresh-clone local run remains outstanding.
- Document specific reproduced failures, if any, with evidence.

## Feature-branch verification — 2026-10-14
- Engineer A head: `2efeb5402010252c4ec824617a95ce0d667ffa41`.
- GitHub Actions PR run: https://github.com/gookonkwo/campusflow/actions/runs/38591267615 — **PASS**.
- The Python 3.9 workflow log explicitly reports **Ran 43 tests in 0.022s**, followed by **OK**.
- This is verified CI evidence for Engineer A's branch only; it does **not** establish that Engineer B's changes or the combined branches pass.
- The three baseline manual CLI scenarios above are still pending actual execution and must not be marked complete.

## Latest Engineer A review-resolution verification — 2026-10-14
- Engineer A head: `1f2798ae4858dc3496361d87555f78ea07354e04`.
- GitHub Actions run: https://github.com/gookonkwo/campusflow/actions/runs/38593520822 — **PASS**.
- The Python 3.9 job log reports **Ran 47 tests in 0.033s**, followed by **OK**.
- New regression coverage checks malformed existing note IDs and preservation of unchanged state on rejection.
- The three CLI scenarios in `tests/test_cli_scenarios_a.py` ran as part of this automated suite. **Interactive manual CLI execution remains pending**; do not conflate these with observed manual results.
- Engineer B's review observation about malformed existing note IDs was addressed in commits `6ccb486` and `1f2798a`.
