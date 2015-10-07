"""A simple command-line interface to silly_words."""

import sys
import argparse
import readline

from pyparsing import (
    Word,
    Literal,
    Optional,
    OneOrMore,
    ParseBaseException,
    Group,
    printables
)

import silly_words


__all__ = ()


############
# Argparse #
############

parser = argparse.ArgumentParser(
    description="Generate silly words from an abstract template."
)

parser.add_argument(
    '--interactive', '-i',
    dest='run_interactive',
    default=False,
    action='store_true',
    help="Run interactively."
)


#############
# Pyparsing #
#############

pos_spec = (
    Literal('.') + (
        Literal('n') ^
        Literal('a')
    )('pos')
)

lexeme = Word(printables, excludeChars='<>.')('lexeme')

template = (
    Literal('<') +
    lexeme +
    Optional(pos_spec) +
    Literal('>')
)

verbatim = Word(printables, excludeChars='<>')('verbatim')

word_spec = verbatim ^ template

sent_spec = OneOrMore(Group(word_spec))


#######
# CLI #
#######

def interactive_session():

    while True:

        try:
            line = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        try:
            result = process_query(line)
        except ParseBaseException as exc:
            print("Could not parse spec:", exc)
        except ValueError as exc:
            print("Could not process query:", exc)
        else:
            print(result)


def process_query(query):

    output = []
    specs = sent_spec.parseString(query, parseAll=True)
    for spec in specs:

        if spec.verbatim:
            output.append(spec.verbatim)
            continue

        if not spec.pos:
            spec.pos = 'n'

        related = silly_words.get_related(spec.lexeme, spec.pos)
        output.append(related)

    output = " ".join(output)
    output = silly_words.fix_determiners(output)
    return output


def console_entry():

    args = parser.parse_args()
    if args.run_interactive:
        interactive_session()
    else:
        for line in sys.stdin.readlines():
            result = process_query(line)
            print(result)
