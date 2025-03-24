import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.Reader;
import java.util.Scanner;

public class Parser {
    public static String line;
    public static void parse(File file) {
        try {
            Scanner sc = new Scanner(file);
            while (sc.hasNext()) {
                line = sc.nextLine().trim();
                checkLine();
            }

        } catch (FileNotFoundException e) {
            System.out.println("input.txt not found.");
            e.printStackTrace();
        }
    }

    public static void checkLine() {
        if (line.equals("# Alphabet")) {
            RegularGrammar newRg = new RegularGrammar();
        }
    }
}
