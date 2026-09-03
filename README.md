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

The receipt confirms that the interactive flow reached completion in the
student's browser. It is not a proctored identity or assessment credential.

## AbstractClassroom connection

The included GitHub workflow securely identifies this repository to AbstractClassroom when the repository is created and whenever content is pushed to main. It uses a short-lived GitHub identity token and contains no stored AbstractClassroom secret.

If the repository name and owner do not match a registered course, AbstractClassroom ignores the workflow request and makes no changes.
