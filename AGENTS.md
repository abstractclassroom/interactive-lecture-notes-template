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
- Every question has a unique ID, Markdown prompt, response list, correct response, and feedback
- Mathematical notation is balanced and readable
- Links use stable relative paths when they refer to repository content
