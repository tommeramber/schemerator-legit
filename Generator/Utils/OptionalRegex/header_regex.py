# Here stored all the regex that they potential to be in headers,
# its important not add here regex that you not sure that need be here!
# The order of the regex is important!
# because in code he start from the beginning and want found the must explicit.

import re

HEADER_REGEXES_STRINGS = [
    # Example Date - "Mon, 06 aug 2018 06:59:57 GMT"
    r'^((Sun|Mon|Tue|Wed|Thu|Fri|Sat), [0-9]{1,2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (2016|2017|2018|2019|2020|2021|2022|2023|2024|2025|2026) [0-9]{2}:[0-9]{2}:[0-9]{2} (GMT|EST|PST|UTC))$',  # Date
    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',  # uuid
    r'^[a-f0-9]{32}$',  # id
    r'^[a-z0-9]{22}$',  # header
    r'^req-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',  # Request-Id
]

OPTIONAL_HEADER_REGEX = [re.compile(s) for s in HEADER_REGEXES_STRINGS]

