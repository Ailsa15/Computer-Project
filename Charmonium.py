import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from scipy.integrate import simpson

def system(state, r, l, m_u, E, a_s, b):
    u, v = state  
    dudr = v       
    dvdr = l*(l+1)*u/(r**2) - 2*m_u*(E+(4*a_s)/(3*r)-b*r) * u   
    return [dudr, dvdr]

def CalculateNodes(x,y):
    cross = 0
    for i in range(1,len(y)):
        if y[i-1]*y[i]<0:
            cross += 1
    return cross

def CalculateTurningPoints(v):
    count = 0
    for i in range(len(v)-1):
        if v[i]*v[i+1]<0:
            count += 1
    return count

def NewEnergy(E1, E2, E3, Node1, Node2, Node3, Count1, Count2, Count3):
    if Node1 == Node2 and Count1 == Count2:
        E1 = E2
        E2 = (E1 + E3)/2 
    else:
        E3 = E2
        E2 = (E1 + E3)/2
    return E1, E2, E3

def Solve(initial_conditions, r, l, m_u, E1, E2, E3, a_s, b):
    solution = odeint(system, initial_conditions, r, args=(l, m_u, E1, a_s, b))
    solution1 = odeint(system, initial_conditions, r, args=(l, m_u, E2, a_s, b))
    solution2 = odeint(system, initial_conditions, r, args=(l, m_u, E3, a_s, b))
    u, v = solution.T
    u1, v1 = solution1.T    
    u2, v2 = solution2.T
    return u, v, u1, v1, u2, v2

def normalisation(u, r):
    normalisation = simpson(u**2, r)
    u_normalised = u/np.sqrt(normalisation)
    u_squared = u_normalised**2
    return u_squared
    
initial_conditions = [0, 1]
l= [0, 1, 0]
n= [1, 1, 2]
m_c = 1.34
m_u = m_c/2
a_s = 0.40 
E1 = 0.3
E2 = 0.4
E3 = 0.5
r = np.linspace(1E-7, 15, 1000)
u, v, u1, v1, u2, v2, u_2, u_3, u_4 = np.zeros((9,3,len(r)))
b = 0.1951228877648632

#for i in range(100):
#while abs(b3 - b1) > 1E-8:
 #   u, v, u1, v1, u2, v2 = Solve(initial_conditions, r, l, m_u, E1, E2, E3, a_s, b)
  #  Node1 = (CalculateNodes(u, v))
   # Node2 = (CalculateNodes(u1, v1))
    #Node3 = (CalculateNodes(u2, v2))
#    Count1 = (CalculateTurningPoints(v))
 #   Count2 = (CalculateTurningPoints(v1))
  #  Count3 = (CalculateTurningPoints(v2))
   # print(E1, E2, E3)
    #print(Node1, Node2, Node3)
    #print(Count1, Count2, Count3)
    #E1, E2, E3 = NewEnergy(E1, E2, E3, Node1, Node2, Node3, Count1, Count2, Count3)
    #u_2 = normalisation(u, r)
    #u_3 = normalisation(u1, r)
    #u_4 = normalisation(u2, r)
#print(E2)   
#u, v, u1, v1, u2, v2, u_2, u_3, u_4 = np.zeros((9,3,len(r)))
#b = 0.1951228877648632
for i in range(0,1):
    while abs(E3 - E1) > 1E-15:
        u[i,:], v[i,:], u1[i,:], v1[i,:], u2[i,:], v2[i,:] = Solve(initial_conditions, r, l[i], m_u, E1, E2, E3, a_s, b)
        Node1 = (CalculateNodes(u[i,:], v[i,:]))
        Node2 = (CalculateNodes(u1[i,:], v1[i,:]))
        Node3 = (CalculateNodes(u2[i,:], v2[i,:]))
        Count1 = (CalculateTurningPoints(v[i,:]))
        Count2 = (CalculateTurningPoints(v1[i,:]))
        Count3 = (CalculateTurningPoints(v2[i,:]))
        E1, E2, E3 = NewEnergy(E1, E2, E3, Node1, Node2, Node3, Count1, Count2, Count3)
    print(E2)
    u_2[i,:] = normalisation(u[i,:], r)
    u_3[i,:] = normalisation(u1[i,:], r)
    u_4[i,:] = normalisation(u2[i,:], r)

plt.figure(figsize=(10, 5))
plt.plot(r, u_3[0], label='x(t)', color='blue')
#plt.plot(r, u_3[1], label='x(t)', color='orange')
#plt.plot(r, u_3[2], label='x(t)', color='red')
#plt.plot(r0, a_1[0], '--', label='Analytic n=1,l=0', color='green')
#plt.plot(r/a_0, a_1[1], '--', label='Analytic n=2,l=0', color='purple')
#plt.plot(r/a_0, a_1[2], '--', label='Analytic n=2,l=1', color='brown')
#plt.plot(r/a_0, u_ratio[0], '--', label='Analytic n=2,l=1', color='brown')
#plt.plot(r/a_0, u_ratio[1], '--', label='Analytic n=2,l=1', color='brown')
#plt.plot(r/a_0, u_ratio[2], '--', label='Analytic n=2,l=1', color='brown')
#plt.legend([n[i] for i in range(3)], title='n values')
plt.xlabel(r'$\frac{r}{a_0}$')
plt.ylabel(r'$|U_{nl}(r)|^{2}$')
plt.grid()
plt.show()

