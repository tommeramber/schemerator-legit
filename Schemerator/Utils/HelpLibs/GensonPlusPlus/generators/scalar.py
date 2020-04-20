from .base import SchemaGenerator, TypedSchemaGenerator
from .MinMax import MinMax

from Utils.ConfigClass import GlobalConfig

from Utils.HelpLibs import regex_founder

import re


class Typeless(SchemaGenerator):
    """
    schema generator for schemas with no type. This is only used when
    there is no other active generator, and it will be merged into the
    first typed generator that gets added.
    """

    @classmethod
    def match_schema(cls, schema):
        return 'type' not in schema

    @classmethod
    def match_object(cls, obj):
        return False


class Null(TypedSchemaGenerator):
    """
    generator for null schemas
    """
    JS_TYPE = 'null'
    PYTHON_TYPE = type(None)


class Boolean(TypedSchemaGenerator):
    """
    generator for boolean schemas
    """
    JS_TYPE = 'boolean'
    PYTHON_TYPE = bool


class String(TypedSchemaGenerator):
    """
    generator for string schemas - works for ascii and unicode strings
    """
    JS_TYPE = 'string'
    PYTHON_TYPE = (str, type(u''))

    _ENGLISH_LETTERS = [chr(ascii_code) for ascii_code in range(ord('a'), ord('z') + 1)]
    _ENGLISH_LETTERS += [chr(ascii_code) for ascii_code in range(ord('A'), ord('Z') + 1)]
    _ENGLISH_LETTERS = set(_ENGLISH_LETTERS)
    _HEBREW_LETTERS = set([chr(ascii_code) for ascii_code in range(ord('א'), ord('ת') + 1)])
    _DIGITS = set([chr(ascii_code) for ascii_code in range(ord('0'), ord('9') + 1)])
    _MIN_OCCURRENCES_FOR_ONE_OPTION = 5
    _EXTRA_ITEM_WHEN_CREATE_NEW_OCCURRENCES = 2

    # Private methods
    def _get_characters_from_string(self, string_to_get_character_from_him: str):
        for character in string_to_get_character_from_him:
            if character in self._ENGLISH_LETTERS:
                self._char_list.update(self._ENGLISH_LETTERS)
            elif character in self._DIGITS:
                self._char_list.update(self._DIGITS)
            else:
                self._char_list.update(character)

    def _build_regex_from_list_of_chars(self):
        regex_string = ""
        is_english_letters = False
        is_hebrew_letters = False
        is_digits = False

        characters_not_in_groups = set()

        for character in self._char_list:
            if character in self._ENGLISH_LETTERS and not is_english_letters:
                regex_string += "a-zA-Z"
                is_english_letters = True
            if character in self._HEBREW_LETTERS and not is_hebrew_letters:
                regex_string += "ת-א"
                is_hebrew_letters = True
            if character in self._DIGITS and not is_digits:
                regex_string += "0-9"
                is_digits = True
            elif (character not in self._ENGLISH_LETTERS) and (character not in self._DIGITS):
                characters_not_in_groups.add(character)

        characters_not_in_groups = re.escape("".join(characters_not_in_groups))

        regex_string += "".join(characters_not_in_groups)

        regex_string = "[{}]".format(regex_string) if regex_string else "."

        return regex_string

    # this is not in __init__ because we want to do somethings in __init__ in SchemaGenerator Object before.
    def init(self):
        self._min_max_length = MinMax()
        self._char_list = set()
        self.pre_pattern = None
        self._optional_string_regex = None
        self._need_search_for_optional_regex = True

    def add_schema(self, schema):
        self._min_max_length.minimum = schema['minLength']
        self._min_max_length.maximum = schema['maxLength']

        if 'pattern' in schema:
            self.pre_pattern = schema['pattern']
            self._all_strings_are_match_pre_pattern = True

    def add_object(self, string):
        if self._need_search_for_optional_regex:
            if GlobalConfig.global_config.vars.OPTIONAL_JSON_SCHEMA_REGEXS:
                self._optional_string_regex = \
                    regex_founder.get_regex(string, GlobalConfig.global_config.vars.OPTIONAL_JSON_SCHEMA_REGEXS)
                self._need_search_for_optional_regex = False
        else:
            if self._optional_string_regex:
                if not re.fullmatch(self._optional_string_regex, string):
                    self._optional_string_regex = None

        self._min_max_length.append(len(string))

        self._get_characters_from_string(string_to_get_character_from_him=string)

        if self.pre_pattern and self._all_strings_are_match_pre_pattern:
            if not re.fullmatch(self.pre_pattern, string):
                self._all_strings_are_match_pre_pattern = False

    def to_schema(self):
        schema = super(String, self).to_schema()
        schema["minLength"] = self._min_max_length.minimum
        schema["maxLength"] = self._min_max_length.maximum

        if self._optional_string_regex:
            del schema["minLength"]
            del schema["maxLength"]
            string_regex = self._optional_string_regex
        else:
            string_regex = "^{}*$".format(self._build_regex_from_list_of_chars())

        if self.pre_pattern:
            if self._all_strings_are_match_pre_pattern:
                string_regex = self.pre_pattern
            else:
                string_regex = "{}|{}".format(self.pre_pattern, string_regex)

        schema['pattern'] = string_regex
        return schema


class Number(SchemaGenerator):
    """
    generator for integer and number schemas. It automatically
    converts from `integer` to `number` when a float object or a
    number schema is added
    """
    JS_TYPES = ('integer', 'number')
    PYTHON_TYPES = (int, float)

    @classmethod
    def match_schema(cls, schema):
        return schema.get('type') in cls.JS_TYPES

    @classmethod
    def match_object(cls, obj):
        return type(obj) in cls.PYTHON_TYPES

    def init(self):
        self._type = 'integer'
        self._min_max = MinMax()

    def add_schema(self, schema):
        self.add_extra_keywords(schema)
        if schema.get('type') == 'number':
            self._type = 'number'

        self._min_max.minimum = schema['minimum']
        self._min_max.maximum = schema['maximum']

    def add_object(self, obj):
        if isinstance(obj, float):
            self._type = 'number'
        self._min_max.append(obj)

    def to_schema(self):
        schema = super(Number, self).to_schema()
        schema['type'] = self._type
        schema["minimum"] = self._min_max.minimum
        schema["maximum"] = self._min_max.maximum
        return schema
