class InvalidDictError(Exception):

    def __init__(
        self,
        message: str,
        lineno: int = None,
        line: str = None,
        offset: int = None,
        *args: object
    ) -> None:
        super().__init__(*args)
        self.line = line
        self.lineno = lineno
        self.message = message
        self.offset = offset
