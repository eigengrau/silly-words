silly-words
===========

Generate related words from an abstract template, to be used as a library when
implementing novelty commands for IRC bots.

silly-words defines a method which, given a query, generates random, related
English words using the WordNet lexicon. What *related* means depends on the
query. Currently, silly-words will generate hyponyms (special cases) for nouns,
and similar terms for adjectives.

A helper method to fix up determiner assimilation (*a* ⇒ *an*) is also provided.

Example
-------

::

   !throw an <angry.a> <mammal> at John Doe

   ⇒ User throws a choleric koala at John Doe

TODO
----

- automatically infer the appropriate part-of-speech in word templates
- generate aliterations

