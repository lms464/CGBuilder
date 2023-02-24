import numpy as np

def Mamal_Lipid(in_Line):
    con = ""
    upper = {"OL":.419,"PC":.696,"PE":.196,"PS":0.000,"PI":0.000,"PA":0.00, "PG":0.00,"SM":.8}
    lower = {"OL":.581,"PC":.304,"PE":.804,"PS":1.00,"PI":1.0,"PA":1.0,"PG":1.00,"SM":.2}
    for l,c in zip(in_Line[::2],in_Line[1::2]):
        con = "-u %s:%d -l %s:%d "%(l,np.floor(upper[l[2:]]*int(c)*10),l,np.floor(lower[l[2:]]*int(c)*10)) + con
    return con
