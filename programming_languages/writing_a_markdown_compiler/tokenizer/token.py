class InvalidTokenError(Exception):
    pass


class BaseToken:
    def null(self):
        raise NotImplementedError()

    def present(self):
        raise NotImplementedError()


class NullToken(BaseToken):
    is_null = True
    present = False


class Token(BaseToken):
    is_null = False
    present = True

    @staticmethod
    def null():
        return NullToken()

    @staticmethod
    def end_of_file():
        return Token(type='EOF', value='')

    def __init__(self, type, value) -> None:
        if type:
            self.type = type
            self.value = value
        else:
            raise InvalidTokenError()

    def length(self):
        return len(self.value)

    def __repr__(self) -> str:
        return f'<{self.type}, value: {self.value}>'
