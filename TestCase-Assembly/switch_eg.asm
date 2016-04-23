;prepare
	movl $16, %ebp
	movl %ebp, %esp
	;set %ebp, %esp to 16
	movl $7, 4(%ebp)
	;set x
	movl $102, 8(%ebp)
	;set n

;switch_eg:
	pushl %ebp
	movl %esp, %ebp

	movl 8(%ebp), %edx
	movl 12(%ebp), %eax

	subl $100, %eax
	cmpl $6, %eax
	jg .L2
	jmp *.L7(, %eax, 4)

.L2:
	movl $0, %eax
	jmp .L8

.L5:
	movl %edx, %eax
	jmp .L9

.L3:
	leal (%edx, %edx, 2), %eax
	leal (%edx, %eax, 4), %eax
	jmp .L8

.L4:
	leal 10(%edx), %eax
;fall through
.L9:
	addl $11, %eax
	jmp .L8

.L6:
	movl %edx, %eax
	imull %edx, %eax

.L8:

.L7:
	.long .L3
	.long .L2
	.long .L4
	.long .L5
	.long .L6
	.long .L2
	.long .L6

	popl %ebp