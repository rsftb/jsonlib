import os
import sys
from pathlib import Path


# comment log: what's up & what's new
#  processerror and parseerror are on hold rn, not bad ideas but what i used them for were json syntax errors
#  i think i need to first lex my input into tokens and then parse the tokens into a dictionary, but how to lex?
#  and check out how to reverse it because they're already tokens n stuff


#class ProcessError(Exception): ...
#class ParseError(Exception): ...
class JSON_SyntaxError(Exception): ...


class TOKEN_list: ...

class TOKEN_dict: ...

class TOKEN_literal: ...


class JSON:

    @staticmethod
    def read(self, path: str) -> dict or None:
        path = Path(path)
        if not os.path.exists(path):
            return None
        else:
            with open(path, 'r') as f:
                f = f.read()
                return preprocess(f)

    @staticmethod
    def preprocess(f: str) -> dict or None:
        for char in (' ', '\n'):
            f = f.replace(char, '')

        if f[0] != '{':
            raise JSON_SyntaxError(f"Missing opening curled bracket '{' for JSON body, found '{f[-1]}' instead.")

        elif f[-1] != '}':
            if f[-1] == " ": raise JSON_SyntaxError("Trailing whitespace beyond the JSON body is not allowed.")
            else:            raise JSON_SyntaxError(f"Missing ending curled bracket '}' for JSON body, found '{f[-1]}' instead.")

        executed = parse(f)
        if not executed:
            return None
        else:
            return executed

    @staticmethod
    def parse(f: str, parent=None) -> dict or False:
        key = ""
        value = None
        
        at_key  = True
        parse_key = False

        semicolon_check = False

        at_value = False

        comma_check = False

        content = {}

        for i, char in enumerate(f):
            if at_key:
                if not parse_key:
                    if char != '"':
                        raise JSON_SyntaxError(f"Expected double quote character (\") while finding start of some key, found '{char}' instead.")
                    else:
                        parse_key = True
                elif parse_key:
                    if char != '"':
                        key += char
                    else:
                        at_key    = False
                        parse_key = False
                        semicolon_check = True
            elif semicolon_check:
                if char != ':':
                    raise JSON_SyntaxError(f"Expected ':' for key \"{key}\", found '{char}' instead.")
                else:
                    semicolon_check = False
                    at_value = True
                    
            elif at_value:
                if char == '[':
                    value_type = 
                elif char == '{':
                    value_type = 
                else:
                    value_type = 

        return content



test = JSON.parse('{"hello": "world", "foo": 4}')
print(test)


#foo = jsonreader.read(path)
#foo["hello"] = "world"
#jsonreader.write(foo, path)
