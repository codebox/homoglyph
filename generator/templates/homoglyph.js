var buildSearchFunction = function(charMap) {
    function hasWordAtStart(symbols, word) {
        if (word.length == 0) {
            return true;
        }
        var textChar = symbols[0],
            wordCharLower = word[0].toLowerCase(),
            wordCharUpper = word[0].toUpperCase(),
            firstCharMatches =
                (textChar == wordCharLower) || (charMap[wordCharLower] && charMap[wordCharLower].indexOf(textChar) >= 0) ||
                (textChar == wordCharUpper) || (charMap[wordCharUpper] && charMap[wordCharUpper].indexOf(textChar) >= 0);

        return firstCharMatches && hasWordAtStart(symbols.slice(1), word.substr(1));
    }
    function checkForWord(symbols, word) {
        var wordLength = word.length, matches = [], i = 0;
        while (symbols.length >= wordLength) {
            if (hasWordAtStart(symbols, word)){
                matches.push({
                    match : symbols.slice(0, word.length).join(''),
                    word : word,
                    index : i
                });
            }
            symbols = symbols.slice(1)
            i++;
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
var search = buildSearchFunction([[chars_json]]);