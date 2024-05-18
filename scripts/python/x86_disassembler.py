#!/usr/bin/python3

import os
import re
import subprocess
import sys

NO_ARGUMENTS = ['27', '2f',
                '37', '3f',
                '60', '61', 
                '90', '98', '99', '9b', '9e', '9f', 
                'c3', 'c9', 'cb', 'cc', 'ce', 'cf', 
                'd6', 'd7',
                'f1', 'f5', 'f8', 'f9', 'fa', 'fb', 'fc', 'fd'] # 1 useful byte
TWO_BYTES_OPCODE = ['0f'] # 2 bytes instruction
EAX_IV = ['05', '0d',
          '15', '1d', 
          '25', '2d', 
          '35', '3d', 
          'a9', 'b8'] # 1 useful byte
EV_GV = ['01', '09',
         '11', '19', 
         '21', '29',
         '31', '39',
         '85', '87', '89'] # 2 useful bytes
GV_EV = ['03', '0b',
         '13', '1b',
         '23', '2b',
         '33', '3b',
         '8b'] # 2 useful bytes

EB_GB = ['00', '08',
         '10', '18',
         '20', '28',
         '30', '38', 
         '84', '86', '88'] # 2 useful bytes
GB_EB = ['02', '0a',
         '12', '1a',
         '22', '2a',
         '32', '3a',
         '8a'] # 2 useful bytes
AL_IB = ['04', '0c',
         '14', '1c',
         '24', '2c',
         '34', '3c',
         'a8',
         'b0', 
         'e4'] # 1 useful byte
ES = ['06', '07'] # 1 useful byte
CS = ['0e'] # 1 useful byte
SS = ['16', '17'] # 1 useful byte
DS = ['1e', '1f'] # 1 useful byte

