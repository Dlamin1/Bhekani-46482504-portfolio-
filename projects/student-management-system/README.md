# Student Management System

A console-based Java application for maintaining student records in a local SQLite database. It demonstrates object-oriented modelling, JDBC, prepared statements and input validation.

## Requirements
- Java 17+
- Maven 3.8+

## Run
```bash
mvn test
mvn package
mvn exec:java -Dexec.args="add 2026001 Thando Mokoena Computer-Science"
mvn exec:java -Dexec.args="list"
mvn exec:java -Dexec.args="find 2026001"
mvn exec:java -Dexec.args="delete 2026001"
```

The database file `students.db` is created in the working directory. Use a unique student number. This is a learning example, not a production student-information system; do not store sensitive personal data in it.
