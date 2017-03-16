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

parser = argparse.ArgumentParser()
parser.add_argument('--fasta', '-f', type = str, required = True)		#input file
parser.add_argument('--threshold', '-tr', type = float, default = 1.3)	#threshold value of G4H score
parser.add_argument('--window', '-ws', type = int, default = 20)		#sliding window size
args = parser.parse_args()
"""
def fastaInput(input): 
	"""
	Converts fasta input into single string, copied from the quadparser found in the internet
	outputs dict: seq, seq_id (e.g. Chr1)
	"""
	raw_seq = open(input, "r")	# open(args.fasta)
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
	return {'seq':seq, 'seq_id':seq_id}
def ntScore(seq): 
	"""
	Give each position in a sequence a score based on a pattern:
	+1 for a single G
	+2 for every G in a double G-tract
	+3 for every G in a triple G-tract
	+4 for every G in a quadruple or more G-tract
	For C's it's analogous, but the values are negative
	A,T gets 0 every time
	raw sequence as an input, returns list of scores for every nt
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
	return score
def meanScore(nt_score):
	"""
	calculates mean score for a range of nt_scores
	"""
	sum=0
	for n in range(len(nt_score)):
		sum+=nt_score[n]*1.0
	return sum/len(nt_score)
def windowScore(nt_score, window_size): 
	"""
	Sliding window scoring
	Outputs a list of G4Hscores, indexes of which correspond to the particular bases
	G4HScore is an arythmetic mean of previously calculated base-scores in a window of given size 
	inputs: score array, window size; output: array of G4score for every window
	"""
	out=[]
	n=0
	w_s= window_size 	#args.window	#window size = 25 
	score = nt_score
	while n <= len(score)-w_s: # last possible window
		out.append(meanScore(score[n:w_s]))
		n += 1
	return out
def aboveTresh(threshold, window_score): 
	'''
	inputs: threshold, window score array
	Output list of windows above threshold [[start,stop,score]] (potential GQs)
	'''
	tresh = threshold #args.treshold #treshold G score
	pre_gs = []
	for idx, itm in enumerate(out):
		if abs(itm) >= tresh:
			pre_gs.append([idx,idx+w_s-1,itm]) # -1 found and fixed 10.11.2016
	return pre_gs
def merge(premer):
	"""
	Merges overlapping sites,
	takes as an input a premerged list
	outputs list [[start,stop, score of first of the merged (+- signs are informative whether dealing with Cs or Gs)]]
	"""
	idx=0		#iterator index
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
def remove(site, seq):
	"""
	Remove A/T's from ends
	input:
	site - site in a following format: [[start,end,.......]]
	seq - refseq for coords above
	returns corrected site
	"""
	if site[2]>0: #sign of a score (+ for G's - for C's)
		base="G"
	else:
		base="C"
	if seq[site[0]]!=base: 	#if start base is not C/G   
		site[0]+=1			#move start forward
		remove(site,seq)	#check again
	if seq[site[1]]!=base:	#same with and base
		site[1]-=1			#but move backward
		remove(site,seq)
	return site
def add(site, seq):
	"""
	Add C/G's to the ends, if possible
	input and output same as remover
	"""
	if site[2]>0:
		base="G"
	else:
		base="C"
	if seq[site[0]-1]==base:	#if base before start base is G/C	
		if site[0]-1>=0:		#negative indexes = list read backwards!!
			site[0]-=1			#move start backwards
			add(site,seq)		#run again
	if site[1]+1<len(seq):		#if not end of list
		if seq[site[1]+1]==base:#if base after end base is G/C							
			site[1]+=1			#move end forwards
			add(site,seq)		#run again		
	return site
def refineEdge(merged, seq):
	"""
	End repair
	adds and removes stuff
	recalculates score
	"""
	"""
	Problem: extending ends always elevates G4Hscore. So does removing.
	Running adder before the remover might lead to the situation, 
	where a less favourable option might be pushed through,
	resulting in a longer site with lower score.
	This can be solved either by conditional post-refining 
	or by simply raising the threshold
	"""
	for n in merged:	#Refine merged sites
		n=add(n,seq)
		n=remove(n,seq)
	for n in merged:
		n[2]=rescore(seq[n[0]:n[1]])
	return merged
def rescore(seq):
	"""
	Calculates G4score for a whole given sequence
	"""
	return meanScore(ntScore(seq))
def gffOutput(merged, seq, seq_id):
	"""
	GFF3 output to stout
	input: merged tab, reference sequence, seq_id (ie. Chr number)
	"""

	for n in merged:				#for each site
		if n[2]>0:					#check strand (+ for G's, - for C's)
			sign="+"
		else:
			sign="-"
		sys.stdout.write(seq_id+"\t"+"."+"\t"+"G_quartet"+"\t"+str(n[0]+1)+"\t"+str(n[1]+1)+"\t"+str(abs(n[2]))+"\t"+sign+"\t"+"."+"\t"+"sequence="+seq[n[0]:n[1]+1]+"\n")
def mainHunter(input_, threshold_, window_size):
	"""
	From fasta to GFF3
	"""
	seq_sid = fastaInput(input_)							#get sequence id and full sequence from fasta file
	seq_=seq_sid['seq']										#seq_ = sequence
	seq_id=seq_sid['seq_id']									#seq_id = sequence id (ChrN)
	score_ = ntScore(seq_)									#score each nucleotide
	window_score = windowScore(score_, window_size)			#sliding window G4H score
	window_score = aboveTresh(threshold_, window_score)		#extract windows above threshold
	window_score = merge(window_score)						#merge overlapping windows
	window_score = refineEdge(window_score, seq_)			#refine edges, rescore
	gffOutput(window_score, seq_, seq_id)					#stream gff3 to stdout
	
if __name__ == '__main__':
	mainHunter(sys.argv[1], 1.5, 20)