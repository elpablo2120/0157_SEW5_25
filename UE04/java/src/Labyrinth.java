
/**
 * Labyrinth.java by Paul Waldecker
 * 2021-11-02
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
	 * @param map  der Plan, ein String je Zeile
	 * @return char[][] des Plans
	 */
	public static char[][] fromStrings(String[] map) {
		// TODO Code fehlt noch
		return null;
	}


	/**
	 * Ausgabe des Layrinths
	 * @param lab
	 */
	public static void printLabyrinth(char[][] lab) {
		// TODO Code fehlt noch
	}

	/**
	 * Sucht, ob ein Weg aus dem Labyrinth führt
	 * @param zeile     aktuelle Position
	 * @param spalte     aktuelle Position
	 * @param lab     Labyrinth
	 * @throws InterruptedException    für die verlangsamte Ausgabe mit sleep()
	 */
	public static boolean suchen(int zeile, int spalte, char[][] lab) throws InterruptedException {
		// TODO Code fehlt noch
		// nur lab[zeile][spalte] betrachten
		return false;
	}

	/**
	 * Ermittelt die Anzahl der Wege, die aus dem Labyrinth führen
	 * @param zeile     aktuelle Position
	 * @param spalte     aktuelle Position
	 * @param lab     Labyrinth
	 * @return anzahl Anzahl der unterschiedlichen Wege, die aus dem Labyrinth führen (ein bereits besuchtes Feld darf nicht nochmals betreten werden)
	 * @throws InterruptedException    für die verlangsamte Ausgabe mit sleep()
	 */
	public static int alleSuchen(int zeile, int spalte, char[][] lab) throws InterruptedException {
		// TODO Code fehlt noch
		return anzahl;
	}


	public static void main(String[] args) throws InterruptedException {
		char[][] labyrinth = fromStrings(maps[2]);
		printLabyrinth(labyrinth);
		System.out.println("Ausgang gefunden: " + (suchen(5, 5, labyrinth) ? "ja" : "nein"));
		// TODO: System.out.println("Anzahl Wege: " + suchenAlle(5, 5, labyrinth));
	}
}
