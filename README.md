#R86

A simplified x86-like architecture simulator built to go through assembly code from chapter 3 of CS:APP 2e.

Not finished yet, still working on procedure calling (`call` and `ret`).

##Usage

    > python3 Simulator.py -h
    usage: Simulator.py [-h] asm begin end

    positional arguments:
      asm         Assembly file
      begin       Memory allocated from
      end         Memory allocated to

##Example

    > python3 Simulator.py TestCase-Assembly/fact_do.asm 0 30
    INTEGER REGISTER
    eax = 120
    ecx = 0
    edx = 1
    ebx = 0
    esi = 0
    edi = 0
    esp = 12
    ebp = 12

    SPECIAL REGISTER
    eip = 12
    ZF = 1
    SF = 0

    SEGMENT REGISTER
    cs = 0
    ss = 0
    ds = 0

    LABEL TABLE
    {'.L2': 7}

    MEMORY
    [28]: 0
    [24]: 0
    [20]: 5
    [16]: 0
    [12]: 16
    [8]: 0
    [4]: 0
    [0]: 0

##Test case index

| Test case                 | in Assembly         | in Python
|:--                        |:--                  |:--
| sum (3.2.2)               | sum.asm
| simple (3.2.3)            | simple.asm
| exchange (3.4.3)          | exchange.asm
| load effective address (Prolbem 3.6)      | load_effective_address.asm
| unary and binary operations (Problem 3.7) | unary_binary_operations.asm
| arith (3.5.3)             | arith.asm
| compare (3.6.2)           | compare.asm
| jump (3.6.3)              | jump.asm
| absdiff (3.6.4)           | absdiff.asm
| test (Problem 3.18)       | 3-18-test.asm
| dw_loop (Problem 3.20)    | dw_loop.asm         | dw_loop.py
| fact_while (3.6.5)        | fact_while.asm      | fact_while.py
| loop_while (Problem 3.32) | loop_while.asm      | loop_while.py
| fun_a (Problem 3.22)      | fun_a.asm           | fun_a.py
| fact_for (3.6.5)          | fact_for.asm        | fact_for.py
| fun_b (Problem 3.23)      | fun_b.asm           | fun_b.py
| switch_eg (3.6.7)         | switch_eg.asm
| swicher (Problem 3.29)    | swicher.asm


##Specific

###Integer register

`eax`, `ecx`, `edx`, `ebx`, `esi`, `edi`, `esp`, `ebp`

###Special register
`eip`: Instruction pointer

`ZF`: Zero Flag. The most recent operation yielded zero.

`SF`: Sign Flag. The most recent operation yielded a negative value.


###Operand forms

| Type       | Form         | Operand value        | Name
|:-----------|:-------------|:---------------------|:-------------
| Immediate  | $Imm         | Imm                  | Immediate
| Register   | Ea           | R[Ea]                | Register
| Memory     | Imm          | M[Imm]               | Absolute
| Memory     | (Ea)         | M[R[Ea]]             | Indirect
| Memory     | Imm(Eb)      | M[Imm+R[Eb]]         | Base+displacement
| Memory     | (Eb,Ei)      | M[R[Eb]+R[Ei]]       | Indexed
| Memory     | Imm(Eb,Ei)   | M[Imm+R[Eb]+R[Ei]]   | Absolute
| Memory     | (,Ei,s)      | M[R[Ei]*s]           | Absolute
| Memory     | Imm(,Ei,s)   | M[Imm+R[Ei]*s]       | Absolute
| Memory     | (Eb,Ei,s)    | M[R[Eb]+R[Ei]*s]     | Absolute
| Memory     | Imm(Eb,Ei,s) | M[Imm+R[Eb]+R[Ei]*s] | Absolute

The scaling factor s must be either 1, 2, 4, or 8.

###Data movement instructions
| Instruction  | Effect                                | Description
|:--           |:--                                    |:--
| movl S,D     | D←S                                   | Move double word
| pushl S      | R[%esp] ← R[%esp]−4; M[R[%esp]] ← S   | Push double word
| popl D       | D ← M[R[%esp]]; R[%esp] ← R[%esp]+4   | Pop double word
                

###Integer arithmetic operations
| Instruction  | Effect     | Description
|:--           |:--         |:--
| leal S,D     | D ← &S     | Load effective address
| incl D       | D ← D + 1  | Increment
| decl D       | D ← D - 1  | Decrement
| negl D       | D ← -D     | Negate
| notl D       | D ← ~D     | Complement
| addl S,D     | D ← D + S  | Add
| subl S,D     | D ← D - S  | Subtract
| imull S,D    | D ← D * S  | Multiply
| xorl S,D     | D ← D ^ S  | Exclusive-or
| shl k,D      | D ← D << k | Left shift
| shr k,D      | D ← D >>L k| Logical right shift

###Comparison and test instructions

| Instruction | Based on  | Description
|:--          |:--        |:--
| cmpl S2, S1 | S1 - S2   | Compare double word
| testl S2, S1| S1 & S2   | Test double word

###The jump instructions

| Instruction | Jump  condition | Description
|:--          |:--              |:--
| jmp Label   | 1               | Direct jump
| jmp *Operand| 1               | Indirect jump
| je Label    | ZF              | Equal / zero
| jne Label   | ~ZF             | Not equal / not zero
| js Label    | SF              | Negative
| jns Label   | ~SF             | Nonnegative
| jg Label    | ~(SF ^ OF) & ~ZF| Greater (signed >)
| jge Label   |  ~(SF ^ OF)     | Greater or equal (signed >=)
| jl Label    | SF ^ OF         | Less (signed <)
| jle Label   | (SF ^ OF)       | ZF Less or equal (signed <=)


