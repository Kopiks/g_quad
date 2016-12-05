"""
G4Hunter implementation,
after
Re-evaluation of G-quadruplex propensity with G4Hunter
Amina Bedrat, Laurent Lacroix, Jean-Louis Mergny
Nucleic Acid Res. 2016
"""



from itertools import islice
import argparse
import string
import re
import sys
import operator
sys.setrecursionlimit(10000)
"""
argument parser,
based on quadparser found in the Internet
"""
parser = argparse.ArgumentParser()
parser.add_argument('--fasta', '-f', type = str, required = True)		#input file
parser.add_argument('--treshold', '-tr', type = float, default = 1.3)	#treshold value of G4H score
parser.add_argument('--window', '-ws', type = int, default = 20)		#sliding window size
args = parser.parse_args()


"""
Converts fasta input into single string, copied from the quadparser found in the internet
"""

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


"""
Give each position in a sequence a score based on a pattern:
+1 for a single G
+2 for every G in a double G-tract
+3 for every G in a triple G-tract
+4 for every G in a quadruple or more G-tract
For C's it's analogous, but the values are negative
A,T gets 0 every time
"""
score =[0]*len(seq) 	#predefined score table
idx=0 		#iterator index
while idx < len(seq):
	if seq[idx] =='G':
		g_row = 0 		#number of G's in a row -1 (0-based)
		k=idx+1			#iterator, starting from base after G
		while k < len(seq) :		#length of a G-tract
			if seq[k] == 'G':	
				g_row += 1		
				k+=1
			else: break
		if g_row < 3:		#scoring for 1,2 and 3 G-tract
			for n in range (g_row + 1):
				score[idx + n] = g_row + 1
			idx += g_row+1			# skip to first base after G-tract		
		else:
			for n in range(g_row + 1):		#scoring for 4+
				score[idx + n] = 4
			idx += g_row+1
	elif seq[idx] =='C':		#C scoring, analogous to G scoring
		c_row = 0
		k=idx+1
		while k < len(seq):
			if seq[k] == 'C':
				c_row += 1
				k+=1
			else: break
		if c_row < 3:
			for n in range (c_row + 1):
				score[idx + n] = -(c_row + 1)
			idx += c_row+1
				
			
		else:
			for n in range(c_row + 1):
				score[idx + n] = -4
			idx += c_row+1
	else:					#score for T's and A's (and N's or similar)
		score[idx] = 0
		idx += 1


"""
Sliding window scoring
Outputs a list of G4Hscores, indexes of which correspond to the particular bases
G4HScore is an arythmetic mean of previously calculated base-scores in a window of given size 
"""
out=[]
n=0
w_s=args.window	#window size = 25 
while n <= len(score)-w_s: # last possible window
	k=0
	for m in range(w_s):
		k+=score[n+m]*1.0 #float
	ilo=k/w_s #mean for the window
	out.append(ilo)
	n+=1	

''' 
Output list of windows above treshold [[start,stop,score]] (potential GQs)
'''
tresh = args.treshold #treshold G score
pre_gs = []
for idx, itm in enumerate(out):
	if abs(itm) >= tresh:
		pre_gs.append([idx,idx+w_s-1,itm]) # -1 found and fixed 10.11.2016

"""
Merges overlapping sites,
takes as an input a premerged list
outputs list [[start,stop, score of first of the merged (+- signs are informative whether dealing with Cs or Gs)]]
"""
def merge(premer):
	idx=0		#iterator
	while idx<= len(premer):
		try:
			if premer[idx][1]>premer[idx+1][0] and premer[idx][2]*premer[idx+1][2]>0:		#if end of 1st overlaps start of 2nd site
																							#and both concern G's or C's (+*- score won't trigger)
				premer[idx:idx+2]=[[premer[idx][0],premer[idx+1][1],premer[idx][2]]]	#merge sites (start of 1, end of 2)
				#print "REC"
				#merge(premer) #run once again to check if newely formed site overlaps next in line
				#print "NEW"
			
			else :
				idx+=1
		except IndexError:	#koniec listy
			break
	return premer

merged = merge(pre_gs) # outputs merged list of putative GQ sites
"""
End repair
"""
"""
Remove A/T's from ends
input:
site - site in a following format: [[start,end,.......]]
seq - refseq for coords above
returns corrected site
"""
def remover(site, seq):
	if site[2]>0: #sign of a score (+ for G's - for C's)
		base="G"
	else:
		base="C"
	if seq[site[0]]!=base: 	#if start base is not C/G   
		site[0]+=1			#move start forward
		remover(site,seq)	#check again
	if seq[site[1]]!=base:	#same with and base
		site[1]-=1			#but move backward
		remover(site,seq)
	return site

"""
Add C/G's to the ends, if possible
input and output same as remover
"""
def adder(site, seq):
	if site[2]>0:
		base="G"
	else:
		base="C"
	if seq[site[0]-1]==base:	#if base before start base is G/C	
		if site[0]-1>=0:		#negative indexes = list read backwards!!
			site[0]-=1			#move start backwards
			adder(site,seq)		#run again
	if site[1]+1<len(seq):		#if not end of list
		if seq[site[1]+1]==base:#if base after end base is G/C							
			site[1]+=1			#move end forwards
			adder(site,seq)		#run again		
	return site

"""
Problem: extending ends always elevates G4Hscore. So does removing.
Running adder before the remover might lead to the situation, 
where a less favourable option might be pushed through,
resulting in a longer site with lower score.
This can be solved either by conditional post-refining 
or by simply raising the treshold
"""

for n in merged:	#Refine merged sites
	n=adder(n,seq)
	n=remover(n,seq)	
"""
Rescoring merged and refined sites

"""

for n in merged:					#for each site
	i=0								#sum of base scores calculated in first step
	for m in range(n[0],n[1]+1):	#for each base in site
		i+=score[m]*1.0				#add base's score to sum
	n[2]=i/(n[1]-n[0]+1)			#score=sum of base scores/length of site



"""
GFF3 output
"""
#fo = open("GQ_sites.gff", "w")
for n in merged:				#for each site
	if n[2]>0:					#check strand (+ for G's, - for C's)
		sign="+"
	else:
		sign="-"
	sys.stdout.write(seq_id+"\t"+"."+"\t"+"G_quartet"+"\t"+str(n[0]+1)+"\t"+str(n[1]+1)+"\t"+str(abs(n[2]))+"\t"+sign+"\t"+"."+"\t"+"sequence="+seq[n[0]:n[1]+1]+"\n")
#fo.close()