class Assembler:
    def __init__(self, inputFile, output):
        self.inputFile = inputFile
        self.output = output
        self.instructions = None

    def read_ins(self):
        temp = []
        with open(self.inputFile, "r", encoding="UTF-8") as file:
            for line in file:
                temp.append(line.strip())
        self.instructions = temp

    def write_to_file(self, array):
        with open(self.output, 'w') as file:
            file.write("v2.0 raw \n")
            for line in array:
                file.write(line + "\t")

    def start(self):
        self.read_ins()
        conv = Converter(self.instructions)
        conv.convert()
        self.write_to_file(conv.hex_codes)


class Converter:
    def __init__(self, instructions):
        self.instructions = instructions
        self.binary_codes = []
        self.hex_codes = []

        self.opcode_dict = {
            "ADD": "00001",
            "SUB": "00010",
            "ADDI": "00011",
            "SUBI": "00100",
            "AND": "00101",
            "ANDI": "00110",
            "OR": "00111",
            "ORI": "01000",
            "XOR": "01001",
            "XORI": "01010",
            "LD": "01011",
            "ST": "01100",
            "JUMP": "01101",
            "PUSH": "01110",
            "POP": "01111",
            "BE": "10000",
            "BNE": "10001",
        }

    def convert(self):
        for instruction in self.instructions:
            binary_code = ""

            line = instruction.split(" ")
            operation = line[0]
            arguments = line[1].split(",")
            opcode = self.opcode_dict.get(operation)
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
                binary_code = opcode + binary_code + "000"

            elif (
                    operation == "ADDI"
                    or operation == "SUBI"
                    or operation == "ANDI"
                    or operation == "ORI"
                    or operation == "XORI"
            ):
                dest = arguments[0]
                src_1 = arguments[1]
                imm = arguments[2]
                registers = self.reg_to_binary(dest=dest, src_1=src_1)
                immediate = self.imm_to_binary(imm=imm)
                binary_code = opcode + "".join(registers) + "".join(immediate)

            elif operation == "LD":
                dest = arguments[0]
                address = arguments[1]
                registers = self.reg_to_binary(dest=dest)
                address = self.address_to_binary(10, address=address)
                binary_code = opcode + "".join(registers) + "".join(address) + "0"
            elif operation == "ST":
                src_1 = arguments[0]
                address = arguments[1]
                registers = self.reg_to_binary(src_1=src_1)
                address = self.address_to_binary(10, address=address)
                binary_code = opcode + "".join(registers) + "".join(address) + "0"
            elif operation == "JUMP":
                address = arguments[0]
                address = self.address_to_binary(10, address=address)
                binary_code = opcode + "".join(address) + "00000"
            elif operation == "PUSH" or operation == "POP":
                src_1 = arguments[0]
                registers = self.reg_to_binary(src_1=src_1)
                binary_code = opcode + "".join(registers) + "00000000000"
            elif operation == "BE" or operation == "BNE":
                src_1 = arguments[0]
                src_2 = arguments[1]
                addrs = arguments[2]
                registers = self.reg_to_binary(src_1=src_1, src_2=src_2)
                address = self.address_to_binary(7, addrs=addrs)
                binary_code = opcode + "".join(registers) + "".join(address)
            self.binary_codes.append(binary_code)
        self.binary_to_hex()

    def binary_to_hex(self):
        for binary in self.binary_codes:
            hexa = hex(int(binary, 2))
            self.hex_codes.append(hexa[2:].upper())
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

    @staticmethod
    def twos_complement(length, **kwargs):
        twos_comp = ""
        for i in kwargs.values():
            absolute = abs(int(i))
            bin_val = str(bin(absolute - 1))[2:].zfill(length)
            twos_comp = (
                bin_val.replace("1", "%temp%").replace("0", "1").replace("%temp%", "0")
            )
        return twos_comp

    @staticmethod
    def imm_to_binary(**kwargs):
        binary = []
        for i in kwargs.values():
            if int(i) < 0:
                sign_bit = "1"
                twos_comp = Converter.twos_complement(6, value=i)
                twos_comp = sign_bit + twos_comp
                binary.append("".join(twos_comp))
            else:
                sign_bit = "0"
                temp = str(bin(int(i)))[2:].zfill(6)
                temp = sign_bit + temp
                binary.append("".join(temp))
        return binary

    @staticmethod
    def address_to_binary(length, **kwargs):
        binary = []
        for i in kwargs.values():
            if int(i) >= 0:
                binary.append(str(bin(int(i)))[2:].zfill(length))
            else:
                sign_bit = "1"
                twos_comp = Converter.twos_complement(length - 1, value=i)
                twos_comp = sign_bit + twos_comp
                binary.append("".join(twos_comp))

        return binary
