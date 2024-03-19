"""
"$ python3 -m tests.run" in project root folder
"""

import os
import sys
import re
import jsonlib

os.chdir("tests")

JSON = jsonlib.JSON

samples = ["trivial_1.json"]


def count_valid_tokens(file: str) -> int:
    i: int = 0

    for char in file:
        if char in ("[", "]", "{", "}", '"', ':', '.', ',', '_'):
            i += 1
        elif re.fullmatch(char, r"[0-9]"):
            i += 1
        elif re.fullmatch(char, r"[a-zA-Z]"):
            i += 1

    return i


def test_lexer(name: str):
    with open(f'{name}', 'r') as f:
        # token check
        output = JSON.lex(f.read())

        len_output   = len(output)
        valid_tokens = count_valid_tokens(f.read())
        total_len_file = len(f.read())
        print(f.read())
        print(total_len_file)
        assert len_output == valid_tokens, f"{name}: {len_output} to {total_len_file}"


for test_file in samples:
    test_lexer(test_file)

