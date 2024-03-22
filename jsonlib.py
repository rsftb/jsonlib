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
class TOKEN_STRINGABLE(TOKEN): ...  # Anything


character_to_token: dict = {
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
                return JSON._preprocess(content)

    @staticmethod
    def _preprocess(f: str) -> dict or None:
        if f[0][0] != '{':
            raise JSON_SyntaxError(f"Missing opening curled bracket '{{' for JSON body, found '{f[-1][-1]}' instead.")

        elif f[-1][-1] != '}':
            if f[-1][-1] == " ":
                raise JSON_SyntaxError("Trailing whitespace beyond the JSON body is not allowed.")
            else:
                raise JSON_SyntaxError(f"Missing ending curled bracket '}}' for JSON body, found '{f[-1][-1]}' instead.")

        return JSON.lex(f)

    @staticmethod
    def _lex(file: list[str]) -> list[TOKEN]:
        """
        Performs lexical analysis, evaluates tokens from text
        Either returns a list of tokens or throws
        """

        tokens: list[TOKEN] = []

        inside_string: bool = False
        dquote_at: tuple = (0, 0)

        for lineno, line in enumerate(file):
            for charno, char in enumerate(line):
                try:
                    tokens.append(character_to_token[char])
                    if char == '"':
                        inside_string = not inside_string
                        dquote_at = (lineno, charno)
                except KeyError:
                    if inside_string:
                        tokens.append(TOKEN_STRINGABLE(char))
                    elif char in (' ', '\n'):
                        continue
                    elif re.fullmatch(r"[0-9]", char):
                        tokens.append(TOKEN_NUMBER(char))
                    elif re.fullmatch(r"[a-z]", char):
                        tokens.append(TOKEN_LETTER(char))
                    else:
                        raise JSON_SyntaxError(f"{path}: line {lineno+1}: char {charno+1}: token {char}")

        if inside_string:
            raise JSON_SyntaxError(f"{path}: unterminated string starting at line {dquote_at[0]+1}, character {dquote_at[1]+1}.")

        return tokens

