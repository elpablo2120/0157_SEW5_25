import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;

/**
 * Labyrinth.java by Paul Waldecker
 */
public class Labyrinth {
    public static String[][] maps = {{
            "############",
            "#  #     # #",
            "## # ### # #",
            "#  # # # # #",
            "## ### # # #",
            "#        # #",
            "## ####### #",
            "#          #",
            "# ######## #",
            "# #   #    #",
            "#   #   # ##",
            "######A#####"
    }, {
            "################################",
            "#                              #",
            "# ############################ #",
            "# # ###       ##  #          # #",
            "# #     ##### ### # ########## #",
            "# #   ##### #     # #      ### #",
            "# # ##### #   ###   # # ## # # #",
            "# # ### # ## ######## # ##   # #",
            "# ##### #  # #   #    #    ### #",
            "# # ### ## # # # # ####### # # #",
            "# #        # #   #     #     # #",
            "# ######## # ######### # ### # #",
            "# ####     #  # #   #  # ##### #",
            "# # #### #### # # # # ## # ### #",
            "#                      # #     #",
            "###########################A####"
    }, {
            "###########################A####",
            "#   #      ## # # ###  #     # #",
            "# ###### #### # # #### ##### # #",
            "# # ###  ## # # # #          # #",
            "# # ### ### # # # # # #### # # #",
            "# #     ### # # # # # ## # # # #",
            "# # # # ### # # # # ######## # #",
            "# # # #     #          #     # #",
            "# ### ################ # # # # #",
            "# #   #             ## # #   # #",
            "# # #### ############# # #   # #",
            "# #                    #     # #",
            "# # #################### # # # #",
            "# # #### #           ###     # #",
            "# # ## # ### ### ### ### # ### #",
            "# #    #     ##  ##  # ###   # #",
            "# ####   ###### #### # ###  ## #",
            "###########################A####"
    }, {
            "#############",
            "#           #",
            "#           #",
            "#           #",
            "###########A#"
    }};

    /**
     * Wandelt (unveränderliche) Strings in Char-Arrays
     *
     * @param map der Plan, ein String je Zeile
     * @return char[][] des Plans
     */
    public static char[][] fromStrings(String[] map) {
        return Arrays.stream(map).map(String::toCharArray).toArray(char[][]::new);
    }


    /**
     * Ausgabe des Layrinths
     *
     * @param lab Das Labyrinth
     */
    public static void printLabyrinth(char[][] lab) {
        Arrays.stream(lab).forEach(System.out::println);
    }

    /**
     * Sucht, ob ein Weg aus dem Labyrinth führt
     *
     * @param zeile  aktuelle Position
     * @param spalte aktuelle Position
     * @param lab    Labyrinth
     * @throws InterruptedException für die verlangsamte Ausgabe mit sleep()
     */
    public static boolean suchen(int zeile, int spalte, char[][] lab) throws InterruptedException {
        // Checken ob A gefunden wurde
        if (lab[zeile][spalte] == 'A') {
            return true;
        }

        // Checken ob eine Wand oder eine bereits besuchte Stelle gefunden wurde
        if (lab[zeile][spalte] == '#' || lab[zeile][spalte] == '.') {
            return false;
        }

        // Die dezeite Stelle als besucht markieren
        lab[zeile][spalte] = '.';


        // Rekursiv nach dem Ausgang suchen
        boolean found = suchen(zeile - 1, spalte, lab) // Up
                || suchen(zeile + 1, spalte, lab) // Down
                || suchen(zeile, spalte - 1, lab) // Left
                || suchen(zeile, spalte + 1, lab); // Right

        // aktuelle Stelle wieder freigeben
        lab[zeile][spalte] = ' ';

        return found;
    }

    /**
     * Ermittelt die Anzahl der Wege, die aus dem Labyrinth führen
     *
     * @param zeile  aktuelle Position
     * @param spalte aktuelle Position
     * @param lab    Labyrinth
     * @return anzahl Anzahl der unterschiedlichen Wege, die aus dem Labyrinth führen (ein bereits besuchtes Feld darf nicht nochmals betreten werden)
     * @throws InterruptedException für die verlangsamte Ausgabe mit sleep()
     */
    public static int alleSuchen(int zeile, int spalte, char[][] lab) throws InterruptedException {
        if (lab[zeile][spalte] == 'A') return 1;

        if (lab[zeile][spalte] == '#' || lab[zeile][spalte] == '.') return 0;
        lab[zeile][spalte] = '.';

        printLabyrinth(lab);
        //Thread.sleep(10); // optional

        int anzahl =
                alleSuchen(zeile - 1, spalte, lab) +  // Oben
                        alleSuchen(zeile + 1, spalte, lab) +  // Unten
                        alleSuchen(zeile, spalte - 1, lab) +  // Links
                        alleSuchen(zeile, spalte + 1, lab); // Rechts

        // WICHTIG: Pfadmarkierung bis hierher wieder löschen, um alle möglichen Pfade zu bekommen
        lab[zeile][spalte] = ' ';

        return anzahl;
    }

    public static char[][] getLabyrinthFromFile(Path path) throws IOException {
        return fromStrings(Files.readAllLines(path).toArray(String[]::new));
    }

    public static void main(String[] args) throws InterruptedException, IOException {
        char[][] labyrinth = fromStrings(maps[2]);
        labyrinth = getLabyrinthFromFile(Path.of("/Users/paulwaldecker/HTL3R_Local/0157_SEW5_25/UE04/l1.txt"));
        printLabyrinth(labyrinth);
        System.out.println("Ausgang gefunden: " + (suchen(1, 1, labyrinth) ? "ja" : "nein"));

        //labyrinth = fromStrings(maps[3]);
        System.out.println("Anzahl Wege: " + alleSuchen(1, 1, labyrinth));
    }
}
