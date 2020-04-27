from typing import Optional
from optional_url_regex import OPTIONAL_URL_REGEX

def get_regex(string, regex_list) -> Optional[str]:
    """
    This function found regex of some string.
    by using list of optional regex pattern (that compiled before).

    :param string: string to found his regex.
    :param regex_list: list of optional regex.
    :return: The first regex that found for the url. or None if not found any regex.
    """
    for rg in regex_list:
        if rg.fullmatch(string):
            return rg.pattern

    return None


def get_regex_of_url(url: str) -> str:
    """
    This method found regex of url.

    :param url: the url for found regex of him.
    :return: regex of url.
    """
    url_regex = ""
    # Split the url for get explicit regex.
    # don't take the url parameters (after the sign '?')
    for url_part in url.split("?", 1)[0].split("/")[1:]:
        if url_part in get_regex_of_url.parts_that_found_regex_for_him:
            part_regex = get_regex_of_url.parts_that_found_regex_for_him[url_part]
        else:
            part_regex = get_regex(url_part, OPTIONAL_URL_REGEX)
            get_regex_of_url.parts_that_found_regex_for_him[url_part] = part_regex

        if not part_regex:
            url_regex += url_part
        else:
            url_regex += part_regex[1:-1]  # without the signs ^ and $
        url_regex += "/"

    # Append '^' in the beginning of regex.
    # But not add the sign '$' to the end because have also url param
    # And remove the last '\' because he is not needed.
    # url_regex = "^" + str(url_regex[:-1])
    # TODO: check if this is needed or not.
    # for now just remove the last '\'
    return url_regex[:-1]

get_regex_of_url.parts_that_found_regex_for_him = dict()