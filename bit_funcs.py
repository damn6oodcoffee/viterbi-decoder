
def hamming_distance(x: str, y: str) -> int:
    distance = 0
    for cx, cy in zip(x, y):
        if cx != cy:
            distance += 1
    return distance 


def reverse_bits(bits_count, val) -> int:
    output = 0
    for i in range(bits_count-1, -1, -1):
        output = (output << 1) + (val & 1)
        val >>= 1
    return output
