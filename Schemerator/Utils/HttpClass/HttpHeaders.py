from typing import List

from .HttpHeaderField import HttpHeaderField


class HttpHeaders:
    """ This class present HTTP header """
    def __init__(self, mjr_version: HttpHeaderField=None, min_version: HttpHeaderField=None, status: HttpHeaderField=None,
                 list_http_header_fields: List[HttpHeaderField]=None):
        """

        :param mjr_version: The major version of HTTP. for example in HTTP 1.2 is 1.
        :param min_version: The minor version of HTTP. for example in HTTP 1.2 is 2.
        :param status: Only for response. the status of response (for example "201 Created"). if None then this request.
        :param list_http_header_fields: list of HttpHeaderField objects that have in Header.
        """
        self.mjr_version = mjr_version
        self.min_version = min_version
        self.status = status

        # because Mutable default arguments.
        self.list_http_header_fields = list_http_header_fields or list()

    def __eq__(self, other):
        return vars(self) == vars(other)

    def __ne__(self, other):
        return vars(self) != vars(other)
