# Level2

This level is the same as before.

We go to the `/matrix/level1/` directory and disassemble the executable:

	level2@gracker:/matrix/level2$ gdb -q level2
	Reading symbols from level2...(no debugging symbols found)...done.
	(gdb) disas main
	Dump of assembler code for function main:
	   0x000000000040083d <+0>:	push   %rbp
	   0x000000000040083e <+1>:	mov    %rsp,%rbp
	   0x0000000000400841 <+4>:	push   %rbx
	   0x0000000000400842 <+5>:	sub    $0x48,%rsp
	   0x0000000000400846 <+9>:	mov    %edi,-0x44(%rbp)
	   0x0000000000400849 <+12>:	mov    %rsi,-0x50(%rbp)
	   0x000000000040084d <+16>:	mov    $0x4009b0,%edi
	   0x0000000000400852 <+21>:	callq  0x400620 <puts@plt>
	   0x0000000000400857 <+26>:	lea    -0x40(%rbp),%rax
	   0x000000000040085b <+30>:	mov    $0x20,%edx
	   0x0000000000400860 <+35>:	mov    %rax,%rsi
	   0x0000000000400863 <+38>:	mov    $0x0,%edi
	   0x0000000000400868 <+43>:	callq  0x4006a0 <read@plt>
	   0x000000000040086d <+48>:	movb   $0x0,-0x21(%rbp)
	   0x0000000000400871 <+52>:	lea    -0x40(%rbp),%rax
	   0x0000000000400875 <+56>:	mov    $0xa,%esi
	   0x000000000040087a <+61>:	mov    %rax,%rdi
	   0x000000000040087d <+64>:	callq  0x400670 <strchr@plt>
	   0x0000000000400882 <+69>:	mov    %rax,-0x20(%rbp)
	   0x0000000000400886 <+73>:	cmpq   $0x0,-0x20(%rbp)
	   0x000000000040088b <+78>:	je     0x400894 <main+87>
	   0x000000000040088d <+80>:	mov    -0x20(%rbp),%rax
	   0x0000000000400891 <+84>:	movb   $0x0,(%rax)
	   0x0000000000400894 <+87>:	movl   $0x0,-0x14(%rbp)
	   0x000000000040089b <+94>:	jmp    0x4008bd <main+128>
	   0x000000000040089d <+96>:	mov    -0x14(%rbp),%eax
	   0x00000000004008a0 <+99>:	cltq
	   0x00000000004008a2 <+101>:	movzbl -0x40(%rbp,%rax,1),%eax
	   0x00000000004008a7 <+106>:	movzbl 0x2005d2(%rip),%edx        # 0x600e80 <XORkey>
	   0x00000000004008ae <+113>:	xor    %eax,%edx
	   0x00000000004008b0 <+115>:	mov    -0x14(%rbp),%eax
	   0x00000000004008b3 <+118>:	cltq
	   0x00000000004008b5 <+120>:	mov    %dl,-0x40(%rbp,%rax,1)
	   0x00000000004008b9 <+124>:	addl   $0x1,-0x14(%rbp)
	   0x00000000004008bd <+128>:	mov    -0x14(%rbp),%eax
	   0x00000000004008c0 <+131>:	movslq %eax,%rbx
	   0x00000000004008c3 <+134>:	lea    -0x40(%rbp),%rax
	   0x00000000004008c7 <+138>:	mov    %rax,%rdi
	   0x00000000004008ca <+141>:	callq  0x400640 <strlen@plt>
	   0x00000000004008cf <+146>:	cmp    %rax,%rbx
	   0x00000000004008d2 <+149>:	jb     0x40089d <main+96>
	   0x00000000004008d4 <+151>:	lea    -0x40(%rbp),%rax
	   0x00000000004008d8 <+155>:	mov    $0x600e60,%esi
	   0x00000000004008dd <+160>:	mov    %rax,%rdi
	   0x00000000004008e0 <+163>:	callq  0x4006c0 <strcmp@plt>
	   0x00000000004008e5 <+168>:	test   %eax,%eax
	   0x00000000004008e7 <+170>:	jne    0x4008ff <main+194>
	   0x00000000004008e9 <+172>:	mov    $0x4009e0,%edi
	   0x00000000004008ee <+177>:	callq  0x400620 <puts@plt>
	   0x00000000004008f3 <+182>:	mov    $0x0,%eax
	   0x00000000004008f8 <+187>:	callq  0x4007e6 <spawn_shell>
	   0x00000000004008fd <+192>:	jmp    0x40090e <main+209>
	   0x00000000004008ff <+194>:	mov    $0x400a59,%edi
	   0x0000000000400904 <+199>:	mov    $0x0,%eax
	   0x0000000000400909 <+204>:	callq  0x400680 <printf@plt>
	   0x000000000040090e <+209>:	mov    $0x0,%eax
	   0x0000000000400913 <+214>:	add    $0x48,%rsp
	   0x0000000000400917 <+218>:	pop    %rbx
	---Type <return> to continue, or q <return> to quit---c
	   0x0000000000400918 <+219>:	pop    %rbp
	   0x0000000000400919 <+220>:	retq
	End of assembler dump.

Something with XOR in `<main+106>`:

	   0x00000000004008a7 <+106>:	movzbl 0x2005d2(%rip),%edx        # 0x600e80 <XORkey>

We set a breakpoint in `<main+163>` when the strcmp() function is called, and read the registers `$eax` and `$esi`:

	(gdb) x/8wx $rdi
	0x7fffffffeac0:	0x41414100	0x41414141	0x41414141	0x41414141
	0x7fffffffead0:	0x41414141	0x41414141	0x00000000	0x00000000
	(gdb) x/2s $esi
	0x600e60 <secret_password>:	")q6\036(2\036\065)p2\036)u\"*r3\036'q--q6(/&\036,r"
	0x600e80 <XORkey>:	"A"

Using the same script as before changing the secret_password we get:

	Password: h0w_is_th1s_h4ck3r_f0ll0wing_m3
	Ascii values: [104, 48, 119, 95, 105, 115, 95, 116, 104, 49, 115, 95, 104, 52, 99, 107, 51, 114, 95, 102, 48, 108, 108, 48, 119, 105, 110, 103, 95, 109, 51]

Usefull resources for this level (same as before):
+ [Wikipedia page for XOR cipher](https://en.wikipedia.org/wiki/XOR_cipher)
+ [StackOverflow question](https://stackoverflow.com/questions/29408173/byte-operations-xor-in-python)