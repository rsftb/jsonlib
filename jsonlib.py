import os
import re
from pathlib import Path
from dataclasses import dataclass


class JSON_SyntaxError(Exception): ...


@dataclass
class TOKEN:
    value: any = None
    pos: tuple[int, int] = ()


class VOID_TOKEN(type):
    """
    Lets me pass any parameter to the class and have it return the class (line 130)
    """
    pass


## Atomic tokens

class TOKEN_LSQUARE(TOKEN): ...  # [
class TOKEN_RSQUARE(TOKEN, metaclass=VOID_TOKEN): ...  # ]

class TOKEN_LCURLY(TOKEN):  # {
    @staticmethod
    def consume(_tokens: list[TOKEN], _list_index: int) -> tuple[TOKEN, int]:
        start_list_index = _list_index
        while _tokens[_list_index] is not TOKEN_RCURLY:
            _list_index += 1

        #tokens = tokens[_list_index:]
        #tokens.insert(TOKEN_OBJECT(tokens[]))
        return _tokens, _list_index

class TOKEN_RCURLY(TOKEN, metaclass=VOID_TOKEN): ...  # }

class TOKEN_DQUOTE(TOKEN): ...  # "
class TOKEN_PERIOD(TOKEN, metaclass=VOID_TOKEN): ...  # .
class TOKEN_COLON(TOKEN, metaclass=VOID_TOKEN): ...  # :
class TOKEN_COMMA(TOKEN, metaclass=VOID_TOKEN): ...  # ,

class TOKEN_NUMBER(TOKEN): ...  # 0-9
class TOKEN_LETTER(TOKEN): ...  # a-z
class TOKEN_SPECIAL(TOKEN): ...  # Anything else, should primarily catch special characters in strings


atomic_token_map: dict[cls] = {
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
    def __init__(self, *args):
        self.content = {}

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
            raise JSON_SyntaxError(f"Missing opening curled bracket '{{' for JSON body, found '{file[-1][-1]}' instead.")
        elif file[-1][-1] != '}':
            raise JSON_SyntaxError(f"Missing ending curled bracket '}}' for JSON body, found '{file[-1][-1]}' instead.")

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

                token = atomic_token_map.get(char, None)
                if not token:
                    if re.fullmatch(r"[0-9]", char):
                        token = TOKEN_NUMBER # or append
                    elif re.fullmatch(r"[a-z]", char):
                        token = TOKEN_LETTER
                    else:
                        token = TOKEN_SPECIAL

                tokens.append(token(char, pos=(lineno, charno)))

        return tokens

    @staticmethod
    def _parse(tokens: list[TOKEN]) -> ParseTree:
        """
        Parses the tokens into a tree
        """
        list_index = 0
        tov = None

        while list_index < len(tokens):
            tokens, list_index = tokens[list_index].consume(tokens)

