f = open(u'_inputs/2021_01_Data.txt', 'r')

last = 99999
cnt = 0

for r in f:
    rdg = int(r.strip())
    
    if rdg > last:
        cnt += 1
        
    last = rdg
    
print(cnt)
    