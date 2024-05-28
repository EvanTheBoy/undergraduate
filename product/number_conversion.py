import numpy as np


def binary_to_decimal(binary_str):
    decimal_value = 0
    power = len(binary_str) - 1

    for digit in binary_str:
        decimal_value += int(digit) * (2 ** power)
        power -= 1

    return decimal_value


def decimal_to_binary(decimal_value, length):
    if decimal_value == 0:
        return "0" * int(length)

    binary_str = ""
    while decimal_value > 0:
        remainder = decimal_value % 2
        binary_str = str(remainder) + binary_str
        decimal_value //= 2

    padding_length = max(length - len(binary_str), 0)
    return "0" * int(padding_length) + binary_str
