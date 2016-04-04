;prepare
	movl $16, %ebp
	movl %ebp, %esp
	;set %ebp, %esp to 16
	movl $-3, %eax
	;set %eax to -3
	movl $7, %ecx
	;set %ecx to 7

;LoadEffectiveAddress:
	pushl %ebp
	movl %esp, %ebp

	leal 6(%eax), %edx
;	leal (%eax, %ecx), %edx
;	leal (%eax, %ecx, 4), %edx
;	leal 7(%eax, %eax, 8), %edx
;	leal 0xA(, %ecx, 4), %edx
;	leal 9(%eax, %ecx, 2), %edx

	popl %ebp