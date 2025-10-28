def CalculateEnergy(x,y):
    cross = 0
    for i in range(1,len(y)):
        if y[i-1]*y[i]<0:
            cross += 1
    return cross

x1 = [1,2,3,4,5]
y1 = [1,2,-7,-3,-4]
x2 = [1,2,3,4,5]
y2 = [1,2,-7,-3,4]
x3 = [1,2,3,4,5]
y3 = [1,2,7,3,4]

for i in range(1,3):
    node = []
    node[i] = CalculateEnergy(x1,y1)
print(node)
        