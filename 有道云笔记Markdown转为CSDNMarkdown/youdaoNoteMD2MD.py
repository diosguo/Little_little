import re
import sys

def main(file_to_process, file_to_save):
    fin = open(file_to_process,'r')
    fou = open(file_to_save,'w')
    math_block = False
    for line in fin:
        line = line.replace('`$','$')
        line = line.replace('$`','$')
        if '```math' in line:
            line = line.replace('```math','$$')
            math_block = True
        if '```' in line and math_block is True:
            print(line)
            math_block = False
            line = line.replace('```','$$')
        fou.write(line)

    fin.close()
    fou.close()





if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])