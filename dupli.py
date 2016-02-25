import operator

def sort_table(table, cols):
    for col in reversed(cols):
        table = sorted(table, key = operator.itemgetter(col))
    return(table)


lista = [
    [1,2,3,4,5],[1,3,3,4,5],[3,4,3,1,1],[1,2,3,2,1],[1,2,1,1,1],[1,2,3,1,1],[3,4,3,4,5]
    ]
lista = sort_table(lista, (0,1,2))
out = []
temp = lista[0]
for n in lista[1:]:
    if "".join(str(n[0:3])) != "".join(str(temp[0:3])):
        out.append(temp)        
        temp = n
    else:     
        for i, j in enumerate(temp[3:]):
            temp[i+3] = j + n[i+3]
out.append(temp)   

print out
        
            
            
