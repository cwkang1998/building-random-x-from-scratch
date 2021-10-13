

from token import Token


SPECIAL_TOKEN = {
    '_': 'UNDERSCORE',
    '*': 'STAR',
    '\n': 'NEWLINE'
}


class ScannerError(Exception):
    pass


class SimpleScanner:
    def from_string(self, str_val):
        char = str_val[0]
        if char in SPECIAL_TOKEN.keys():
            return Token(type=SPECIAL_TOKEN[char], value=char)
        else:
            chars = ''
            for c in str_val:
                if(c in SPECIAL_TOKEN.keys()):
                    break
                chars = chars + c
            if chars:
                return Token('TEXT', chars)
            return Token.null()
