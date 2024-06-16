import re


_regex = re.compile(
    r'^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$'
)

def is_root_domain(domain: str) -> bool:
    """is_root_domain"""

    return re.match(_regex, domain) is not None