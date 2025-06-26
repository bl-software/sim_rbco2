###################################################
### Fuctions that return a Params calculated value
###################################################
import math
import numpy as np
from numpy.polynomial import Polynomial
from Params.RBCO2_LUT import RBCO2_LUT

################
### Helper Funcs
def req_setup( req_params ):
    ''' req_params - list of params
        returns max len and list of var lists
        Ex. ml=3  rpvals=[ [1.2,1.4,1.6], [400] ]
    '''
    rpvals = [ p() for p in req_params ]
    lens = set([1])
    [lens.add(len(vl)) for vl in rpvals]
    #print('req_setup: %s  %s'%(','.join([r.mlvar_name for r in req_params]),lens))

    ml = max(lens) 
    for i,pvals in enumerate(rpvals):
        if len(pvals) < ml:
            rpvals[i] = pvals*ml
    return ml,rpvals

#############################
### Formula Val Functions ###
#############################
#RBC
def f__HbTotIn(params):
    ''' calc Hbtot_in from MCH '''
    ml,(mch,mcv)= req_setup([ params['MCH'], params['MCV'] ])
    mw= 64316
    '''
    molesHb = mch * 0.000000000001 / mw # C34/D34
    Vcm3pc  = mcv * 0.000000000001      # G25 * 0.0....
    Vlpc    = Vcm3pc * 0.001            # F34 * 0.001
    cmchc   = molesHb * 1000 / Vlpc     # E34 * 1000 / G34
    hbtotin = 4 * cmchc                 # I34 * 4
    hbtotin = 4 * (molesHb * 1000 / Vlpc)
    hbtotin = 4 * 1000 * molesHb / Vlpc

    hbtotin = 4 * 1000 * molesHb 
              -----------------------
                (Vcm3pc) * 0.001

    hbtotin = 4 * 1000 * molesHb 
              -----------------------
                mcv * 0.000000000001 * 0.001

    hbtotin = 4 * 1000 * (mch * 0.000000000001 / mw)
              -----------------------
                mcv * 0.000000000001 * 0.001

    hbtotin = 4 * 1000 * mch * 0.000000000001 
              -----------------------
                mcv * 0.000000000001 * 0.001 * mw

    hbtotin = 4 * 1000 * mch      4000000 * mch    
              ----------------- = ----------------- 
              mcv * 0.001 * mw    mcv * mw  
    '''
    hbtotin = [ (4000000 * mch[i])/(mcv[i]*mw) for i in range(ml) ]
    return  hbtotin


#def f__rbco2_LUT(params,subp):
#    '''lookup table for RBCO2 exps'''
#    ml,(s,g,m)= req_setup([ params['Species'], params['Genetic_Bkg'], params['Mutation'] ])
#    print(f's:{s}  g:{g}  m:{m}')
#    rv=RBCO2_LUT[s[0]][g[0]][m[0]][subp]
#    #print('rv=',type(rv),rv)
#    return [ rv ] # no need for list comp - only 1 selection here

#JTB
def f__d_inf(params):
    ''' f__d_inf is 2 * thickness + D '''
    ml,(thickness,D)= req_setup([ params['thickness'], params['D'] ])
    r= [ ( 2 * thickness[i] ) + D[i] for i in range(ml) ]
    return  r

def f__thickness(params):
    ''' f__thickness is ( D_inf - D ) / 2 '''
    ml,(D_inf,D)= req_setup([ params['D_inf'], params['D'] ])
    r=  [ (D_inf[i] - D[i]) / 2 for i in range(ml) ]
    return  r

def f__D_cm(params): # RBC - convert µm to cm in model
    ml,(d,)= req_setup([ params['Dµm'] ])
    print('ml',type(ml),ml)
    print(' d',type(d),d)
    rval= [ d[i] / 10000.0 for i in range(ml) ]
    #print('f__D_cm rval=', rval)
    return rval
def f__rtorus_cm(params): # RBC - convert µm to cm in model
    #print('f__rtorus_cm >>>')
    ml,(r,)= req_setup([ params['rµm'] ])
    return [ r[i] / 10000.0 for i in range(ml) ]
