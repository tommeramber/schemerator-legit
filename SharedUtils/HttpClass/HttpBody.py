class HttpBody:
    """ This class present HTTP body
        type_body can be JSON, XML etc
        and according to that the value change.
        now we work only with json body"""
    def __init__(self, type_body: str=None, value=None):
        """

        :param type_body: type_body can be JSON, XML etc.
        :param value: the body of request/response http.
        """
        self.type_body = type_body
        self.value = value

    def __eq__(self, other):
        return vars(self) == vars(other)

    def __ne__(self, other):
        return vars(self) != vars(other)

    def is_empty(self):
        return not self.type_body and not self.value
