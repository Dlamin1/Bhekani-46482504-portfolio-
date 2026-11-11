package za.bhekani.students;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

/** JDBC repository. All user values are bound with prepared statements. */
public class StudentRepository implements AutoCloseable {
    private final Connection connection;

    public StudentRepository(String databasePath) throws SQLException {
        connection = DriverManager.getConnection("jdbc:sqlite:" + databasePath);
        try (Statement statement = connection.createStatement()) {
            statement.executeUpdate("""
                CREATE TABLE IF NOT EXISTS students (
                  student_number TEXT PRIMARY KEY,
                  full_name TEXT NOT NULL,
                  programme TEXT NOT NULL
                )
                """);
        }
    }

    public void add(Student student) throws SQLException {
        String sql = "INSERT INTO students(student_number, full_name, programme) VALUES (?, ?, ?)";
        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setString(1, student.studentNumber());
            statement.setString(2, student.fullName());
            statement.setString(3, student.programme());
            statement.executeUpdate();
        }
    }

    public List<Student> findAll() throws SQLException {
        List<Student> students = new ArrayList<>();
        try (PreparedStatement statement = connection.prepareStatement(
                "SELECT student_number, full_name, programme FROM students ORDER BY full_name");
             ResultSet result = statement.executeQuery()) {
            while (result.next()) students.add(new Student(result.getString(1), result.getString(2), result.getString(3)));
        }
        return students;
    }

    public Student findByNumber(String number) throws SQLException {
        try (PreparedStatement statement = connection.prepareStatement(
                "SELECT student_number, full_name, programme FROM students WHERE student_number = ?")) {
            statement.setString(1, number);
            try (ResultSet result = statement.executeQuery()) {
                return result.next() ? new Student(result.getString(1), result.getString(2), result.getString(3)) : null;
            }
        }
    }

    public boolean delete(String number) throws SQLException {
        try (PreparedStatement statement = connection.prepareStatement("DELETE FROM students WHERE student_number = ?")) {
            statement.setString(1, number);
            return statement.executeUpdate() == 1;
        }
    }

    @Override public void close() throws SQLException { connection.close(); }
}
