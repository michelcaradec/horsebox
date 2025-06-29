#!/bin.bash

PS4="\n\033[1;33m>>>\033[0m "; set -x

###############
# Information #
###############

# Get the version of Horsebox.
hb --version

# Show the schema of the index.
hb schema

# Show the configuration.
hb config

#############
# Searching #
#############

# Search in text files under the folder `demo`.
hb search --from ./demo/ --pattern "*.txt" --query "better" --highlight

# Search in text files under the folder `demo`, using a line-by-line collector.
hb search --from ./demo/ --pattern "*.txt" --using fileline --query "better" --highlight --limit 5

# Count the number of results found
hb search --from ./demo/ --pattern "*.txt" --using fileline --query "better" --count

# Proximity search.
hb search --from ./demo/raw.json --using raw --query "'engine inspired'~1" --highlight

# Guess mode.
hb search --from ./demo/raw.json --query "'engine inspired'~1" --highlight

# Fuzzy search.
hb search --from ./demo/raw.json --using raw --query "engne~1"

# Search on multiple datasources.
if [[ "${HB_TEST_MODE}" == "1" ]]
then
    hb search \
        --from "@demo/rss/pythonlibrary.xml" \
        --from "@demo/rss/planetpython.xml" \
        --from "@demo/rss/realpython.xml" \
        --using rss --query "duckdb" --highlight

    # Guess mode.
    hb search \
        --from "@demo/rss/pythonlibrary.xml" \
        --from "@demo/rss/planetpython.xml" \
        --from "@demo/rss/realpython.xml" \
        --query "duckdb" --highlight
else
    hb search \
        --from "https://www.blog.pythonlibrary.org/feed/" \
        --from "https://planetpython.org/rss20.xml" \
        --from "https://realpython.com/atom.xml?format=xml" \
        --using rss --query "duckdb" --highlight
fi

#-----------------#
# Search on dates #
#-----------------#

# Single date.
# The date must be enclosed in single quotes.
hb search --from ./demo/raw.json --using raw --query "date:'2025-01-01T10:00:00.00Z'"

# Range of dates
# Inclusive boundaries are specified with square brackets.
hb search --from ./demo/raw.json --using raw --query "date:[2025-01-01T10:00:00.00Z TO 2025-01-04T10:00:00.00Z]"

# Range of dates
# Exclusive boundaries are specified with curly brackets.
hb search --from ./demo/raw.json --using raw --query "date:{2025-01-01T10:00:00.00Z TO 2025-01-04T10:00:00.00Z}"

# Range of dates
# Inclusive and exclusive boundaries can be mixed.
hb search --from ./demo/raw.json --using raw --query "date:[2025-01-01T10:00:00.00Z TO 2025-01-04T10:00:00.00Z}"

#####################
# Building An Index #
#####################

# Build an index `.index-demo` from the text files under the folder `demo`.
hb build --from ./demo/ --pattern "*.txt" --index ./.index-demo

# Search the built index
hb search --index ./.index-demo --query "better" --highlight

#######################
# Refreshing An Index #
#######################

# Refresh the previously built index `.index-demo`.
hb refresh --index ./.index-demo

#######################
# Inspecting An Index #
#######################

# Get technical information on a built index.
hb inspect --index ./.index-demo

# Get the most frequent keywords.

hb search --index ./.index-demo --top

######################################
# Indexing/Searching With Collectors #
######################################

# Search in text files under the folder `demo`, only the filename is indexed.
hb search --from ./demo/ --pattern "*.txt" --using filename --query "*" --limit 5

# Search in text files under the folder `demo`, the content of the file as a whole document is indexed.
hb search --from ./demo/ --pattern "*.txt" --using filecontent --query "better" --highlight --limit 5

# Search in text files under the folder `demo`, each line of a file is is indexed as a separate document.
hb search --from ./demo/ --pattern "*.txt" --using fileline --query "better" --highlight --limit 5

