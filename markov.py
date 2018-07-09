"""Generate Markov text from text files."""

from random import choice
from string import punctuation
import sys


def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    f = open(file_path)
    return f.read()
    


def make_chains(text_string, len_of_ngram):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']
        
        >>> chains[('there','juanita')]
        [None]
    """

    chains = {}

    text_lst = text_string.split()
    index = 0

    while index < len(text_lst) - len_of_ngram:
        ngram_lst = []
        for i in range(len_of_ngram):
            ngram_lst.append(text_lst[index + i])
        ngram_tuple = tuple(ngram_lst)
    #     bigram = (text_lst[index], text_lst[index + 1])
        
        if ngram_tuple in chains:
            chains[ngram_tuple].append(text_lst[index + len_of_ngram])
        else:
            chains[ngram_tuple] = [text_lst[index + len_of_ngram]]
        index += 1
    # for k,v in chains.items():
    #     print(k,": ", v)
    return chains


def make_text(chains):
    """Return text from chains."""

    words = []

    random_tuple = choice(list(chains.keys()))

    while not random_tuple[0].istitle():
        random_tuple = choice(list(chains.keys()))

    words.extend(random_tuple)

    while random_tuple in chains:
        next_word = choice(chains[random_tuple])
        words.append(next_word)

        reuse_words = list(random_tuple)
        reuse_words = reuse_words[1:]
        random_tuple = tuple(reuse_words) + (next_word, )
        last_char = next_word[-1]
        if last_char in punctuation:
            break

    return " ".join(words)


input_path = sys.argv[1]
input_ngram_len = int(sys.argv[2])


# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text, input_ngram_len)

# Produce random text
random_text = make_text(chains)

print(random_text)
