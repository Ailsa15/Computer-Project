def CalculateEnergy(x,y):
    cross = 0
    for i in range(1,len(y)):
        if y[i-1]*y[i]<0:
            cross += 1
    return cross

x = [1,2,3,4,5]
y = [1,2,-7,-3,-4]

nodes = CalculateEnergy(x,y)
print(nodes)
        