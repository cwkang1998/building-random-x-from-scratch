from token import Token
from scanner import ScannerError, SimpleScanner


class Tokenizer:
    scanner = SimpleScanner()

    def tokenize(self, markdown):
        return self._tokens_as_array(markdown)

    def _tokens_as_array(self, markdown):
        if(not markdown):
            return [Token.end_of_file()]
        token = self._scan_one_token(markdown)
        return [token] + self._tokens_as_array(markdown[(token.length()):])

    def _scan_one_token(self, md_str) -> Token:
        token = self.scanner.from_string(md_str)
        if token:
            return token
        raise ScannerError(f'The scanners could not match the given input: {md_str}')
