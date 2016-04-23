;prepare
	movl $16, %ebp
	movl %ebp, %esp
	;set %ebp, %esp to 16
	movl $3, 4(%ebp)
	;set a
	movl $19, 8(%ebp)
	;set b
	movl $37, 12(%ebp)
	;set c

;swicher:
	pushl %ebp
	movl %esp, %ebp

	movl 8(%ebp), %eax
	cmpl $7, %eax
	jg .L2
	jmp *.L7(, %eax, 4)

.L2:
	movl 12(%ebp), %eax
	jmp .L8

.L5:
	movl $4, %eax
	jmp .L8

.L6:
	movl 12(%ebp), %eax
	xorl $15, %eax
	movl %eax, 16(%ebp)

.L3:
	movl 16(%ebp), %eax
	addl $112, %eax
	jmp .L8

.L4:
	movl 16(%ebp), %eax
	addl 12(%ebp), %eax
	sall $2, %eax

.L8:

.L7:
	.long .L3
	.long .L2
	.long .L4
	.long .L2
	.long .L5
	.long .L6
	.long .L2
	.long .L4

	popl %ebp