class Converter:
    def __init__(self, instructions):
        self.instructions = instructions
        self.binary_code = []
        self.hex_code = []

        self.opcode_dict = {
            'ADD': '00001',
            'SUB': '00010'
        }

    def convert(self):
        for instruction in self.instructions:
            binary_code = ''

            line = instruction.split(' ')
            operation = line[0]
            operation = self.opcode_dict[operation]
            arguments = line[1].split(',')

    def reg_to_binary(self, **kwargs):
        binary = []
        for i in kwargs.values():
            register = int(i.split('R')[1])

            if register > 15:
                print(f"There is no register such {register}\n")
