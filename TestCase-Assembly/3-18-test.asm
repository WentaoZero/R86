;prepare
	movl $16, %ebp
	movl %ebp, %esp
	;set %ebp, %esp to 16
	movl $2, 4(%ebp)
	;set x
	movl $9, 8(%ebp)
	;set y

;Test:
	pushl %ebp
	movl %esp, %ebp

	movl 8(%ebp), %eax
	movl 12(%ebp),%edx
	cmpl $-3, %eax
	jge .L2
	cmpl %edx, %eax
	jle .L3
	imull %edx, %eax
	jmp .L4

.L3:
	leal (%edx, %eax), %eax
	jmp .L4

.L2:
	cmpl $2, %eax
	jg .L5
	xorl %edx, %eax
	jmp .L4

.L5:
	subl %edx, %eax

.L4: