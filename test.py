import assembler
from assembler import *
def main():
    assembler1 = Converter.reg_to_binary(dest="R11",src_1="R12",src_2="R13")
    print(assembler1)
if __name__ == '__main__':
    main()

    print('clear')

