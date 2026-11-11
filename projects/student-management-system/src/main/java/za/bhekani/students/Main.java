package za.bhekani.students;

/** Small CLI: add, list, find and delete student records. */
public class Main {
    private static final String DB = "students.db";

    public static void main(String[] args) {
        if (args.length == 0) { usage(); return; }
        try (StudentRepository repository = new StudentRepository(DB)) {
            switch (args[0].toLowerCase()) {
                case "add" -> {
                    if (args.length < 4) { usage(); return; }
                    repository.add(new Student(args[1], args[2].replace('-', ' '), String.join(" ", java.util.Arrays.copyOfRange(args, 3, args.length)).replace('-', ' ')));
                    System.out.println("Student saved.");
                }
                case "list" -> repository.findAll().forEach(System.out::println);
                case "find" -> {
                    if (args.length != 2) { usage(); return; }
                    Student student = repository.findByNumber(args[1]);
                    System.out.println(student == null ? "No student found." : student);
                }
                case "delete" -> {
                    if (args.length != 2) { usage(); return; }
                    System.out.println(repository.delete(args[1]) ? "Student deleted." : "No student found.");
                }
                default -> usage();
            }
        } catch (IllegalArgumentException error) {
            System.err.println("Invalid input: " + error.getMessage());
            System.exit(2);
        } catch (Exception error) {
            System.err.println("Operation failed: " + error.getMessage());
            System.exit(1);
        }
    }

    private static void usage() {
        System.out.println("Commands:\n  add <number> <full-name-with-dashes> <programme-with-dashes>\n  list\n  find <number>\n  delete <number>");
    }
}
