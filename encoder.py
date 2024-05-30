from bit_funcs import reverse_bits

class ConvEncoder:

    def __init__(self, constraint: int, polynomials: list[int]) -> None:
        self.polynomials = polynomials
        self.constraint = constraint
        self.parity_bits_count = len(self.polynomials)
        self.outputs = None
        self._init_outputs()

    def encode(self, bits: str) -> str:
        state = 0
        bits += '0' * (self.constraint-1)
        encoded_bits = ""

        for b in bits:
            encoder_input = state | (int(b) << (self.constraint-1))
            encoded_bits += self.outputs[encoder_input]
            state = (state >> 1) | (int(b) << (self.constraint-2))
        
        return encoded_bits

    def _init_outputs(self):
         # pre-compute encoder outputs from all possible inputs
        self.outputs = []
        encoder_inputs_count = 1 << self.constraint
        for i in range(encoder_inputs_count):
            self.outputs.append("")
            for j in range(self.parity_bits_count):
                polynomial = reverse_bits(self.constraint, self.polynomials[j])
                encoder_input = i
                output = 0
                for k in range(self.constraint):
                    output ^= (encoder_input & 1) & (polynomial & 1)
                    polynomial >>= 1
                    encoder_input >>= 1
                if output == 1:
                    self.outputs[i] += "1"
                else:
                    self.outputs[i] += "0"
        print(self.outputs)