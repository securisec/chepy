import collections
import math
from typing import Any


def shannon_entropy(data: Any, unit="shannon") -> float:
    """Calculate the Shannon entropy of any data type. Units 
    could be `natural`, `shannon` or `hartley`

    - 0 represents no randomness (i.e. all the bytes in the data have the same value) 
        whereas 8, the maximum, represents a completely random string.
    - Standard English text usually falls somewhere between 3.5 and 5.
    - Properly encrypted or compressed data of a reasonable length should have an entropy of over 7.5.

    Args:
        data (Any): Any data type
        unit (str, optional): Unit type. Defaults to "shannon".
    
    Returns:
        float: Calculated entropy
    """
    base = {"shannon": 2.0, "natural": math.exp(1), "hartley": 10.0}

    if len(data) <= 1:  # pragma: no cover
        return 0

    counts = collections.Counter()

    for d in data:
        counts[d] += 1

    ent = 0

    probs = [float(c) / len(data) for c in counts.values()]
    for p in probs:
        if p > 0.0:
            ent -= p * math.log(p, base[unit])

    return ent


def index_of_coincidence(data: Any) -> float:
    """Index of Coincidence (IC) is the probability of two randomly 
    selected characters being the same.

    - 0 represents complete randomness (all characters are unique), whereas 1 represents no randomness (all characters are identical).
    - English text generally has an IC of between 0.67 to 0.78.
    - 'Random' text is determined by the probability that each letter occurs the same number of times as another.

    `Reference <https://gist.github.com/enigmaticape/4254054>`__
    
    Args:
        data (Any): Any data type
    
    Returns:
        float: IC as float
    """
    cipher_flat = "".join([x.upper() for x in data.split() if x.isalpha()])

    N = len(cipher_flat)
    freqs = collections.Counter(cipher_flat)
    alphabet = map(chr, range(ord("A"), ord("Z") + 1))
    freqsum = 0.0

    for letter in alphabet:
        freqsum += freqs[letter] * (freqs[letter] - 1)

    try:
        IC = freqsum / (N * (N - 1))
    except ZeroDivisionError:
        IC = 0
        
    return IC
