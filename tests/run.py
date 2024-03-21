"""
"$ python3 -m tests.run" in project root folder
"""

import os
import sys
import re
from jsonlib import JSON


samples = ["trivial_1.json"]

os.chdir("tests")


def count_valid_json_tokens(file: list[str]) -> int:
    """
    Does a quick count of the amount of valid tokens the lexer should produce
    """
    token_count: int = 0
    foo = ""

    for line in file:
        for char in line:
            if char in ("[", "]", "{", "}", '"', ':', '.', ',', '_'):
                foo += char
                token_count += 1
            elif re.fullmatch(char, r"[0-9]"):
                token_count += 1
                foo += char
            elif re.fullmatch(char, r"[a-zA-Z]"):
                token_count += 1
                foo += char

    return token_count


def test_lexer(file: str) -> None or AssertionError:
    with open(f"{file}", 'r') as f:
        f = f.readlines()
        output = JSON.lex(f)
        lexer_tokens_len = len(output)
        valid_tokens_len = count_valid_json_tokens(f)

        with open('lex.log', 'w') as log:
            log.write(str(output))

        assert lexer_tokens_len == valid_tokens_len, f"{file}: test_lexer(): {lexer_tokens_len} to {valid_tokens_len}"


def main():
    for test_file in samples:
        print(f"| {test_file}... ", end='')
        test_lexer(test_file)

        print("\033[32m passed!\033[0m")


if __name__ == "__main__":
    print("\n* Starting jsonlib tests")
    print("* Using:", samples)
    main()

