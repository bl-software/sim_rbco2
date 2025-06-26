import wx
import math
from functools import wraps

##################
### Validators ###
##################
def listvalidator(vfunc):
    @wraps(vfunc)
    def list_wrapper(alist):
        #print('  lvalid: alist=',alist)
        #for li in alist:
        #    print('  lvalid: li=',li)
        #    vfunc(li)
        return [ vfunc(li) for li in alist ]
    return list_wrapper

@listvalidator
def no_test(v):
    return v

@listvalidator
def a_string(str_val):
    return str(str_val)

@listvalidator
def sci_float(str_val):
    '''pseudo type for float parameters in sci notation'''
    #dprint(( 'mfloat', str_val))
    return float(str_val)

@listvalidator
def mlfloat(str_val): # MATLAB float uses 5*10^-7 instead of pythons 5e-07
    '''pseudo type for matlab defined float parameters'''
    #dprint(( 'mfloat', str_val))
    return float(str_val.replace('*10^', 'e'))

@listvalidator
def mlarrayf(str_val): # MATLAB float uses 5*10^-7 instead of pythons 5e-07
    '''pseudo type for matlab defined array of floats parameters'''
    #dprint(( 'mlarrayf', str_val))
    mat_a = str_val.strip('[]').split(';')
    for i in mat_a:
        float(i.replace('*10^', 'e'))
    return mat_a

@listvalidator
def mlbool(str_val):
    '''pseudo type for matlab boolean parameters'''
    #dprint(( mlbool, str_val))
    return str_val in [ 'True', 'true', 'TRUE', '1', 'yes', 'on', True ]

@listvalidator
def pos_float(v):
    pf = float(v)
    #print('POSF',v)
    if pf >= 0:
        return pf
    #print('POSF',v, 'BAD  RAISIN')
    raise ValueError('Positive Float Value required!')

@listvalidator
def reg_float(v):
    return float(v)

@listvalidator
def pos_int(v):
    pi = int(v)
    if pi >= 0:
        return pi
    raise ValueError('Positive Integer Value Required!')

@listvalidator
def choice(v):
    print('choice, got:',v)
    return v

@listvalidator
def reg_int(v):
    return int(v)

@listvalidator
def percent(v):
    fv= float(v)
    if 0 <= fv <= 100:
        return float(v)
    raise ValueError( 'Float Range of [0, 100] Required!')

@listvalidator
def pH(v):
    #print('lv_pH:',v)
    ph = float(v)
    if 0 <= ph <= 14:
        return ph
    raise ValueError( 'Float Range of [0, 14] Required!')

@listvalidator
def Dtorus(v):
    if float(v) > 5.14:
        return float(v)
    else:
        dlg = wx.MessageDialog(None,
                               'There are no real roots of the poly below 5.14, enter a larger number.',
                               "Polynomial Root Error!",
                               wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()

        return 5.14




