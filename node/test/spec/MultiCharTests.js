var homoglyphSearch = require('../../index');

// End-to-end tests for multi-codepoint confusable detection, i.e. cases where a single
// glyph in the text stands in for a run of characters in the target word. All of the
// glyph -> prototype mappings exercised here are taken from the Unicode UTS #39
// confusables data (e.g. 'ﬃ' U+FB03 resembles "ffi", the letter 'm' resembles "rn").
describe("Homoglyph Search - Multi-Codepoint Data Tests", function () {

    function single(text, word){
        var results = homoglyphSearch.search(text, [word]);
        expect(results.length).toEqual(1);
        return results[0];
    }

    it("ligature ﬃ (U+FB03) stands in for 'ffi'", function () {
        expect(homoglyphSearch.search('oﬃce', ['office']))
            .toEqual([{ match: 'oﬃce', word: 'office', index: 0 }]);
    });

    it("ligature ﬁ (U+FB01) stands in for 'fi'", function () {
        expect(homoglyphSearch.search('ﬁnal', ['final']))
            .toEqual([{ match: 'ﬁnal', word: 'final', index: 0 }]);
    });

    it("ligature ﬄ (U+FB04) stands in for 'ffl' at the end of a word", function () {
        expect(homoglyphSearch.search('waﬄe', ['waffle']))
            .toEqual([{ match: 'waﬄe', word: 'waffle', index: 0 }]);
    });

    it("æ (U+00E6) stands in for 'ae'", function () {
        expect(homoglyphSearch.search('æther', ['aether']))
            .toEqual([{ match: 'æther', word: 'aether', index: 0 }]);
    });

    it("œ (U+0153) stands in for 'oe'", function () {
        expect(homoglyphSearch.search('œuvre', ['oeuvre']))
            .toEqual([{ match: 'œuvre', word: 'oeuvre', index: 0 }]);
    });

    it("the letter m stands in for 'rn'", function () {
        expect(homoglyphSearch.search('comer', ['corner']))
            .toEqual([{ match: 'comer', word: 'corner', index: 0 }]);
    });

    it("roman numeral ⅷ (U+2177) stands in for 'viii'", function () {
        expect(homoglyphSearch.search('xⅷ', ['xviii']))
            .toEqual([{ match: 'xⅷ', word: 'xviii', index: 0 }]);
    });

    it("multi-codepoint match is case-insensitive", function () {
        expect(homoglyphSearch.search('oﬃce', ['OFFICE']))
            .toEqual([{ match: 'oﬃce', word: 'OFFICE', index: 0 }]);
    });

    it("multi-codepoint match is located at the correct index within longer text", function () {
        var r = single('please visit the oﬃce today', 'office');
        expect(r.index).toEqual(17);
        expect(r.match).toEqual('oﬃce');
    });

    it("the matched text can be shorter than the target word", function () {
        var r = single('comer', 'corner');
        expect(r.match.length).toBeLessThan('corner'.length);
    });

    it("a multi-codepoint substitution can combine with a single-codepoint substitution", function () {
        // '0' is a homoglyph of 'o', and 'ﬃ' stands in for 'ffi', so '0ﬃce' matches 'office'.
        expect(homoglyphSearch.search('0ﬃce', ['office']))
            .toEqual([{ match: '0ﬃce', word: 'office', index: 0 }]);
    });

    it("does not report a match when the surrounding characters differ", function () {
        expect(homoglyphSearch.search('oﬃce', ['orifice'])).toEqual([]);
    });

    it("plain text without homoglyphs is unaffected", function () {
        expect(homoglyphSearch.search('office', ['office']))
            .toEqual([{ match: 'office', word: 'office', index: 0 }]);
    });

    it("buildSearchFunction accepts a custom multi-codepoint map", function () {
        var search = homoglyphSearch.buildSearchFunction({}, { 'œ': ['oe'] });
        expect(search('œuvre', ['oeuvre']))
            .toEqual([{ match: 'œuvre', word: 'oeuvre', index: 0 }]);
    });

    it("buildSearchFunction still works when no multi-codepoint map is supplied", function () {
        var search = homoglyphSearch.buildSearchFunction({ 'O': ['0'] });
        expect(search('c0rner', ['corner']))
            .toEqual([{ match: 'c0rner', word: 'corner', index: 0 }]);
        // With no multi map, the ligature is not expanded.
        expect(search('oﬃce', ['office'])).toEqual([]);
    });

});
