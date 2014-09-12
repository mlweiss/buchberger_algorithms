def S(f,g):
    L = LCM(f.lm(), g.lm())
    S = (L/f.lt())*f - (L/g.lt())*g
    return S
    
