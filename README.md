# word-ladder
Generates a path between two words consisting only of valid words which differ by one letter

Nothing original here just a learning project. 

## Basic Run:
Run wordchain.py with two parameters, a starting word and a target word. For example: 
> python chain.py song bird

Returns:
> ['bird', 'bind', 'bing', 'bong', 'song']

## Common Word List
This was built from three sources. 
* [Wikipedia Word Frequency List (2019)](https://github.com/IlyaSemenov/wikipedia-word-frequency/blob/master/results/enwiki-20190320-words-frequency.txt)
* [SOWPODS Scrabble dictionary](https://www.wordgamedictionary.com/sowpods/download/sowpods.txt)
* A Merriam Webster wordlist which for which I haven't found a safe public source link, but is in this repository. 

The Wikipedia list serves to provide words that are actually used and can allow us to filter out any exceptionally obscure words.

SOWPODS is a fairly generous dictionary and includes lots of words that are never used but provides us with a game friendly list of words excluding names, locations and other proper nouns. 

The Merriam Webster word list is a bit dated which is a feature since it excludes any very new words. 

The common word list is the set which is common to all three lists. 

## Building Ladder JSON
> python builder.py word_length [top_n_words_by_frequency to use, default=100]

e.g.:
> `python builder.py 3 50 ` 

The purpose of the top n argument is to limit the duration of the run,and also to keep the results interesting. Finding paths between two unused words isn't terribly fun. 