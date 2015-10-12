#Lexeme
Lexeme is a command-line constructed language word database, generation, and declension program. Contributions are very welcome: see (CONTRIBUTING.md).

##Features
+ Words are saved in a searchable, filterable SQLite database.
+ Generate words according to a basic syllable rule, or use advanced rules to specify unique patterns for different parts of speech. Phonotactics rules can be further applied during generation.
+ Tag words with custom fields, for example gender or vowel harmony type, and filter the database according to any field.
+ Batch generate words from file.
+ Set declension rules and autodecline or conjugate words to different tenses, aspects, cases, or any other desired form.
+ Automatically convert words to their phonetic representation through specified rules.
+ Export database to a csv file compatible with [Polyglot](https://github.com/DraqueT/PolyGlot) or spreadsheet software.
+ Easily configurable through a file.

##Installation
To be honest, who knows?

##Usage
###Running
Run Lexeme from the commandline with `python main.py`. For a list of command-line options, including the ability to set custom database and configuration files, use `python main.py -h`.

###Configuration
The default location for the configuration file is `config.txt`. The comments in example file should help to customise the rules to suit other conlangs.

###Database Structure
Inside the database, each word is represented as a row. The three mandatory
fields are 'english' (the word in English), 'word' (the word in the conlang),
and 'form', which usually contains the part of speech and can be used to apply
custom rules during word generation. Words can have an arbitrary number of
custom user-specified fields, such as gender, that are added during word
generation or adding. These fields can then be used in sorting and are
displayed alongside the word in search results.

###Commands
####Generate
The `generate` command is used to create a new word using rules in the configuration.

	Enter command: generate
	Enter word form (adjective/adverb/noun/verb/other): noun
	Enter word in English: t-shirt

	Conlang       English    Form
	------------  ---------  ------
	kōnbőnkőn     t-shirt    noun
	/kɔːnbønkøn/
	[kɔːnbønkøn]

	Accept word? (y/n): y
	Add custom field? (y/n): n
	Word saved in database!

Custom fields can be specified or created during generation.

    Add custom field? (y/n): y
    Enter desired field (form/gender/modality/dissonance/other): gender
    Enter word value (male/other): other
    Enter new word value: female

####Add
The `add` command is used to add pre-existing words to the database.

    Enter command: add
    Enter meaning in English: pig
    Enter word in conlang: yokotun
    Enter word form (adjective/adverb/noun/verb/other): noun
    Add custom field? (y/n): n
    Word saved in database!

####Batch
The `batch` command allows a text file of English words to be used in
generation. The command will step through each word in the file, structured
like so:
    
    lemonade
    to hit
    soft
    quickly

On each word, it will run generation with the word as the English base.

####Decline
The `decline` command puts a specified word into a conjugated or declined form
as specified by rules in the configuration file.

    Enter word (in conlang) to decline: pōyōmő
    Select declension:
    (1) prog
    (2) inch
    Enter selection: 1

    Conlang        English    Form    Gender    Modality    Dissonance
    -------------  ---------  ------  --------  ----------  ------------
    pōyōmőba       to drawl   verb
    /pɔːjɔːmøba/
    [pʷɔːjɔːmøba]

Rules are specified in the configuration file using regular expressions, as
seen in the following example:

    [DECLENSION]
    PROG = $->ba
    INCH = $->tse

Here, the INCH (inchoative) rule changes the end of the line to 'tse', in
effect adding a suffix. Through specifying these rules using regular
expressions, suffixes, prefixes, and infixes can all be easily handled by
Lexeme.

####Export
The `export` command simply exports the current database to a specified file in
csv format. This can then be imported into spreadsheet programs like
Libreoffice Calc or programs such as [Polyglot](https://github.com/DraqueT/PolyGlot).

####List
The `list` command lists words in the database, and can be filtered by specific
field.

    Enter list type (all/field): field
    Enter desired field (form/gender/modality/dissonance): form
    Enter option to list (adjective/adverb/noun/verb): noun

    English     Conlang         Form
    ----------  --------------  ------
    test        ān              noun
    weekend     hőnyőnhān       noun
    eye         yőntsēnsen      noun
    muffin      pēto            noun
    t-shirt     kōnbőnkőn       noun
    pig         yokotun         noun

The command autodetects fields and options present within the database.

####Search
The `search` command can search by English or conlang word.

    search term: test

    English    Conlang    Form
    ---------  ---------  ------
    test       kōndőn     noun
            /kɔːndøn/
            [kɔːndøn]

####Statistics
The `statistics` command simply outputs some statistics about the word
database.

####Quit
Fairly self-explanatory.

##Contact
For any feature requests or help, open an issue or email me at
cadel@cadelwatson.com.

##License
Lexeme is licensed under the MIT License. See [LICENSE.md] for more
information.
