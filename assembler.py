from bitstring import Bits


class Converter:
    def __init__(self, instructions):
        self.instructions = instructions
        self.binary_code = []
        self.hex_code = []

        self.opcode_dict = {"ADD": "00001", "SUB": "00010"}

    def convert(self):
        for instruction in self.instructions:
            binary_code = ""

            line = instruction.split(" ")
            operation = line[0]
            operation = self.opcode_dict[operation]
            binary_code += operation
            arguments = line[1].split(",")
            if (
                operation == "ADD"
                or operation == "SUB"
                or operation == "AND"
                or operation == "OR"
                or operation == "XOR"
            ):  # they have same form
                dest = arguments[0]
                src_1 = arguments[1]
                src_2 = arguments[2]

                registers = self.reg_to_binary(dest=dest, src_1=src_1, src_2=src_2)
                binary_code += "".join(registers)
            if (
                operation == "ADDI"
                or operation == "SUBI"
                or operation == "ANDI"
                or operation == "ORI"
                or operation == "XORI"
            ):
                dest = arguments[0]
                src_1 = arguments[1]
                imm = arguments[2]
                registers = self.reg_to_binary(dest = dest, src_1= src_1)
                immediate = self.imm_to_binary(imm = imm)
                binary_code += ''.join(registers)
                binary_code += ''.join(immediate)



    @staticmethod
    def reg_to_binary(**kwargs):
        binary = []
        for i in kwargs.values():
            register = int(i.split("R")[1])

            if register > 15:
                print(f"There is no register such {register}\n")
                exit(-1)
            binary.append(str(bin(register))[2:].zfill(4))
        return binary

    def imm_to_binary(self, **kwargs):
        binary = []
        for i in kwargs.values():
            if int(i) < 0:
                sign_bit = "1"
                absolute = abs(int(i))
                bin_val = str(bin(absolute - 1))[2:].zfill(6)
                twos_comp = (
                    bin_val.replace("1", "%temp%")
                    .replace("0", "1")
                    .replace("%temp%", "0")
                )
                twos_comp = sign_bit + twos_comp
                binary.append("".join(twos_comp))
            else:
                sign_bit = "0"
                temp = str(bin(int(i)))[2:].zfill(6)
                temp = sign_bit + temp
                binary.append("".join(temp))
        return binary
