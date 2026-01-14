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

def round_sig_fig(x, sig=3):
    from math import log10, floor
    if x == 0:
        return f"0.{(sig-1)*'0'}"
    dec = sig - 1 - floor(log10(abs(x)))
    return f"{x:.{max(dec,0)}f}"
    
initial_conditions = [0, 1]
l= [0, 0, 1]
n= [1, 2, 2]
m_e=0.51099895069 
#m_e = 0.511
a= 1/137
#a = 7.30E-3
a_0 = 1/(m_e*a)
r = [np.linspace(1E-7*a_0, 2000, 10000), np.linspace(1E-7*a_0, 10000, 10000), np.linspace(1E-7*a_0, 10000, 10000)]
r1 = [np.linspace(1E-7*a_0, 2000, 10000), np.linspace(1E-7*a_0, 4000, 10000), np.linspace(1E-7*a_0, 4250, 10000)]
u, v, u1, v1, u2, v2, u_2, u_3, u_4  = np.zeros((9,3,len(r[0])))

Energy = np.zeros(3, dtype=object)
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
    E2 = E2*1E6
    #E2 = round_sig_fig(E2, sig=15)
    Energy[i] = E2
    #u_2[i,:] = normalisation(u[i,:], r[i])
    #u_3[i,:] = normalisation(u1[i,:], r[i])
    #u_4[i,:] = normalisation(u2[i,:], r[i])
    
#u_31_trunc = u_3[1, :4000]
#u_32_trunc = u_3[2, :4250]
r_trunc1 = r[1][:4000]    
r_trunc2 = r[2][:4250]
u_3[0] = normalisation(u1[0,:], r[0]/a_0)
u_31_trunc = normalisation(u1[1,:4000], r_trunc1/a_0)
u_32_trunc = normalisation(u1[2,:4250], r_trunc2/a_0)

Energya = np.zeros(3, dtype=object)
u_analytic, v_analytic, a_1, u_ratio = np.zeros((4, 3, len(r1[0])))
for i in range(0,3):
    E = -a/(2*a_0*n[i]**2)
    analytic = odeint(system, initial_conditions, r1[i], args=(l[i], m_e, E, a, n[i]))
    u_analytic[i,:], v_analytic[i,:] = analytic.T 
    a_1[i,:] = normalisation(u_analytic[i,:], r1[i]/a_0)
    E = E*1E6
    E = round_sig_fig(E, sig=12)
    Energya[i] = E
    #u_ratio[i,:] = (u_3[i,:]/a_1[i,:])

print(Energy)
print(Energya)

plt.figure(figsize=(10, 5))
plt.plot(r[0]/a_0, u_3[0], label=f'Numerical (1,0)', color="#5A2E98")
plt.plot(r_trunc1/a_0, u_31_trunc, label=f'Numerical (2,0)', color="#B22222")
plt.plot(r_trunc2/a_0, u_32_trunc, label=f'Numerical (2,1)', color="#009E8E")
plt.plot(r1[0]/a_0, a_1[0], '--', label=f'Analytic (1,0)', color='#C9A7F5')
plt.plot(r1[1]/a_0, a_1[1], '--', label=f'Analytic (2,0)', color="#FFB5A7")
plt.plot(r1[2]/a_0, a_1[2], '--', label=f'Analytic (2,1)', color="#7FE7D3")
#plt.plot(r/a_0, u_ratio[0], '--', label='Analytic n=2,l=1', color='brown')
#plt.plot(r/a_0, u_ratio[1], '--', label='Analytic n=2,l=1', color='brown')
#plt.plot(r/a_0, u_ratio[2], '--', label='Analytic n=2,l=1', color='brown')
plt.legend()
plt.xlabel(r'$\frac{r}{a_0}$', fontsize = 16)
plt.ylabel(r'$|U_{nl}(r)|^{2}$', fontsize = 16)

plt.savefig("Truncation.png", dpi=300, bbox_inches='tight')

plt.show()
for i in range(3):
    per_diff = (abs(float(Energy[i]) - float(Energya[i]))/abs(float(Energya[i])))*100
    print(per_diff)