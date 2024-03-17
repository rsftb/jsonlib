import os
import sys
from pathlib import Path
from dataclasses import dataclass

# comment log: what's up & what's new
#  hope i get to use processerror and parseerror
#  lexer turns relevant characters into tokens, parser turns that list of tokens into something meaningful
#  turned the TOKEN class into a @dataclass
#  changed meta a little bit, turned parse() into lex(), recursion now takes
#   place on the json string 'f' itself instead of a dictionary, return should
#   accomodate for this


# class ProcessError(Exception): ...
# class ParseError(Exception): ...
class JSON_SyntaxError(Exception): ...


@dataclass
class TOKEN:
    value: any

class TOKEN_KEY(TOKEN): ...
class TOKEN_VALUE(TOKEN): ...

# class TOKEN_COLON(TOKEN): ...  # Could be used,
# class TOKEN_COMMA(TOKEN): ...  #  just don't have to be

class TOKEN_LSQUARED(TOKEN): ...
class TOKEN_RSQUARED(TOKEN): ...

class TOKEN_LCURLY(TOKEN): ...
class TOKEN_RCURLY(TOKEN): ...

class TOKEN_OBJECT(TOKEN):
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
                f = f.read()
                return JSON.preprocess(f)

    def preprocess(f: str) -> dict or None:
        for char in (' ', '\n'):  # removing this and skipping ' ' and '\n' while lexing instead may be better
            f = f.replace(char, '')  # also allows for accurate line no. info

        if f[0] != '{':
            raise JSON_SyntaxError(f"Missing opening curled bracket '{{' for JSON body, found '{f[-1]}' instead.")

        elif f[-1] != '}':
            if f[-1] == " ": raise JSON_SyntaxError("Trailing whitespace beyond the JSON body is not allowed.")
            else:            raise JSON_SyntaxError(f"Missing ending curled bracket '}}' for JSON body, found '{f[-1]}' instead.")

        executed = parse(f)

        if not executed:
            return None
        else:
            return executed

    @staticmethod
    def lex(f: str, parent=None) -> list:
        """
        Performs lexical analysis, evaluates tokens from text
        Either returns a list of tokens or throws JSON_SyntaxError
        Recursive function because I can
        """

        key = ""
        value = None

        at_key:   bool = True
        read_key: bool = False

        semicolon_check: bool = False

        at_value: bool = False
        got_type: bool = False
        value_type: str = None

        comma_check: bool = False

        tokens: list[TOKEN] = []

        for i, char in enumerate(f):
            if at_key:
                if not read_key:
                    if char != '"':
                        raise JSON_SyntaxError(f"Expected double quote character (\") while finding start of some key, found '{char}' instead.")
                    else:
                        read_key = True
                elif read_key:
                    if char != '"':
                        key += char
                    else:
                        tokens.append(TOKEN_KEY(key))
                        at_key   = False
                        read_key = False
                        semicolon_check = True
            elif semicolon_check:
                if char != ':':
                    raise JSON_SyntaxError(f"Expected ':' after key \"{key}\", found '{char}' instead.")
                else:
                    semicolon_check = False
                    at_value = True

            elif at_value:
                if not got_type:
                    if char == '[':
                        value_type = "array"
                    elif char == '{':
                        value_type = "dict" # recursion could take place here
                    else:
                        value_type = "literal"
                    got_type = True

                elif got_type:
                    if value_type == "array":
                        pass
                    elif value_type == "dict":
                        pass
                    elif value_type == "literal":
                        pass
                    else:
                        pass



        return tokens

    def parse(self):
        pass



test = JSON.str_to_dict('{"hello": "world", "foo": 4}')
print(test)


#foo = jsonreader.read(path)
#foo["hello"] = "world"
#jsonreader.write(foo, path
