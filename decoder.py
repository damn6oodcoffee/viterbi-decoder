
MAX_INT = 1 << (32-1) - 1


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


class ViterbiDecoder:

    def __init__(self, constraint: int, polynomials: list[int]) -> None:
        self.polynomials = polynomials
        self.constraint = constraint
        self.states_count = (1 << (self.constraint - 1)) 
        self.parity_bits_count = len(self.polynomials)
        self.bits = None
        self.trellis = None
        self.outputs = None
        self.path_metrics = None
        self.decoded_bits = None
        self._init_outputs()

    def decode(self, bits: str) -> str:
        self.bits = bits
        self._compute_metrics()
        self._traceback()
        return self.decoded_bits

    def _init_outputs(self) -> None:
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

    def _branch_metric(self, 
                       current_bits: str, 
                       src_state: int, 
                       dest_state: int) -> int:
        # bit which caused src_state to transition to dest_state
        bit = (dest_state >> (self.constraint-2)) << (self.constraint - 1)
        encoder_input = src_state | bit
        return hamming_distance(current_bits, self.outputs[encoder_input])

    def _path_metric(self, 
                     current_bits: str, 
                     state: int) -> tuple[int, int]:
        # mask last len(state)-1 bits of the current state which were
        # the leading bits of the previous source states, shift the masked
        # bits to the left by 1 and then get the respective source states
        s = (state & ((1 << (self.constraint - 2)) - 1)) << 1
        src_state1 = s
        src_state2 = s | 1

        pm1 = self.path_metrics[src_state1]
        if pm1 < MAX_INT:
            pm1 += self._branch_metric(current_bits, src_state1, state)
        
        pm2 = self.path_metrics[src_state2]
        if pm2 < MAX_INT:
            pm2 += self._branch_metric(current_bits, src_state2, state)

        if pm1 <= pm2:
            return pm1, src_state1
        else:
            return pm2, src_state2

    def _update_path_metrics(self, current_bits: str) -> None:
        new_path_metrics = []
        new_trellis_column = []
        for state in range(self.states_count):
            pm, src_state = self._path_metric(current_bits, state)
            new_path_metrics.append(pm)
            new_trellis_column.append(src_state)
        self.path_metrics = new_path_metrics
        self.trellis.append(new_trellis_column)

    def _compute_metrics(self) -> None:
        self.path_metrics = []
        self.trellis = []
        for i in range(1 << (self.constraint-1)):
            self.path_metrics.append(MAX_INT)
        self.path_metrics[0] = 0

        for i in range(0, len(self.bits), self.parity_bits_count):
            if i + self.parity_bits_count >= len(self.bits):
                current_bits = self.bits[i:]
            else:
                current_bits = self.bits[i:i + self.parity_bits_count]

            while len(current_bits) < self.parity_bits_count:
                current_bits += "0"
            
            self._update_path_metrics(current_bits)
        print(self.path_metrics)
        print(self.trellis)

    def _min_path_metric_index(self) -> int:
        min_value = min(self.path_metrics)
        for i, v in enumerate(self.path_metrics):
            if v == min_value:
                return i

    def _traceback(self) -> None:
        decoded = ""
        state = self._min_path_metric_index()
        for i in range(len(self.trellis)-1, -1, -1):
            if state >> (self.constraint-2) == 1:
                decoded += "1"
            else:
                decoded += "0"
            state = self.trellis[i][state]
        decoded_reversed = decoded[::-1]
        cutoff_idx = len(decoded_reversed) - self.constraint + 1
        print(decoded_reversed)
        self.decoded_bits = decoded_reversed[:cutoff_idx]

    
    
if __name__ == "__main__":
    decoder = ViterbiDecoder(3, [7, 5])
    print(decoder.decode("1110000110"))
