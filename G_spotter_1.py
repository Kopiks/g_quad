import re
import sys
import string
import argparse
#I-MOTIFS
#METYLACJE
"""=====ARGUMENT_PARSER====="""
parser = argparse.ArgumentParser()
parser.add_argument('--fasta', '-f', type = str, required = True)
parser.add_argument('--maxtetr', '-mt', type = int, required = True)
parser.add_argument('--loop', '-l', type = int, default = 7)
parser.add_argument('--maxlength', '-ml', type = int, default = 45)
args = parser.parse_args()

"""================"""


"""===================="""

"""====LIST SORTER====="""

import operator

def sort_table(table, cols):
    for col in reversed(cols):
        table = sorted(table, key = operator.itemgetter(col))
    return(table)

"""==================="""

"""====G-spotter===="""


"""********REGEX GENERATOR********"""

m = args.maxtetr
loop = args.loop

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
        tb.append("".join(tab[0:x+1])+'[cCtTaA]'+"".join(tab[x+1:m]))
    bulge.append(tb)
    for x in range(a-2):
        tm.append("".join(tab[0:x+1])+'[cCtTaA]'+"".join(tab[x+2:m]))
    mm.append(tm)
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
        tf.append("\w{1,%d}"%loop)
        temp = []
    for a in range(x):
        temp.append("[gG]")
    tf.append("".join(temp))
    final.append(tf)
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
intab="gGcCtTaA"
outtab="cCgGaAtT"
transtab = string.maketrans(intab, outtab)
for j, i in enumerate(final):
    regex.append({"seq":"".join(i), 'g_type':'perfect', 's_type':"", 'mm_n':"", 'bg_n':"", 'strand':'+', 'im_stack':"", 'no_g':'%d'%(j+3)})
    temp_rev = "".join(i).translate(transtab)
    regex.append({"seq":temp_rev, 'g_type':'perfect', 's_type':"", 'mm_n':"", 'bg_n':"", 'strand':'-', 'im_stack':"",'no_g':'%d'%(j+3)})
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
                regex.append({"seq":"".join(temp), 'g_type':'imperfect', 's_type':"bulge", 'im_stack':"%d"%((k/2)+1), 'mm_n':"", 'bg_n':"%d"%(x+1), 'strand':'+', 'no_g':'%d'%(i+3)})
                temp_rev = "".join(temp).translate(transtab)
                regex.append({"seq":temp_rev, 'g_type':'imperfect', 's_type':"bulge", 'im_stack':"%d"%((len(j)/2)-(k/2)+1), 'mm_n':"", 'bg_n':"%d"%(len(bulge[i])-x), 'strand':'-', 'no_g':'%d'%(i+3)})
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
                regex.append({"seq":"".join(temp), 'g_type':'imperfect', 's_type':"mismatch", 'im_stack':"%d"%((k/2)+1), 'mm_n':"%d"%(x+1), 'bg_n':"", 'strand':'+','no_g':'%d'%(i+3)})
                temp_rev = "".join(temp).translate(transtab)
                regex.append({"seq":temp_rev, 'g_type':'imperfect', 's_type':"mismatch", 'im_stack':"%d"%(len(j)/2-(k/2)+1), 'mm_n':"%d"%(len(bulge[i])-x-1), 'bg_n':"", 'strand':'-','no_g':'%d'%(i+3)})
       
f = open("regex_table.txt","w")
for line in regex:
    f.write(str("".join(line["seq"]))+"\n")
f.close()
"""***********"""
"""***********"""

"""QUADPARSER"""
"""finds and enlists gqs"""
refseq_raw = open(args.fasta)

refseq = []
line = (refseq_raw.readline()).strip()
fa_id = re.sub('^>', '', line)
linre = (refseq_raw.readline()).strip()
gq_list = []

while True:
    while line.startswith('>') is False:
        refseq.append(line)
        line = (refseq_raw.readline()).strip()
        if line == '':
            break
    refseq = ''.join(refseq)
    

    for i in regex:
        for m in re.finditer("".join(i['seq']), refseq):
            if i['strand']=='+':                
                gq_list.append([fa_id, m.start()+1, m.end(), m.group(0), len(m.group(0)),i['no_g'], i['strand'], i['g_type'], [i['s_type']], [i['im_stack']], [i['mm_n']], [i['bg_n']]])
            else:
                gq_list.append([fa_id, len(refseq)-m.end()+1, len(refseq)-m.start(), m.group(0).translate(transtab)[::-1], len(m.group(0)),i['no_g'], i['strand'], i['g_type'], [i['s_type']], [i['im_stack']], [i['mm_n']], [i['bg_n']]])
    fa_id = re.sub('^>', '', line)
    refseq = []
    line = (refseq_raw.readline()).strip()
    if line == '':
        break

gq_sorted = sort_table(gq_list, (0,1,2,3))

"""********"""
"""MAXLENGTH"""
max_l = args.maxlength
for i in gq_sorted:
    if i[4] > max_l:
        gq_sorted.remove(i)
"""*******"""

'''DUPLICATES REMOVAL'''
'''perfect match is favored, imperfect ones are of equal value'''
gq_unique = []
temp  = gq_sorted[0]
for n in gq_sorted[1:]:
    if temp[7]=="imperfect":
        if "".join(str(n[0:7])) != "".join(str(temp[0:7])):
            gq_unique.append(temp)
            temp = n
        else:
            for i, j in enumerate(temp[8:]):
                for k in n[i+8]:
                    temp[i+8].append(k)
    else:
        if "".join(str(n[0:7])) != "".join(str(temp[0:7])):
            gq_unique.append(temp)
            temp = n
        else:
            continue;
    
gq_unique.append(temp)

'''*******'''

'''SCORING'''
'''allloopslength*y/n^2, n=1 for perfect, 2 for imperfect match.'''
'''y=60.153 - 1.5291x ; sodium; Aurore Guedin 2010'''
for n in gq_unique:
    temp = 60.153-1.5291*(n[4]-4*int(n[5]))
    if n[7] != 'perfect':
        temp = temp/4
    n.append(temp)
        
'''*****'''

"""OUTPUT FILE"""
flag_p = 0
for i in gq_unique:
    if i[7]=="perfect":
        flag_p += 1

        
fo = open("test.txt","w")
xx = 1
for line in gq_unique:
    line = '\t'.join([str(x) for x in line])
    fo.write(str(xx)+" "+line+"\n")
    xx += 1

fo.write("PERFECT MATCHES: %d"%flag_p)
fo.close()
"""***********"""

""" OUTPUT GFF3"""
fo = open("test.gff","w")
for line in gq_unique:
    fo.write(line[0]+'\t'+'.'+'\t'+'G_quartet'+'\t'+str(line[1])+'\t'+str(line[2])+'\t'+str(line[12])+'\t'+line[6]+'\t'+'.'+'\t'+'.'+'\n')
fo.close()
"""************"""
