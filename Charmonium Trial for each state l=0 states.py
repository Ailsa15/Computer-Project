import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from scipy.integrate import simpson

#Energies for l=0, n=1 state
#E = 0.35692156851291656
#DeltaE = 

#Mass of charmonium = 1.28 +- 0.025 GeV
#Mass of bottomonium = 4.18 +- 0.03 GeV 
#Mass of bottomonium (1S) = 4.65 +- 0.03 GeV

#Difference in Energy: 0.009283393621444591
#Difference in delta E: 1.286891157444112e-05
#These are calculated using l=1, n=1 state and by adding and subtracting uncertaintiy in beta and finding the waves for that. Then the difference is calculated and divided by 2. 

#Energies for l=1 and n=1
#E1 = 0.8
#E2 = 1
#E3 = 1.2

#Energies for l=1 and n=2
#E1 = 1.3
#E2 = 1.4
#E3 = 1.5

#Energies for l=1 and n=3
#E1 = 1.72
#E2 = 1.75
#E3 = 1.78

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

def calculatea_s(N_f, Lambda_QCD, mQ):
    mu = 2*mQ*mQ/(mQ + mQ)
    a_S = 4*np.pi/((11-2/3*N_f)*np.log(mu**2/Lambda_QCD**2))
    return a_S

def expectation_inv_r3(r, u):
    R = u / r
    integrand = np.abs(R)**2 / r
    return simpson(integrand, r)

def DeltaE(N_f, a_s, m_c, val):
    return 8/9*(1/4-N_f/3)*(a_s**2)/np.pi *1/m_c**2*val
    
    
initial_conditions = [0, 1]
l= 0
n= 1
#m_c = 1.321
m_c = 1.28
m_u = m_c/2
E1 = 0.35
E2 = 0.4
E3 = 0.45
r = np.linspace(1E-7, 15, 1000)
u, v, u1, v1, u2, v2, u_2, u_3, u_4 = np.zeros((9,3,len(r)))
b = 0.229953092713145 
Deltab = 0.02307530737980575
N_f = 4
Lambda_QCD = 0.16  # GeV
#mQ = 1.321  # GeV
mQ = 1.28
a_s = calculatea_s(N_f, Lambda_QCD, mQ)

#for i in range(100):
while abs(E3 - E1) > 1E-8:
    u, v, u1, v1, u2, v2 = Solve(initial_conditions, r, l, m_u, E1, E2, E3, a_s, b)
    Node1 = (CalculateNodes(u, v))
    Node2 = (CalculateNodes(u1, v1))
    Node3 = (CalculateNodes(u2, v2))
    Count1 = (CalculateTurningPoints(v))
    Count2 = (CalculateTurningPoints(v1))
    Count3 = (CalculateTurningPoints(v2))
    #print(E1, E2, E3)
    #print(Node1, Node2, Node3)
    #print(Count1, Count2, Count3)
    E1, E2, E3 = NewEnergy(E1, E2, E3, Node1, Node2, Node3, Count1, Count2, Count3)
    u_2 = normalisation(u, r)
    u_3 = normalisation(u1, r)
    u_4 = normalisation(u2, r)
print(E2)   

R = np.sqrt(u_3)/(r)
norm = simpson(r**2 * np.abs(R)**2, x=r)
#print("Normalization =", norm)

u = np.sqrt(u_3)
val = expectation_inv_r3(r, u)
print("<1/r^3> =", val)

DeltaE = DeltaE(N_f, a_s, m_c, val)
print("Delta E =", DeltaE, "GeV")

plt.figure(figsize=(10, 5))
plt.plot(r, u_3, label='x(t)', color='blue')

plt.xlabel(r'$\frac{r}{a_0}$')
plt.ylabel(r'$|U_{nl}(r)|^{2}$')
plt.grid()
plt.show()

#h = (0.8632815033197403-0.8447147160768511)/2
#g = (0.0019475916679201409-0.0019218538447712586)/2
#print(h)
#print(g)