# Basic arithmetic calculations using x86 assembly wrapped in Python

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
