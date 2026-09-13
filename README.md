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
