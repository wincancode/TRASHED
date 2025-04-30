def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

def clamp_abs(value, max_value,treshold=0.001):

    if abs(value) < treshold:
        return 0.0

    return max(min(value, max_value), -max_value)