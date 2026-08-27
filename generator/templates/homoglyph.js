var buildSearchFunction = function(charMap, multiCharMap) {
    multiCharMap = multiCharMap || {};

    function singleCharMatches(textChar, wordChar) {
        var wordCharLower = wordChar.toLowerCase(),
            wordCharUpper = wordChar.toUpperCase();
        return (textChar == wordCharLower) || (charMap[wordCharLower] && charMap[wordCharLower].indexOf(textChar) >= 0) ||
               (textChar == wordCharUpper) || (charMap[wordCharUpper] && charMap[wordCharUpper].indexOf(textChar) >= 0);
    }

    function wordStartsWithPrototype(word, wordIndex, prototype) {
        if (wordIndex + prototype.length > word.length) {
            return false;
        }
        return word.substr(wordIndex, prototype.length).toLowerCase() === prototype.toLowerCase();
    }

    // Attempts to match word[wordIndex..] starting at symbols[symbolIndex], returning the number of
    // symbols consumed on success or -1 on failure. A single symbol usually matches a single word
    // character, but a multi-codepoint confusable (e.g. 'ﬃ' for "ffi") lets one symbol stand in for
    // a run of word characters. Alternatives are explored with backtracking.
    function matchLengthAt(symbols, symbolIndex, word, wordIndex) {
        if (wordIndex >= word.length) {
            return 0;
        }
        if (symbolIndex >= symbols.length) {
            return -1;
        }
        var textChar = symbols[symbolIndex];

        if (singleCharMatches(textChar, word[wordIndex])) {
            var rest = matchLengthAt(symbols, symbolIndex + 1, word, wordIndex + 1);
            if (rest >= 0) {
                return rest + 1;
            }
        }

        var prototypes = multiCharMap[textChar];
        if (prototypes) {
            for (var p = 0; p < prototypes.length; p++) {
                var prototype = prototypes[p];
                if (wordStartsWithPrototype(word, wordIndex, prototype)) {
                    var restMulti = matchLengthAt(symbols, symbolIndex + 1, word, wordIndex + prototype.length);
                    if (restMulti >= 0) {
                        return restMulti + 1;
                    }
                }
            }
        }

        return -1;
    }

    function checkForWord(symbols, word) {
        var matches = [];
        if (word.length === 0) {
            return matches;
        }
        for (var i = 0; i < symbols.length; i++) {
            var length = matchLengthAt(symbols, i, word, 0);
            if (length >= 1) {
                matches.push({
                    match : symbols.slice(i, i + length).join(''),
                    word : word,
                    index : i
                });
            }
        }
        return matches;
    }

    function makeSymbolArray(txt){
        var a = [], s;
        for (s of txt) {
            a.push(s)
        }
        return a;
    }

    return function(inputText, targetWords) {
        var allMatches = [],
            inputTextSymbolArray = makeSymbolArray(inputText);
        targetWords.forEach(function(targetWord){
            Array.prototype.push.apply(allMatches, checkForWord(inputTextSymbolArray, targetWord));
        });
        return allMatches;
    };
};

// Builds a search function that checks for homoglyphs of the following characters: [[chars_list]]
var search = buildSearchFunction([[chars_json]], [[multi_chars_json]]);
