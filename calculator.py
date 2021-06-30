from unicorn import Uc, UcError
from keystone import Ks, KS_ARCH_X86, KS_MODE_32, KsError
from unicorn.unicorn_const import UC_ARCH_X86, UC_MODE_32
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EBX, UC_X86_REG_ECX
import re
from typing import List

""" 
Compute a+b
    eax = a
    eax = b
"""
x86_ADD = """
    mov ecx, eax
    add ecx, ebx
"""

""" 
Compute a-b
    eax = a
    eax = b
"""
x86_SUB = """
    mov ecx, eax
    sub ecx, ebx
"""

""" 
Egyptian multiplication
Compute a*b
    eax = a
    eax = b
"""
x86_MUL = """
    mov ecx, 0
loop:
    cmp eax, 0
    je end
    
    test eax, 1
    jnz impair

    add ebx, ebx
    shr eax, 1
    jmp loop

impair:
    add ecx, ebx
    add ebx, ebx
    shr eax, 1
    jmp loop
    
end:

"""

""" 
Compute a/b
    eax = a
    eax = b
"""
x86_DIV = """
    mov ecx, ebx
    mov edx, 0
    div ecx
    mov ecx, eax
"""

""" 
Compute xor 2 bytes by 2 bytes along a 32bit string
    eax = string
"""
x86_CIPHER = """

"""

def run_loop():
    while True:
        inp = input('>> ')
        if inp == 'exit':
            break
        if not check_input(inp):
            log('Invalid syntax, retry', 'err')
            continue
        
        inp = parse_input(inp)
        operator, op1, op2 = inp[1], int(inp[0]), int(inp[2])
        if operator == '+':
            do_assembly(x86_ADD, op1, op2)
        if operator == '-':
            do_assembly(x86_SUB, op1, op2)
        if operator == '*':
            do_assembly(x86_MUL, op1, op2)
        if operator == '/':
            do_assembly(x86_DIV, op1, op2)

def do_assembly(x86_code: str, op1: int, op2: int):
    try:
        ks = Ks(KS_ARCH_X86, KS_MODE_32)
        x86_HEX, _ = ks.asm(x86_code)
        x86_HEX = bytes(x86_HEX)
        log(f"bytecode: {x86_HEX}")
    except KsError as e:
        log("Keystone Error: %s" % e, 'err')
        exit(1)

    ADDRESS = 0x1000000

    try:
        mu = Uc(UC_ARCH_X86, UC_MODE_32)
        mu.mem_map(ADDRESS, 2 * 1024 * 1024)
        mu.mem_write(ADDRESS, x86_HEX)
        mu.reg_write(UC_X86_REG_EAX, op1)
        mu.reg_write(UC_X86_REG_EBX, op2)
        mu.emu_start(ADDRESS, ADDRESS + len(x86_HEX))
        cx = mu.reg_read(UC_X86_REG_ECX)
        log(f"result: {cx}")
    except UcError as e:
        log("Unicorn Error: %s" % e, 'err')

def parse_input(inp: str) -> List[str]:
    symbols = re.compile('(\d+|[^ 0-9])')
    return re.findall(symbols, inp)

def check_input(inp: str):
    if ',' in inp or '.' in inp:
        return False
    inp = parse_input(inp)
    if len(inp) != 3 or not inp[0].isdigit() or not inp[2].isdigit():
        return False

    op1, op2 = int(inp[0]), int(inp[2])
    operator = inp[1]
    if operator == '-':
        valid = op2 <= op1
        if not valid:
            log('Can\'t compute a negative substraction', 'err')
        return valid
    if operator == '/':
        valid = op2 != 0
        if not valid:
            log('Can\'t divide by 0', 'err')
        return valid
    return True

def log(msg: str, level: str='msg'):
    CYAN = '\033[96m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    col = FAIL if level == 'err' else CYAN
    print(f'>> {col}{msg}{ENDC}')
   
if __name__ == '__main__':
    print('Usage:\t a +|-|*|/ b')
    print('Ex:\t 123*42')
    print('Exit:\t exit')
    run_loop()