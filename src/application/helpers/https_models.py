from typing import Dict, Any


class HttpRequest:
    """Class representing an HTTP request."""

    def __init__(self, header: Any = None, body: Any = None, query: Any = None):
        self.header = header
        self.body = body
        self.query = query

    def __repr__(self):
        return (
            f"HttpRequest (header={self.header}, body={self.body}, query={self.query})"
        )


class HttpResponse:
    """Class representing an HTTP response."""

    def __init__(self, status_code: int = None, body: Any = None):
        self.status_code = status_code
        self.body = body

    def __repr__(self):
        return f"HttpResponse (status_code={self.status_code}, body={self.body})"
