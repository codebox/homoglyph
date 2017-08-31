describe("Homoglyph Search - Data Tests", function () {
    function check(targetChar, homoglyphs){
        describe("Homoglyphs of '" + targetChar + "'", function(){
            homoglyphs.forEach(function (c) {
                it("Checking '" + c + "'", function () {
                    var textContainingHomoglyph = 'xx' + c + 'xx',
                        targetWord = 'xx' + targetChar + 'xx';
                    expect(search(textContainingHomoglyph, [targetWord])).toEqual([{match: textContainingHomoglyph, word: targetWord, index: 0}]);
                })
            });
        })
    }

[[check_statements]]

});
