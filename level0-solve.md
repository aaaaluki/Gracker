# Level0

For level 1 first we go to the website and see the source code (Ctrl+u)
   
```<!doctype html>
<html>
<head></head>
<body>
<h1>the journey begins...</h1>
<?php echo "asd"; ?>
<!--
`ssh level0@gracker.org`
password: level0
--!>
</body>
</html>
```

The hostname is the same as the web and the username:password are:
   `level0:level0`

Reading all the info on the home dir we found that the games are located in /matrix/<levelX>

For the first level we found an executable `level0`

If we runit with gdb (with silent mode):

	level0@gracker:/matrix/level0$ gdb -q ./level0
	Reading symbols from ./level0...(no debugging symbols found)...done.

Disassemble main as assembly code:

	(gdb) disas main
	Dump of assembler code for function main:
	   0x00000000004007ed <+0>:		push   %rbp
	   0x00000000004007ee <+1>:		mov    %rsp,%rbp
	   0x00000000004007f1 <+4>:		sub    $0x40,%rsp
	   0x00000000004007f5 <+8>:		mov    %edi,-0x34(%rbp)
	   0x00000000004007f8 <+11>:	mov    %rsi,-0x40(%rbp)
	   0x00000000004007fc <+15>:	mov    $0x400920,%edi
	   0x0000000000400801 <+20>:	callq  0x4005e0 <puts@plt>
	   0x0000000000400806 <+25>:	lea    -0x30(%rbp),%rax
	   0x000000000040080a <+29>:	mov    $0x20,%edx
	   0x000000000040080f <+34>:	mov    %rax,%rsi
	   0x0000000000400812 <+37>:	mov    $0x0,%edi
	   0x0000000000400817 <+42>:	callq  0x400650 <read@plt>
	   0x000000000040081c <+47>:	movb   $0x0,-0x11(%rbp)
	   0x0000000000400820 <+51>:	lea    -0x30(%rbp),%rax
	   0x0000000000400824 <+55>:	mov    $0xa,%esi
	   0x0000000000400829 <+60>:	mov    %rax,%rdi
	   0x000000000040082c <+63>:	callq  0x400620 <strchr@plt>
	   0x0000000000400831 <+68>:	mov    %rax,-0x8(%rbp)
	   0x0000000000400835 <+72>:	cmpq   $0x0,-0x8(%rbp)
	   0x000000000040083a <+77>:	je     0x400843 <main+86>
	   0x000000000040083c <+79>:	mov    -0x8(%rbp),%rax
	   0x0000000000400840 <+83>:	movb   $0x0,(%rax)
	   0x0000000000400843 <+86>:	lea    -0x30(%rbp),%rax
	   0x0000000000400847 <+90>:	mov    $0x600df0,%esi
	   0x000000000040084c <+95>:	mov    %rax,%rdi
	   0x000000000040084f <+98>:	callq  0x400670 <strcmp@plt>
	   0x0000000000400854 <+103>:	test   %eax,%eax
	   0x0000000000400856 <+105>:	jne    0x40086e <main+129>
	   0x0000000000400858 <+107>:	mov    $0x4009a0,%edi
	   0x000000000040085d <+112>:	callq  0x4005e0 <puts@plt>
	   0x0000000000400862 <+117>:	mov    $0x0,%eax
	   0x0000000000400867 <+122>:	callq  0x400796 <spawn_shell>
	   0x000000000040086c <+127>:	jmp    0x40087d <main+144>
	   0x000000000040086e <+129>:	mov    $0x400a19,%edi
	   0x0000000000400873 <+134>:	mov    $0x0,%eax
	   0x0000000000400878 <+139>:	callq  0x400630 <printf@plt>
	   0x000000000040087d <+144>:	mov    $0x0,%eax
	   0x0000000000400882 <+149>:	leaveq
	   0x0000000000400883 <+150>:	retq
	End of assembler dump.

At location <main+98> the function strcmp is called, this function compares strings, so it's likely that this is used to check if the password is correct. So we set a breakpoint there, and we run it.

	(gdb) b *main+98
	Breakpoint 1 at 0x40084f
	(gdb) r
	Starting program: /matrix/level0/level0
	 _____
	| _ _ |
	|| | || Hidden
	||_|_||   Backdoor
	| _ _ o  by
	|| | ||     ~Zero Cool
	||_|_||
	|_____|

	Enter Secret Password:
	AAAAAAAAAAAAAAAAAAAAAAAAA

Enter an easy password to recognize in hex A=0x41

We read what is stored in register $esi:

	Breakpoint 1, 0x000000000040084f in main ()
	(gdb) x/32wx $esi
	0x600df0 <secret_password>:	0x72633373	0x625f7433	0x646b6361	0x5f723030
	0x600e00 <secret_password+16>:	0x73736170	0x64723077	0x00000000	0x00000000
	0x600e10:	0x00000000	0x00000000	0x00000000	0x00000000
	0x600e20:	0x00000000	0x00000000	0x00000000	0x00000000
	0x600e30:	0x00000000	0x00000000	0x00000000	0x00000000
	0x600e40:	0x00000000	0x00000000	0x00000000	0x00000000
	0x600e50:	0x00000000	0x00000000	0x00000000	0x00000000
	0x600e60:	0x00000000	0x00000000	0x00000000	0x00000000

There it's the secret password, to show it as a string run the following

	(gdb) x/s $esi
	0x600df0 <secret_password>:	"s3cr3t_backd00r_passw0rd"


Usefull resources for this level:
+ [x command for gdb](https://visualgdb.com/gdbreference/commands/x)