EXTENDED_REGISTERS = ['50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '5a', '5b', '5c', '5d', '5e', '5f'] # 1 useful byte

SEGMENT_OVERRIDE = ['26', '2e',
                    '36', '3e', 
                    '64', '65'] # 1 useful byte
REX = ['40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '4a', '4b', '4c', '4d', '4e', '4f'] # 1 useful byte
OPERAND_SIZE_OVERRIDE = ['66'] # 1 useful byte
ADDRESS_SIZE_OVERRIDE = ['67'] # 1 useful byte
LOCK_REPNE_REPNZ = ['f0', 'f2', 'f3'] # 1 useful byte
EW_GW = ['63'] # 2 useful bytes
IV = ['68'] # 1 useful byte
GV_EV_IV = ['69'] # 1 useful byte
IB = ['6a',
      'cd',
      'd4', 'd5'] # 1 useful byte
GV_EV_IB = ['6b'] # 1 useful byte
YB_DX = ['6c'] # 1 useful byte
YZ_DX = ['6d'] # 1 useful byte
DX_XB = ['6e'] # 1 useful byte
DX_XV = ['6f'] # 1 useful byte
JB = ['70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '7a', '7b', '7c', '7d', '7e', '7f',
      'e0', 'e1', 'e2', 'e3', 'eb'] # 1 useful byte
EB_IB = ['80', '82',
         'c0', 'c6'] # 2 useful bytes
EV_IV = ['81',
         'c7'] # 2 useful bytes
EV_IB = ['83',
         'c1'] # 2 useful bytes
EW_SW = ['8c'] # 2 useful bytes
GV_M = ['8d'] # 1 useful bytes
SW_EW = ['8e'] # 2 useful bytes
EV = ['8f',
      'f7'] # 2 useful byte
EAX_ECX = ['91'] # 1 useful byte
EAX_EDX = ['92'] # 1 useful byte
EAX_EBX = ['93'] # 1 useful byte
EAX_ESP = ['94'] # 1 useful byte
EAX_EBP = ['95'] # 1 useful byte
EAX_ESI = ['96'] # 1 useful byte
EAX_EDI = ['97'] # 1 useful byte
AP = ['9a',
      'ea'] # 1 useful byte
FV = ['9c', '9d'] # 1 useful byte
AL_OB = ['a0'] # 1 useful byte
EAX_OV = ['a1'] # 1 useful byte
OB_AL = ['a2'] # 1 useful byte
OV_EAX = ['a3'] # 1 useful byte
XB_YB = ['a4', 'a6'] # 1 useful byte
XV_YV = ['a5', 'a7'] # 1 useful byte
YB_AL = ['aa'] # 1 useful byte
YV_EAX = ['ab'] # 1 useful byte
AL_XB = ['ac'] # 1 useful byte
EAX_XV = ['ad'] # 1 useful byte
AL_YB = ['ae'] # 1 useful byte
EAX_YV = ['af'] # 1 useful byte
CL_IB = ['b1'] # 1 useful byte
DL_IB = ['b2'] # 1 useful byte
BL_IB = ['b3'] # 1 useful byte
AH_IB = ['b4'] # 1 useful byte
CH_IB = ['b5'] # 1 useful byte
DH_IB = ['b6'] # 1 useful byte
BH_IB = ['b7'] # 1 useful byte
ECX_IV = ['b9'] # 1 useful byte
EDX_IV = ['ba'] # 1 useful byte
EBX_IV = ['bb'] # 1 useful byte
ESP_IV = ['bc'] # 1 useful byte
EBP_IV = ['bd'] # 1 useful byte
ESI_IV = ['be'] # 1 useful byte
EDI_IV = ['bf'] # 1 useful byte
IW = ['c2'] # 1 useful byte
GV_MP = ['c4', 'c5'] # 2 useful bytes
EB_1 = ['d0'] # 1 useful byte
EV_1 = ['d1'] # 1 useful byte
EB_CL = ['d2'] # 1 useful byte
EV_CL = ['d3'] # 1 useful byte
ESC = ['d8', 'd9', 'da', 'db', 'dc', 'dd', 'de', 'df'] # 1 useful byte
EAX_IB = ['e5'] # 1 useful byte
IB_AL = ['e6'] # 1 useful byte
IB_EAX = ['e7'] # 1 useful byte
JZ = ['e8', 'e9'] # 1 useful byte
AL_DX = ['ec'] # 1 useful byte
EAX_DX = ['ed'] # 1 useful byte
DX_AL = ['ee'] # 1 useful byte
DX_EAX = ['ef'] # 1 useful byte
EB = ['f6'] # 2 useful byte
INC_DEC = ['fe', 'ff'] # 2 useful byte


PREFIXES = SEGMENT_OVERRIDE + REX + OPERAND_SIZE_OVERRIDE + ADDRESS_SIZE_OVERRIDE + LOCK_REPNE_REPNZ 

ONE_USEFUL_BYTE = NO_ARGUMENTS + EAX_IV + AL_IB + ES + CS + SS + DS + EXTENDED_REGISTERS + SEGMENT_OVERRIDE + OPERAND_SIZE_OVERRIDE + ADDRESS_SIZE_OVERRIDE + LOCK_REPNE_REPNZ + IV + GV_EV_IV + IB + GV_EV_IB + YB_DX + YZ_DX + DX_XB + DX_XV + JB + GV_M + EAX_ECX + EAX_EDX + EAX_EBX + EAX_ESP + EAX_EBP + EAX_ESI + EAX_EDI + AP + FV + EAX_OV + OB_AL + OV_EAX + XB_YB + XV_YV + YB_AL + YV_EAX + AL_XB + EAX_XV + AL_IB + CL_IB + DL_IB + BL_IB + AH_IB + CH_IB + DH_IB + BH_IB + ECX_IV + EDX_IV + EBX_IV + ESP_IV + EBP_IV + ESI_IV + EDI_IV + IW + EB_1 + EV_1 + EB_CL + EV_CL + ESC + EAX_IB + IB_AL + IB_EAX + JZ + AL_DX + EAX_DX + DX_AL + DX_EAX
TWO_USEFUL_BYTES = TWO_BYTES_OPCODE + EV_GV + GV_EV + EB_GB + GB_EB + EW_GW + EB_IB + EV_IV + EV_IB + EW_SW + SW_EW + EV + GV_MP + EB + INC_DEC

def check_file_exists():
    """
    Check if a file exists.

    This function checks if a file exists based on the command line argument provided.
    If the file does not exist, it prints an error message and exits the program.

    Returns:
        str: The filename if it exists.

    Raises:
        SystemExit: If the command line argument is not provided or the file does not exist.
    """
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <input_file>')
        sys.exit(1)
    filename = sys.argv[1]
    if not os.path.isfile(filename):
        print(f'Error: {filename} does not exist')
        sys.exit(1)
    return filename

def get_bytes(filename):
    """
    Retrieves the bytes from a file using the 'pedis' command-line tool.

    Args:
        filename (str): The name of the file to retrieve bytes from.

    Returns:
        list: A list of bytes found in the file.
    """
    command = f"pedis --entrypoint -i 10 {filename}"
    output_pedis = subprocess.run(command, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
    regex = r"[0-9a-f]{3}:\s+((?:[0-9a-f]{2} ){1,8})\s+" 
    matches = re.findall(regex, output_pedis) # find all matches
    bytes_found = [match.rstrip().replace(' ', '') for match in matches] # remove unnecessary spaces and join the bytes
    
    return bytes_found

    
def parse_bytes(byte):
    """
    Parses a byte and returns the number of useful bytes it represents.

    Args:
        byte (int): The byte to be parsed.

    Returns:
        int: The number of useful bytes represented by the input byte.

    Raises:
        ValueError: If the byte is not found in any of the predefined lists.
    """
    if byte in TWO_USEFUL_BYTES:
        return 2
    elif byte in PREFIXES:
        return -1
    elif byte in ONE_USEFUL_BYTE: # Never gets here, already filtered
        return 1
    else:
        raise ValueError('Byte not found in any list')
  
def parse_instruction(instruction):
    """
    Parses the given instruction and prints the total bytes and useful bytes.

    Args:
        instruction (str): The instruction to be parsed.

    Raises:
        ValueError: If the instruction length is not valid.

    Returns:
        None
    """
    length = len(instruction)
    useful_bytes = ''
    if (length / 2) == 1: # One byte instruction / no arguments
        useful_bytes = instruction
    elif (length / 2) > 1:
        num_useful_bytes = parse_bytes(instruction[0:2])
        if num_useful_bytes == 1: # Useful part of the instruction is the first byte
            useful_bytes = instruction[0:2]
        elif num_useful_bytes == 2: # Useful part of the instruction is the first two bytes
            useful_bytes = instruction[0:4]
        elif num_useful_bytes == -1: # Prefix, need to take next byte
            num_useful_bytes = parse_bytes(instruction[2:4])
            if num_useful_bytes == -1:
                useful_bytes = instruction
            elif num_useful_bytes == 1:
                useful_bytes = instruction[0:4]
            elif num_useful_bytes == 2:
                useful_bytes = instruction[0:6]
    else:
        raise ValueError('Instruction length is not valid')
    return useful_bytes
          
def total_useful_bytes(filtered_instructions):
    """
    Concatenates the useful bytes from a list of filtered instructions.

    Args:
        filtered_instructions (list): A list of filtered instructions.

    Returns:
        str: A string containing the concatenated useful bytes.
    """
    useful_bytes = ''
    for instruction in filtered_instructions:
        useful_bytes += instruction
    return useful_bytes

if __name__ == '__main__':
    filename = check_file_exists()
        
    bytes_found = get_bytes(filename)
    num_instructions = len(bytes_found)
    useful_part_instructions = []
    
    for i in range(num_instructions):
        useful_part_instructions.append(parse_instruction(bytes_found[i]))
    print(total_useful_bytes(useful_part_instructions))