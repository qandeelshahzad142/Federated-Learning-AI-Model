import numpy as np

def add_noise(weights, noise_level=0.01):
    return [w + np.random.normal(0, noise_level, w.shape) for w in weights]