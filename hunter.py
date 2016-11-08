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

seq = "GGGCCCGGGCCCGGGCCCGGGCCCGGGCCCGGGAAAGGGAAAGGGAAAGGGAAAGGGAAAGGGAAA"

win_s = 0
win = []
score =[0]*25
win = seq[win_s:win_s+25]
print win


idx=0
while idx < len(win):
	if win[idx] =='A' or win[idx] == 'T':
		score[win_s+idx] = 0
		print 'skip'
	elif win[idx] =='G':
		g_row = 0
		for n in range (idx + 1, 24):
			if win[n] == 'G':
				g_row += 1
			else: break
		if g_row < 3:
			for n in range (g_row + 1):
				print n
				print idx
				score[win_s + idx + n] = g_row + 1
				print score
			
		else:
			for n in range(g_row + 1):
				score[win_s + idx + n] = 4
				print score	
	idx += 1
