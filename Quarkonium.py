import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from scipy.integrate import simpson
from decimal import Decimal, getcontext

def system(state, r, l, m_e, E, a, n):
    u, v = state  
    dudr = v       
    dvdr = l*(l+1)*u/(r**2) - 2*m_e*(E+a/r) * u   
    return [dudr, dvdr]

def CalculateInitialEnergy(n):
    E1 = -1.36E-5/n**2+1E-6
    E3 = -1.36E-5/n**2-1E-6
    E2 = (E1 + E3)/2
    return E1, E2, E3

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

def Solve(initial_conditions, r, l, m_e, E1, E2, E3, a, n):
    solution = odeint(system, initial_conditions, r, args=(l, m_e, E1, a, n))
    solution1 = odeint(system, initial_conditions, r, args=(l, m_e, E2, a, n))
    solution2 = odeint(system, initial_conditions, r, args=(l, m_e, E3, a, n))
    u, v = solution.T
    u1, v1 = solution1.T    
    u2, v2 = solution2.T
    return u, v, u1, v1, u2, v2

def normalisation(u, r):
    normalisation = simpson(u**2, r)
    u_normalised = u/np.sqrt(normalisation)
    u_squared = u_normalised**2
    return u_squared

def round_sig(x, sig=3):
    return float(f"{x:.{sig}g}")

def round_sig_fig(x, sig=3):
    from math import log10, floor
    if x == 0:
        return f"{0:.{sig-1}f}"
    dec = sig - 1 - floor(log10(abs(x)))
    return f"{x:.{max(dec,0)}f}"
    
initial_conditions = [0, 1]
l= [0, 0, 1]
n= [1, 2, 2]
#m_e=0.51099895069 
m_e = 0.511
#a= 1/137
a = 7.30E-3
a_0 = 1/(m_e*a)
r = [np.linspace(1E-7*a_0, 2000, 1000), np.linspace(1E-7*a_0, 4200, 1000), np.linspace(1E-7*a_0, 4250, 1000)]
u, v, u1, v1, u2, v2, u_2, u_3, u_4 = np.zeros((9,3,len(r[0])))

Energy = np.zeros((3))
for i in range(0,3):
    E1, E2, E3 = CalculateInitialEnergy(n[i]) 
    while abs(E3 - E1) > 1E-15:
        u[i,:], v[i,:], u1[i,:], v1[i,:], u2[i,:], v2[i,:] = Solve(initial_conditions, r[i], l[i], m_e, E1, E2, E3, a, n[i])
        Node1 = (CalculateNodes(u[i,:], v[i,:]))
        Node2 = (CalculateNodes(u1[i,:], v1[i,:]))
        Node3 = (CalculateNodes(u2[i,:], v2[i,:]))
        Count1 = (CalculateTurningPoints(v[i,:]))
        Count2 = (CalculateTurningPoints(v1[i,:]))
        Count3 = (CalculateTurningPoints(v2[i,:]))
        E1, E2, E3 = NewEnergy(E1, E2, E3, Node1, Node2, Node3, Count1, Count2, Count3)
    E2 = round_sig(E2, sig=3)
    Energy[i] = E2*1E6 
    u_2[i,:] = normalisation(u[i,:], r[i])
    u_3[i,:] = normalisation(u1[i,:], r[i])
    u_4[i,:] = normalisation(u2[i,:], r[i])

Energya = np.zeros(3, dtype=object)
u_analytic, v_analytic, a_1, u_ratio = np.zeros((4, 3, len(r[0])))
for i in range(0,3):
    E = -1.36E-5/n[i]**2
    analytic = odeint(system, initial_conditions, r[i], args=(l[i], m_e, E, a, n[i]))
    u_analytic[i,:], v_analytic[i,:] = analytic.T 
    a_1[i,:] = normalisation(u_analytic[i,:], r[i])
    E = E*1E6
    E = round_sig_fig(E, sig=3)
    Energya[i] = E
    #u_ratio[i,:] = (u_3[i,:]/a_1[i,:])
print(Energy)
print(Energya)
plt.figure(figsize=(10, 5))
plt.plot(r[0]/a_0, u_3[0], label=f'Numerical (1,0) Energy = {Energy[0]} eV', color='blue')
plt.plot(r[1]/a_0, u_3[1], label=f'Numerical (2,0) Energy = {Energy[1]} eV', color='orange')
plt.plot(r[2]/a_0, u_3[2], label=f'Numerical (2,1) Energy = {Energy[2]} eV', color='red')
plt.plot(r[0]/a_0, a_1[0], '--', label=f'Analytic (1,0) Energy = {Energya[0]} eV', color='green')
plt.plot(r[1]/a_0, a_1[1], '--', label=f'Analytic (2,0) Energy = {Energya[1]} eV', color='purple')
plt.plot(r[2]/a_0, a_1[2], '--', label=f'Analytic (2,1) Energy = {Energya[2]} eV', color='brown')
#plt.plot(r/a_0, u_ratio[0], '--', label='Analytic n=2,l=1', color='brown')
#plt.plot(r/a_0, u_ratio[1], '--', label='Analytic n=2,l=1', color='brown')
#plt.plot(r/a_0, u_ratio[2], '--', label='Analytic n=2,l=1', color='brown')
plt.legend()
plt.xlabel(r'$\frac{r}{a_0}$')
plt.ylabel(r'$|U_{nl}(r)|^{2}$')

plt.savefig("Truncation.png", dpi=300, bbox_inches='tight')

plt.show()

