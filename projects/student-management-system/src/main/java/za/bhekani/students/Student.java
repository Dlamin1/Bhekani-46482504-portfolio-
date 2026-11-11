package za.bhekani.students;

/** Immutable student record. */
public record Student(String studentNumber, String fullName, String programme) {
    public Student {
        if (studentNumber == null || studentNumber.isBlank()) throw new IllegalArgumentException("Student number is required");
        if (fullName == null || fullName.isBlank()) throw new IllegalArgumentException("Full name is required");
        if (programme == null || programme.isBlank()) throw new IllegalArgumentException("Programme is required");
        studentNumber = studentNumber.trim();
        fullName = fullName.trim();
        programme = programme.trim();
    }
}
