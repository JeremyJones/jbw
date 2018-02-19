"""
return the variance from the requirements
"""
import numpy as np


def calculate_variance_reqs(price, prices) -> float:
    average = np.mean(prices)
    return price - average
