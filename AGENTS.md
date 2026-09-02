# Agent guide for this course repository

## Purpose

Help the instructor author Interactive Lecture Notes without changing the content, voice, or instructional intent unless asked.

## Lesson structure

Every publishable lesson directory must contain all three files:

- `lecture.md`
- `metadata.json`
- `questions.json`

Use existing sample lessons as the schema reference. Keep JSON valid and use stable question IDs within each lesson.

## Authoring rules

- Preserve the instructor's terminology and teaching voice
- Use Markdown for prose, examples, headings, tables, and mathematical notation
- Put objectives and prerequisites in `metadata.json`, not in duplicated Markdown sections
- Put interactive checks in `questions.json`
- Do not invent citations, course policies, due dates, or grading rules
- Do not delete or rename existing lessons without explicit approval
- Validate every edited JSON file before finishing

## Review checklist

- The lesson directory contains the three expected files
- The metadata title is concise and student-facing
- Objectives use observable verbs
- Prerequisites name only knowledge actually needed by the lesson
- Every question has a unique ID, prompt, type, answer, and feedback
- Mathematical notation is balanced and readable
- Links use stable relative paths when they refer to repository content
