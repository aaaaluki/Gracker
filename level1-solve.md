# Level1

Same as before, we go to the `/matrix/level1/` directory and disassemble the executable:

	level1@gracker:/matrix/level1$ gdb -q level1
	Reading symbols from level1...(no debugging symbols found)...done.
	(gdb) disas mian
	No symbol table is loaded.  Use the "file" command.
	(gdb) disas main
	Dump of assembler code for function main:
	   0x000000000040083d <+0>:		push   %rbp
	   0x000000000040083e <+1>:		mov    %rsp,%rbp
	   0x0000000000400841 <+4>:		push   %rbx
	   0x0000000000400842 <+5>:		sub    $0x48,%rsp
	   0x0000000000400846 <+9>:		mov    %edi,-0x44(%rbp)
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
	   0x000000000040089b <+94>:	jmp    0x4008c1 <main+132>
	   0x000000000040089d <+96>:	mov    -0x14(%rbp),%eax
	   0x00000000004008a0 <+99>:	cltq
	   0x00000000004008a2 <+101>:	movzbl 0x600e40(%rax),%eax
	   0x00000000004008a9 <+108>:	movzbl 0x2005ad(%rip),%edx        # 0x600e5d <XORkey>
	   0x00000000004008b0 <+115>:	xor    %eax,%edx
	   0x00000000004008b2 <+117>:	mov    -0x14(%rbp),%eax
	   0x00000000004008b5 <+120>:	cltq
	   0x00000000004008b7 <+122>:	mov    %dl,0x600e40(%rax)
	   0x00000000004008bd <+128>:	addl   $0x1,-0x14(%rbp)
	   0x00000000004008c1 <+132>:	mov    -0x14(%rbp),%eax
	   0x00000000004008c4 <+135>:	movslq %eax,%rbx
	   0x00000000004008c7 <+138>:	mov    $0x600e40,%edi
	   0x00000000004008cc <+143>:	callq  0x400640 <strlen@plt>
	   0x00000000004008d1 <+148>:	cmp    %rax,%rbx
	   0x00000000004008d4 <+151>:	jb     0x40089d <main+96>
	   0x00000000004008d6 <+153>:	lea    -0x40(%rbp),%rax
	   0x00000000004008da <+157>:	mov    $0x600e40,%esi
	   0x00000000004008df <+162>:	mov    %rax,%rdi
	   0x00000000004008e2 <+165>:	callq  0x4006c0 <strcmp@plt>
	   0x00000000004008e7 <+170>:	test   %eax,%eax
	   0x00000000004008e9 <+172>:	jne    0x400901 <main+196>
	   0x00000000004008eb <+174>:	mov    $0x4009e0,%edi
	   0x00000000004008f0 <+179>:	callq  0x400620 <puts@plt>
	   0x00000000004008f5 <+184>:	mov    $0x0,%eax
	   0x00000000004008fa <+189>:	callq  0x4007e6 <spawn_shell>
	   0x00000000004008ff <+194>:	jmp    0x400910 <main+211>
	   0x0000000000400901 <+196>:	mov    $0x400a59,%edi
	   0x0000000000400906 <+201>:	mov    $0x0,%eax
	   0x000000000040090b <+206>:	callq  0x400680 <printf@plt>
	   0x0000000000400910 <+211>:	mov    $0x0,%eax
	   0x0000000000400915 <+216>:	add    $0x48,%rsp
	   0x0000000000400919 <+220>:	pop    %rbx
	   0x000000000040091a <+221>:	pop    %rbp
	---Type <return> to continue, or q <return> to quit---
	   0x000000000040091b <+222>:	retq
	End of assembler dump.

As it we can see in `<main+108>` the password is XORed with a key. if we go to the registers for this values:

	0x00000000004008a9 <+108>:	movzbl 0x2005ad(%rip),%edx        # 0x600e5d <XORkey>


	(gdb) x/s 0x600e40
	0x600e40 <secret_password>:	"/q#q%8\036&4r22$2\036\065)(t\036\061 226q3%"
	(gdb) x/s 0x600e5d
	0x600e5d <XORkey>:	"A"

Now we just have to decode he encoded password with the given key:

	#!/usr/bin/env python3

	from itertools import cycle

	encrypted = '/q#q%8\036&4r22$2\036\065)(t\036\061 226q3%'
	key = 'A'

	encoding = 'utf-8'

	decrypted = [e ^ k for (e, k) in zip(bytes(encrypted, encoding), cycle(bytes(key, encoding)))]
	password = ''.join([chr(i) for i in decrypted])

	print(f'Password: {password}\nAscii values: {decrypted}')

And we get the decoded password:

	Password: n0b0dy_gu3sses_thi5_passw0rd
	Ascii values: [110, 48, 98, 48, 100, 121, 95, 103, 117, 51, 115, 115, 101, 115, 95, 116, 104, 105, 53, 95, 112, 97, 115, 115, 119, 48, 114, 100]

Usefull resources for this level:
+ [Wikipedia page for XOR cipher](https://en.wikipedia.org/wiki/XOR_cipher)
+ [StackOverflow question](https://stackoverflow.com/questions/29408173/byte-operations-xor-in-python)
