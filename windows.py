seq = "GGGAAAGGGAAAGGGAAAGGGAAACCCAAACCCAAACCCAAACTCCCCGGGACCCAGGGACCCAGGGACCCCCAGGGA"
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
                                                tab.append(["".join(temp), score, i+1, i+(len("".join(temp))), n[2]])
                except IndexError:
                        if seq[len(seq)-1]==n[0]:
                               # temp.append("G")
                                if tetrs == 4:
                                        tab.append(["".join(temp),score,i+1,i+(len("".join(temp))), n[2]])
                        else:
                           break
print "LENSEQ: %d"%(len(seq))
print "FINAL:"
for x,y in enumerate(tab): print y
