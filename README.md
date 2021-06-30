# Basic arithmetic operations using x86 assembly wrapped in Python
A simple calculator implemented in Python, with arithmetics implemented in ASM x86 using unicorn CPU emulator library and keystone for assembling the ASM code in hexa machine code to emulate.
```assembly
Usage:   a +|-|*|/ b
Ex:      123*42
Exit:    exit
>> 2 * 42
   bytecode: b'\xb9\x00\x00\x00\x00\x83\xf8\x00t\x15\xa9\x01\x00\x00\x00u\x06\x01\xdb\xd1\xe8\xeb\xee\x01\xd9\x01\xdb\xd1\xe8\xeb\xe6'
   result: 84
>> 18927 / 67
   bytecode: b'\x89\xd9\xba\x00\x00\x00\x00\xf7\xf1\x89\xc1'
   result: 282
>> 
```

### Assembly arithmetic operations
```assembly
x86_ADD = """
mov ecx, eax
add ecx, ebx
"""
```


```assembly
"""
x86_SUB = """
    mov ecx, eax
    sub ecx, ebx
"""
```


```assembly
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
```

```assembly
x86_DIV = """
    mov ecx, ebx
    mov edx, 0
    div ecx
    mov ecx, eax
"""
```
