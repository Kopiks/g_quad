
from itertools import islice

seq = "GGGACCGGGGGCTTACCGGGCCCGGGCCCGGGCCCGGGAAAGGGAAAAGGGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGGGAAAGGGAAAGGGAAAGGGAAACCAAAAAAAGGAACACCA"


"""Give each position in a sequence a score based on a pattern:
+1 for a single G
+2 for every G in a double G-tract
+3 for every G in a triple G-tract
+4 for every G in a quadruple or more G-tract
For C's it's analogous, but the values are negative
A,T gets 0 every time """
score =[0]*len(seq) 	#predefined score table
idx=0 		#iterator index
while idx < len(seq):
	if seq[idx] =='A' or seq[idx] == 'T':		#score T's and A's
		score[idx] = 0
		idx += 1		 #index incrementation
	elif seq[idx] =='G':
		g_row = 0 		#number of G's in a row -1 (0-based)
		for n in range (idx + 1, len(seq)-1):		#length of a G-tract
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
		for n in range (idx + 1, len(seq)-1):
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

"""Sliding window scoring
Outputs a list of scores, indexes of which correspond to the """
out=[]
n=0
w_s=20	#window size = 25 
while n <= len(score)-w_s: 
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

''' Output list of windows above treshold [[start,stop,score]] (potential GQs)'''
tresh = 1.3 #treshold G score
pre_gs = []
for idx, itm in enumerate(out):
	if itm >= tresh:
		pre_gs.append([idx,idx+w_s,itm])
print pre_gs

"""Merge
Merges overlapping sites,
takes as an input a premerged list
outputs list [[start,stop]]
"""
def merge(premer):
	idx=0
	while idx<= len(premer):
		try:
			print premer[idx][0]
			print premer[idx+1][1]
			if premer[idx][1]>premer[idx+1][0]:
				premer[idx:idx+2]=[[premer[idx][0],premer[idx+1][1]]]
				print premer
				merge(premer)
			idx+=1
		except IndexError:
			break
	return premer
merged = merge(pre_gs)
print "merged"
print merged