def f__r_inf_cm(params): # RBC - convert µm to cm in model
    ml,(r,)= req_setup([ params['R_infµm'] ])
    return [ r[i] / 10000.0 for i in range(ml) ]
def f__deuf_cm(params): # RBC - convert µm to cm in model
    ml,(d,)= req_setup([ params['d_eufµm'] ])
    return [ d[i] / 10000.0 for i in range(ml) ]

# RBC
def f__RfromD(params):
    #print('f__RfromD >>>')
    ml,(D,r)= req_setup([ params['Dµm'], params['rµm'] ])
    rv= [ (D[i]-2*r[i])/2 for i in range(ml) ]
    #print(f'f__RfromD <<< rv={rv}')
    return rv #[ (D[i]-2*r[i])/2 for i in range(ml) ]

# RBC
def solve_torus_poly(D,MCV):
    #print('    solve_torus_poly')
    #print(f'      D: {D}  MCV:{MCV}')
    a= 2* np.pi**2
    b= -(np.pi**2)*D
    c=0
    d=MCV
    #print(f'      a={a}\n      b={b}\n      c={c}\n      d={d}')
    thepoly= Polynomial([d, c, b, a])
    #p= Polynomial([MCV, 0, -(np.pi**2)*D, 2* np.pi**2])
    #print(f'    stp:Poly= {thepoly}')
    roots= thepoly.roots()
    #print('    stp:roots=',roots)
    #breakpoint()
    return roots[np.where(roots>0)][0]
    #try:
    #    reals=roots[np.isreal(roots)]
    #    firstreal=reals.real[0]
    #    ''' isreal gives T/F mask [ True, False, False ]
    #        roots[isreal] selects the real ones
    #        .real selects the real part - since the others are still complex with j part
    #        then the first one if multiple
    #    '''
    #    print(f'roots={roots}\nreals={reals}\n  returning roots[0].real={firstreal}')
    #    return firstreal
    #except Exception as e:
    #    print(f'EXC:{e}')
    #    return 0.0

#    solve_torus_poly
#      D: 3.14  MCV:45.57
#      a=19.739208802178716
#      b=-30.990557819420584
#      c=0
#      d=45.57
#    stp:Poly= 45.57 + 0.0·x - 30.99055782·x² + 19.7392088·x³
#    stp:roots= [-0.95600015+0.j          1.26300007-0.90536585j  1.26300007+0.90536585j]
#    D= [3.14]

#    solve_torus_poly
#      D: 4.5  MCV:49.4
#      a=19.739208802178716
#      b=-44.41321980490211
#      c=0
#      d=49.4
#    stp:Poly= 49.4 + 0.0·x - 44.4132198·x² + 19.7392088·x³
#    stp:Poly=  19.7392088*x**3 - 44.4132198*x**2 + 0.0*x  + 49.4
#    stp:roots= [-0.89241495+0.j          1.57120748-0.57934891j  1.57120748+0.57934891j]




# RBC
def f__rsphere(params):
    ml,(r,)= req_setup([ params['rµm'] ])
    #print('r=',r)
    return r

# RBC
def f__rtorus(params):
    #print('f__rtorus >>>')
    ml,(D,MCV)= req_setup([ params['Dµm'], params['MCV'] ])
    rv= [ solve_torus_poly(D[i],MCV[i]) for i in range(ml)]
    #print('    D=',D)
    #print(f'f__rtorus <<< rv={rv}')
    return rv#[ solve_torus_poly(D[i],MCV[i]) for i in range(ml)]

def f__r_inf(params):
    ml,(R,d_euf)= req_setup([ params['rµm'], params['d_eufµm'] ])   # Little r is same as rxo R in code
    #print('f__r_inf  R=',R)
    rinf= [(R[i] + d_euf[i]) for i in range(ml)]
    #print('f__r_inf  R_inf=',rinf)
    return rinf

