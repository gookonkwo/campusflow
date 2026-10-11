# CampusFlow: two-person finish plan

The application is implemented. Both engineers should use this same complete package; splitting the code into separate incomplete apps would prevent integrated testing.

## Engineer A — GoodGod
Own: main.py, campusflow/tickets.py, campusflow/storage.py, tests/test_cli.py, tests/test_tickets.py, tests/test_storage.py.

1. Run the CLI and verify create, list and view.
2. Verify all four priority rules and invalid input messages.
3. Close and restart the program; confirm tickets and the next ticket ID persist.
4. Review and improve these files as needed. Run the full test suite.
5. Commit changes on a separate branch and open a pull request.
6. Review Engineer B's workflow changes.

## Engineer B — teammate
Own: campusflow/workflow.py, campusflow/reports.py, tests/test_workflow.py.

1. Verify assignment, starting, resolving and reopening tickets.
2. Confirm blank staff and invalid transitions leave tickets unchanged.
3. Verify only open tickets appear in the queue, ordered by priority then numeric ID.
4. Verify status and priority report counts, including an empty collection.
5. Review the included workflow validation improvements and tests; make useful changes if needed. Run the full test suite.
6. Commit changes on a separate branch and open a pull request.
7. Review Engineer A's CLI, ticket and storage changes.

## Run and test
Python 3.9 or newer; no third-party packages.

    python3 main.py
    python3 -m unittest discover -s tests -v

The supplied version passes 27 tests.

## Repository handoff
The completion baseline is already pushed to feat/complete-cli. Each engineer creates their branch FROM that baseline:

    git fetch origin
    git switch -c YOUR_BRANCH origin/feat/complete-cli

Engineer A branch suggestion: feat/a-cli-storage-review
Engineer B branch suggestion: feat/b-workflow-review

Copy the contents of this package into the repository root (the folder with .git). main.py, tests/, and campusflow/ must be side by side. Do not place the entire outer folder inside the repository. The ZIP does not include .git or local ticket data.

Open follow-up pull requests against feat/complete-cli while the baseline PR is still open. Once the baseline is merged, target main and update your branch accordingly. Run all tests after combining changes.

## Before submission
- Fill in both real names and actual contributions in README.md.
- Add genuine pull request review links. Do not invent reviews or attribute assistant-written code to someone merely because they pushed it.
- Verify the merged main branch passes all tests.
- Record a short demo: create, assign, start, resolve, reopen, queue, report, restart.

Shared-code ownership is a review division; each person should be able to explain their area. No further feature is required solely to create a contribution.
