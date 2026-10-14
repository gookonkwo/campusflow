# CampusFlow Next — CLI Helpdesk

CampusFlow Next is a Python standard-library command-line helpdesk for creating and prioritizing campus support tickets, assigning staff, managing ticket workflows, searching records, recording follow-up notes, reporting, and persisting tickets to JSON.

## Team and contributions
- **Engineer A — [eeyung1](https://github.com/eeyung1)** ([issue #3](https://github.com/gookonkwo/campusflow/issues/3), [PR #5](https://github.com/gookonkwo/campusflow/pull/5)): ticket and workflow validation safeguards, structured follow-up note domain API, JSON note validation and persistence, ID continuity, regression tests, baseline and learning documentation.
- **Engineer B — [gookonkwo](https://github.com/gookonkwo)** ([PR #6](https://github.com/gookonkwo/campusflow/pull/6)): case-insensitive ticket search and combined filters, expanded reports, CLI note/search menus, Engineering Understanding Check, and regression tests.
- Both engineers completed reciprocal code review and approved each other's feature PR before merge.

## Requirements
Python 3.9 or newer. No third-party packages required.

## Run
```bash
python3 main.py
```

Use a separate data file for experiments:
```bash
python3 main.py --data data/demo.json
```

The default data file is `data/tickets.json`. Changes are saved after successful mutations. For isolated manual checks, use a new path; do not delete an existing data file without backing it up.

## CLI menu
| Option | Action |
| --- | --- |
| 1 | Create ticket |
| 2 | List tickets |
| 3 | View ticket |
| 4 | Assign staff |
| 5 | Change status / reopen |
| 6 | Work queue |
| 7 | Reports |
| 8 | Exit |
| 9 | Search tickets |
| 10 | Engineering Understanding Check |
| 11 | Add follow-up note |
| 12 | View ticket notes |

Option 8 remains Exit for compatibility. Search accepts an optional title substring and category, status, and priority filters (blank means all). The Engineering Understanding Check has six questions.

## Core behavior
- **Priority:** high urgency with at least 10 affected users = critical; otherwise high urgency or 10+ users = high; medium urgency or 3+ users = medium; otherwise low.
- **Workflow:** tickets start open; starting work requires assignment. Tickets can progress to in_progress and resolved; resolved tickets must be reopened before reassignment or follow-up notes.
- **Work queue:** open tickets ordered by priority and numeric ticket ID.
- **Notes:** per-ticket IDs such as `N001`, with author and message; invalid or blank inputs are rejected. Notes persist in JSON and retain ID continuity after reload.
- **Search:** case-insensitive title matching with optional AND-combined category, status, and priority filters. Results are independent copies.
- **Reports:** ticket counts by status, priority and category, unresolved and resolved totals, and a resolution percentage that handles an empty dataset.
- **Persistence:** JSON content is validated when loaded and saved. Invalid saved data causes a startup error rather than silent replacement. Successful saves use temporary-file replacement; rejected operations do not commit mutations.

## Automated tests
```bash
python3 -m unittest discover -s tests -v
```

**Final merged `main` verification (2026-10-14):** 67 tests passed, zero failures, Python 3.9 GitHub Actions. [Workflow evidence](https://github.com/gookonkwo/campusflow/actions/runs/38596294987). This is automated CI evidence, not a claim that every CLI feature was manually exercised on final `main`.

## Manual verification and audit evidence
- [Baseline and feature-branch CLI verification](docs/baseline-check.md): scenario 1 has supplied terminal output; scenarios 2–3 were confirmed as passing by the operator without complete transcripts. Those interactive checks ran on Engineer A's feature branch, not on final `main`.
- [Final integration verification](docs/final-verification.md): merge SHAs, test count, CI evidence, and remaining manual verification scope.
- [Engineer A AI learning log](docs/engineer-a-ai-learning-log.md).
- [Engineer A PR #5](https://github.com/gookonkwo/campusflow/pull/5) and [Engineer B PR #6](https://github.com/gookonkwo/campusflow/pull/6) contain the reciprocal review discussion and approvals.
- [Temporary integration PR #7](https://github.com/gookonkwo/campusflow/pull/7) was used for verification only and must not be merged.

## Limitations
This is a local single-user CLI; it does not implement authentication, multi-process concurrency, or a graphical interface. Run only one instance against a given JSON file.
