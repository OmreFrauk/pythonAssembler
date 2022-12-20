from assembler import *


def main():
    assembler1 = Assembler("opcode.txt", "test")
    assembler1.read_ins()
    #print(assembler1.convert())


if __name__ == '__main__':
    main()

    print('clear')
