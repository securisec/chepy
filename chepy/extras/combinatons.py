import itertools
from typing import List, Any, Iterator


def generate_combo(
    words: List[Any], min_length: int = 0, max_length: int = None, join_by: str = None
) -> Iterator[tuple]:
    """Creates all possible combinations from the `words` being passed. 
    Returns a generator. `length` controls the length of the permutations.
    
    Args:
        words (List[Any]): List of strings.
        min_length (int, optional): Minimum length of permutations. By default, 0 which 
            will generate all
        max_length (int, optional): Maximum length of permutations. 
            By default, it is the length of the `words` list
    
    Returns:
        Iterator[tuple]: A generator containing tuples of combinations
    """
    if min_length > 0 and max_length is not None:
        for L in range(min_length, max_length + 1):
            for subset in itertools.permutations(words, L):
                yield join_by.join(subset) if join_by is not None else subset
    elif max_length is None:
        for L in range(min_length, len(words) + 1):
            for subset in itertools.permutations(words, L):
                yield join_by.join(subset) if join_by is not None else subset
    else:
        for subset in itertools.permutations(words, max_length):
            yield join_by.join(subset) if join_by is not None else subset


def hex_chars() -> list:
    """Returns an array of all the hex characters
    
    Returns:
        list: List of all hex characters
    """
    return list("{:02x}".format(x) for x in range(0, 256))

