from .HttpHeaders import HttpHeaders
from .HttpBody import HttpBody


class Packet:
    """ This class present Packet"""
    def __init__(self, http_headers: HttpHeaders=None, http_body: HttpBody=None):
        """

        :param http_headers: HttpHeaders object.
        :param http_body:  HttpBody object.
        """
        self.http_headers = http_headers or HttpHeaders()
        self.http_body = http_body or HttpBody()

    def __eq__(self, other):
        return vars(self) == vars(other)

    def __ne__(self, other):
        return vars(self) != vars(other)
