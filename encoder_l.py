
def convert(x,n):
  x=int(str(x),8)
  return(bin(x)[2:])

def convert_to_bits(input_string):
    output_bits = ""
    for char in input_string:
        char_bits = "{0:08b}".format(ord(char))
        output_bits += char_bits
    return output_bits

def convolutional_encode(input_data, constraint_length, polynomials):

    input_bits = [int(bit) for bit in input_data]
    shift_register = [0] * (constraint_length + 1)

    output_data = ""

    for bit in input_bits:
        shift_register = [bit] + shift_register[:-1]
        output_bit1 = 0
        for i in range(len(polynomials[0])):
          p=polynomials[0]
          if p[i] == '1':
            output_bit1 += shift_register[i]
        output_bit2 = 0
        for i in range(len(polynomials[1])):
          p=polynomials[1]
          if p[i] == '1':
            output_bit2 += shift_register[i]
        output_bit1 = output_bit1%2
        output_bit2 = output_bit2%2
        output_data += str(output_bit1) + str(output_bit2)

    shift_register = [0] * (constraint_length + 1)
    return output_data

if __name__ == "__main__":
    # Пример использования
    #st = "Hello World!"
    #input_data=convert_to_bits(st)
    input_data='10111'
    constraint_length = 2
    polynomials = ["7", "5"]
    polynomials2=[convert(polynomials[0],8),convert(polynomials[1],8)]
    encoded_data = convolutional_encode(input_data, constraint_length, polynomials2)
    print("Входная последовательность:", input_data)
    print("Закодированная последовательность:", encoded_data)

    encoded_data+=(constraint_length+1)*'0'
    # Записываем строки в файл
    with open("encoder_output.txt", "w", encoding="utf-8") as file:
        file.write("".join(encoded_data))