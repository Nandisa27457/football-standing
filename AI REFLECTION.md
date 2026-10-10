# AI Reflection: How I Used Codex on the Football Standings Project

## Overview

I used OpenAI Codex CLI to build a Python CLI that turns match results into a 1974/75 league table. I worked piece by piece, with an AGENTS.md file holding the rules and conventions. Each prompt named the exact files Codex could touch, the behaviour I wanted, the tests to write, and a final instruction to run `python -m pytest` and show me the result. I reviewed each session's output instead of trusting the final report.

## How I directed the AI

* **Fixed rules in AGENTS.md.** Scoring, ranking order, the infinity rule for zero goals against, the input and output formats, and the coding conventions all lived in one file that Codex reads at the start of every session.
* **One piece per session.** The parser (Session 2), the formatter and CLI (Session 3) and the end-to-end test (Session 4) were separate requests.
* **A tight file list in every prompt.** I named the files Codex was allowed to touch and told it not to change the rest.
* **Tests as the proof.** Every prompt required tests and a pytest run shown to me, so I could check the claim "it works" against output.

## What I asked, what the AI did instead, and how I corrected it

### 1. Documenting Session 2 in the existing log file

* **What I asked:** Document the second session under the existing Codex session file.
* **What the AI did instead:** It created a new file that held the content of the first file plus the Session 2 content. That duplicated the first session's record and left the original file out of date.
* **How I corrected it:** I restored the intended setup, with one existing session file extended by the new session, instead of a second copy of the history.
* **Lesson:** "Add to this file" needs to say "edit in place, do not create or replace a file."

### 2. TeamRecord handling

* **What I asked:** Standings built from the match results, using the TeamRecord model.
* **What the AI did instead:** It wrote the team record data one item at a time. The code worked, but it was hard to read what the information said, and hard to maintain.
* **How I corrected it:** I wrote a function that collects that data in one place, which made the record clearer and easier to maintain. To do this I edited the code and added a helper function.
* **Lesson:** Passing tests do not make code readable. Structure and readability need my own review.

### 3. "Do not delete or rename any file" (Session 3)

* **What I asked:** Implement the formatter and CLI without deleting or renaming any file.
* **What the AI did instead:** It used a delete on `league/formatter.py` and `league/cli.py` and re-created both, instead of editing the stubs in place. Git showed them as modified, and the final report did not mention the deletions.
* **How I found it:** I read the session log, not only the summary.
* **Lesson:** A constraint in the prompt is not a guarantee. I check `git diff --stat` and the session log after each run, and I add "edit in place, never delete" to the prompt or AGENTS.md.

### 4. Quality gaps in the CLI (Session 3)

* **What the AI did:** It opened the `-o` output file before parsing, so a bad input line could leave an empty output file. It used one vague message for both read and write failures. Its missing-file test only checked that the word "traceback" was absent from stderr.
* **Status:** Found in review. The session logs do not show these fixed.
* **Lesson:** Tests that pass can still be weak. I need to read what each assertion actually proves.

### 5. The end-to-end test (Session 4)

* **What I asked:** Compare the CLI output to `tests/expected_week10.csv` exactly, and check seven totals, each with a comment explaining why it must be true.
* **What the AI did:**
  * The expected file was actually at `tests/tests/expected_week10.csv`. Codex used that path and told me.
  * It first halved the played, won, drawn and lost sums, which made the totals test fail. It then fixed the assertions itself.
  * One comment says "22 clubs in its 22 matches", which is wrong. 22 teams with one game each is 11 matches.
  * The exact-text test still fails (27 passed, 1 failed) because the expected CSV has no final newline and the CLI output does. Codex did not change the fixture because only one file was allowed, and it reported the failure openly.
* **Status:** The newline mismatch, the misplaced fixture and the wrong comment are still to be fixed.

## What worked well

* Rules in AGENTS.md kept the ranking and scoring logic consistent across sessions.
* Naming the allowed files kept changes small. The parser, standings and models files were left alone in Session 3, and the existing comments in them were kept.
* Requiring a pytest run meant failures were visible. In Session 4 Codex reported the failing test instead of hiding it.

## What I will do differently

* Say exactly how to change a file ("edit in place", "append to the existing file") and state that no new file should be created.
* Check the real changes with `git diff --stat` and the log after every session.
* Review readability and structure myself, because a working solution can still be hard to maintain.
* Check that fixtures and data files are where the prompt says they are before starting.
* Check that comments and test explanations are factually right, not only that the assertions pass.