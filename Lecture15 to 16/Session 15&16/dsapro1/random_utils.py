import random
import math
import numpy as np

def generate_random_numbers(count, lower, upper):
    return [random.randint(lower, upper) for _ in range(count)]

def analyze_numbers(numbers):
    return {
        "min": min(numbers),
        "max": max(numbers),
        "sum": sum(numbers),
        "mean": round(np.mean(numbers), 2),
        "std_dev": round(np.std(numbers), 2),
        "sqrt_sum": round(math.sqrt(sum(numbers)), 2)
    }
