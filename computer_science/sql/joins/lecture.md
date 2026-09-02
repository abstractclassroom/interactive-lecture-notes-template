# Combining Rows with SQL Joins

Relational databases often separate related facts into different tables. A join combines rows when a condition describes how those rows are related.

```sql
SELECT students.name, enrollments.course_code
FROM students
INNER JOIN enrollments
  ON enrollments.student_id = students.student_id;
```

The `ON` clause matches the foreign key in `enrollments` to the primary key in `students`. An inner join returns only rows that satisfy this condition.

Use table-qualified column names when more than one table contains a column with the same name. Clear qualification also makes the relationship easier for a reader to verify.
