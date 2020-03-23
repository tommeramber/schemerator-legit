from .StringConfig import StringConfig


class HttpConfigHeaderField:
    """This class represent config of http header field.
    its might look like:

    name = "connection"
    validator_type = "regex"
    value = StringConfig or MinMax object
    required = False
    _occurrences = 1

    or

    name = "content-length"
    validator_type = "numeric"
    value = MinMax object(0,30000)
    required = False
    _occurrences = 1

    or something like that...

    """
    OPTIONAL_VALIDATOR_TYPE = ["regex", "numeric", "enum"]

    def __init__(self, name: str, value=None, required=False, occurrences=None):
        """

        :param name: the name of the allowed header to validate, e.g. status / url / content-length
        :param value: The value of header schema. can be MinMax object. or StringConfig object. according to validator_type.
        :param required: if True, this header is required.
        :param occurrences: maximum _occurrences of this header.
        """
        # Header names in HTTP Config must start with lower case.
        self.name = name.lower()
        self.value = value
        self.required = required
        self.occurrences = occurrences

    # Properties definitions.
    @property
    def validator_type(self) -> str:
        if isinstance(self.value, StringConfig):
            return "enum" if self.value.is_enum() else "regex"
        else:
            return "numeric"

    @property
    def required(self):
        return self._required

    @required.setter
    def required(self, val: bool):
        if isinstance(val, bool):
            self._required = val
        else:
            raise TypeError("HttpConfigHeaderField.required must be boolean.")

    @property
    def occurrences(self):
        return self._occurrences

    @occurrences.setter
    def occurrences(self, val: int):
        self._occurrences = int(val) if val else None

    def to_string(self):
        string_to_return = "{} ".format(self.name)
        string_to_return += "req " if self.required else ""
        string_to_return += "{} ".format(str(self.occurrences)) if self.occurrences else ""

        if self.validator_type == "numeric":
            string_to_return += 'numeric "{}" "{}"'.format(self.value.minimum, self.value.maximum)
        elif self.validator_type == "regex":
            string_to_return += '{}'.format(self.value.string)
        elif self.validator_type == "enum":
            # if this is enum then have "# occurrences" in self.value.string and we need take this to the first line.
            occurrences_that_create_enum, enum_val = self.value.string.split("\n")

            string_to_return = "{}\n{}{}".format(occurrences_that_create_enum, string_to_return, enum_val)

        string_to_return += "\n"

        return string_to_return

    def append_val(self, new_val):
        self.value.append(new_val)

    def __eq__(self, other):
        return vars(self) == vars(other)

    def __ne__(self, other):
        return vars(self) != vars(other)
