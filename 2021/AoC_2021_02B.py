f = open(u'_inputs/2021_02_Data.txt', 'r')

PuzzleData = []
for tIn in f:
    [cmd, dist] = tIn.strip().split(' ')
    PuzzleData.append([cmd, int(dist)])

CurPos = [0, 0, 0]

for tData in PuzzleData:

    if tData[0] == 'forward':
        CurPos[0] += tData[1]
        CurPos[1] += CurPos[2] * tData[1]
        
    elif tData[0] == 'down':
        CurPos[2] += tData[1]
        
    elif tData[0] == 'up':
        CurPos[2] -= tData[1]

print(CurPos[0] * CurPos[1])