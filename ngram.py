import re
from collections import Counter
import argparse
import random


# Helper functions
def tokenize_words(text):
    return re.findall(r"(?:[A-Z]\.)+|\d+\.\d+|\w+(?:'\w+)?|[^\w\s]", text)

def clean(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text

def build_ngrams(tokens, n):
    slices = list([tokens[i:] for i in range(n)])
    ngrams = list(zip(*slices))

    return ngrams

def build_model(tokens, n):
    ngrams = build_ngrams(tokens, n)
    ngram_count = Counter(ngrams)
    context = list([ngram[:-1] for ngram in ngrams])
    context_count = Counter(context)

    return ngram_count, context_count

def generated_text(ngram_count, seed, n, num_words):
    generated_text = list(seed)
    for i in range(num_words):
        next_words = [ngram[-1] for ngram in ngram_count if ngram[:-1] == seed]
        weights = [ngram_count[ngram] for ngram in ngram_count if ngram[:-1] == seed]

        if not next_words:
            break

        generated_text.append(random.choices(next_words, weights)[0])
        seed = tuple(generated_text[-(n-1):])
        i += 1

    return generated_text


# Print the top 'n' bigrams and trigrams
def top_bigrams_and_trigrams(filepath, top_n=10):
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()
    tokens = tokenize_words(clean(raw))

    bigram_count, bigram_context_count = build_model(tokens, 2)
    trigram_count, trigram_context_count = build_model(tokens, 3)

    print("=" * 50)
    print(f"Top {top_n} bigrams:")
    print("-" * 50)

    for ngram, count in bigram_count.most_common(top_n):
        context = ngram[:-1]
        context_count = bigram_context_count[context]
        print(f"{ngram} (count: {count}) | context: {context} (count: {context_count})")

    print("=" * 50)
    print(f"Top {top_n} trigrams:")
    print("-" * 50)

    for ngram, count in trigram_count.most_common(top_n):
        context = ngram[:-1]
        context_count = trigram_context_count[context]
        print(f"{ngram} (count: {count}) | context: {context} (count: {context_count})")
    
    print("=" * 50)


# Generate text based on a seed
def generate(filepath, n, num_words):
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()
    tokens = tokenize_words(clean(raw))

    ngram_count, ngram_context_count = build_model(tokens, n)

    text = generated_text(ngram_count, ('i', 'did', 'not'), n, num_words)

    print(" ".join(text))


# Command-line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict the next words based on 'n' previous words")
    parser.add_argument("filepath", help="Path to the text file to analyze")
    parser.add_argument("--function", "-f", choices=["generate", "top",], default="generate", help="Analysis function to run")
    parser.add_argument("--number", "-n", type=int, default=4, help="Number of the ngrams")
    parser.add_argument("--words", "-w", type=int, default=50, help="Number of words for the generated text")
    
    args = parser.parse_args()

    if args.function == "generate":
        generate(args.filepath, n=args.number, num_words=args.words)
    elif args.function == "top":
        top_bigrams_and_trigrams(args.filepath)