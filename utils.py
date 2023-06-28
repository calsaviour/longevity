import numpy as np


def min_max_scale(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))
