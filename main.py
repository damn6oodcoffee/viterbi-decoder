from encoder_l import convolutional_encode, convert
from decoder import ViterbiDecoder, hamming_distance
from encoder import ConvEncoder



def main_old():
    input_data='101110010010101010111101011111'
    constraint_length = 2
    polynomials = [4, 6]
    polynomials2=[convert(str(polynomials[0]),8),convert(str(polynomials[1]),8)]
    encoded_data = convolutional_encode(input_data, constraint_length, polynomials2)
    print("Входная последовательность:", input_data)
    print("Закодированная последовательность:", encoded_data)

    encoded_data+=(constraint_length+1)*'0'
    # Записываем строки в файл
    with open("encoder_output.txt", "w", encoding="utf-8") as file:
        file.write("".join(encoded_data))

    with open("encoder_output.txt", "r", encoding="utf-8") as file:
        encoded_data_from_file = file.read()
    encoded_data_from_file
    print("encoded_data_from_file: ", encoded_data_from_file)

    decoder = ViterbiDecoder(constraint_length+1, polynomials)
    decoded_data = decoder.decode(encoded_data_from_file)
    print("Декодированная последовательность: ", decoded_data)

    dist = hamming_distance(input_data, decoded_data)
    print("hamming distance: ", dist)


def main_coder():
    constr = 5
    poly = [8, 17, 7, 6]
    input_msg = "101010110111110101010111010111111001111111100011"
    coder = ConvEncoder(constr, [8, 17, 7, 1])
    encoded_msg = coder.encode(input_msg)
    decoder = ViterbiDecoder(constr, poly)
    decoded_msg = decoder.decode(encoded_msg)
    dist = hamming_distance(input_msg, decoded_msg)
    print(f"len(input) = {len(input_msg)}\n"
          f"len(encoded) = {len(encoded_msg)}\n"
          f"len(decoded) = {len(decoded_msg)}")
    print("hamming distance: ", dist)
    print(list(zip(input_msg, decoded_msg)))

def main_coder_test():
    input_msg = "101010110111110101010111010111111001111111100011"
    constr = 3
    poly = [3, 6]
    poly2=[convert(str(poly[0]),8),convert(str(poly[1]),8)]
    encoder = ConvEncoder(constr, poly)
    encoded_l = convolutional_encode(input_msg + '0'*(constr-1), constr-1, poly2)
    encoded = encoder.encode(input_msg)
    print(f"len(input) = {len(input_msg)}\n"
          f"len(encoded) = {len(encoded)}\n"
          f"len(encoded_l) = {len(encoded_l)}")
    dist = hamming_distance(encoded, encoded_l)
    print("hamming distance: ", dist)
    print(list(zip(encoded, encoded_l)))

    decoder = ViterbiDecoder(constr, poly)
    decoded = decoder.decode(encoded)
    decoded_l = decoder.decode(encoded_l)
    print("hamming distance: ", hamming_distance(input_msg, decoded))
    print("hamming distance_L: ", hamming_distance(input_msg, decoded_l))

def main():
    input_msg = "101010110111110101010111010111111001111111100011"
    constr = 4
    poly = [5, 7]

    if True:
        poly2=[convert(str(poly[0]),8),convert(str(poly[1]),8)]
        encoded = convolutional_encode(input_msg + '0'*(constr-1), constr-1, poly2)
    else:
        encoder = ConvEncoder(constr, poly)
        encoded = encoder.encode(input_msg)

    decoder = ViterbiDecoder(constr, poly)
    decoded = decoder.decode(encoded)
    dist = hamming_distance(input_msg, decoded)
    print("hamming distance: ", dist)
    print(list(zip(input_msg, decoded)))

if __name__ == "__main__":
    main()