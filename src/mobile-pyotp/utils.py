import unicodedata
from hmac import compare_digest


def strings_equal(s1: str, s2: str) -> bool:   # check 2 string equality
    """
    Timing-attack resistant string comparison.

    Normal comparison using == will short-circuit on the first mismatching
    character. This avoids that by scanning the whole string, though we
    still reveal to a timing attack whether the strings are the same
    length.
    """
    s1 = unicodedata.normalize('NFKC', s1)
    s2 = unicodedata.normalize('NFKC', s2)
    return compare_digest(s1.encode("utf-8"), s2.encode("utf-8"))
