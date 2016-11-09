"""seq = "GGGCCCGGGCCCGGGCCCGGGCCCGGGCCCGGGAAAGGGAAAGGGAAAGGGAAAGGGAAAGGGAAA"

win_s = 0
win = []
score =[0]*25
win = seq[win_s:win_s+25]
print win
for idx, elm in enumerate(win):
		if elm == 'A' or elm == 'T':
			score[win_s+idx] = 0
		elif elm == 'G':
			g_row=0
			for n in range(idx+1,24):
				if win[n]=='G':
					g_row += 1
				else: break
			if g_row < 3:
				for n in range(g_row+1):
					print n	
					print idx		
					score[win_s+idx+n] = g_row+1
					print win
					print score
				break
				
			else:
				for n in range(g_row+1):
					score[win_s+idx+n] = 4
					print score
				break
"""				



from itertools import islice

seq = "GGGACCGGGGGCTTACCGGGCCCGGGCCCGGGCCCGGGAAAGGGAAAGGGAAAGGGAAAGGGAAAGGGAAACCAAAAAAAGGAACACCA"


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
#create a list of lists [[Base,Score]]
out = []
for idx, itm in enumerate(seq):
	out.append([itm,score[idx]])




