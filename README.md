# NgramGenerator
A Python text generation tool that uses N-gram language models to predict and generate new text based on patterns learned from a source file.
 
 
## Features
- **N-gram Language Model**: Builds probabilistic models from any plain-text corpus
- **Weighted Random Sampling**: Generates text by sampling next words proportionally to their frequency
- **Flexible N-gram Order**: Configurable `n` parameter to control how much context is used
- **Multiple Generation Modes**: Start from a predefined seed or a random context
- **N-gram Statistics**: Inspect the most frequent bigrams and trigrams in a corpus
## Installation
Requires Python 3.6+ with no external dependencies beyond the standard library.
 
 
## Quick Start
```bash
# Generate text from a predefined seed
python textgenerator.py corpus.txt --function generate-predefined
 
# Generate text from a random seed
python textgenerator.py corpus.txt --function generate-random
 
# Display top bigrams and trigrams
python textgenerator.py corpus.txt --function top
```
 
 
## Usage
### Command-Line Interface
```bash
python textgenerator.py <filepath> [--function <function_name>] [--number <n>] [--words <num_words>]
```
 
### Options
- `filepath`: Path to the plain-text file to use as a corpus (required)
- `--function, -f`: Analysis function to run (default: `generate-predefined`)
- `--number, -n`: N-gram order, i.e. how many tokens form each n-gram (default: `4`)
- `--words, -w`: Number of words to generate (default: `50`)
### Input Format
A plain UTF-8 text file. Any genre or domain works — novels, scripts, articles, etc.
 
### Available Functions
 
**`generate-predefined`** (default) — Generate text starting from the fixed seed `('i', 'did', 'not')`
```bash
python textgenerator.py corpus.txt
```
 
**`generate-random`** — Generate text starting from a randomly chosen context
```bash
python textgenerator.py corpus.txt --function generate-random
```
 
**`top`** — Print the most frequent bigrams and trigrams with their context counts
```bash
python textgenerator.py corpus.txt --function top
```
 
 
## How It Works
### Building the Model
1. **Loading**: Reads the text file as a raw string
2. **Cleaning**: Lowercases text and strips all non-alphabetic characters
3. **Tokenization**: Extracts words, contractions, abbreviations, and decimals
4. **N-gram Construction**: Slides a window of size `n` across the token list to produce all consecutive n-grams
5. **Counting**: Tallies n-gram frequencies and context (prefix) frequencies separately
### Text Generation
Starting from a seed tuple of length `n - 1`, the model repeatedly:
1. Looks up all n-grams whose prefix matches the current seed
2. Samples the next word using weighted random selection proportional to frequency
3. Advances the seed by one token and repeats until the desired word count is reached
Generation stops early if the current seed has no known continuations in the corpus.
 
 
## Function Reference
### Core Functions
- `tokenize_words(text)` — Tokenizes text into words, contractions, abbreviations, and decimals
- `clean(text)` — Lowercases text and removes all non-alphabetic characters
- `build_ngrams(tokens, n)` — Returns a list of all consecutive n-gram tuples from a token list
- `build_model(tokens, n)` — Returns n-gram counts and context counts as `Counter` objects
- `generate_text(ngram_count, seed, n, num_words)` — Generates a list of tokens from a seed using weighted sampling
### Analysis Functions
- `generate_predefined(filepath, n, num_words)` — Generates and prints text from the seed `('i', 'did', 'not')`
- `generate_random(filepath, n, num_words)` — Generates and prints text from a randomly selected seed
- `top_bigrams_and_trigrams(filepath, top_n=10)` — Prints the most frequent bigrams and trigrams with context statistics
## Example Output
 
### `--function generate-predefined`
```
i did not feel the inconvenience of the weather i was better fitted by my conformation for the endurance of cold than heat but my chief delights were the sight of a part of my journey on horseback i afterwards hired a mule as the more surefooted and least liable to receive injury
```
 
### `--function generate-random`
```
course towards the mainland i shuddered to think who might be the next victim sacrificed to his insatiate revenge and then i shall be happy again even after the sad death of my aunt grief had given softness and a winning mildness to her manners which had before been remarkable for vivacity nor
```
 
### `--function top`
```
==================================================
Top 10 bigrams:
--------------------------------------------------
('of', 'the') (count: 526) | context: ('of',) (count: 2639)
('of', 'my') (count: 272) | context: ('of',) (count: 2639)
('in', 'the') (count: 262) | context: ('in',) (count: 1127)
...
==================================================
Top 10 trigrams:
--------------------------------------------------
('which', 'i', 'had') (count: 38) | context: ('which', 'i') (count: 149)
('i', 'did', 'not') (count: 34) | context: ('i', 'did') (count: 39)
('i', 'could', 'not') (count: 32) | context: ('i', 'could') (count: 77)
...
==================================================
```
 
 
## Notes
- All text processing is case-insensitive
- Punctuation and digits are stripped during cleaning, so only alphabetic tokens are modelled
- Generation with a high `n` value produces more coherent but less varied text; lower `n` produces more creative but noisier output
- The predefined seed `('i', 'did', 'not')` requires those tokens to appear consecutively in the corpus
- Short forms: `-f` for `--function`, `-n` for `--number`, `-w` for `--words`