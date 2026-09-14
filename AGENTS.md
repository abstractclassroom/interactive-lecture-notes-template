# Agent guide for this course repository

## Purpose

Help the instructor author Interactive Lecture Notes without changing the content, voice, or instructional intent unless asked.

## Lesson structure

Every publishable lesson directory must contain `config.json`. Its `order` array
lists the Markdown and `*.question.json` files presented to students. Use the
lessons under `set_theory/` as the schema reference. Keep JSON valid and use
stable question IDs within each lesson.

## Authoring rules

- Preserve the instructor's terminology and teaching voice
- Use Markdown for prose, examples, headings, tables, and mathematical notation
- Put objectives and prerequisites in `config.json`, not in duplicated Markdown sections
- Put each interactive check in its own `*.question.json` file
- Do not invent citations, course policies, due dates, or grading rules
- Do not delete or rename existing lessons without explicit approval
- Validate every edited JSON file before finishing

## Review checklist

- The lesson directory contains `config.json` and every file named by `order`
- The metadata title is concise and student-facing
- Objectives use observable verbs
- Prerequisites name only knowledge actually needed by the lesson
- Every question has a unique ID, Markdown prompt, and correct/incorrect feedback
- Single-choice questions use `type: "single_choice"`, a response list, and a correct response ID
- Fill-in-the-blank questions use `type: "fill_in_blank"` and one `answer` object: `string` (trimmed, case-sensitive `value`), `integer` (safe integer `value`), or `approximate` (required inclusive `min_value` and `max_value`)
- Do not mix choice fields with typed answers; see README for exact fields, input limits, and sample questions
- Mathematical notation is balanced and readable
- Links use stable relative paths when they refer to repository content

## Publishing

The workflow and `.github/scripts/sync-content.py` publish complete, validated
lesson snapshots to AbstractClassroom's private S3 content bucket. Keep both
files when updating the template. Student delivery reads the active S3 snapshot;
changes become visible after the publishing workflow succeeds. GitHub OIDC and
the established immutable repository ID authorize only this course's staging
upload. Never add permanent AWS credentials or loosen the course binding.

Initial pairing requires the course-scoped `ABSTRACTCLASSROOM_PAIRING_TOKEN` in
repository Actions secrets. It expires after two hours and is consumed once the
publishing workflow binds the immutable repository ID. Future runs do not need
it. Never commit, print, or copy the token into lesson files. Repository names
are suggestions and provide no pairing authority.