# Get the top keywords of an RSS feed.
if [[ "${HB_TEST_MODE}" == "1" ]]
then
    hb search --from "@demo/rss/planetpython.xml" --using rss --top
    # Guess mode.
    hb search --from "@demo/rss/planetpython.xml" --top
else
    hb search --from "https://planetpython.org/rss20.xml" --using rss --top
fi

# Search in an HTML page (and limit the size of the content to render).
if [[ "${HB_TEST_MODE}" == "1" ]]
then
    HB_RENDER_MAX_CONTENT=200 hb search --from "@demo/html/python_programming_language.html" --using html --query "python" --limit 5
    # Guess mode.
    HB_RENDER_MAX_CONTENT=200 hb search --from "@demo/html/python_programming_language.html" --query "python" --limit 5
else
    HB_RENDER_MAX_CONTENT=200 hb search --from "https://en.wikipedia.org/wiki/Python_(programming_language)" --using html --query "python" --limit 5
fi

# Search in JSON documents (using pipe).
cat ./demo/raw.json | hb search --from - --using raw --query "adipiscing" --highlight --limit 5

# Search in JSONL documents (using pipe).
cat ./demo/raw.jsonl | hb search --from - --using raw --query "adipiscing" --highlight --limit 5 --jsonl

# Search in a PDF file.
hb search --from ./demo/zen-of-python.pdf --using pdf --query "better" --highlight --limit 5
# Guess mode.
hb search --from ./demo/zen-of-python.pdf --query "better" --highlight --limit 5

#######################
# Analyzing Some Text #
#######################

TEXT="Tantivy is a full-text search engine library inspired by Apache Lucene and written in Rust."

#------------#
# Tokenizers #
#------------#

# Simple (i.e. non-configurable) tokenizers
for TOKENIZER in raw simple whitespace facet
do
    hb analyze --text "${TEXT}" --tokenizer ${TOKENIZER}
done

# Regular expression tokenizer
# Extract Capitalized words only
hb analyze --text "${TEXT}" --tokenizer regex --tokenizer-params "pattern=[A-Z][a-z]+"

# NGram tokenizer
hb analyze --text "${TEXT}" --tokenizer ngram --tokenizer-params "min_gram=3;max_gram=3;prefix_only=False"

#---------#
# Filters #
#---------#

# Simple (i.e. non-configurable) filters
for FILTER in alphanum_only ascii_fold lowercase
do
    hb analyze --text "${TEXT}" --filter ${FILTER}
done

# Exclude long words
hb analyze --text "${TEXT}" --filter remove_long --filter-params "length_limit=7"

# Stem
# Tokens are expected to be lowercased beforehand.
hb analyze --text "${TEXT}" --filter lowercase --filter stemmer --filter-params "|language=english"

# Filter English stopwords.
hb analyze --text "${TEXT}" --filter stopword --filter-params "language=english"

# Filter a provided list of stopwords.
# See also the configuration `HB_CUSTOM_STOPWORDS`.
hb analyze --text "${TEXT}" --filter custom_stopword --filter-params "stopwords=[is,and,in]"

# Split compound words (i.e. words made of multiple ones)
# See https://docs.rs/tantivy/latest/tantivy/tokenizer/struct.SplitCompoundWords.html
hb analyze --text "As a countermeasure, we decided to order a cheeseburger" --filter split_compound --filter-params "constituent_words=[counter,measure,cheese,burger]"
# Using the default analyzer
hb analyze --text "As a countermeasure, we decided to order a cheeseburger"

#------------------#
# Combined filters #
#------------------#

# Analyze a string by converting to lower case, and excluding words with 7 characters or more.
hb analyze --text "${TEXT}" --filter lowercase --filter remove_long --filter-params "|length_limit=7"

# Analyze a string by excluding english stop-words
hb analyze --text "${TEXT}" --filter stopword --filter-params "language=english"

# Analyze a string by converting to lower case, excluding words with 5 characters or more, and excluding a custom list of stop-words
hb analyze --text "${TEXT}" --filter lowercase --filter remove_long --filter custom_stopword --filter-params "|length_limit=5|stopwords=[is,and,in]"
