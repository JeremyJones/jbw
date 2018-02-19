"""
routine for the variance using np's var method
"""
import numpy as np


def calculate_variance_npvar(price, prices) -> float:
    raise NotImplementedError
    return np.var(prices, ddof=1)
