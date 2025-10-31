def system(state, r, l, m_e, E, a):
    u, v = state  
    dudr = v       
    dvdr = l*(l+1)*u/(r**2) - 2*m_e*(E+a/r) * u         
    return [dudr, dvdr]


while abs(E3 - E1) > 1E-10: