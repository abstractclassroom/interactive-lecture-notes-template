# Interactive Lecture Notes

This repository contains the source for your course's interactive lecture notes. You own the repository and every file in it.

Each lesson is a directory. Its directory path becomes the lesson path after the permanent course registration ID. For example:

```text
mathematics/set_theory/subsets
```

is published at:

```text
https://interactive.abstractclassroom.com/<course_registration_id>/mathematics/set_theory/subsets
```

Each lesson directory contains:

- `config.json` for the title, subtitle, publication status, description,
  objectives, prerequisites, and ordered presentation files
- Markdown files for instructor-authored lesson blocks
- One `*.question.json` file for each interactive check

The `order` array in `config.json` is the complete student presentation order.
Markdown is rendered with GitHub-style tables, links, images, fenced code, and
LaTeX expressions. Question prompts, responses, and feedback also accept
Markdown.

## Lesson configuration

Use this shape for `config.json`:

```json
{
  "schemaVersion": 1,
  "title": "Lesson title",
  "subtitle": "A short student-facing subtitle",
  "published": true,
  "description": "What this lesson covers",
  "order": [
    "01-concept.md",
    "concept-check.question.json",
    "02-example.md"
  ],
  "prerequisites": ["Knowledge students should already have"],
  "objectives": ["An observable outcome for this lesson"]
}
```

Setting `published` to `false` keeps the directory unavailable to students.
Every filename in `order` must be in the same lesson directory.

Use this shape for a question file:

```json
{
  "schemaVersion": 1,
  "id": "stable-question-id",
  "type": "single_choice",
  "prompt": "Which statement is **true**?",
  "responses": [
    { "id": "a", "markdown": "First response" },
    { "id": "b", "markdown": "Second response" }
  ],
  "correctResponse": "a",
  "feedback": {
    "correct": "Correct feedback",
    "incorrect": "A concise hint"
  }
}
```

The included lessons are safe samples. Replace, rename, or reorganize them to fit your curriculum.

## Fill-in-the-blank questions

Use `type: "fill_in_blank"` in a normal `*.question.json` file and list it in
`config.json`'s `order`, just like a multiple-choice question. Schema version
remains 1. No Markdown syntax, publishing workflow, or MDX changes are needed.

```json
{
  "schemaVersion": 1,
  "id": "generator-count-c48",
  "type": "fill_in_blank",
  "prompt": "How many generators does $C_{48}$ have?",
  "answer": { "mode": "integer", "value": 16 },
  "feedback": {
    "correct": "Correct! $\\varphi(48)=16$.",
    "incorrect": "Try again. Use Euler's totient function."
  }
}
```

Choose exactly one of these answer shapes:

| Mode | Required answer object | Matching rule |
| --- | --- | --- |
| String | `{"mode":"string","value":"cyclic"}` | Trim leading/trailing whitespace from both entries, then match exactly. Capitalization and internal whitespace matter. |
| Integer | `{"mode":"integer","value":16}` | Accept signed whole-number digits, e.g. `16`, `+16`, `016`. Reject decimals (`16.0`), exponents, fractions, and expressions. |
| Approximate | `{"mode":"approximate","min_value":3.14,"max_value":3.15}` | Accept a finite number in the inclusive range: `min_value <= answer <= max_value`. Decimal and scientific notation are allowed. |

Both approximate bounds are mandatory JSON numbers; `min_value` cannot exceed
`max_value`. Equal bounds are allowed. Integer `value` must be a JSON integer
between -9007199254740991 and 9007199254740991, inclusive. String `value` must be
single-line, nonempty after trimming, and at most 2,000 characters. Student input is limited to
2,000 characters. All modes ignore leading/trailing input whitespace and reject
blank submissions. Numeric input uses ASCII digits, optional `+`/`-`, and a
period for the decimal separator; commas, units, arithmetic, hexadecimal,
non-finite values, and numeric overflow/underflow are not accepted.

Only the fields shown for the chosen mode are permitted inside `answer`.
Do not include `responses` or `correctResponse` on a fill-in-the-blank question.
There is one labeled answer field beneath the Markdown prompt; underscores in
Markdown do not create additional inputs. Typed answers are plain text, not Markdown.

