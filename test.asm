	pushl %ebp
	movl %esp, %ebp
	movl 12(%ebp), %eax
	addl 8(%ebp), %eax
	popl %ebp


	Immediate $Imm          Imm                        Immediate
	Register  Ea            R[Ea]                      Register
	Memory    Imm           M[Imm]                     Absolute
	Memory    (Ea)          M[R[Ea]]                   Indirect
	Memory    Imm(Eb)       M[Imm + R[Eb]]             Base + displacement
	Memory    (Eb,Ei)       M[R[Eb]+ R[Ei]]            Indexed
Memory    Imm(Eb,Ei)    M[Imm + R[Eb]+ R[Ei]]      Indexed
Memory    (,Ei,s)       M[R[Ei] . s]               Scaled indexed
Memory    Imm(,Ei,s)    M[Imm + R[Ei] . s]         Scaled indexed
Memory    (Eb,Ei,s)     M[R[Eb]+ R[Ei] . s]        Scaled indexed
Memory    Imm(Eb,Ei,s)  M[Imm + R[Eb]+ R[Ei] . s]  Scaled indexed


		  S, D
	mov:
		movb movw movz
	movs:
		movsbw movsbl movswl
	movz:
		movzbw movzwl
	push:
		pushl popl

		D
	inc
	dec
	neg
	not

		S, D
	leal

	add
	sub
	imul
	xor
	or
	and
		k, D
	sal
	shl
	sar
	shr

	jump instruction:
	jmp Label
	jmp *Operand
		Label
	je
	jne
	Js
	jns
	jg
	jge
	jl
	jle
	ja
	jae
	jb
	jbe

	call Label
	call *Operand

	leave
	ret

OneOperandIns
TwoOperandIns
JumpIns
NoOperandIns




