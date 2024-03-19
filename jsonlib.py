import os
import sys
import re
from pathlib import Path
from dataclasses import dataclass

import inspect

def current_line_number() -> int:
    return inspect.currentframe().f_back.f_lineno


# class ProcessError(Exception): ...
# class ParseError(Exception): ..,
class JSON_SyntaxError(Exception): ...
class UnreachableCode(Exception): ...

@dataclass
class TOKEN:
    value: any = None


class TOKEN_KEY(TOKEN): ...
class TOKEN_VALUE(TOKEN): ...

# class TOKEN_COLON(TOKEN): ... # could be used,
# class TOKEN_COMMA(TOKEN): ... #  just don't have to be

class TOKEN_LSQUARE(TOKEN): ...  # [
class TOKEN_RSQUARE(TOKEN): ...  # ]

class TOKEN_LCURLY(TOKEN): ...  # {
class TOKEN_RCURLY(TOKEN): ...  # }

class TOKEN_UNDERSCORE(TOKEN): ... # _
class TOKEN_DQUOTE(TOKEN): ...  # "
class TOKEN_PERIOD(TOKEN): ...  # .
class TOKEN_COLON(TOKEN): ...  # :
class TOKEN_COMMA(TOKEN): ...  # ,_


class TOKEN_NUMBER(TOKEN): ...  # a-zA-Z
class TOKEN_ALPHA(TOKEN): ...  # a-zA-Z0-9



class TOKEN_OBJECT(TOKEN):  # complete dictionary
    def consume(self, l: TOKEN_LCURLY, r: TOKEN_RCURLY):
        pass

class TOKEN_ARRAY(TOKEN): ...


class JSON:

    @staticmethod
    def read(path: str) -> dict or None:
        path = Path(path)
        if not os.path.exists(path):
            return None
        elif path[-5:] != ".json":
            return None
        else:
            with open(path, 'r') as f:
                content = f.readlines()
                return JSON.preprocess(content)

    def preprocess(f: str) -> dict or None:
        if f[0][0] != '{':
            raise JSON_SyntaxError(f"Missing opening curled bracket '{{' for JSON body, found '{f[-1][-1]}' instead.")

        elif f[-1][-1] != '}':
            if f[-1][-1] == " ": raise JSON_SyntaxError("Trailing whitespace beyond the JSON body is not allowed.")
            else:            raise JSON_SyntaxError(f"Missing ending curled bracket '}}' for JSON body, found '{f[-1][-1]}' instead.")

        lexed = JSON.lex(f)

        if not lexed:
            return None
        else:
            return lexed

    @staticmethod
    def lex(file: list[str]) -> list[TOKEN]:
        """
        Performs lexical analysis, evaluates tokens from text
        Either returns a list of tokens or throws
        """

        tokens: list[TOKEN] = []

        for lineno, line in enumerate(file):
            for charno, char in enumerate(line):
                if char in (' ', '\n'):
                    continue
                elif char == '[':
                    tokens.append(TOKEN_LSQUARE())
                elif char == ']':
                    tokens.append(TOKEN_RSQUARE())
                elif char == '{':
                    tokens.append(TOKEN_LCURLY())
                elif char == '}':
                    tokens.append(TOKEN_RCURLY())
                elif char == '"':
                    tokens.append(TOKEN_DQUOTE())
                elif char == ':':
                    tokens.append(TOKEN_COLON())
                elif char == '.':
                    tokens.append(TOKEN_PERIOD())
                elif char == ',':
                    tokens.append(TOKEN_COMMA())
                elif char == '_':
                    tokens.append(TOKEN_UNDERSCORE())
                elif re.fullmatch(r"[0-9]", char):
                    tokens.append(TOKEN_NUMBER(char))
                elif re.fullmatch(r"[a-zA-Z]", char):
                    tokens.append(TOKEN_ALPHA(char))
                else:
                    raise JSON_SyntaxError(f"in json file: line {lineno+1}: char {charno+1}: token {char}")

        return tokens

