"""REGEX GEN """
import string
import sys

m = 4
loop = 10

"""MISMATCH AND BULGE"""
""" generates lists of possible bulges and mismatches for g-stack of (3:n) height"""
bulge = []
mm = []
for a in range (3,m+1):
    tab = []
    tb = []
    tm = []
    for x in range(a):
        tab.append("[gG]")
    for x in range(a-1):
        tb.append("".join(tab[0:x+1])+'\w'+"".join(tab[x+1:m]))
    bulge.append(tb)
    for x in range(a-2):
        tm.append("".join(tab[0:x+1])+'\w'+"".join(tab[x+2:m]))
    mm.append(tm)

print "BULGE: \n" + str(bulge)
print "MISMATCH: \n" + str(mm)
"""*******************************"""

"""CANONICAL"""
""" generates a list of canonical gq's for (3:n) stacks, with (1:loop) loop length"""
final = []
for x in range (3,m+1):
    temp = []
    tf = []
    for n in range(3):
        for a in range(x):
            temp.append("[gG]")    
        tf.append("".join(temp))
        tf.append("\w{1, %d}"%loop)
        temp = []
    for a in range(x):
        temp.append("[gG]")
    tf.append("".join(temp))
    final.append(tf)
print "CANONICAL"
for i in final:
    print str(i)+"\n"
"""*********************"""

"""REGEX DICT"""
"""generates a dictionary of all possible gq's (settings as in canonical), either perfect or with one imperfection"""
"""
key:value
seq: regex
g_type: perfect/imperfect
s_type: bulge/mismatch ; empty if g_type == perfect
im_stack: no. of stack with imperfection (5' -> 3'); empty if g_type == perfect
mm_n: position of mismatch, according to the pattern:
5'-G-G-G-G-...3'
     1 2   ...
bg_n: position of a bulge, according to the pattern:
5'-G-G-G-...3'
    1 2
strand: +/-
"""
regex = []
temp_rev = []
intab="gG"
outtab="cC"
transtab = string.maketrans(intab, outtab)
for i in final:
    regex.append({"seq":"".join(i), 'g_type':'perfect', 's_type':"", 'mm_n':"", 'bg_n':"", 'strand':'+'})
    temp_rev = str(i).translate(transtab)
    regex.append({"seq":"".join(temp_rev), 'g_type':'perfect', 's_type':"", 'mm_n':"", 'bg_n':"", 'strand':'-'})
for i, j in enumerate(final):
    for x, y in enumerate(bulge[i]):
        for k,l in enumerate(j):
            temp = []
            temp_rev = []
            if k%2==0:
                for m,n in enumerate(j):
                    if m%2==0:
                        if m==k:
                            temp.append(y)
                        else:
                            temp.append(n)
                    else:
                        temp.append(n)                
                regex.append({"seq":"".join(temp), 'g_type':'imperfect', 's_type':"bulge", 'im_stack':"%d"%((k/2)+1), 'mm_n':"", 'bg_n':"%d"%(x+1), 'strand':'+'})
                temp_rev = str(temp).translate(transtab)
                regex.append({"seq":"".join(temp_rev), 'g_type':'imperfect', 's_type':"bulge", 'im_stack':"%d"%((len(j)/2)-(k/2)+1), 'mm_n':"", 'bg_n':"%d"%(len(bulge[i])-x), 'strand':'-'})
    for x, y in enumerate(mm[i]):
        for k,l in enumerate(j):
            temp = []
            temp_rev = []
            if k%2==0:
                for m,n in enumerate(j):
                    if m%2==0:
                        if m==k:
                            temp.append(y)
                        else:
                            temp.append(n)
                    else:
                        temp.append(n)
                regex.append({"seq":"".join(temp), 'g_type':'imperfect', 's_type':"mismatch", 'im_stack':"%d"%((k/2)+1), 'mm_n':"%d"%(x+1), 'bg_n':"", 'strand':'+'})
                temp_rev = str(temp).translate(transtab)
                regex.append({"seq":"".join(temp_rev), 'g_type':'imperfect', 's_type':"mismatch", 'im_stack':"%d"%(len(j)/2-(k/2)+1), 'mm_n':"%d"%(len(bulge[i])-x-1), 'bg_n':"", 'strand':'-'})

        
    
for i in regex:
    print str(i)+"\n"

"""***********"""






