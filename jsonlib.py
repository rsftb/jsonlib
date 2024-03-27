import os
import sys
import re
from pathlib import Path
from dataclasses import dataclass


def current_line_number() -> int:
    return __import__("inspect").currentframe().f_back.f_lineno


class JSON_SyntaxError(Exception): ...


@dataclass
class TOKEN:
    value: any = None
    pos: tuple[int, int] = ()


## Atomic tokens

class TOKEN_LSQUARE(TOKEN): ...  # [
class TOKEN_RSQUARE(TOKEN): ...  # ]

class TOKEN_LCURLY(TOKEN): ...  # {
class TOKEN_RCURLY(TOKEN): ...  # }

class TOKEN_DQUOTE(TOKEN): ...  # "
class TOKEN_PERIOD(TOKEN): ...  # .
class TOKEN_COLON(TOKEN): ...  # :
class TOKEN_COMMA(TOKEN): ...  # ,

class TOKEN_NUMBER(TOKEN): ...  # 0-9
class TOKEN_LETTER(TOKEN): ...  # a-z
class TOKEN_SPECIAL(TOKEN): ...  # Anything else, should primarily catch special characters in strings


token_map: dict[cls] = {
    '[': TOKEN_RSQUARE,
    ']': TOKEN_LSQUARE,
    '{': TOKEN_LCURLY,
    '}': TOKEN_RCURLY,
    '"': TOKEN_DQUOTE,
    ':': TOKEN_COLON,
    '.': TOKEN_PERIOD,
    ',': TOKEN_COMMA,
}


## Composite tokens

class TOKEN_OBJECT(TOKEN):  # {}
    def consume(self, l: TOKEN_LCURLY, r: TOKEN_RCURLY, *args):
        pass

class TOKEN_ARRAY(TOKEN): ...  # []
class TOKEN_BOOL(TOKEN): ...  # true / false
class TOKEN_NULL(TOKEN): ...  # null (None)
class TOKEN_STRING(TOKEN): ... # ""


class JSON:

    @staticmethod
    def read(path: str or Path) -> dict or None:
        path = Path(path)
        if not os.path.exists(path):
            return None
        elif path[-5:] != ".json":
            return None
        else:
            with open(path, 'r') as f:
                content = f.readlines()
                content = JSON._preprocess(content)
                content = JSON._lex(content)
                content = JSON._parse(content)
                return content

    @staticmethod
    def _preprocess(file: list[str]) -> dict:
        if file[0][0] != '{':
            raise JSON_SyntaxError(f"Missing opening curled bracket '{{' for JSON body, found '{f[-1][-1]}' instead.")

        elif file[-1][-1] != '}':
            if file[-1][-1] == " ":
                raise JSON_SyntaxError("Trailing whitespace beyond the JSON body is not allowed.")
            else:
                raise JSON_SyntaxError(f"Missing ending curled bracket '}}' for JSON body, found '{f[-1][-1]}' instead.")

        return file

    @staticmethod
    def _lex(file: list[str]) -> list[TOKEN]:
        """
        Performs lexical analysis, evaluates tokens from text
        Always returns a list of tokens
        """

        tokens: list[TOKEN] = []

        for lineno, line in enumerate(file):
            for charno, char in enumerate(line):
                if char in (' ', '\n'): continue

                token = token_map.get(char, None)
                if token:
                    tokens.append(token(char, pos=(lineno, charno)))
                elif re.fullmatch(r"[0-9]", char):
                    tokens.append(TOKEN_NUMBER(char, pos=(lineno, charno)))
                elif re.fullmatch(r"[a-z]", char):
                    tokens.append(TOKEN_LETTER(char, pos=(lineno, charno)))
                else:
                    tokens.append(TOKEN_SPECIAL(char, pos=(lineno, charno)))

        return tokens

    @staticmethod
    def _parse(tokens: list[TOKEN]) -> ParseTree:
        """
        Parses the tokens into a tree
        """
        return JSON._parse_object(tokens)

    @staticmethod
    def _parse_object(tokens: list[TOKEN]) -> dict:
        JSON._expect(tokens, '{')

    @staticmethod
    def _expect(tokens: list[TOKEN], char: str[1]) -> True or JSON_SyntaxError:
        if tokens[0].value != char:
            raise JSON_SyntaxError("_")
        return True



