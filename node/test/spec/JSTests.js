var homoglyphSearch = require('../../index');

describe("Homoglyph Search - JavaScript Code Tests", function () {

    var map = {
        'I' : '1l',
        'E' : '3',
        'O' : '0',
        'S' : '5',
        'B' : '8'
    };

    var search = homoglyphSearch.buildSearchFunction(map);

    it("empty text string", function () {
        expect(search('', ['TEST'])).toEqual([]);
    });

    it("no matches in text", function () {
        expect(search('nothing to see here', ['TEST'])).toEqual([]);
    });

    it("text exactly matches target word", function () {
        expect(search('TEST',['TEST'])).toEqual([{ match: 'TEST', word: 'TEST', index: 0 }]);
    });

    it("target word appears in text", function () {
        expect(search('UNIT TESTING',['TEST'])).toEqual([{ match: 'TEST', word: 'TEST', index: 5 }]);
    });

    it("text exactly matches target word after substitutions", function () {
        expect(search('T35T',['TEST'])).toEqual([{ match: 'T35T', word: 'TEST', index: 0 }]);
    });

    it("target word appears in text after substitutions", function () {
        expect(search('UNIT T35TING',['TEST'])).toEqual([{ match: 'T35T', word: 'TEST', index: 5 }]);
    });

    it("target word appears in text after substitutions and change of case", function () {
        expect(search('unit t35tinG',['TEST'])).toEqual([{ match: 't35t', word: 'TEST', index: 5 }]);
    });

    it("multiple matches for single target word found", function () {
        expect(search('RET3ST ALL TE5TS',['TEST'])).toEqual([{ match: 'T3ST', word: 'TEST', index: 2 },{ match: 'TE5T', word: 'TEST', index: 11 }]);
    });

    it("multiple target words matched in text", function () {
        expect(search('THE 501L T35TS',['test', 'soil'])).toEqual([{ match: 'T35T', word: 'test', index: 9 },{ match: '501L', word: 'soil', index: 4 }]);
    });

    it("multiple overlapping matches", function () {
        expect(search('1lI1',['II'])).toEqual([{ match: '1l', word: 'II', index: 0 },{ match: 'lI', word: 'II', index: 1 },{ match: 'I1', word: 'II', index: 2 }]);
    });

    it("target words with common stem", function () {
        expect(search('T35T1NG',['TEST','TESTING'])).toEqual([{ match: 'T35T', word: 'TEST', index: 0 },{ match: 'T35T1NG', word: 'TESTING', index: 0 }]);
    });

});
