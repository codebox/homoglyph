var homoglyphSearch = require('homoglyph-search');

var textToSearch = 'Get free ϲrEd1ᴛ';
var bannedWords = ['credit'];

var result = homoglyphSearch.search(textToSearch, bannedWords); 

console.log(result);