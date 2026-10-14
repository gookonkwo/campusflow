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
- Exact test count, complete verbose output, and a separate fresh-clone run: **not captured here**. They must not be represented as verified.

## Three required manual input checks — pending reproduction
The following are proposed reproducible inputs and expected results, not observed manual test outcomes.

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
- Record full unittest count/output from a fresh clone or downloadable CI log.
- Document specific reproduced failures, if any, with evidence.
