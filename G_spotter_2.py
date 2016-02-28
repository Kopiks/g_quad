import argparse
import string
import re
import sys
import operator

parser = argparse.ArgumentParser()
parser.add_argument('--fasta', '-f', type = str, required = True)
parser.add_argument('--maxlength', '-ml', type = int, default = 50)
args = parser.parse_args()

def sort_table(table, cols):
    for col in reversed(cols):
        table = sorted(table, key = operator.itemgetter(col))
    return(table)



raw_seq = open(args.fasta)
line = (raw_seq.readline()).strip()
seq_id = re.sub('^>', '', line)
line = (raw_seq.readline()).strip()
seq =[]

while line.startswith('>') is False:
       	seq.append(line)
        line = (raw_seq.readline()).strip()
        if line == '':
        	break
seq = ''.join(seq)


strand=[['G','GGG','+'],['C','CCC','-']]
tab = []
for n in strand:
        for i in range(len(seq)):
                try:
                        temp = []
                        score = 0
                        if seq[i] == n[0]:     
                                if seq[i+2] == n[0]:
                                        leng = 3
                                        tetrs = 1
                                        if "".join(seq[i:i+3]) != n[1]:
                                                score += 1
                                        temp.append(seq[i:i+4])
                                        flag = 4
                                        while len("".join(temp))<98 and tetrs < 4:
                                                if seq[i+flag] == n[0]:
                                                        if seq[i+flag+2] == n[0]:
                                                                if "".join(seq[i+flag:i+flag+3]) != n[1]:
                                                                        score += 1
                                                                if tetrs != 3:
                                                                        temp.append(seq[i+flag:i+flag+4])
                                                                        tetrs += 1
                                                                else:
                                                                        temp.append(seq[i+flag:i+flag+3])
                                                                        g_counter = 0
                                                                        tetrs += 1
                                                                        while seq[i+flag+3+g_counter] == n[0]:
                                                                                temp.append(seq[i+flag+3+g_counter])
                                                                                g_counter += 1
                                                                flag += 4
                                                        else:                                                                
                                                                flag += 1                                                                        
                                                                temp.append(seq[i+flag])
                                                else:                                                               
                                                        temp.append(seq[i+flag])
                                                        flag += 1
                                        if tetrs == 4:
                                                tab.append([seq_id,"".join(temp), score, i+1, i+(len("".join(temp))), n[2]])
                except IndexError:
                        if seq[len(seq)-1]==n[0]:
                               # temp.append("G")
                                if tetrs == 4:
                                        tab.append([seq_id,"".join(temp),score,i+1,i+(len("".join(temp))), n[2]])
                        else:
                           break

tab_sorted=sort_table(tab,(0,3,4))

print tab_sorted


fo = open("The_list.gff","w")
for line in tab_sorted:
	temp=line[1]
    	fo.write(line[0]+'\t'+'.'+'\t'+'G_quartet'+'\t'+str(line[3])+'\t'+str(line[4])+'\t'+str(line[2])+'\t'+line[5]+'\t'+'.'+'\t'+'sequence: %s'%(temp)+'\n')
fo.close()

scores=[0,0,0,0,0]
tout=0
for n,m in enumerate(scores):
	for line in tab_sorted:
		if line[2]==n:
			m += 1
	tout += 1
for n in scores:
	print n
f = open("numbers.txt","w")
f.write('ALL: %d\n0: %d\n1: %d\n2: %d\n3: %d\n4: %d'%(tout,int(scores[0]),int(scores[1]),int(scores[2]),int(scores[3]),int(scores[4])))
f.close()
	

