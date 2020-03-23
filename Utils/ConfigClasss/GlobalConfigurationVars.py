class GlobalConfigurationVars:
    INPUT_PCAP_PATH = ""
    OUTPUT_FOLDER_PATH = "res_folder"
    PRE_SCHEMAS_FOLDER = None
    GENERATE_JSON_SCHEMAS = True
    GENERATE_HTTP_CONFIG = True
    EXPAND_SIZES_IN_HTTP_CONFIG = True
    ADD_REQUIRED_IN_JSON_SCHEMA = True

    OPTIONAL_URL_REGEXS = []
    OPTIONAL_HEADER_REGEXS = []
    OPTIONAL_JSON_SCHEMA_REGEXS = []

    # Configuration for create regex for headers.
    ADD_LENGTH_TO_REGEX_IN_HEADERS = True
    ADD_GROUPS_LETTERS_TO_REGEXS_IN_HEADERS = True
    ADD_ENUMS_IN_HEADERS = True