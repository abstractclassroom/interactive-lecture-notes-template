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

- `lecture.md` for the lesson content
- `metadata.json` for the title, objectives, and prerequisites
- `questions.json` for interactive follow-up questions

The two included lessons are safe samples. Replace, rename, or reorganize them to fit your curriculum.

## AbstractClassroom connection

The included GitHub workflow securely identifies this repository to AbstractClassroom when the repository is created and whenever content is pushed to main. It uses a short-lived GitHub identity token and contains no stored AbstractClassroom secret.

If the repository name and owner do not match a registered course, AbstractClassroom ignores the workflow request and makes no changes.
