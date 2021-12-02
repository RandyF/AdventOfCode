f = open(u'_inputs/2021_01_Data.txt', 'r')

win_size = 3

last = 99999
cnt = 0

Data = []
for r in f:
    Data.append(int(r.strip()))


pos = 0
while pos < (len(Data)-win_size+1):
    rdg = sum(Data[pos:pos+win_size])

    if rdg > last:
        cnt += 1

    print(Data[pos:pos+win_size], sum(Data[pos:pos+win_size]), cnt)

        
    last = rdg
    pos += 1
    
print(cnt)
    