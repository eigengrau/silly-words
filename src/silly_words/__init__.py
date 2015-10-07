"""Generate related words from an abstract template.

silly_words defines a method which, given a query, generates random, related
English words using the WordNet lexicon. What *related* means depends on the
query. Currently, it will generate hyponyms (special cases) for nouns, and
similar terms for adjectives.

A helper method to fix up determiner assimilation (*a* ⇒ *an*) is also provided.

"""

import random

import nltk
from nltk.corpus import wordnet


__all__ = (
    'get_related',
    'fix_determiners'
)


# NLTK seems to check for updates and tries to unzip the corpus even when it’s
# already installed, which slows down the import, so only invoke nltk.download()
# if wordnet isn’t already available.
try:
    wordnet.ensure_loaded()
except:
    try:
        nltk.download('wordnet')
    except BaseException as exc:
        raise ImportError("Could not download WordNet:", exc)


_VOWELS = "aeiou"


def get_related(query, pos='n'):
    """If query is for a noun, return a random hyponym for query. If query is
    for an adjective, return a related adjective.

    Args:
        query (str): A word lemma. May contain whitespace for complex lemmata
            (*bowler hat*).
        pos (Optional[str]): The queries’ part-of-speech.

    Returns:
        str: A related word lemma.

    Raises:
        ValueError: If no related lemma is found, or when an invalid
            part-of-speech is supplied.

    """

    pos = pos.lower()

    # WordNet uses the underscore to split lemmata.
    query = query.replace(" ", "_")

    if pos == 'n':
        result = _get_hyponym_n(query)
    elif pos == 'a':
        result = _get_related_a(query)
    else:
        raise ValueError("Unknown POS: {pos}".format(**locals()))

    result = result.replace("_", " ")
    return result


def fix_determiners(text):
    """Fix up occurrences of *a* and *an*.

    Args:
        text (str): Arbitrary English text.

    Returns:
        str: The text, with instances of *a* and *an* fixed up appropriately.

    """

    def pairwise(l):
        return zip(l[:-1], l[1:])

    def is_det(token):
        return token in ("a", "an")

    fixed = []
    tokens = text.split(" ")
    for t1, t2 in pairwise(tokens):
        if is_det(t1):
            t1 = "an" if t2[0] in _VOWELS else "a"
        fixed.append(t1)
    fixed.append(tokens[-1])

    return " ".join(fixed)


def _lemmata_by_freq(query, pos):
    """Return lemmata for query, sorted descending by frequency.

    """

    lemmata = wordnet.lemmas(query, pos)
    return sorted(
        lemmata,
        key=lambda lemma: lemma.count(),
        reverse=True
    )


def _get_related_a(query):
    """Return a related adjective."""

    adj_lemmas = _lemmata_by_freq(query, pos=wordnet.ADJ)
    adj_senses = list(map(lambda lemma: lemma.synset(), adj_lemmas))

    if not adj_senses:
        raise ValueError("No results for query {}".format(query))

    # Commit to the most frequent sense.
    adj_synset = adj_senses[0]

    related = adj_synset.similar_tos()

    if not related:
        err = "No related adjectives for query {}".format(query)
        raise ValueError(err)

    related_sense = random.choice(related)
    related_lemma = random.choice(related_sense.lemmas())
    return related_lemma.name()


def _get_hyponym_n(query):
    """Return a random hyponym."""

    thing_lemmas = _lemmata_by_freq(query, pos=wordnet.NOUN)
    thing_senses = list(map(lambda lemma: lemma.synset(), thing_lemmas))

    if not thing_senses:
        raise ValueError("No results for query {}".format(query))

    # Commit to the most frequent sense.
    thing_synset = thing_senses[0]

    def get_hyponym(lemma):
        return lemma.hyponyms()

    hyponyms = [
        hyponym_lemma.name()
        for hyponym_synset in thing_synset.closure(get_hyponym)
        for hyponym_lemma in hyponym_synset.lemmas()
    ]

    if not hyponyms:
        raise ValueError("No hyponyms for query {}".format(query))

    # Fix up whitespace.
    hyponyms = list(map(lambda lexeme: lexeme.replace("_", " "), hyponyms))

    return random.choice(hyponyms)
