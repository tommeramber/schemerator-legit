from .MinMax import MinMax

import Utils.HelpLibs.regex_founder as regex_founder

from Utils.ConfigClass import GlobalConfig

import re
import math


class StringConfig:
    _ENGLISH_LETTERS = [chr(ascii_code) for ascii_code in range(ord('a'), ord('z') + 1)]
    _ENGLISH_LETTERS += [chr(ascii_code) for ascii_code in range(ord('A'), ord('Z') + 1)]
    _ENGLISH_LETTERS = set(_ENGLISH_LETTERS)
    _HEBREW_LETTERS = set([chr(ascii_code) for ascii_code in range(ord('א'), ord('ת') + 1)])
    _DIGITS = set([chr(ascii_code) for ascii_code in range(ord('0'), ord('9') + 1)])
    _MIN_OCCURRENCES_FOR_ONE_OPTION = 5
    _EXTRA_ITEM_WHEN_CREATE_NEW_OCCURRENCES = 2

    # when want to create enum then save in self._strings_in_header all the various strings and they occurrences
    # but we do not want to save more then _MAX_VARIOUS_STRINGS_FOR_CREATE_ENUM various option.
    _MAX_VARIOUS_STRINGS_FOR_CREATE_ENUM = 30

    def __init__(self,
                 list_optional_regexs=None,
                 string: str = None,
                 min_max=None,
                 regex=None,
                 enum: list = None,
                 occurrences: int = None):
        # Check if have optional regex for this string.
        """
        Constructor for StringConfig object.
        StringConfig represent string config in HTTP Config file.
        its can be Regex or Enum.


        :param list_optional_regexs: list of regex that maybe this regex is one of them.
                                     this help for found explicit regex and not only to try create new regex.
        :param string: when init for create Regex, then start with this string.
        :param min_max: when init for create Regex, then start with this minimum and maximum
        :param regex: an optional regex to start with him.
        :param enum: If initialize StringConfig from enum.
        :param occurrences: only when enum (param) is used.
        """
        self.pre_regex_from_user = regex
        self._optional_string_regex = None

        if GlobalConfig.global_config.vars.ADD_GROUPS_LETTERS_TO_REGEXS_IN_HEADERS:
            self._char_list = set()
        if GlobalConfig.global_config.vars.ADD_ENUMS_IN_HEADERS:
            self._strings_in_header = {}
            self._occurrences = 0
        if GlobalConfig.global_config.vars.ADD_LENGTH_TO_REGEX_IN_HEADERS:
            self.min_max = min_max or MinMax()
        if GlobalConfig.global_config.vars.ADD_ENUMS_IN_HEADERS:
            self.need_check_for_enum = True

        # Only when want to create new regex/enum
        if string:
            if list_optional_regexs:
                self._optional_string_regex = regex_founder.get_regex(string, list_optional_regexs)

            if GlobalConfig.global_config.vars.ADD_LENGTH_TO_REGEX_IN_HEADERS:
                string_len = len(string)
                self.min_max = min_max or MinMax(minimum=string_len, maximum=string_len)

            if GlobalConfig.global_config.vars.ADD_GROUPS_LETTERS_TO_REGEXS_IN_HEADERS:
                self._get_characters_from_string(string_to_get_character_from_him=string)

            if GlobalConfig.global_config.vars.ADD_ENUMS_IN_HEADERS:
                self.add_string_to_strings_in_header(string)
        # if have pre regex or pre enum (so string is None).
        elif regex:
            self._all_strings_are_match_pre_regex = True
        elif enum:
            for item in enum:
                self._strings_in_header[item] = self._MIN_OCCURRENCES_FOR_ONE_OPTION
            self._occurrences = \
                occurrences or (2 ** (len(enum) + self._EXTRA_ITEM_WHEN_CREATE_NEW_OCCURRENCES))

    def add_string_to_strings_in_header(self, value: str):
        self._occurrences += 1
        if value not in self._strings_in_header.keys():
            if len(self._strings_in_header.keys()) > self._MAX_VARIOUS_STRINGS_FOR_CREATE_ENUM:
                self.need_check_for_enum = False
            else:
                self._strings_in_header[value] = 1
        else:
            self._strings_in_header[value] += 1

    @property
    def string(self):
        """
        This method return string that represent the StringConfig.
        if have enum then it return something like that:
        "enum "Keep-Alive" "Close" "Other string"

        and if have regex then it return:
        "regex "some_regex..."

        :return: String that represent the regex/enum.
        """
        if self._optional_string_regex:
            return 'regex "{}"'.format(self._optional_string_regex)
        if self.pre_regex_from_user and self._all_strings_are_match_pre_regex:
            return 'regex "{}"'.format(self.pre_regex_from_user)

        # If not found regex from list of optional regex,
        # and also not have regex from user that match all pre regex.
        # then create the regex by regex of group _letters (if needed)
        # and also from length (if needed) or just accept any character.
        # and if can create enum (and user ask for this) then create enum.
        if GlobalConfig.global_config.vars.ADD_ENUMS_IN_HEADERS:
            if self.is_enum():
                # Return something like that:
                '''
                # occurrences 506
                enum "Keep-Alive" "Close" "Other string"
                '''
                return '# occurrences {}\n' \
                       'enum "{}"'.format(self._occurrences,
                                          '" "'.join(self._strings_in_header.keys()))

        return 'regex "{}"'.format(self._create_regex())

    def expand_integer_sizes(self):
        self.min_max.expand_integer_sizes()

    def append(self, string, string_len=None):
        if self._optional_string_regex:
            if not re.fullmatch(self._optional_string_regex, string):
                self._optional_string_regex = None

        if self.pre_regex_from_user and self._all_strings_are_match_pre_regex:
            if not re.fullmatch(self.pre_regex_from_user, string):
                self._all_strings_are_match_pre_regex = False

        if GlobalConfig.global_config.vars.ADD_LENGTH_TO_REGEX_IN_HEADERS:
            string_len = string_len or len(string)
            self.min_max.append(string_len)

        if GlobalConfig.global_config.vars.ADD_GROUPS_LETTERS_TO_REGEXS_IN_HEADERS:
            self._get_characters_from_string(string)

        if GlobalConfig.global_config.vars.ADD_ENUMS_IN_HEADERS:
            self.add_string_to_strings_in_header(string)
            self._occurrences += 1

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

    def is_enum(self):
        return (not self._optional_string_regex) and \
               (not (self.pre_regex_from_user and self._all_strings_are_match_pre_regex)) and \
               ((self._occurrences > 0) and
                (len(self._strings_in_header.keys()) <= math.log(self._occurrences, 2)) and
                (min(self._strings_in_header.values()) >= self._MIN_OCCURRENCES_FOR_ONE_OPTION))

    def get_regex(self):
        if self._optional_string_regex:
            return self._optional_string_regex
        if self.pre_regex_from_user and self._all_strings_are_match_pre_regex:
            return self.pre_regex_from_user

        return self._create_regex()

    def _create_regex(self):
        if GlobalConfig.global_config.vars.ADD_GROUPS_LETTERS_TO_REGEXS_IN_HEADERS:
            string_regex = self._build_regex_from_list_of_chars()
        else:
            # '.' in regex is Any single character.
            string_regex = "."

        if GlobalConfig.global_config.vars.ADD_LENGTH_TO_REGEX_IN_HEADERS:
            # Create regex that might look like ".{2,20}"
            string_regex = "{}{}{},{}{}".format(string_regex, "{", self.min_max.minimum, self.min_max.maximum, "}")
        else:
            # '*' Mean match zero or more consecutive of what have before.
            string_regex += "*"

        if self.pre_regex_from_user and not self._all_strings_are_match_pre_regex:
            string_regex = "{}|{}".format(self.pre_regex_from_user, string_regex)

        return string_regex

    def get_enum_options(self):
        return list(self._strings_in_header.keys())

    def __eq__(self, other):
        return vars(self) == vars(other)

    def __ne__(self, other):
        return vars(self) != vars(other)

