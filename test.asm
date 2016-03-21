	pushl %ebp
	movl %esp, %ebp
	movl 12(%ebp), %eax
	addl 8(%ebp), %eax
	popl %ebp


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




