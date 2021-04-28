from typing import List, Tuple

input_data_x_type = float
input_data_y_type = float
input_data_type = List [Tuple [input_data_x_type, input_data_y_type]]

class ZeroSlopeError (Exception): pass

def linear_regression (*, input_data: input_data_type):
    if not (len (input_data) > 1): raise Exception ("needs at least two input data points")
    # according to https://www.varsitytutors.com/hotmath/hotmath_help/topics/line-of-best-fit
    # mean of x-values and y-values
    input_data_length = len (input_data)
    x_mean = sum (point [0] for point in input_data) / input_data_length
    y_mean = sum (point [1] for point in input_data) / input_data_length
    slope = sum ((point [0] - x_mean) * (point [1] - y_mean) for point in input_data) / sum ((point [0] - x_mean) ** 2 for point in input_data)
    y_intercept = y_mean - (slope * x_mean)
    return slope, y_intercept

def find_y_for_x (*, input_data: input_data_type, x: input_data_x_type):
    slope, y_intercept = linear_regression (input_data = input_data)
    return (slope * x) + y_intercept

def find_x_for_y (*, input_data: input_data_type, y: input_data_y_type):
    slope, y_intercept = linear_regression (input_data = input_data)
    if slope == 0: raise ZeroSlopeError ("slope cannot be zero when finding x for y")
    return (y - y_intercept) / slope