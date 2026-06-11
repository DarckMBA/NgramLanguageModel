import re
import argparse


# Helper functions
def tokenize_words(text):
    return re.findall(r"(?:[A-Z]\.)+|\d+\.\d+|\w+(?:'\w+)?|[^\w\s]", text)

def clean(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text

def build_ngrams(tokens, n):
    slices = list([tokens[i:] for i in range(n)])
    ngrams = zip(*slices)

    return ngrams


# Print the first 'n' bigrams and trigrams
def first_ngrams(filepath, top_n=9):
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()
    tokens = tokenize_words(clean(raw))

    bigrams = list(build_ngrams(tokens, 2))
    trigrams = list(build_ngrams(tokens, 3))

    print("=" * 50)
    print(f"Top {top_n} bigrams:")
    print("-" * 50)

    for i in range(top_n):
        print(f"{bigrams[i]}")

    print("=" * 50)
    print(f"Top {top_n} trigrams:")
    print("-" * 50)

    for i in range(top_n):
        print(f"{trigrams[i]}")
    
    print("=" * 50)


# Command-line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict the next words based on 'n' previous words")
    parser.add_argument("filepath", help="Path to the text file to analyze")
    parser.add_argument("--function", "-f", choices=["lists"], default="lists", help="Analysis function to run")
    
    args = parser.parse_args()
    
    if args.function == "lists":
        first_ngrams(args.filepath)