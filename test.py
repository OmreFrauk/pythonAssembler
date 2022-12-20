from assembler import *


def main():
    assembler1 = Assembler("opcode.txt", "output.txt")
    assembler1.start()
    #print(assembler1.convert())


if __name__ == '__main__':
    main()

    print('clear')
