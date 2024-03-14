from capstone import *
import subprocess
import sys
import os

def filter_instruction_bytes(assembly_code):
    md = Cs(CS_ARCH_X86, CS_MODE_64) # Inicializar el desensamblador
    
    filtered_instructions = []

    for instr in md.disasm(assembly_code, 0x1000):
        instruction_bytes = instr.bytes
        if len(instruction_bytes) > 2:
            instruction_bytes = instruction_bytes[:-1]
        if instr.mnemonic == 'jmp' or instr.mnemonic == 'call':
            instruction_bytes = instr.bytes[:1]
        filtered_instructions.append(instruction_bytes)
    
    # Convertir la lista de bytes de instrucción en una cadena de texto
    filtered_bytes_string = ''.join(''.join(f'{byte:02x}' for byte in instr_bytes) for instr_bytes in filtered_instructions)

    return filtered_bytes_string

def to_hex_format(input_hex):
    # Eliminar cualquier caracter de nueva línea de la entrada
    input_hex = input_hex.replace('\\n', '')
    
    # Añadir un 0 al final si la longitud de la entrada es impar
    if len(input_hex) % 2 != 0:
        input_hex = input_hex + '0'
    
    # Dividir la entrada en pares de caracteres
    pares_hex = [input_hex[i:i+2] for i in range(0, len(input_hex), 2)]
    
    # Convertir los pares de caracteres en bytes
    try:
        bytes_data = bytes.fromhex(''.join(pares_hex))
    except ValueError:
        print('-')
        sys.exit(1)

    return bytes_data

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <input_hex>')
        sys.exit(1)
    filename = sys.argv[1]
    if not os.path.isfile(filename):
        print(f'Error: {filename} does not exist')
        sys.exit(1)
        
    command = f"pedis --entrypoint -i 10 {filename} | cut -d' ' -f29-44 | od -c | cut -d' ' -f2- | tr -d '\n' | sed -e 's/ //g' -e 's/\\n//g'"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = process.communicate()
    input_hex = output.decode().strip()
    
    hex_data = to_hex_format(input_hex)
    filtered_bytes_string = filter_instruction_bytes(hex_data)
    
    print(filtered_bytes_string)    