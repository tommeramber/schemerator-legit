class HttpHeaderField:
    """ This class present one http header

        might look like:
        type:numeric
        name:"content-length"
        value:3256

    """
    OPTIONAL_TYPES = ["numeric", "string"]

    def __init__(self, name: str=None, header_type: str=None, value=None):
        """

        :param name: The name of header (for example "Content-length").
        :param header_type: The type of header, can be only one of ["numeric", "string"].
        :param value: The value of header, can be number, string or list (according to header_type).
        """

        self.name = name
        self.header_type = header_type

        # if have value but don't have header_type.
        if header_type is None and value:
            if value.isdigit():
                self.header_type = "numeric"
            elif isinstance(value, str):
                self.header_type = "string"
            else:
                raise TypeError("HTTPHeader header_type can be only one of {}".format(HttpHeaderField.OPTIONAL_TYPES))

        if self.header_type == "numeric":
            self.value = int(value)
        else:
            self.value = value

    def __eq__(self, other):
        return vars(self) == vars(other)

    def __ne__(self, other):
        return vars(self) != vars(other)


