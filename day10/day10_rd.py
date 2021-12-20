from collections import Counter, deque
from typing import List, Union

CLOSING_CHAR_MAP = {"[": "]", "{": "}", "(": ")", "<": ">"}
LEFT_CHARS = list(CLOSING_CHAR_MAP.keys())
RIGHT_CHARS = list(CLOSING_CHAR_MAP.values())

SCORING_MAP = {")": 3, "]": 57, "}": 1197, ">": 25137}


def read_data(raw_data_file: str) -> List[str]:
    """
    Reads data from `raw_data_file` into list
    """
    data = []
    with open(raw_data_file, "r") as f:
        while line := f.readline().rstrip():
            data.append(line)
    return data


def first_illegal_character(line: str) -> Union[None, str]:
    """
    Returns first illegal character if `line` is corrupt
    """
    unread_stack, read_stack = deque(line), deque()
    while unread_stack:
        if unread_stack[0] in LEFT_CHARS:
            read_stack.append(unread_stack.popleft())
        elif CLOSING_CHAR_MAP[read_stack[-1]] == unread_stack[0]:
            read_stack.pop()
            unread_stack.popleft()
        else:
            return unread_stack.popleft()  # First illegal character in "corrupt" line
    return  # Return `None` for "incomplete" line


def syntax_error_score(data: List[str]) -> Counter:
    """
    Returns first character of line if corrupt
    """
    first_char_counter = Counter([first_illegal_character(line) for line in data])
    score = 0
    for char, occurrences in first_char_counter.items():
        if char:
            score += SCORING_MAP[char] * occurrences
    return score


if __name__ == "__main__":
    data = read_data("./subsystem_rd.txt")
    print(syntax_error_score(data))  # Part 1 Solution: 462693
