import random


def generate_binary_string(length):
    binary_string = ""
    for _ in range(length):
        binary_string += str(random.randint(0, 1))
    return binary_string
