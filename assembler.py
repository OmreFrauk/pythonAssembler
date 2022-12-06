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
