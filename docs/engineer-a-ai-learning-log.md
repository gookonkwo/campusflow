# Engineer A — AI Learning Log (CampusFlow Next)

## Scope and verification standard
This log records work performed on issue #3, branch `feat/3-validation-and-notes`. AI assistance was used for repository inspection, test planning, implementation, and CI-log analysis. Results below distinguish verified observations from pending checks.

## 1. Baseline before changes
- Inspected the existing ticket, workflow, storage, and CLI code and recorded baseline expectations in `docs/baseline-check.md`.
- Existing GitHub Actions baseline was green. The three manual CLI scenarios described in the baseline document remain **pending actual execution**; they are not claimed as passed.

## 2. Test-first validation and safeguards
- Added regression tests for invalid workflow changes (unassigned in-progress transitions and reassignment of resolved tickets) and for invalid ticket input.
- The validation test commit `d2d6260` initially produced a red CI run. A narrow change to `get_ticket` in commit `4815298` rejected non-string and blank IDs before calling `.strip()`; CI then passed.
- Learning: reject malformed input before mutating shared state, and verify that failed operations leave the collection unchanged.

## 3. Structured notes and persistence
- Added tests before implementing `add_note(tickets, ticket_id, author, message)`. The test-only commit `a0776aa` failed CI as expected; the implementation commit `a1bd5b9` passed.
- Note records use `{id, author, message}`; per-ticket IDs begin at `N001`. Blank author/message and notes on resolved tickets are rejected.
- Added persistence tests for restart continuity, invalid saved note records, and safe save failures. The test-only commit `7e9c6cd` failed before implementation. Commits `de747a2` and `2efeb54` implemented notes initialization and storage validation; CI passed.
- Learning: the JSON schema is a shared interface. Validate it at the persistence boundary and keep legacy tickets without a notes field readable.

## 4. Partner integration observation
- Engineer B's CLI originally accessed `note['note_id']`, whereas Engineer A's agreed API returns `note['id']`. Engineer B subsequently changed their CLI to use `id`.
- Engineer B's standalone CI also reported missing `campusflow.notes`, because that module lives on Engineer A's unmerged branch. This does **not** prove that the combined branches fail.
- Combined-branch execution and reciprocal PR review are still **pending**.

## 5. Verified automated evidence
- Engineer A GitHub Actions run: https://github.com/gookonkwo/campusflow/actions/runs/38591267615
- Log states: **Ran 43 tests in 0.022s** followed by **OK** on Python 3.9.
- Documentation-only follow-up commit `424a015` also passed GitHub Actions.
- The 43-test result is **Engineer A branch only**, not a combined-branch test.

## 6. Remaining actions
- Execute and record three manual CLI scenarios against a controlled checkout.
- Verify full test suite with both feature branches integrated.
- Complete reciprocal PR review with at least two substantive review observations each, resolve findings, then approve and merge according to team agreement.