def f__n_in(params):
    try:
        ml,(r,)= req_setup([ params['r'] ])
    except KeyError:
        ml,(r,)= req_setup([ params['rµm'] ])
    nin= [round(r[i] / 1e-2) for i in range(ml)] # R is in microns 
    return nin

def f__n_out(params):
    try:
        ml,(r,Rinf)= req_setup([ params['r'], params['R_inf'] ])
    except KeyError:
        ml,(r,Rinf)= req_setup([ params['rµm'], params['R_infµm'] ])
    nout= [round((Rinf[i]-r[i]) / 1e-2) for i in range(ml)]
    return nout

def f__pO2(params):
    '''O2_pc*(PB-PH2O)/100'''
    ml,(o2pc,PB,PH2O)= req_setup([ params['O2_pc'], params['PB'], params['PH2O'] ])
    return [ o2pc[i] * (PB[i] - PH2O[i]) / 100 for i in range(ml) ]


def f__pK1(params):
    '''- log10 ( kb_1 / kb_2 )'''
    ml,(kb_1,kb_2)= req_setup([ params['kb_1'], params['kb_2'] ])
    return [- math.log10( kb_1[i] / kb_2[i] ) for i in range(ml) ]

def f__kb_X(params,kbn,pKstr):
    '''kb_3 / ( 10 ** ( - pK2 + 3 ) )'''
#    print('PS=',params)
#    print(kbn,pKstr)
    kb_X = 'kb_%d'%kbn   # Ex. kb_3 kb_5 kb_7
    pKX  = 'pK%s'%pKstr  # Ex. pk2  pkHA2_out
    ml,(kb,pK)= req_setup([ params[kb_X], params[pKX] ])
    return [ kb[i] / ( 10 ** ( - pK[i] + 3 ) ) for i in range(ml) ]

def f__kb_HAX_in_minus(params,bufnum):
    '''kb_HAX_in_plus / ( 10 ** ( - pKHAX_in + 3 ) )
       bufnum: number like 1 ni HA1 '''
    ml,(kb_HAX_in_plus,pKHAX_in)= req_setup([ params['kb_HA%d_in_plus'%bufnum],params['pKHA%d_in'%bufnum] ])
    return [ kb_HAX_in_plus[i] / ( 10 ** ( - pKHAX_in[i] + 3 ) ) for i in range(ml) ]

def f__AXtot_in(params,n):
    #print('AXtot',n,params)
    ''' Calculate total concentration inside oocyte at initial'''
    ml,(pH_in_init, pH_in_final, CO2_in, CO2_pc, PB, PH2O, sCO2, pK1, pK2, Buff_pc)= \
        req_setup([ params['pH_in_init'],
                params['pH_in_final'],
                params['CO2_in'],
                params['CO2_pc'],
                params['PB'],
                params['PH2O'],
                params['sCO2'],
                params['pK1'],
                params['pK2'],
                params['Buff_pc'],
              ])

    # partial CO2 pressure in EUF
    PCO2 = [ CO2_pc[i]*(PB[i]-PH2O[i])/100 for i in range(ml) ]
    # concentration CO2 in EUF - Henry's Law
    CO2_out = [ sCO2[i]*PCO2[i] for i in range(ml) ]
    pK_CO2 = [ pK1[i] + pK2[i] for i in range(ml) ]

    Hplus_in = [ 10**(-pH_in_init[i]+3) for i in range(ml) ]
    H2CO3_in = [ 10**(-pK1[i])*CO2_in[i] for i in range(ml) ]
    HCO3m_in = [ 10**(-pK2[i])*H2CO3_in[i]/Hplus_in[i] for i in range(ml) ]

    HCO3m_fin = [ CO2_out[i]* 10**(pH_in_final[i] - pK_CO2[i]) for i in range(ml) ]
    slope = [ (HCO3m_fin[i]-HCO3m_in[i])/(pH_in_final[i]-pH_in_init[i]) for i in range(ml) ]

    # mean intrinsic buffer (HA/Am) power
    beta_HA  = [-slope[i] for i in range(ml) ]

    pK = [(pH_in_init[i]+pH_in_final[i])/2 for i in range(ml) ]
    # as mean between initial and final (acidic) pHi

    K = [10**(-pK[i]) for i in range(ml) ]
    Q = [(1/(1+K[i]*10**pH_in_init[i]))-(1/(1+K[i]*10**pH_in_final[i])) for i in range(ml) ]
    AXtot_in = [((pH_in_final[i]-pH_in_init[i])*beta_HA[i])/Q[i] for i in range(ml) ]

    if n == 1:
        AXtot_in = [(  Buff_pc[i]/100) *AXtot_in[i] for i in range(ml) ]
    elif n == 2:
        AXtot_in = [(1-Buff_pc[i]/100) *AXtot_in[i] for i in range(ml) ]
    
    return AXtot_in