Students use **Check Answer** or Enter to submit and can retry until correct.
Correct answers unlock **Continue**. The accepted entry and instructor explanation
remain visible in the completed card and in **Print Notes**. Answers are kept
only in the current page's memory, not sent to the server; refreshing restarts
the lesson. This remains practice, not server-verified assessment.

The Cardinality sample includes one question for each mode. Existing
instructor repositories are not changed by this template update: add question
files and update their lesson order when you want to use the feature.

## Completion receipts

After the final block, a student can download a signed JWT completion receipt to
submit through your LMS. The receipt identifies the course, lesson path, exact
lesson-content digest, completion time, signing-key version, and a unique receipt
ID. It does not contain the student's name, username, or email address. Your
educator dashboard can validate submitted receipts for courses you own.

The receipt authenticates AbstractClassroom-issued lesson claims. It does not
independently establish student identity or prove completion of the browser flow.

## AbstractClassroom connection and publishing

Register your course in AbstractClassroom, then choose **Link repository** and
open repository setup. The dashboard provides a token valid for two hours. In this repository:

1. Open **Settings → Secrets and variables → Actions → New repository secret**.
2. Name the secret `ABSTRACTCLASSROOM_PAIRING_TOKEN` and paste the generated value.
3. Open **Actions → Publish to AbstractClassroom → Run workflow** on `main`.

This same workflow pairs the repository and publishes its lesson files. A run
before adding the secret cannot connect; add the secret and rerun it. You may
choose any repository name, including at creation. No GitHub App installation is
required, and personal or organization repositories use the same process.

The first authenticated run binds your course to GitHub's immutable numeric
repository ID and consumes the token. You can then delete the secret: future
publishing uses OIDC and the stored repository ID. An expired secret left behind
also does not block publishing. Renames and transfers retain the association;
a fork, copy, or newly created replacement has a different identity. Generating a
replacement token before connection invalidates the previous token.

Every push to `main`, or a manual run of **Publish to AbstractClassroom**, checks
out the exact workflow commit and runs `.github/scripts/sync-content.py`:

1. Collect tracked lesson `config.json` files, their ordered Markdown and question
   JSON files, and supported images inside those lesson directories.
2. Authenticate with GitHub OIDC and obtain 15-minute AWS credentials restricted
   to this course's staging prefix in a private shared S3 bucket.
3. Sync files to staging and upload their checksummed manifest last.
4. Wait while AbstractClassroom validates the complete snapshot and publishes it.

Students read the published S3 snapshot. AbstractClassroom does not fetch lesson
files from GitHub while serving students. GitHub remains your authoring source,
and public and private repositories use the same publishing flow. The one-time
pairing token belongs only in GitHub Actions secrets. No permanent AWS credentials
are needed, and no credentials belong in repository files.

A failed sync leaves the previous publication active. A successful sync replaces
the course's complete snapshot: files removed from the lesson configuration or
repository are absent from the new publication. Older workflow runs cannot
replace a newer publication. Lessons with `published: false` remain unavailable.

Uploads support up to 1000 files and 100 MB per publication. Individual limits
are 64 KB for JSON, 256 KB for Markdown, and 5 MB for AVIF, GIF, JPEG, PNG, or WebP
images. Symlinks, untracked files, unrelated JSON, and files outside lesson
directories are excluded or rejected. Do not place credentials in lesson files.

When adopting this publishing workflow in an existing course repository, copy
both `.github/workflows/abstractclassroom.yml` and
`.github/scripts/sync-content.py`, commit them to `main`, and run the workflow.
Copying or updating the template does not update existing course repositories.

To replace the linked repository, choose **Change repo** in the course dashboard.
Type **CHANGE REPOSITORY** and check **I understand**. The current repository is
disconnected immediately and no lessons are served until the replacement is
linked and published. Add the new token to the replacement repository using the
same secret name above. **Repository unlinked** reopens the instructions; after
two hours it generates a fresh token. Reloading the dashboard also requires a
fresh token because tokens are kept only in page memory.
