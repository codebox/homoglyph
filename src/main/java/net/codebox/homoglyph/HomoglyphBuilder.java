package net.codebox.homoglyph;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

/**
 * Helper class providing methods that supply populated Homoglyph objects.
 *
 * @author Rob Dawson
 */
public class HomoglyphBuilder {
    private static final String CHAR_CODES_FILE = "/char_codes.txt";

    /**
     * Parses the bundled char_codes.txt file, and uses it to construct a populated Homoglyph object.
     *
     * @return a Homoglyph object populated using the contents of the char_codes.txt file
     *
     * @throws MissingResourceException if the char_codes.txt file is missing
     * @throws IOException if the char_codes.txt exists but cannot be read
     */
    public static Homoglyph build() throws IOException {
        final InputStream is = HomoglyphBuilder.class.getResourceAsStream(CHAR_CODES_FILE);
        if (is == null){
            throw new MissingResourceException("Unable to read " + CHAR_CODES_FILE,
                    HomoglyphBuilder.class.getName(), CHAR_CODES_FILE);
        }

        return build(new InputStreamReader(is));
    }

    /**
     * Parses the specified file and uses it to construct a populated Homoglyph object.
     *
     * @param path the path to a file containing a list of homoglyphs (see the bundled char_codes.txt
     *             file for an example of the required format)
     *
     * @return a Homoglyph object populated using the contents of the specified file
     *
     * @throws IOException if the specified file cannot be read
     */
    public static Homoglyph build(final String path) throws IOException {
        return build(new FileReader(path));
    }

    /**
     * Consumes the supplied Reader and uses it to construct a populated Homoglyph object.
     *
     * @param reader a Reader object that provides access to homoglyph data (see the bundled
     *               char_codes.txt file for an example of the required format)
     *
     * @return a Homoglyph object populated using the data returned by the Reader object
     *
     * @throws IOException if the specified Reader cannot be read
     */
    public static Homoglyph build(final Reader reader) throws IOException {
        final List<Set<Integer>> homoglyphs = new ArrayList<Set<Integer>>();

        try (final BufferedReader bufferedReader = new BufferedReader(reader)) {
            String line;
            while((line = bufferedReader.readLine()) != null){
                line = line.trim();
                if (line.startsWith("#") || line.length() == 0){
                    continue;
                }
                final Set<Integer> set = new HashSet<Integer>();
                for (String charCode : line.split(",")) {
                    try {
                        set.add(Integer.parseInt(charCode, 16));
                    } catch (NumberFormatException ex){
                        // ignore badly formatted lines
                    }
                }
                homoglyphs.add(set);
            }
        }

        return new Homoglyph(homoglyphs);
    }

}
