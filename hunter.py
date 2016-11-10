
from itertools import islice

seq = "GGGGGGGGGGGGAAACCCCCCCTGTGCGAGTGAGAGACGCGTGACGGTTTTTTTTTATATATATATAGTAGCGCCCACACACCCCCCAAAAAAGGGGGGGGAAAAAAAGGAAAAAAGGCC"


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
	if seq[idx] =='A' or seq[idx] == 'T':		#score T's and A's
		score[idx] = 0
		idx += 1		 #index incrementation
	elif seq[idx] =='G':
		g_row = 0 		#number of G's in a row -1 (0-based)
		for n in range (idx + 1, len(seq)):		#length of a G-tract
			if seq[n] == 'G':
				g_row += 1
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
		g_row = 0
		for n in range (idx + 1, len(seq)):
			if seq[n] == 'C':
				g_row += 1
			else: break
		if g_row < 3:
			for n in range (g_row + 1):
				score[idx + n] = -(g_row + 1)
			idx += g_row+1
				
			
		else:
			for n in range(g_row + 1):
				score[idx + n] = -4
			idx += g_row+1
print score
"""
Sliding window scoring
Outputs a list of G4Hscores, indexes of which correspond to the particular bases
G4HScore is an arythmetic mean of previously calculated base-scores in a window of given size 
"""
out=[]
n=0
w_s=20	#window size = 25 
while n <= len(score)-w_s: # last possible window
	k=0
	for m in range(w_s):
		k+=score[n+m]*1.0 #float
	ilo=k/w_s #mean for the window
	out.append(ilo)
	n+=1	
print out
'''
#create a list of lists [[Base,Score]]
out_score = []
for idx, itm in enumerate(seq):
	try:
		out_score.append([itm,out[idx]])
	except IndexError:
		break
print out_score
print len(seq)

'''

''' 
Output list of windows above treshold [[start,stop,score]] (potential GQs)
'''
tresh = 1.3 #treshold G score
pre_gs = []
for idx, itm in enumerate(out):
	if abs(itm) >= tresh:
		pre_gs.append([idx,idx+w_s-1,itm]) # -1 found and fixed 10.11.2016

print pre_gs
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
				merge(premer) #run once again to check if newely formed site overlaps next in line
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
	if seq[site[0]-1]==base:	#negative indexes = list read backwards!!
		if site[0]-1>=0:
			site[0]-=1
			adder(site,seq)
		else:
			pass
	if seq[site[1]+1]==base:
		try:					#end of list error handling
			site[1]+=1
			adder(site,seq)
		except IndexError:
			pass
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
print "\n"
print merged
print "\n"
for n in merged:
	i=0
	for m in range(n[0],n[1]+1):
		print score[m]
		i+=score[m]*1.0
	print i
	print n[1]-n[0]+1
	n[2]=i/(n[1]-n[0]+1)
print merged
