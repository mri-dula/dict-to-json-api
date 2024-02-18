class InvalidDictError(Exception):
    message: str
    lineno: int
    line: str

    def __init__(self, message: str, lineno: int, line: str, *args: object) -> None:
        super().__init__(*args)
        self.line = line
        self.lineno = lineno
        self.message = message
