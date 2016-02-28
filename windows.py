seq = "TTTGGGTTTGGGTTTGGGTTTGGGGTTTGTGAAAGGGAAAGGGAAAGTGAAA"
tab = []
for i in range(len(seq)):
        temp = []
        score = 0
        print i
        if seq[i] == 'G':
                print "".join(seq[i:i+3])            
                if seq[i+2] == "G":
                        leng = 3
                        tetrs = 1
                        if "".join(seq[i:i+3]) != "GGG":
                                score += 1
                        print score
                        temp.append(seq[i:i+4])
                        print temp
                        flag = 4
                        while leng<100 and tetrs < 4:
                                print 'check'
                                if seq[i+flag] == "G":
                                        print "znalazlem G"
                                        if seq[i+flag+2] == "G":
                                                if "".join(seq[i+flag:i+flag+3]) != "GGG":
                                                        score += 1
                                                        print score
                                                if tetrs != 3:
                                                        temp.append(seq[i+flag:i+flag+4])
                                                else:
                                                        temp.append(seq[i+flag:i+flag+3])
                                                        print 'LALA'
                                                        g_counter = 0
                                                        while seq[i+flag+3+g_counter] == "G":
                                                                print 'LALALA'
                                                                temp.append(seq[i+flag+3+g_counter])
                                                                g_counter += 1
                                                     
                
                                                flag += 4
                                                leng += 4
                                                if tetrs == 4:
                                                        break
                                                else:
                                                        tetrs += 1         
                                else:   
                                            
                                        temp.append(seq[i+flag])
                                        leng += 1
                                        flag += 1
                                print temp
                        tab.append(["".join(temp), score, i+1, i+(len("".join(temp)))])
                        print tab
                
                        
            
                        

       
