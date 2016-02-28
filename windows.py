seq = "GGGAAAGGGAAAGGGAAAGGGAAACCCAAACCCAAACCCAAACTCCCCGGGACCCAGGGACCCAGGGACCCCCAGGGA"
strand=[['G','GGG','+'],['C','CCC','-']]
tab = []
for n in strand:
        for i in range(len(seq)):
                try:
                        temp = []
                        score = 0
                        print i
                        if seq[i] == n[0]:
                                print "".join(seq[i:i+3])            
                                if seq[i+2] == n[0]:
                                        leng = 3
                                        tetrs = 1
                                        if "".join(seq[i:i+3]) != n[1]:
                                                score += 1
                                        print score
                                        temp.append(seq[i:i+4])
                                        print temp
                                        flag = 4
                                        while len("".join(temp))<98 and tetrs < 4:
                                                print 'check'
                                                if seq[i+flag] == n[0]:
                                                        print "znalazlem G"
                                                        if seq[i+flag+2] == n[0]:
                                                                if "".join(seq[i+flag:i+flag+3]) != n[1]:
                                                                        score += 1
                                                                        print score
                                                                if tetrs != 3:
                                                                        temp.append(seq[i+flag:i+flag+4])
                                                                        tetrs += 1
                                                                else:
                                                                        temp.append(seq[i+flag:i+flag+3])
                                                                        print temp
                                                                        print 'LALA'
                                                                        g_counter = 0
                                                                        tetrs += 1
                                                                        while seq[i+flag+3+g_counter] == n[0]:
                                                                                print temp
                                                                                print 'LALALA'
                                                                                temp.append(seq[i+flag+3+g_counter])
                                                                                g_counter += 1
                                                                     
                                
                                                                flag += 4
                                                        else:
                                                                
                                                                flag += 1                                                                        
                                                                temp.append(seq[i+flag])
                                                                         
                                                else:   
                                                            
                                                        temp.append(seq[i+flag])
                                                        flag += 1
                                                print temp
                                        if tetrs == 4:
                                                tab.append(["".join(temp), score, i+1, i+(len("".join(temp))), n[2]])
                                        print tab
                except IndexError:
                        print "IERROR"
                        if seq[len(seq)-1]==n[0]:
                               # temp.append("G")
                                print "APPENDING"
                                print temp
                                if tetrs == 4:
                                        tab.append(["".join(temp),score,i+1,i+(len("".join(temp))), n[2]])
                        else:
                           print "PASSING/BREAKING"
                           break
print "LENSEQ: %d"%(len(seq))
print "FINAL:"
for x,y in enumerate(tab): print y
