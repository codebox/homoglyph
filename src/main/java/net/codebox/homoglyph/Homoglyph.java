package net.codebox.homoglyph;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

/**
 * Use this class to detect occurrences of target words inside a String, where the target words may have been
 * disguised using homoglyph substitution and/or by mixing upper/lower case letters (for example, the class
 * will find the word "credit" in the String "Free Ꮯгⴹԁ1ｔ").
 *
 * You can supply your own list of homoglyphs, or use the char_codes.txt which should accompany this source file.
 * You can find the latest version of char_codes.txt at https://github.com/codebox/homoglyph
 *
 * @author Rob Dawson
 */
public class Homoglyph {
    private static final List<Set<Integer>> homoglyphs = new ArrayList<Set<Integer>>();

    private final CachingLookup cache = new CachingLookup();

    /**
     * Supply a List of Sets, with each Set containing a group of Unicode codepoints that are homoglyphs. Codepoints
     * must be represented using Integer rather than Character values because some are too large to be held by the
     * 16-bit Character type.
     *
     * @param homoglyphs a List of Sets, with each Set containing a group of Unicode codepoints that are homoglyphs
     */
    public Homoglyph(final List<Set<Integer>> homoglyphs){
        this.homoglyphs.addAll(homoglyphs);
    }

    /**
     * Search the String {@code text} to locate all occurrences of the words contained in {@code targetWords},
     * accounting for homoglyph substitution and variations of case.
     *
     * @param text text to be searched
     * @param targetWords words to be located
     * @return a List containing the results of the search, if no matches were found an empty list will be returned
     */
    public List<SearchResult> search(final String text, final Collection<String> targetWords){
        final List<SearchResult> allResults = new ArrayList<SearchResult>();

        final CodePoints textCodepoints = new CodePoints(text);

        for (final String targetWord : targetWords) {
            allResults.addAll(checkForWord(textCodepoints, new CodePoints(targetWord)));
        }

        return allResults;
    }

    /**
     * Search the String {@code text} to locate all occurrences of the words contained in {@code targetWords},
     * accounting for homoglyph substitution and variations of case.
     *
     * @param text text to be searched
     * @param targetWords words to be located
     * @return a List containing the results of the search, if no matches were found an empty list will be returned
     */
    public List<SearchResult> search(final String text, final String... targetWords){
        return search(text, Arrays.asList(targetWords));
    }


    private Collection<SearchResult> checkForWord(final CodePoints text, final CodePoints targetWord) {
        final Collection<SearchResult> results = new ArrayList<SearchResult>();

        int lastIndex = text.getLength() - targetWord.getLength();
        for (int i = 0; i <= lastIndex; i++) {
            if (hasWordAtIndex(text, targetWord, i)) {
                results.add(new SearchResult(i, text.subStringAt(i, targetWord.getLength()), targetWord.getText()));
            }
        }

        return results;
    }

    private boolean hasWordAtIndex(final CodePoints text, final CodePoints targetWord, final int index){
        for (int i=0; i<targetWord.getLength(); i++){
            final int targetCharLower = Character.toLowerCase(targetWord.getValue(i));
            final int targetCharUpper = Character.toUpperCase(targetWord.getValue(i));
            final int textChar = text.getValue(index + i);
            if (!checkForHomoglyphs(targetCharLower, textChar) && !checkForHomoglyphs(targetCharUpper, textChar)){
                return false;
            }
        }
        return true;
    }

    private boolean checkForHomoglyphs(final int cp1, final int cp2) {
        final Set<Integer> cp1Set = cache.lookup(cp1);
        return cp1Set.contains(cp2);
    }

    public static class SearchResult {
        public SearchResult(final int index, final String match, final String word){
            this.index = index;
            this.match = match;
            this.word = word;
        }
        public int index;
        public String match;
        public String word;
    }

    public static class CodePoints{
        private final Integer[] codepoints;
        private final String text;

        public CodePoints(String text){
            this.text = text;

            final List<Integer> codepointList = new ArrayList<>();
            int codepoint;
            for (int offset = 0; offset < text.length(); ) {
                codepointList.add(codepoint = text.codePointAt(offset));
                offset += Character.charCount(codepoint);
            }
            codepoints = codepointList.toArray(new Integer[0]);
        }

        public int getValue(int i) {
            return codepoints[i];
        }

        public int getLength(){
            return codepoints.length;
        }

        public String getText(){
            return text;
        }

        public String subStringAt(final int s, final int l){
            final StringBuilder sb = new StringBuilder(l);
            for (int i=0; i<l; i++){
                sb.appendCodePoint(this.codepoints[s+i]);
            }
            return sb.toString();
        }
    }

    public static class CachingLookup{
        private final Map<Integer, Set<Integer>> lookup = new HashMap<Integer, Set<Integer>>();

        public Set<Integer> lookup(final int cp){
            Set<Integer> s = lookup.get(cp);
            if (s == null){
                for (Set<Integer> thisSet : homoglyphs){
                    if (thisSet.contains(cp)){
                        s = thisSet;
                        break;
                    }
                }
                if (s == null){
                    s = new HashSet<Integer>();
                    s.add(cp);
                }
                lookup.put(cp, s);
            }
            return s;
        }
    }

    public static List<Set<Integer>> parseCharCodesFile(final String path) throws IOException {
        final List<Set<Integer>> homoglyphs = new ArrayList<Set<Integer>>();
        final BufferedReader reader = new BufferedReader(new FileReader(path));

        String line;
        while((line = reader.readLine()) != null){
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

        return homoglyphs;
    }
}