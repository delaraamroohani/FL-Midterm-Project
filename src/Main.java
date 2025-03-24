import java.io.File;

public class Main {
    public static void main(String[] args) {
        File file = new File("input.txt");
        Parser.parse(file);
    }
}