def f__pH_in_init(params):
    ml,(oocyte_type,CO2_pc)= req_setup([ params['oocyte_type'], params['CO2_pc'] ])
    #print(f'{oocyte_type}, {CO2_pc}')
    pii = {\
         1.5 : { 'Tris' : 7.22,
                 'H2O'  : 7.28,
                 'CAII' : 7.21,
                 'CAIV' : 7.40, },
         5.0 : { 'Tris' : 7.24,
                 'H2O'  : 7.23,
                 'CAII' : 7.21,
                 'CAIV' : 7.37, },
        10.0 : { 'Tris' : 7.18,
                 'H2O'  : 7.16,
                 'CAII' : 7.21,
                 'CAIV' : 7.40, }, }
    #print('pii=',pii)
    #for i in range(ml):
    #    print('i=',i)
    #    print( 'oot',oocyte_type)
    #    print(f'oot[{i}]',oocyte_type[i])
    #    print( 'co2pc',CO2_pc)
    #    print(f'co2pc[{i}]',CO2_pc[i])
    #    print(f'pii[c[i]]',pii[CO2_pc[i]])
    #    print(f'pii[c[i]][oot[i]',pii[CO2_pc[i]][oocyte_type[i]])
    return [ pii[CO2_pc[i]][oocyte_type[i]] for i in range(ml) ]
                
def f__pH_in_acid(params):
    ml,(oocyte_type,CO2_pc)= req_setup([ params['oocyte_type'], params['CO2_pc'] ])
    pia = {\
         1.5 : { 'Tris' : 6.99,
                 'H2O'  : 7.01,
                 'CAII' : 6.98,
                 'CAIV' : 7.06, },
         5.0 : { 'Tris' : 6.79,
                 'H2O'  : 6.84,
                 'CAII' : 6.77,
                 'CAIV' : 6.79, },
        10.0 : { 'Tris' : 6.67,
                 'H2O'  : 6.69,
                 'CAII' : 6.66,
                 'CAIV' : 6.61, }, }
    return [ pia[CO2_pc[i]][oocyte_type[i]] for i in range(ml) ]
 

p_funcs={
    'f__d_inf': f__d_inf,
    'f__r_inf': f__r_inf,
    'f__n_in': f__n_in,
    'f__n_out': f__n_out,
    'f__pO2': f__pO2,
    'f__thickness': f__thickness,
    'f__pK1': f__pK1,
    'f__kb_X': f__kb_X,
    'f__kb_HAX_in_minus': f__kb_HAX_in_minus,
    'f__AXtot_in': f__AXtot_in,
    'f__pH_in_init': f__pH_in_init,
    'f__pH_in_acid': f__pH_in_acid,
#    'f__rbco2_LUT': f__rbco2_LUT,
    'f__HbTotIn': f__HbTotIn,
    'f__RfromD': f__RfromD,
    'f__rtorus': f__rtorus,
    'f__rsphere': f__rsphere,
    'f__D_cm': f__D_cm,
    'f__rtorus_cm': f__rtorus_cm,
    'f__r_inf_cm': f__r_inf_cm,
    'f__deuf_cm': f__deuf_cm,
}
