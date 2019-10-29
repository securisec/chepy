import itertools
from typing import List, Iterator, Any


def all_combinations_from_list(words: List[Any], length: int = None) -> Iterator[tuple]:
    """Creates all possible combinations from the `words` being passed. 
    Returns a generator. `length` controls the length of the permutations.
    
    Parameters
    ----------
    words : List[Any]
        List of strings.
    length : int, optional
        Length of permutations. By default, it is the length of the `words` list
    
    Returns
    -------
    Iterator[tuple]
        A generator containing tuples of combinations
    """
    if length is None:
        for L in range(0, len(words) + 1):
            for subset in itertools.permutations(words, L):
                yield subset
    else:
        for subset in itertools.permutations(words, length):
            yield subset
