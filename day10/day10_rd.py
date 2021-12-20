from collections import Counter, deque
from typing import List, Tuple, Union

import numpy as np

CLOSING_CHAR_MAP = {"[": "]", "{": "}", "(": ")", "<": ">"}
LEFT_CHARS = list(CLOSING_CHAR_MAP.keys())
RIGHT_CHARS = list(CLOSING_CHAR_MAP.values())

SYNTAX_SCORING_MAP = {")": 3, "]": 57, "}": 1197, ">": 25137}
AUTOCOMPLETE_SCORING_MAP = {")": 1, "]": 2, "}": 3, ">": 4}


def read_data(raw_data_file: str) -> List[str]:
    """
    Reads data from `raw_data_file` into list
    """
    data = []
    with open(raw_data_file, "r") as f:
        while line := f.readline().rstrip():
            data.append(line)
    return data


def first_illegal_character(line: str) -> Tuple[Union[None, str], deque]:
    """
    Returns first illegal character if `line` is corrupt, `None` if incomplete
    """
    unread_stack, read_stack = deque(line), deque()
    while unread_stack:
        if unread_stack[0] in LEFT_CHARS:
            read_stack.append(unread_stack.popleft())
        elif CLOSING_CHAR_MAP[read_stack[-1]] == unread_stack[0]:
            read_stack.pop()
            unread_stack.popleft()
        else:
            return (
                unread_stack.popleft(),  # First illegal character in "corrupt" line
                read_stack,
            )
    return (None, read_stack)  # Return `None` for "incomplete" line


def autocompleted_string(line: str) -> Union[None, str]:
    """
    Returns the remaining string of closing characters to finish an incomplete line
    """
    is_corrupt, read_stack = first_illegal_character(line)
    autocompleted_chars = ""
    if not is_corrupt:
        while read_stack:
            autocompleted_chars += CLOSING_CHAR_MAP[read_stack.pop()]
        return autocompleted_chars


def syntax_error_score(data: List[str]) -> int:
    """
    Returns syntax error score
    """
    first_char_counter = Counter([first_illegal_character(line)[0] for line in data])
    score = 0
    for char, occurrences in first_char_counter.items():
        if char:
            score += SYNTAX_SCORING_MAP[char] * occurrences
    return score


def winning_autocomplete_score(data: List[str]) -> int:
    """
    Returns median autocomplete score
    """
    autocompleted_strings = [
        autocompleted_string(line) for line in data if autocompleted_string(line)
    ]
    scores = []
    for string in autocompleted_strings:
        score = 0
        for char in string:
            score = (5 * score) + AUTOCOMPLETE_SCORING_MAP[char]
        scores.append(score)
    return int(np.median(scores))


if __name__ == "__main__":
    data = read_data("./subsystem_rd.txt")
    print(syntax_error_score(data))  # Part 1 Solution: 462693
    print(winning_autocomplete_score(data))  # Part 2 Solution: 3094671161
