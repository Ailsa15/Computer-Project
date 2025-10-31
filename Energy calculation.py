import numpy as np
def CalculateEnergy(x,y):
    cross = 0
    for i in range(1,len(y)):
        if y[i-1]*y[i]<0:
            cross += 1
    return cross

from sympy import symbols, diff, solve

x = symbols('x')
f = x**3 - 3*x**2 + 4  

f_prime = diff(f, x)

stationary_points = solve(f_prime, x)
count = len(stationary_points)

print("Function:", f)
print("Derivative:", f_prime)
print("Stationary Points:", stationary_points)
print(count)


x1 = [1,2,3,4,5]
y1 = [1,2,-7,-3,-4]
x2 = [1,2,3,4,5]
y2 = [1,2,-7,-3,4]
x3 = [1,2,3,4,5]
y3 = [1,2,7,3,4]

#for i in range(1,3):
 #   node = []
  #  node[i] = CalculateEnergy(x1,y1)
#print(node)
        
def CalculateTurningPoints(u,v, f_prime):
    for i in range(0,len(v)):
        f_prime1 = np.gradient(v[i],u[i])
        print(f_prime, f_prime1)
        f_prime = f_prime1
        #if f_prime * f_prime1 <0:
         #   count += 1
    return f_prime, f_prime1

#print(CalculateTurningPoints(x1,y1, 0))


u = [0, 1, 2, 4]
v = [1, -1, 2, -2]
f_prime = 0
for i in range(0,len(v)):
        f_prime1 = np.gradient(v[i],u[i])
        print(f_prime, f_prime1)
        f_prime = f_prime1
        #if f_prime * f_prime1 <0:
         #   count += 1
    #return f_prime, f_prime1

print(np.gradient(v,u))

def CalculateTurningPoints(u,v):
    gradient = np.gradient(v, u)
    count = 0
    for i in range(len(v) - 1):
        if gradient[i] * gradient[i + 1] < 0:
            count += 1
    return count