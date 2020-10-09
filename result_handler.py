import os
import re

from difflib import SequenceMatcher


# commands in file should be separated with at least 10 symbols '#'
SEPARATOR = '#' * 10


class SearchResult:
    def __init__(self, description, tags, command, example, explanation, notes, score):
        self.description = description
        self.tags = tags
        self.command = command
        self.example = example
        self.explanation = explanation
        self.notes = notes
        self.score = score


def get_tags_score(tags, user_input):
    """ Find how many words match tags.
    
    Example:
        tags - linux bash files find
        user_input - find files by name

    words "find" and "files" match tags, 2 words from 4 tags, thus score 2/4 = 0.5
    """
    tag_words = tags[:]
    words = user_input.split()
    match = 0
    for word in words:
        if word in tag_words:
            match += 1
            tag_words.remove(word)
    return match / len(tags)


def parse_command(command_str, user_input):
    description = re.findall('# description:(.*)# tags:', command_str, re.DOTALL)[0].strip()
    tags = re.findall('# tags:(.*)# command:', command_str, re.DOTALL)[0].strip().split()
    command = re.findall('# command:(.*)# example:', command_str, re.DOTALL)[0].strip()
    example = re.findall('# example:(.*)# explanation:', command_str, re.DOTALL)[0].strip()
    explanation = re.findall('# explanation:(.*)# notes:', command_str, re.DOTALL)[0].strip()
    notes = re.findall('# notes:(.*)' + SEPARATOR, command_str, re.DOTALL)[0].strip()
    score = SequenceMatcher(None, description, user_input).ratio() * get_tags_score(tags, user_input)

    # TODO: remove debug prints
    print(description)
    print(score)
    return SearchResult(description, tags, command, example, explanation, notes, score)


def parse_file(filename, user_input):
    """ Command structure:

    description: <description>
    tags: <tags>
    command: <command>
    example: <example>
    explanation: <explanation>
    notes: <notes>

    All values can be multiline
    """
    results = []
    command = ''
    with open(filename) as f:
        for line in f:
            if line.startswith(SEPARATOR):
                # add separator for easier regex
                command += line
                results.append(parse_command(command, user_input))
                command = ''
            else:
                command += line
    return results


def find_command(user_input):
    """ Look recursively through all files in data folder. """
    results = []
    for root, subdirs, files in os.walk('data'):
        for filename in files:
            full_path = os.path.join(root, filename)
            results.append(parse_file(full_path, user_input))
    return results
