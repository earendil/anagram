#!/usr/bin/env python3
import re
import sys
from os.path import isfile
import argparse
from collections import defaultdict


def file_handler(file_path: str):
    """ Generator that handles a file resource yielding one line at a time.

    :param: file_path: A file folder location
    :returns: Generator containing lines of given file as strings.
    :raises: FileNotFoundError
    """
    with open(file_path) as file:
        for line in file:
            yield line.strip("\n")


class Anagrams(object):
    """ A class that represents a collection of grouped anagrams.
    """

    def __init__(self, file_path):
        self.words = file_handler(file_path)
        self.anagrams = defaultdict(set)

    @staticmethod
    def validate(word: str):
        """ Ensures a string is simply a word, by a regular expression match.

        :param word: A string expecting to contain a single word.
        :return: True if input is a word, False otherwise
        """
        return bool(re.match(r"^\w+$", word))

    def populate(self):
        """ Populates groups of anagrams, using a python defaultdict and adding each sorted word as key
        to the anagram group. Each file line is validated as a word beforehand.

        :return: True if all words pass validation, False otherwise.
        """
        for word in self.words:
            if not self.validate(word):
                return False
            key = "".join(sorted(word))
            self.anagrams[key].add(word)
        return True

    def print(self):
        """ Prints anagrams separated by groups.
        The groups are separated by new lines and the words inside each group by commas.
        """
        for value in self.anagrams.values():
            print(", ".join(value))


def _main(args):

    if not isfile(args.file_path):
        sys.exit(f"File not found within path: {args.file_path}")

    anagram_groups = Anagrams(args.file_path)

    if not anagram_groups.populate():
        sys.exit(
            f"Unexpectedly formatted line within file, please ensure the file contains one word per line."
        )

    anagram_groups.print()


def main(args):

    parser = argparse.ArgumentParser(
        description="""
         A program that takes as argument the path to a file containing one word per line, 
         groups the words that are anagrams to each other, and writes to the standard output each of these groups. 
         The groups are separated by new lines and the words inside each group by commas.
        """
    )

    parser.add_argument("file_path", help="Path to file containing words to be grouped")
    parsed_args = parser.parse_args(args)

    _main(parsed_args)


if __name__ == "__main__":
    main(sys.argv[1:])
