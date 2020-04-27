import re

# Here stored all the regex for urls, its important not add here regex that you not sure that need be here.
# The order of the regex is important, because in code he start from the beginning and want found the must explicit.
"""
OPTIONAL_URL_REGEX_STRINGS = [
    r'^([0-9a-f]){8}-([0-9a-f]){4}-([0-9a-f]){4}-([0-9a-f]){4}-([0-9a-f]){12}$',
    r'^[a-f0-9]{32}$',
    r'^v2$',
    r'^v3$',
    r'^v2.0$',
    r'^v2.1$',
    r'^([0-9a-f]){8}-([0-9a-f]){4}-([0-9a-f]){4}-([0-9a-f]){4}-([0-9a-f]){12}.json$',
    r'^[a-f0-9]{32}.json$'
]
"""

# a dumb regex to match student id
OPTIONAL_URL_REGEX_STRINGS = [
    r'^[0-9]$'
]

OPTIONAL_URL_REGEX = [re.compile(s) for s in OPTIONAL_URL_REGEX_STRINGS]