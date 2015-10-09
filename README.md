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

###Generate
The `generate` command is used to create a new word using rules in the configuration.

	Please enter a command: generate
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