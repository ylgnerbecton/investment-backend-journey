from http import HTTPStatus


class GenericError(Exception):
    def __init__(self, code=None, message=None):
        self.code = code if code else HTTPStatus.UNPROCESSABLE_ENTITY
        self.description = message if message else "An error occurred."

    def __str__(self):
        return f"GenericError(code={self.code}, description={self.description})"


class NotFoundError(Exception):
    def __init__(self, message=None):
        self.code = HTTPStatus.NOT_FOUND
        self.description = message if message else f"was not found."

    def __str__(self):
        return f"NotFoundError(code={self.code}, description={self.description})"
