from encoder_l import convolutional_encode, convert
from decoder import ViterbiDecoder, hamming_distance




def main():
    input_data='101110010010101010111101011111'
    constraint_length = 2
    polynomials = [4, 5]
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
    encoded_data_from_file = "0100100110111101001101001000100010001001101011100010011010101111"
    decoded_data = decoder.decode(encoded_data_from_file)
    print("Декодированная последовательность: ", decoded_data)

    dist = hamming_distance(input_data, decoded_data)
    print("hamming distance: ", dist)

if __name__ == "__main__":
    main()