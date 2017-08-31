package net.codebox.homoglyph;

import org.junit.Before;
import org.junit.Test;

import java.io.IOException;
import java.util.*;

import net.codebox.homoglyph.Homoglyph.SearchResult;

import static org.junit.Assert.*;

public class HomoglyphLogicTest {
    private Homoglyph homoglyph;

    private Set<Integer> makeSet(char... chrs){
        Set<Integer> s = new HashSet<Integer>(chrs.length);

        for (char c : chrs){
            s.add((int)c);
        }
        return s;
    }

    @Before
    public void setup() throws IOException {
        List<Set<Integer>> s = Arrays.asList(
            makeSet('1', 'I', 'l', '|'),
            makeSet('0', 'O'),
            makeSet('5', 'S')
        );

        homoglyph = new Homoglyph(s);
    }

    @Test
    public void whenTextDoesNotContainAnyTargetWords_thenNoMatchesFound(){
        List<SearchResult> r = homoglyph.search("Nothing to see here", "TARGET");
        assertEquals(0, r.size());
    }

    @Test
    public void whenTextIdenticalToTargetWord_thenMatchFound(){
        List<SearchResult> r = homoglyph.search("SOIL", "SOIL");
        assertEquals(1, r.size());
        checkResult(r.get(0), 0, "SOIL", "SOIL");
    }

    @Test
    public void whenTextContainsTargetWord_thenMatchFound(){
        List<SearchResult> r = homoglyph.search("I have SOIL in my garden", "SOIL");
        assertEquals(1, r.size());
        checkResult(r.get(0), 7, "SOIL", "SOIL");
    }

    @Test
    public void whenTextContainsOneOfTheTargetWords_thenMatchFound(){
        List<SearchResult> r = homoglyph.search("I have SOIL in my garden", "CHEESE", "SOIL", "FALCONS");
        assertEquals(1, r.size());
        checkResult(r.get(0), 7, "SOIL", "SOIL");
    }

    @Test
    public void whenTargetWordContainsHomoglyphs_thenMatchFound(){
        List<SearchResult> r = homoglyph.search("I have 501L in my garden", Arrays.asList("CHEESE", "SOIL", "FALCONS"));
        assertEquals(1, r.size());
        checkResult(r.get(0), 7, "SOIL", "501L");
    }

    @Test
    public void whenTargetWordIsAtStartOfText_thenMatchFound(){
        List<SearchResult> r = homoglyph.search("FALC0N5 fly", Arrays.asList("CHEESE", "SOIL", "FALCONS"));
        assertEquals(1, r.size());
        checkResult(r.get(0), 0, "FALCONS", "FALC0N5");
    }

    @Test
    public void whenTargetWordIsAtEndOfText_thenMatchFound(){
        List<SearchResult> r = homoglyph.search("I like FALC0N5", Arrays.asList("CHEESE", "SOIL", "FALCONS"));
        assertEquals(1, r.size());
        checkResult(r.get(0), 7, "FALCONS", "FALC0N5");
    }

    @Test
    public void whenTargetWordHasDifferentCaseInText_thenMatchFound(){
        List<SearchResult> r = homoglyph.search("I like fALc0N5 fly", "Falcons");
        assertEquals(1, r.size());
        checkResult(r.get(0), 7, "Falcons", "fALc0N5");
    }

    @Test
    public void whenTargetWordContainsMultipleMatchesWithDifferentHomoglyphs_thenMatchFound(){
        List<SearchResult> r = homoglyph.search("I have 501L and FALC0N5 in my garden, I prefer the SO|L", Arrays.asList("CHEESE", "SOIL", "FALCONS"));
        assertEquals(3, r.size());
        checkResult(r.get(0), 7, "SOIL", "501L");
        checkResult(r.get(1), 51, "SOIL", "SO|L");
        checkResult(r.get(2), 16, "FALCONS", "FALC0N5");
    }

    private void checkResult(SearchResult result, int expectedIndex, String expectedWord, String expectedMatch){
        assertEquals(expectedIndex, result.index);
        assertEquals(expectedWord, result.word);
        assertEquals(expectedMatch, result.match);
    }
}