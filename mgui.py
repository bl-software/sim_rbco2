#!/usr/bin/env python3

# Copyright © 2015 Dale Huffman, Walter Boron
# SPDX-License-Identifier: GPL-3.0-or-later

'''
NOTES:
   git log --name-status --diff-filter= 
'''

'''
min L  max L which
0.014  0.06  gamswpCTRL DK
0.1    1.0   gamswpCAII DK
0.2    1.0   gamswpCAIV DK
m
'''
'''NOTES:
1. Qs = µ vs cm
    - add cm vars that are dependent on µ vars
    which constants depend on dimensions µ vs cm

2. For testing with rxo numbers, I have to fake it since we calculate those and decimals are off.
   Only thing that matters in sim is r_torus
     No (big R), no D - but our input is geno,species -gives-> MCV, MCH, D - we then calc r_torus, Hbtot_in

Notes:
    Tests: rxo vs gui
        ⁂ Created RXOTest dropdowns with various D,MCH values to match sim3_ files from rxo
        ⁂   Added k_lysate to allow for kb[1,2] to mache sim3_ values
        ⁂ fielddump.m and fielddumpdir.m
            ran on Sims dir to create .csv dumps for all sim3_ .mat files
            for small vars (not large matricies)
        • Step1: save params and run sim - can't verify yet
        • Step2: in Matlab
            S=load('rbc2024_k145/rbc2024_k145.mat')
            ofname='rbc2024_k145/rbc2024_k145_fields.csv'
            fielddump
            -- this creates dump to compare
        • Step3: Compare parameters
            python comparecsv.py Sims/sim3_WT_k_0p125.csv rbc2024_k145/rbc2024_k145_fields.csv
        • Step4: Compare output in Matlab
            load('rbc2024_k145/rbc2024_k145.mat')
            Calculate_t37_20190215
            load('Sims/sim3_WT_k_0p125.mat')
            Calculate_t37_20190215
           verify outputs are same
        • Step5: Compare plots
            figtitle='sim3_WT_k_0p125'
            load(strcat('Sims/',figtitle,'.mat'))
            Plot6dale_SI_Fig10_PrevFig7

            figtitle='rbc2024_k145'
            load(strcat(figtitle,'/',figtitle,'.mat'))
            Plot6dale_SI_Fig10_PrevFig7

I'v tested:
    Sims/sim3_WT_k_0p625.csv vs. rbc2024_k725/rbc2024_k725_fields.csv
        then ran with dropdown mouse values
        rbc2024_k725mouse/rbc2024_k725mouse.mat
        rxo     t_37,0.2881 k37,3.4712
        mouse   t_37,0.2873 k37,3.4809

    Sims/sim3_WT_k_0p125.csv vs. rbc2024_k145/rbc2024_k145_fields.csv

    Sims/sim3_WT_Pm_0p35.csv Sims/sim3_WT_Pm_3p00.csv VS.
    BatchMode
    rbc2024_pmo2_0p35_v_3p0/
        rbc2024_pmo2_0p35_v_3p0__Pm_O2_0_35_fields.csv
        rbc2024_pmo2_0p35_v_3p0__Pm_O2_3_0_fields.csv

    Bovine
    Sims/DiffSpecies/Sims_Bovine_Diam_klys_Human.csv rbc2024_bovine/rbc2024_bovine_fields.csv
    match good
     
Do we want DO2 - what about zeros for the kappa_out?
Do we want 3 vals for kappa_in?
'''

r'''GUI frontend for Cell Modelling program'''
USE_MATLAB=True
#USE_MATLAB=False
USE_OCTAVE= not USE_MATLAB

import sys
sys.path.append('openglpy')
print('\n'*20)
#print(sys.path)
import socket
import os
import string
import wx
import wx.svg
import wx.lib.scrolledpanel as scrolled
#from wx.lib.fancytext import StaticFancyText
print(f'wxpython: {wx.version()}')
print('Name:',__name__)
import collections
from itertools import zip_longest
#import copy
import datetime
import math
import re
import glob
#import types
import time
import pickle
import pprint
pp = pprint.PrettyPrinter(indent=3)
#USAGE pp.pprint(FigParams)


import pdb

from CCI import ColChangeInput #, ColChangeInput_2

import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter, FuncFormatter, MaxNLocator
import matplotlib as mpl
import matplotlib.artist as mpla
#import matplotlib.patches as mpatch
#from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg    as FigureCanvas
from matplotlib.figure import Figure
#from cycler import cycler
#from adjustText import adjust_text
import numpy as np
import pandas as pd

# At work this is ../../openglpy - at home something else - if symlink is good it should work
#sys.path.append('../openglpy/')
#print(sys.path)
#import ..openglpy.bicon
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#print(sys.path)
from openglpy import bicon

#from oct2py import octave
#octave.addpath('/home/dhuffman/anaconda3/envs/modelling_py37_M2019b/bin/octave')
if USE_MATLAB:
    import matlab.engine
#'''NOTES - after Matlab Upgrade
#$ cd /usr/local/MATLAB/R2016b/extern/engines/python/
#$ sudo python3 setup.py install
#'''
elif USE_OCTAVE:
    import oct2py

'''
MATLAB INSTALL NOTES - need to run as non root to use venv - but then need to build in writable loc
python3 setup.py build --build-base="~/matbuild" install
NOT SURE IF ~ works - just general for this code
'''

'''
OCTAVE build notes:
export OCTAVE_EXECUTABLE=/home/dhuffman/octave/bin/octave-cli
follow - build instructions on website for debian - figure it out again and document.

HERE: Notes
Trench Free DiffEQ page 14 exercises 1.2 4c  answers on 583

Then Sundials pdf ida_guide.pdf
then set solver for ode15s in octave if can
    maybe use sudials directly
    then get rid of all matrix building - numpy -> sundials direct ??? look into

FIrst - short names - by run1, run2, run3 - etc.
Then verify CAIV vs CAII/TRIS plot
   fig4DALE??? - maybe I forget
    Maybe make dropdown TRIS/CA... in to list of text ??? think about
'''

import wx.lib.fancytext as fancytext
def o_start_sub(self, attrs):
    ''' this is to override the subscript height '''
    if attrs.keys():
        raise ValueError("<sub> does not take attributes")
    font = self.getCurrentFont()
    self.offsets.append(self.offsets[-1] + self.dc.GetFullTextExtent("M", font)[1]*0.2)
    self.start_font({"size" : font.GetPointSize() * 0.9})
fancytext.Renderer.start_sub= o_start_sub
#types.MethodType(start_sub, wx.lib.fancytext.Renderer)



#GET RID OF Params files and test - tryin g
#PYOPENGL_PLATFORM=egl python mgui.py --simtype=2 --paper=0 --figure=6
#and pickup up 5PSIGMOIDstraint - shouldnt, params is setting the dropdown /????????


from VERSION import version
program_version= version.split(' ')[0]

import wx.lib.wxcairo
import cairo
haveCairo = True
#    haveCairo = False

#INSPECT=True
INSPECT=False
if INSPECT:
    import wx.lib.inspection

#import Figures
from Params import myParams
pprint.pp(myParams)
#OLD from Params import * # Creates Params__JTB_fig_3_4_5, Params__JTB_fig_6 etc.
from Params.Param_Validators import *

from Params.RBCO2_LUT import RBCO2_LUT
#print('RBCO2_LUT')
#pp.pprint(RBCO2_LUT)

from Figures import Figs
pprint.pp(Figs)

from support import *

def hex_to_float( h ):
    return float((h>>16)&0xff)/255, float((h>>8)&0xff)/255, float(h&0xff)/255

class RGB_JTB_2012:
    icfo     = hex_to_float( 0xA9CFA0 )
    icfi     = hex_to_float( 0x79AF70 )
    eufo     = hex_to_float( 0xb1dcff )
    eufi     = hex_to_float( 0xC1C1D5 )
    memsurf  = hex_to_float( 0x9F7F5D )
    memcent  = hex_to_float( 0xA4AF7F )
    rad      = hex_to_float( 0x606060 )
    radtxt   = hex_to_float( 0x000000 )
    arrowtxt = hex_to_float( 0x0000ff )
    arrow    = hex_to_float( 0x0000ff )
    bg = '#b1dcff'
class RGB_AJP_2014:
    icfo     = hex_to_float( 0x8C5D2F )
    icfi     = hex_to_float( 0x231000 )
    eufo     = hex_to_float( 0xDBDBE6 )
    eufi     = hex_to_float( 0xC1C1D5 )
    memsurf  = hex_to_float( 0x465723 )
    memcent  = hex_to_float( 0xC1C1D5 )
    rad      = hex_to_float( 0xf0f0f0 )
    radtxt   = hex_to_float( 0xffffff )
    arrowtxt = hex_to_float( 0xc0c0ff )
    arrow    = hex_to_float( 0xffffff )
    bg= '#808080'
class RGB_RBCO2:
    icfo     = hex_to_float( 0x8C5D2F )
    icfi     = hex_to_float( 0x231000 )
    eufo     = hex_to_float( 0xDBDBE6 )
    eufi     = hex_to_float( 0xC1C1D5 )
    memsurf  = hex_to_float( 0x465723 )
    memcent  = hex_to_float( 0xC1C1D5 )
    rad      = hex_to_float( 0xf0f0f0 )
    radtxt   = hex_to_float( 0xffffff )
    arrowtxt = hex_to_float( 0xc0c0ff )
    arrow    = hex_to_float( 0xffffff )
    bg= '#008888'


rgbs = { 'JTB'      : RGB_JTB_2012,
         'AJP'      : RGB_AJP_2014,
         'RBCO2'    : RGB_RBCO2,
         'RBCO2Simp': RGB_RBCO2,
}

#TODO this is now a bad name since it is no longer a wx.Panel
class CellPanel(object):#(wx.Panel):
    def __init__(self,app,cpname='CPNull',xsz=600,ysz=800,makepanel=True):
        #print(f'CP:name={cpname}')
        self.app= app
        self.panelsize_x = xsz
        self.panelsize_y = ysz
        self.panelsize = (self.panelsize_x, self.panelsize_y)
        self.rendercount=0
        if makepanel:
            #self.parent=self.app.panel
            self.vs= wx.BoxSizer(wx.VERTICAL)
            self.panel= wx.Panel(self.app.panel, wx.ID_ANY, size=(self.panelsize_x,self.panelsize_y), name=cpname)
            self.vs.Add(self.panel, 0)

    def Destroy(self):
        self.panel.Destroy()
        self.vs.Remove(self.panel, 0)

    def angled_linetext(self, ctx, angle, li,lj,lk,ll, textlines, spacing=2, lineoffset=1.0, dx=0, dy=0, dr=0, dc=0, debug=[]):
        ''' centers on the radial line (I think)'''
        #print('AL:',li,lj,lk,ll)
        #print('TLs=',textlines)
        r=math.radians(angle)
        angle= math.degrees(math.atan2(math.sin(r),math.cos(r)))
        radians= math.radians(angle)#2*math.pi*angle/360
        #textlines.insert(0,'%s'%angle)

        #print(textlines)
        line_cx= (li + lk) /2
        line_cy= (lj + ll) /2
        #print('LC:',line_cx, line_cy)
        #print('ijkl=', li, lj, lk, ll, 'line_cx', line_cx, 'line_cy', line_cy )
        
        # Test -- cross
        def cross(x,y,r=None,g=None,b=None,a=None):
            #print('cross:',x,y,r,g,b,a)
            if r or g or b or a:
                ctx.set_source_rgba( r, g, b, a)
            ctx.move_to( x-100, y )
            ctx.line_to( x+100, y )
            ctx.move_to( x    , y-100 )
            ctx.line_to( x    , y+100 )
            ctx.stroke()

        if 'initcross' in debug:
            cross(line_cx,line_cy, 1.0, 1.0, 0.0, 1.0) # Yellow
            cross(   20.0,   20.0, 0.0, 0.0, 0.0, 1.0) # Black

        if 'blah' in debug:
            ctx.set_source_rgba( 0.5, 0.5, 0.5, 0.5)
            ctx.move_to(100,100)
            ctx.line_to(500,500)
            ctx.stroke()
        # Test -- Perp Line
        #xs= line_cx-math.sin(radians)*100
        #ys= line_cy-math.cos(radians)*100
        #ctx.move_to( xs, ys )
        #xe= line_cx+math.sin(radians)*100
        #ye= line_cy+math.cos(radians)*100
        #ctx.line_to( xe, ye )
        #ctx.stroke()
        #self.arrowhead( ctx, 1.0,1.0,1.0, xs, ys, xe, ye)

        face = wx.lib.wxcairo.FontFaceFromFont(wx.FFont(10, wx.SWISS))#, wx.FONTFLAG_BOLD))
        height= ctx.font_extents()[2]
        #print( 'angle=', angle, 'radians=', radians, 'height=', height )
        ctx.set_font_face(face)
        ctx.set_font_size(16)
        ctx.set_source_rgb(*self.rgb.rad)
        ctx.move_to(line_cx,line_cy)
        #print('mt:',line_cx, line_cy)

        for i,tl in enumerate(textlines):
            x_bearing, y_bearing, width, Xheight, Xxadvance, Xyadvance = ctx.text_extents(tl)
            #print('init  tes', ctx.text_extents(tl))
            ctx.save()
            if abs(angle) < 90:
                text_x, text_y = self.PolarToCartesian((i+lineoffset)*(height + spacing), angle -90 , line_cx, line_cy )
                #if 'trace' in debug:
                #    ctx.set_source_rgba( 1.0, 0.0, 0.0, 1.0)
                #    ctx.line_to(text_x,text_y)
                #    ctx.stroke()
                #    print('lt1a:',text_x,text_y)
                #    cross(text_x+15,text_y+15,1.0, 0.0, 0.0, 1.0)
                text_x, text_y = self.PolarToCartesian(   (width + x_bearing)/2, angle -180,  text_x,  text_y )
                #if 'trace' in debug:
                #    ctx.set_source_rgba( 0.0, 1.0, 0.0, 1.0)
                #    ctx.line_to(text_x,text_y)
                #    ctx.stroke()
                #    print('lt1b:',text_x,text_y)
                #    cross(text_x,text_y,0.0, 1.0, 0.0, 1.0)
                #    cross(0.0,0.0,0.0, 1.0, 1.0, 1.0)
            else:
                text_x, text_y = self.PolarToCartesian((i+lineoffset)*(height + spacing), angle +90 , line_cx, line_cy )
                #if 'trace' in debug:
                #    ctx.set_source_rgba( 1.0, 0.0, 0.0, 1.0)
                #    ctx.line_to(text_x,text_y)
                #    print('lt2a:',text_x,text_y)
                #    ctx.stroke()
                text_x, text_y = self.PolarToCartesian(   (width + x_bearing)/2, angle     ,  text_x,  text_y )
                #if 'trace' in debug:
                #    ctx.set_source_rgba( 0.0, 1.0, 0.0, 1.0)
                #    ctx.line_to(text_x,text_y)
                #    print('lt2b:',text_x,text_y)
                #    ctx.stroke()
            ctx.translate(text_x, text_y )
            if abs(angle) < 90:
                ctx.rotate(-radians) # ROTATE is positive clockwise
            else:
                ctx.rotate(math.pi-radians)#abs(radians)%math.pi/2) # ROTATE is positive clockwise
            ctx.move_to(0,0)
            #print('final tes', ctx.text_extents(tl))
            ctx.show_text(tl)
            if 'pathcross' in debug:
                cross(0.0,0.0, 1.0, 1.0, 1.0, 1.0)
            ctx.restore()

        if 'initcross' in debug:
            #print('OUTCROSS:')
            cross( 0.0, 0.0, 1.0, 0.0, 1.0, 1.0) # Magenta offset from IN

    def arrowhead(self, ctx, r, g, b, xs, ys, xe, ye, length=5, deg=math.pi * .15):
        angle = math.atan2 (ye - ys, xe - xs) + math.pi

        x1 = xe + length * math.cos(angle - deg)
        y1 = ye + length * math.sin(angle - deg)
        x2 = xe + length * math.cos(angle + deg)
        y2 = ye + length * math.sin(angle + deg)
 
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)

        ctx.set_source_rgba( *self.rgb.arrowtxt, 1 )
        ctx.move_to (xe, ye)
        ctx.line_to (x1, y1)
        ctx.stroke()

        ctx.set_source_rgba( *self.rgb.arrowtxt, 1 )
        ctx.move_to (xe, ye)
        ctx.line_to (x2, y2)
        ctx.stroke()

    def offset(self,x,y,l,deg):
        rads= math.radians(deg)
        return x+l*math.cos(rads), y+l*math.sin(rads)

    def PolarToCartesian(self, radius, angle, cx, cy):
        x = radius * math.cos(math.radians(angle))
        y = radius * math.sin(math.radians(angle))
        return (cx+x, cy-y)

class CellPanel_RBCOPENGL(CellPanel):
    def __init__(self,app):
        super().__init__(app, 'CellPanel_RBCOPENGL', 400, 400, makepanel=False)
        # canvas is used instead of default panel

        self.vs= wx.BoxSizer(wx.VERTICAL)

        #canvas=ConeCanvas(self)
        #canvas=ConeCanvas(app.panel)
        self.set_bicon_kwargs()
        self.bicon=bicon.BiCon(app.panel,1000,1000,self.bicon_kwargs)
        self.bicon.run()
        self.vs.Add(self.bicon.glcanv)#, proportion=1, flag=wx.EXPAND)
        #self.SetSizer(self.vs)
        #wx.CallLater(250,self.init_refresh)

    def set_bicon_kwargs(self):
        D=self.app.cur_params['Dµm']()[0]
        R=self.app.cur_params['R'  ]()[0]
        r=self.app.cur_params['rµm'  ]()[0]
        sp=self.app.cur_params['Species']
        gb=self.app.cur_params['Genetic_Bkg']
        gt=self.app.cur_params['Genotype']
        graphics_kwargs= {'D':D,'R':R,'r':r, 'sp':sp, 'gb':gb, 'gt':gt}
        hud_kwargs= {}#'hudtext':f'HUD {D} μm'}
        self.bicon_kwargs= {**graphics_kwargs, **hud_kwargs}

    def Destroy(self):
        '''try 
            vs.Hide(glcanv)
            glcanv.Destroy

        '''
        print('CellPanel_RBCOPENGL.Destroy 1\n')
        #self.vs.Remove(self.bicon.glcanv)
        self.vs.Hide(self.bicon.glcanv)
        self.vs.Detach(self.bicon.glcanv)
        print('CellPanel_RBCOPENGL.Destroy 2\n')
        self.bicon.Destroy()
        print('CellPanel_RBCOPENGL.Destroy 3\n')

    def Refresh(self): # CellPanel_RBCOPENGL
        print('CellPanel_RBCOPENGL.Refresh\n'*10)
        self.set_bicon_kwargs()
        self.bicon.updateScenes( self.bicon_kwargs )
        #self.bicon.OnPaint('evt_mgui')
        wx.CallLater(1, self.uppy)
        #TODO find out why this is necessary - something isn't refreshing properly 
        # when change D for example the HUD doesn't update until some event forces a refresh/update
        # like tabbing to another window, or mouseing over the glcanvas

    def uppy(self):
        self.bicon.glcanv.Refresh()
        self.bicon.glcanv.Update()

class CellPanel_RBC(CellPanel):
    def __init__(self,app):
        super().__init__(app, 'CellPanel_RBC', 800, 800)
        self.rgb= rgbs[self.app.cur_sim_type]

        self.paint_panel= wx.Panel(self.panel,wx.ID_ANY,size=(self.panelsize_x,int(self.panelsize_y/2)),name='paint_panel')
        self.torus_panel= wx.Panel(self.panel,wx.ID_ANY,size=(self.panelsize_x,int(self.panelsize_y/2)),name='torus_panel')
        #self.paint_panel= wx.Panel(self,wx.ID_ANY,name='paint_panel')
        #self.torus_panel= wx.Panel(self,wx.ID_ANY,name='torus_panel')
        self.vs.Add(self.paint_panel, 0, wx.EXPAND)
        self.vs.Add(self.torus_panel, 0, wx.EXPAND)

        rbc_svg_filename= 'RBC_image_woBKG.svg'
        rbc_png_filename= 'RBC_image_woBKG.png'

        #self.vs
        #self.rbc_img = wx.svg.SVGimage.CreateFromFile(rbc_svg_filename)

        #dcdim = min(self.Size.width, self.Size.height)
        #imgdim = min(self.rbc_img.width, self.rbc_img.height)
        #scale = dcdim / imgdim
        #width = int(self.rbc_img.width * scale)
        #height = int(self.rbc_img.height * scale)

        
        
        #self.rbc_bmp = self.rbc_img.ConvertToBitmap(scale=scale, width=width, height=height)
        self.rbc_bmp = wx.Bitmap(rbc_png_filename)

        self.paint_panel.Bind(wx.EVT_PAINT, self.OnPaint)
        wx.CallLater(250,self.init_refresh)

    def OnPaint(self,e): # CellPanel_RBC
        dc=wx.PaintDC(self.paint_panel)    # NOTE this is called a LOT
        #if self.paint_panel.IsDoubleBuffered():
        #    dc=wx.PaintDC(self.paint_panel)    # NOTE this is called a LOT
        #    #print('PaintDC=',dc)
        #else:
        #    dc=wx.BufferedPaintDC(self.paint_panel)
        #    #print('BPaintDC=',dc) # NOTE - never called while printing
        self.rb,self.gb,self.bb= hex_to_float( 0xb1dcff )
        dc.Clear()
        self.Render(dc)

    def init_refresh(self): # CellPanel_RBC
        gml= self.app.wxapp.GetMainLoop()

        #print('GML:IR:', gml)
        if not gml:
            #print('not yet')
            wx.CallLater(100,self.init_refresh)
        else:
            print('==============refreshing')
            self.Refresh() # QQQ panel.Refresh ??? - not using so not tested
            self.Update()


    def Render(self, dc): # CellPanel_RBC
        print( f'RENDER CP_RBC dc={dc}----------------------------------')
        self.rgb= rgbs[self.app.cur_sim_type]
        self.SetBackgroundColour( self.rgb.bg )

        i= self.rbc_bmp.ConvertToImage()#wx.ImageFromBitmap(self.rbc_bmp)
        i= i.Scale(400,400,wx.IMAGE_QUALITY_HIGH)
        self.rbc_bmp_scaled= wx.Bitmap(i)#wx.BitmapFromImage(i)
        dc.DrawBitmap(self.rbc_bmp_scaled,0,0)

        r_torus= self.app.cur_params["r"]()[0]
        R_torus= self.app.cur_params["R"]()[0]
        self.torus(R_torus,r_torus)

        w,h=self.paint_panel.Size.width, self.paint_panel.Size.height
        print('paint panel',w,h)
        w,h=self.torus_panel.Size.width, self.torus_panel.Size.height
        print('torus panel',w,h)
        print( f'RENDER CP_RBC DONE dc={dc}----------------------------------')

    def torus(self,R,r):
        n = 100
        theta      = np.linspace(0, 2.*np.pi, n)
        phi        = np.linspace(0, 2.*np.pi, n)
        theta, phi = np.meshgrid(theta, phi)

        x = (R + r*np.cos(theta)) * np.cos(phi)
        y = (R + r*np.cos(theta)) * np.sin(phi)
        z = r * np.sin(theta)

        #cx= int(self.panelsize_x/2)
        w= 800#self.panelsize_x
        h= 400#int(self.panelsize_y/2)
        px = 1/plt.rcParams['figure.dpi']
        self.torus_fig = Figure(constrained_layout=True, figsize=(w*px,h*px))

        ax1 = self.torus_fig.add_subplot(121, projection='3d')
        ax1.set_zlim(-3,3)
        ax1.plot_surface(x, y, z, rstride=5, cstride=5, color='#9a0020', edgecolors='w')
        ax1.view_init(36, 26)
        ax1.set_xlabel('scale= \u00b5m')

        ax2 = self.torus_fig.add_subplot(122, projection='3d')
        ax2.set_zlim(-3,3)
        ax2.plot_surface(x, y, z, rstride=5, cstride=5, color='#9a0020', edgecolors='w')
        ax2.view_init(0, 0)
        ax2.set_xticks([])
        ax2.set_ylabel('scale= \u00b5m')

        self.torus_fig.set_tight_layout('tight')
        self.torus_canv= FigureCanvas(self.torus_panel,wx.ID_ANY,self.torus_fig)
        #plt.show() 


class CellPanel_Oocyte(CellPanel):
    def __init__(self,app):
        super().__init__(app, 'CellPanel_Oocyte')
        self.rgb= rgbs[self.app.cur_sim_type]
        self.panel.SetBackgroundColour( self.rgb.bg )

        self.paint_panel= self.panel
        self.panel.Bind(wx.EVT_PAINT, self.OnPaint)
        wx.CallLater(250,self.init_refresh)

    def Refresh(self):
        print('Refresh')
        self.panel.Refresh()
        

    def OnPaint(self,e): # CellPanel_Oocyte
        #print(f'OnPaint e={e}')
        dc=wx.PaintDC(self.paint_panel)    # NOTE this is called a LOT
        #print(f'   dc={dc}')
        #if self.paint_panel.IsDoubleBuffered():
        #    dc=wx.PaintDC(self.paint_panel)    # NOTE this is called a LOT
        #    #print('PaintDC=',dc)
        #else:
        #    dc=wx.BufferedPaintDC(self.paint_panel)
        #    #print('BPaintDC=',dc) # NOTE - never called while printing
        self.rb,self.gb,self.bb= hex_to_float( 0xb1dcff )
        dc.Clear()
        self.Render(dc)

    def init_refresh(self): # CellPanel_Oocyte
        return
        #gml= self.app.wxapp.GetMainLoop()
        ##print('GML:IR:', gml)
        #if not gml:
        #    #print('not yet')
        #    wx.CallLater(100,self.init_refresh)
        #else:
        #    #print('==============refreshing')
        #    #self.Refresh()
        #    #self.Update()
        #    self.OnPaint(None) dont do this - need event


    def Render(self, dc): # CellPanel_Oocyte
        self.rendercount+=1
        if self.rendercount %100 == 0:
            print(f'CP_Oocyte:render rendercount={self.rendercount}')
        #if not dc:
        #    print( 'RENDER NO DC----------------------------------------')
        #    print( 'RENDER DO SOMETHING----------------------------------------')
        self.rgb= rgbs[self.app.cur_sim_type]
        self.panel.SetBackgroundColour( self.rgb.bg )

        cx= self.cx = int(self.panelsize_x/2)
        cy= self.cy = int(self.panelsize_x/2 + 50)
        center_pt = wx.Point(cx, cy)

        # D and D_inf are in mm 
        actual_radius_cell_mm = self.app.cur_params["D"]()[0] / 2
        actual_radius_euf_mm  = self.app.cur_params["D_inf"]()[0] / 2
        actual_thickness_euf_mm  = actual_radius_euf_mm - actual_radius_cell_mm
        #print('actual_radius_cell_mm:', actual_radius_cell_mm,
        #      'actual_radius_euf_mm:', actual_radius_euf_mm,
        #      'actual_thickness_euf_mm:', actual_thickness_euf_mm )

        graphical_space_around_cell= 50
        ratio = (self.panelsize_x - graphical_space_around_cell)/2 / actual_radius_euf_mm  # pixels / mm
        #print( 'ratio=', ratio )
        radius_cell = actual_radius_cell_mm * ratio
        radius_euf = actual_radius_euf_mm * ratio
        thickness_euf = actual_thickness_euf_mm * ratio
        one_mm_line = 1.0 * ratio
        #print('ratio:', ratio, 'radius_cell', radius_cell,'radius_euf',radius_euf)

        num_shells_in= self.app.cur_params["n_in"]()[0]
        num_shells_out= self.app.cur_params["n_out"]()[0]

        shell_thick_in= actual_radius_cell_mm / num_shells_in * 1000
        #shell_thick_out= (actual_thickness_euf_mm - actual_radius_cell_mm) / num_shells_out * 1000
        shell_thick_out= actual_thickness_euf_mm / num_shells_out * 1000

        self.arrowPen= wx.Pen(wx.BLACK,width=4,style=wx.PENSTYLE_SOLID)
        self.linePen= wx.Pen(wx.BLACK,width=2,style=wx.PENSTYLE_SOLID)

        ctx = wx.lib.wxcairo.ContextFromDC(dc)

        ### 1mm Scale line
        # the line
        ctx.set_line_width(2)
        line_y=5
        ctx.move_to( 5, line_y )
        ctx.line_to( 5 + one_mm_line, line_y )
        ctx.set_source_rgba( 0,0,0, 1 )
        line_y_lower= ctx.stroke_extents()[3]
        ctx.stroke()
        # the text
        the_text= '1.00 mm'
        spacing= 2
        face = wx.lib.wxcairo.FontFaceFromFont(wx.FFont(10, wx.SWISS))#, wx.FONTFLAG_BOLD))
        ctx.set_font_face(face)
        ctx.set_font_size(16)
        x_bearing, y_bearing, width, height, xadvance, yadvance = ctx.text_extents(the_text)
        #print(x_bearing, y_bearing, width, height, xadvance, yadvance )
        #print( ctx.font_extents() )
        #ctx.move_to((5 + one_mm_line + width -x_bearing ) / 2, 5 + height )
        text_y= line_y_lower + height + spacing
        ctx.move_to((5 + one_mm_line ) / 2, text_y )
        ctx.set_source_rgb(0, 0, 0)
        ctx.show_text(the_text)

        ### CELL ###
        ## Cell Body
        ptn= cairo.RadialGradient( cx, cy, 0, cx, cy, radius_cell )
        ptn.add_color_stop_rgba( 0, *self.rgb.icfi, 1.0 )
        ptn.add_color_stop_rgba( 1, *self.rgb.icfo, 1.0 )
        ctx.set_source( ptn )
        ctx.arc(cx, cy, radius_cell, 0, math.pi*2)
        #print( 'rad=', radius_cell )
        #print( 'cell>', ctx.fill_extents() )
        ctx.fill()
        #print( 'cell>', ctx.fill_extents() )

        # Membrane
        membrane_line_width= 3
        ctx.set_line_width(membrane_line_width)
        # Membrane - outer
        ctx.set_source_rgba( *self.rgb.memsurf, 1 )
        ctx.arc(cx, cy, radius_cell, 0, math.pi*2)
        #print( '1', ctx.stroke_extents() )
        ctx.stroke()
        #print( '2', ctx.stroke_extents() )
        # Membrane - middle
        ctx.set_source_rgba( *self.rgb.memcent, 1 )
        ctx.arc(cx, cy, radius_cell - membrane_line_width, 0, math.pi*2)
        #print( '1', ctx.stroke_extents() )
        ctx.stroke()
        #print( '2', ctx.stroke_extents() )
        # Membrane - inner
        ctx.set_source_rgba( *self.rgb.memsurf, 1 )
        ctx.arc(cx, cy, radius_cell - 2*membrane_line_width, 0, math.pi*2)
        #print( '1', ctx.stroke_extents() )
        ctx.stroke()
        #print( '2', ctx.stroke_extents() )

        #EUF
        euf_start= membrane_line_width / 2 + radius_cell
        ptn= cairo.RadialGradient( cx, cy, euf_start, cx, cy, radius_euf )
        ptn.add_color_stop_rgba( 0, *self.rgb.eufi, 1.0 )
        ptn.add_color_stop_rgba( 1, *self.rgb.eufo, 1.0 )
        ctx.set_source( ptn )
        ctx.arc(cx, cy, euf_start, 0, math.pi*2)
        ctx.arc(cx, cy, radius_euf, 0, math.pi*2)
        ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        #print( 'euffill', ctx.fill_extents() )
        ctx.fill()
        # EUF : outer ring highlight
        if self.app.cur_sim_type == 'JTB_2012':
            ctx.set_source_rgba( *hex_to_float( 0xb5e0ff ), 1 )
            ctx.arc(cx, cy, radius_euf, 0, math.pi*2)
            ctx.stroke()
 
        # Cell Radius
        ctx.set_source_rgba( *self.rgb.rad, 1 )
        ctx.move_to(cx, cy)
        ctx.line_to( cx + radius_cell, cy )
        li,lj,lk,ll= ctx.stroke_extents()
        ctx.stroke()
        self.arrowhead( ctx, *self.rgb.rad, cx, cy, cx + radius_cell, cy, 7)
        self.arrowhead( ctx, *self.rgb.rad, cx + radius_cell, cy, cx, cy, 7)

        angle=0
        textlines= [ #'%s'%angle,
                     '%0.0f \u00b5m'%(actual_radius_cell_mm*1000),
                     '%d shells'%(num_shells_in),
                     '%0.2f \u00b5m/shell'%(shell_thick_in),
                   ]
        self.angled_linetext( ctx, 0, li,lj,lk,ll, textlines )

        ### EUF ###
        ## EUF Short Radius
        angle = -30
        xs,ys = self.PolarToCartesian( euf_start, angle, cx, cy)
        xe,ye = self.PolarToCartesian( radius_euf+30, angle, cx, cy)
        textlines= [ #'%s'%angle,
                     '%0.0f \u00b5m'%(actual_thickness_euf_mm*1000),
                     '   %d shells'%(num_shells_out),
                     '      %0.2f \u00b5m/shell'%(shell_thick_out),
                   ]

        ctx.set_source_rgba( *self.rgb.rad, 1 )
        ctx.move_to(xs, ys)
        ctx.line_to(xe, ye)
        li,lj,lk,ll= ctx.stroke_extents()
        ctx.stroke()

        self.arrowhead( ctx, *self.rgb.rad, xs, ys, xe, ye)
        self.arrowhead( ctx, *self.rgb.rad, xe, ye, xs, ys)

        self.angled_linetext( ctx, angle, xs,ys,xe,ye, textlines)
        #TODO Move EUF to here above the line
        #TODO   pretxt and posttext
        #TODO Add ICF in middle
        #TODO Add Bulk(BECF) in top right blue area

        eq_top = int(cy * 1.75 + 50)
        #print('eq_top= ', eq_top)
        for eq in self.app.equations.values():
            if eq['visible'] == True:
                bm = eq[ 'bm' ]
                #print('bm h:',bm.GetHeight(),'bm w:', bm.GetWidth())
                eq[ 'p' ] = dc.DrawBitmap( bm, cx - int(bm.GetWidth()/2) , eq_top)
                eq_top += bm.GetHeight()

        ## EUF Circle
        #dc.SetPen(wx.Pen('#0000FF', width=3))
        angle = 30
        #dc.DrawCircle(center_pt, radius_euf)
        ## EUF Radius
        #loc = self.PolarToCartesian( radius_euf, angle, center[0], center[1] )
        #dc.DrawLine( center_pt[0],center_pt[1], loc[0], loc[1])
        ## EUF Title
        loc = self.PolarToCartesian( (radius_euf - 5), angle + 10, cx, cy)
        dc.DrawRotatedText( 'EUF', int(loc[0]), int(loc[1]),-(90-(angle + 10)))
        #text1= '%0.0f \u00b5m'%(actual_radius_euf_mm*1000)
        #extsx= dc.GetTextExtent(text1)[0]
        #loc = self.PolarToCartesian( (radius_euf - extsx)/2, angle, center[0], center[1] )
        #dc.DrawRotatedText( text1, loc[0], loc[1],angle)

        # SHELL MARKERS
        sm_line_width= 1
        ctx.set_line_width(sm_line_width)
        ctx.set_source_rgba( *self.rgb.arrow, 1 )
        r_per_shell_in  = radius_cell / num_shells_in
        r_per_shell_out = (radius_euf - radius_cell) / num_shells_out

        def arrow_at(rad, angle, off=5, deg=-45, length=150, **overrides):
            xe,ye = self.PolarToCartesian( rad, angle, cx, cy)
            xlinestart,ylinestart = self.offset(xe,ye,off,deg)
            if 'xlinestart' in overrides:
                xlinestart=overrides['xlinestart']
            if 'ylinestart' in overrides:
                ylinestart=overrides['ylinestart']
            ctx.move_to(xlinestart ,ylinestart)

            xtext,ytext= self.offset(xlinestart,ylinestart,length,deg)
            if 'xtext' in overrides:
                xtext=overrides['xtext']
            if 'ytext' in overrides:
                ytext=overrides['ytext']
            ctx.line_to(xtext, ytext)
            self.arrowhead( ctx, *self.rgb.arrowtxt, xtext, ytext, xlinestart, ylinestart, length=20, deg=math.pi * .15)
            ctx.stroke()
            ctx.move_to(xtext +5,ytext + height/2)
            ctx.show_text(the_text)
            return xlinestart,ylinestart,xtext,ytext
      
        # equal lenth
        ''' l = r1 * as * math.pi = r2 * 2 * math.pi '''

        divider=2
        rings = range(0,num_shells_in,divider)
        lrings = len(rings)
        scale= 5
        ''' arc angles starts at pos x axis and goes clockwise UGH!!!'''
        for ii,i in enumerate(rings):
            ctx.new_sub_path()
            r_ring = i * r_per_shell_in
            sa_arc= 9*math.pi/8
            ea_arc= 10*math.pi/8
            #print(ii,i,'r_ring=',r_ring,'r_per_shell_in=',r_per_shell_in)
            ea_arc= (11-i/num_shells_in)*math.pi/8
            #print('SAEA:', sa_arc, ea_arc)
            ctx.arc(cx, cy, r_ring, sa_arc, ea_arc)
            ctx.stroke()

        text_offset = radius_cell / 4

        #the_text= 'Shell 0'
#        x_bearing, y_bearing, width, Xheight, Xxadvance, Xyadvance = ctx.text_extents(the_text)
        ea = 2*math.pi - ea_arc
        angle = math.degrees(ea)

        the_text= 'Shell 0 = Center of Cell'
        xlinestart,ylinestart,xtext,ytext=\
            arrow_at( divider*r_per_shell_in/2, angle, length=80, deg=-40  )

        the_text= 'Shell %d = Membrane'%(num_shells_in)
        xlinestart,ylinestart,xtext,ytext=\
            arrow_at( radius_cell, angle,  length=80, deg=-20  )

        the_text= 'Shell %d = At Inner Surface'%(num_shells_in-1)
        xlinestart,ylinestart,xtext,ytext=\
            arrow_at( radius_cell - 2 * membrane_line_width - divider*r_per_shell_in/2, angle, length=80, deg=0, xtext=xtext  )

        divider=10
        rings = range(0,num_shells_out,divider)
        lrings = len(rings)
        scale= 5
        ''' arc angles starts at pos x axis and goes clockwise UGH!!!'''
        for ii,i in enumerate(rings):
            ctx.new_sub_path()
            r_ring = radius_cell + (i * r_per_shell_out)
            ctx.arc(cx, cy, r_ring, sa_arc, ea_arc)
            ctx.stroke()

        the_text= 'Shell %d = Edge of EUF'%(num_shells_in+num_shells_out)
        xlinestart,ylinestart,xtext,ytext=\
            arrow_at( radius_euf, angle, deg=-60, length=100 + 2.0*height )#, xlinestart=40 )
        the_text= 'Shell %d = At Outer Surface'%(num_shells_in+1)
        xlinestart,ylinestart,xtext,ytext=\
            arrow_at( radius_cell + 2 * membrane_line_width - divider*r_per_shell_out, angle,
                deg=-60, length=100,
                )#xtext=xtext, ytext=ytext+height*2.0 )
        
        #Vesicles
        vpink= hex_to_float( 0xFFCDE6 )
        vbrown= hex_to_float( 0x0B0706 )
        rings = range(0,num_shells_in)
        idx= int(0.9*len(rings))
        #print(rings)
        #print(idx)
        ves_rings = np.arange(idx,idx + 5)*r_per_shell_in
        #print(ves_rings)
        vesdel = ves_rings[-1] - ves_rings[0]
        sa=150
        ea=360
        oos_tort_lambda= self.app.cur_params["oos_tort_lambda"]()[0]
        density=oos_tort_lambda/0.125# 1.0#1.0
        for ri,vr in enumerate(ves_rings):
            #print(ri)
            a=np.arange(sa,ea) + (np.random.random_sample(ea-sa)-0.5)
            degs= np.random.choice(a,int(90*density))
            for deg in degs:
                #print(deg)
                vrad=vr+np.random.random()*0.1
                ctx.new_sub_path()
                icx, icy = self.PolarToCartesian(vrad, deg, cx, cy)
                #print(vrad,deg,icx,icy)
                thisr= np.random.random_sample()*r_per_shell_in #+r_per_shell_in/2.0
                ctx.set_source_rgb( *vpink )
                ctx.arc(icx, icy, thisr, 0, 360)
                #ctx.set_source_rgba( *vbrown, 0.01 )
                #ctx.arc(icx, icy, thisr*1.2, 0, 360)
                ctx.stroke()
                #ctx.fill()

        if self.rendercount %100 == 0:
            print(f'CP_Oocyte:render DONE rendercount={self.rendercount}')


class InputError(Exception):
    pass

from operator import add
class ModelApp(object):
    '''The app'''
    #pylint: disable=too-many-instance-attributes, too-many-statements
    def sims(self,nvi='v',li='i'):
        ''' 'n','v','i'= names, values, items
            'l','i'= list, iterator
        '''
        rv= { 'n' : myParams.keys,
              'v' : myParams.values,
              'i' : myParams.items
            }[nvi]()
        return { 'i' : rv,
                 'l' : list(rv)}[li]

    def papers(self,nvi='v',li='i',sim_name=None):
        ''' 'n','v','i'= names, values, items
            'l','i'= list, iterator
        '''
        if not sim_name:
            sim_name= self.cur_sim_type
        rv= { 'n' : myParams[sim_name].keys,
              'v' : myParams[sim_name].values,
              'i' : myParams[sim_name].items
            }[nvi]()
        return { 'i' : rv,
                 'l' : list(rv)}[li]

    def figures(self,nvi='v',li='i',sim_name=None,paper_name=None):
        ''' 'n','v','i'= names, values, items
            'l','i'= list, iterator
        '''
        if not sim_name:
            sim_name= self.cur_sim_type
        if not paper_name:
            paper_name= self.cur_paper
        rv= { 'n' : myParams[sim_name][paper_name].keys,
              'v' : myParams[sim_name][paper_name].values,
              'i' : myParams[sim_name][paper_name].items
            }[nvi]()
        return { 'i' : rv,
                 'l' : list(rv)}[li]

    def __init__(self, myargs):
        self.myargs=myargs
        if myargs.testing:
            self.TESTING = True
        else:
            self.TESTING = False

        self.on_val_funcs= {\
            'update_buffs'   :self.update_buffs,
            'sel_newspecies' : self.sel_newspecies,
            'sel_newgenbkg'  : self.sel_newgenbkg,
            'sel_newgenotype': self.sel_newgenotype,

        }

        if USE_MATLAB:
            self.matlab_eng = None
        elif USE_OCTAVE:
            self.oc = oct2py.Oct2Py()#executable='/home/dhuffman/octave/bin/octave')

        self.cur_sim_type= self.sims('n','l')[0]
        print(f'\ncur_sim_type={self.cur_sim_type}')

        self.cur_paper= self.papers('n','l')[0]
        print(f'\ncur_paper={self.cur_paper}\n')

        self.cur_fig= self.figures('n','l')[0]

        self.wxapp = wx.App()
        hn= socket.gethostname()
        #print(f'HN: {hn}')
        ww=2500
        wh=1600
        if hn in ['cheliax',] :
            #mypos= (3800,100) # 3mon
            mypos= (2000,100) # 2mon
            ww=2200
            wh=1600
        elif hn in ['egorian',] :
            mypos= (800,64)
            ww=2200
            wh=1400
        elif hn in ['opti','tomahawk'] :
            ww=2200
            wh=1400
            #mypos= (2500,32)
            mypos= (200,32)
        else:
            #mypos= (1920,0)
            mypos= (0,32)

        self.frame = wx.Frame(None, wx.ID_ANY, f'Modelling Front End ({program_version})', pos=mypos, size=(ww,wh))
        #print( 'FGBC =',self.frame.GetBackgroundColour() )
        self.frame.SetBackgroundColour((249,249,248,255))#wx.NullColour)
        #print( 'FGBC =',self.frame.GetBackgroundColour() )
        self.panel = scrolled.ScrolledPanel(self.frame, wx.ID_ANY, name='main_panel')
        #print( 'SPGBC=',self.panel.GetBackgroundColour() )
        self.panel.SetBackgroundColour((249,249,248,255))#wx.NullColour)
        #print( 'SPGBC=',self.panel.GetBackgroundColour() )

        spacer_size= 20
        v_spacer_size= 10

        self.t_sim_type = wx.StaticText(self.panel, wx.ID_ANY, 'Simulation Type: ')
        self.c_sim_type = wx.Choice(    self.panel, wx.ID_ANY, choices=self.sims('n','l'), name='SimTypes')
        self.t_sim_type.SetForegroundColour( wx.BLACK )
        self.c_sim_type.Bind(wx.EVT_CHOICE, self.OnSelectSimType)
        self.c_sim_type.SetSelection(0)

        self.t_load_def       = wx.StaticText(self.panel, wx.ID_ANY, 'Load Default Parameters for: ')
        self.t_load_def_paper = wx.StaticText(self.panel, wx.ID_ANY, 'Paper:')
        self.c_load_def_paper = wx.Choice(    self.panel, wx.ID_ANY, choices=self.papers('n','l'), name='Paper')
        self.t_load_def_fig   = wx.StaticText(self.panel, wx.ID_ANY, 'Figure:')
        self.c_load_def_fig   = wx.Choice(    self.panel, wx.ID_ANY, choices=['',], name='Fig')
        self.t_load_def.SetForegroundColour( wx.BLACK )
        self.t_load_def_paper.SetForegroundColour( wx.BLACK )
        self.t_load_def_fig.SetForegroundColour( wx.BLACK )
        self.c_load_def_paper.Bind(wx.EVT_CHOICE, self.OnSelectPaper)
        self.c_load_def_fig.Bind(wx.EVT_CHOICE, self.OnSelectFigure)
        self.c_load_def_paper.SetSelection(0)
        self.c_load_def_fig.SetSelection(0)
        
        self.t_load_cust = wx.StaticText(self.panel, wx.ID_ANY, 'Load Custom Parameters File: ')
        self.b_load_cust = wx.Button(self.panel, wx.ID_ANY, label='Load')
        self.t_load_cust.SetForegroundColour( wx.BLACK )
        self.b_load_cust.Bind(wx.EVT_BUTTON, self.OnLoadParamFile)

        self.t_load_sim = wx.StaticText(self.panel, wx.ID_ANY, 'Load Sim Data Files: ')
        self.b_load_sim = wx.Button(self.panel, wx.ID_ANY, label='Load')
        self.t_load_sim.SetForegroundColour( wx.BLACK )
        self.b_load_sim.Bind(wx.EVT_BUTTON, self.OnLoadSimData)

        br_acv_al = wx.RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT
        bl_acv_ar = wx.LEFT  | wx.ALIGN_CENTER_VERTICAL# | wx.ALIGN_RIGHT

        self.hsiz_simt = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_simt.Add( self.t_sim_type          , 0, br_acv_al, border=5 ) #pylint: disable=bad-whitespace
        self.hsiz_simt.Add( self.c_sim_type          , 0, bl_acv_ar, border=5 ) #pylint: disable=bad-whitespace

        self.hsiz_load_def = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_load_def.Add( self.t_load_def      , 0, br_acv_al, border=5 ) #pylint: disable=bad-whitespace
        self.hsiz_load_def.AddSpacer(spacer_size)
        self.hsiz_load_def.Add( self.t_load_def_paper, 0, br_acv_al, border=5 ) #pylint: disable=bad-whitespace
        self.hsiz_load_def.Add( self.c_load_def_paper, 0, bl_acv_ar, border=5 ) #pylint: disable=bad-whitespace
        self.hsiz_load_def.AddSpacer(spacer_size)
        self.hsiz_load_def.Add( self.t_load_def_fig  , 0, br_acv_al, border=5 ) #pylint: disable=bad-whitespace
        self.hsiz_load_def.Add( self.c_load_def_fig  , 0, bl_acv_ar, border=5 ) #pylint: disable=bad-whitespace

        self.hsiz_load_cust = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_load_cust.Add( self.t_load_cust    , 0, br_acv_al, border=5 ) #pylint: disable=bad-whitespace
        self.hsiz_load_cust.Add( self.b_load_cust    , 0, bl_acv_ar, border=5 ) #pylint: disable=bad-whitespace
        self.hsiz_load_sim = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_load_sim.Add( self.t_load_sim     , 0, br_acv_al, border=5 ) #pylint: disable=bad-whitespace
        self.hsiz_load_sim.Add( self.b_load_sim     , 0, bl_acv_ar, border=5 ) #pylint: disable=bad-whitespace

        self.vsiz_load = wx.BoxSizer(wx.VERTICAL)
        self.vsiz_load.Add(self.hsiz_load_def        , 0, wx.ALL , border=5)
        self.vsiz_load.Add(self.hsiz_load_cust       , 0, wx.ALL , border=5)
        self.vsiz_load.Add(self.hsiz_load_sim        , 0, wx.ALL , border=5)

        self.hsiz_sim_load = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_sim_load.Add( self.hsiz_simt       , 0, wx.ALIGN_CENTER_VERTICAL )
        self.hsiz_sim_load.AddSpacer(spacer_size)
        self.hsiz_sim_load.Add( self.vsiz_load       , 0, wx.ALIGN_CENTER_VERTICAL )

        ### Save/Run Current Simulation ###
        self.t_save_cur_params = wx.StaticText(self.panel, wx.ID_ANY, 'Save Parameters Only without Running Simulation')
        self.b_save_cur_params = wx.Button(    self.panel, wx.ID_ANY,  label='Save Only')
        self.t_run_cur_sim     = wx.StaticText(self.panel, wx.ID_ANY, 'Set Ouput Folder, Save Parameters and Run Simulation')
        self.b_run_cur_sim     = wx.Button(    self.panel, wx.ID_ANY,  label='Run Simulation')
        self.t_save_cur_params.SetForegroundColour( wx.BLACK )
        self.t_run_cur_sim.SetForegroundColour( wx.BLACK )
        self.b_save_cur_params.Bind(wx.EVT_BUTTON, self.OnSaveCurParams)
        self.b_run_cur_sim    .Bind(wx.EVT_BUTTON, self.OnRunSim)
        self.b_run_cur_sim.SetBackgroundColour((244,100,100,255))
        self.b_run_cur_sim.SetMinSize(self.b_run_cur_sim.GetSize()*1.1)
        self.b_save_cur_params.SetMinSize(self.b_run_cur_sim.GetSize())

        self.hsiz_save_cur_params = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_save_cur_params.AddSpacer(v_spacer_size)
        self.hsiz_save_cur_params.Add( self.b_save_cur_params, 0, wx.EXPAND )# | wx.ALIGN_CENTER_VERTICAL)
        self.hsiz_save_cur_params.AddSpacer(spacer_size)
        self.hsiz_save_cur_params.Add( self.t_save_cur_params, 0, wx.EXPAND )# | wx.ALIGN_CENTER_VERTICAL)

        self.hsiz_run_cur_sim = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_run_cur_sim.AddSpacer(v_spacer_size)
        self.hsiz_run_cur_sim.Add( self.b_run_cur_sim, 0, wx.EXPAND )#| wx.ALIGN_CENTER_VERTICAL)
        self.hsiz_run_cur_sim.AddSpacer(spacer_size)
        self.hsiz_run_cur_sim.Add( self.t_run_cur_sim, 0, wx.EXPAND )#| wx.ALIGN_CENTER_VERTICAL)

        # Fig Buttons
        self.hsiz_cur_button= wx.BoxSizer(wx.HORIZONTAL)
        self.t_jspecific_figs  = wx.StaticText(self.panel, wx.ID_ANY, label=f'Valid SimType-Paper Figures:')
        self.t_jspecific_figs.SetForegroundColour( wx.BLACK )
        self.hsiz_cur_button.Add( self.t_jspecific_figs, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT, border=5 ) 

#PAR        self.fig_buttons= {}
#PAR        for st in self.sim_types:
#PAR            for cp,cpv in self.param_groups[st].items():
#PAR                dprint(DBG_PF, '\ncp=', cp, 'cpv(keys)=', list(cpv.keys()) )
#PAR                for sim,simv in cpv.items():
#PAR                    dprint(DBG_PF,'  sim=',sim,'simv[valid_figs]=',simv['valid_figs'])
#PAR                    for i,vf in enumerate(simv['valid_figs']):
#PAR                        dprint(DBG_PF,'    vf=',vf)
#PAR                        but_name = '%s %s'%(cp,vf)
#PAR                        dprint(DBG_PF,'    but_name=',but_name)
#PAR                        try:
#PAR                            self.fig_buttons[but_name]
#PAR                        except KeyError:
#PAR                            b= wx.Button(self.panel, wx.ID_ANY, label=vf)
#PAR                            b.SetBackgroundColour((0xaa,0x0,0xff,255))
#PAR                            b.Bind(wx.EVT_BUTTON, lambda e, figname=vf : self.OnCreateFigure(e,figname))
#PAR#                        b.Disable()
#PAR                            self.hsiz_cur_button.Add( b, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, border=5 )
#PAR                            self.fig_buttons[but_name]=b
#PAR                        dprint(DBG_PF,'  fig_buts[keys]=',list(self.fig_buttons.keys()) )
        #hprint('making buttons')
        #pprint.pp(myParams)
        self.fig_buttons= {}
        for sim_n,sim in self.sims('i','i'):
            for paper_n,paper in self.papers('i','i',sim_n):
                for fig_n,fig in paper.items():
                    #dprint(DBG_PF,'  fig_n=',fig_n,'fig["params"]["valid_figs"]=',fig['valid_figs'])
                    for i,vf in enumerate(fig['valid_figs']):
                        dprint(DBG_PF,'\n    vf=',vf)
                        but_name = '%s %s'%(paper_n,vf)
                        dprint(DBG_PF,'    but_name=',but_name)
                        try:
                            self.fig_buttons[but_name]
                        except KeyError:
                            b= wx.Button(self.panel, wx.ID_ANY, label=vf)
                            b.SetBackgroundColour((0xaa,0x0,0xff,255))
                            b.Bind(wx.EVT_BUTTON, lambda e, figname=vf : self.OnCreateFigure(e,figname))
#                        b.Disable()
                            self.hsiz_cur_button.Add( b, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, border=5 )
                            self.fig_buttons[but_name]=b
        dprint(DBG_PF,'  fig_buts[keys]=',list(self.fig_buttons.keys()) )

        self.vsiz_save_run = wx.BoxSizer(wx.VERTICAL)
        self.vsiz_save_run.Add( self.hsiz_save_cur_params, 1, wx.EXPAND)
        self.vsiz_save_run.AddSpacer(5)
        self.vsiz_save_run.Add( self.hsiz_run_cur_sim , 1, wx.EXPAND) #pylint: disable=bad-whitespace
        self.vsiz_save_run.AddSpacer(5)
        self.vsiz_save_run.Add( self.hsiz_cur_button , 0 )#, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT )

        ### Current Sim and Output ###
        self.l_sim_outputf = wx.StaticText(self.panel, wx.ID_ANY, 'Output Folder: ')
        self.t_sim_outputf = wx.TextCtrl(  self.panel, wx.ID_ANY, '<NOT SET>' )
        self.l_sim_current = wx.StaticText(self.panel, wx.ID_ANY, 'Current Param File: ' )
        self.t_sim_current = wx.TextCtrl(  self.panel, wx.ID_ANY, '')

        self.l_sim_outputf.SetForegroundColour( wx.BLACK )
#       self.l_sim_outputf.SetBackgroundColour((255,25,255,255))
        self.l_sim_outputf.SetMinSize((150,-1))
        self.t_sim_outputf.SetForegroundColour( wx.BLACK )
        self.t_sim_outputf.SetBackgroundColour((255,255,255,255))
        self.t_sim_outputf.SetEditable(False)
        #self.t_sim_outputf.SetMinSize((400,-1))

        self.l_sim_current.SetForegroundColour( wx.BLACK )
        self.l_sim_current.SetMinSize((150,-1))
#       self.l_sim_current.SetBackgroundColour((255,25,255,255))
        self.t_sim_current.SetForegroundColour( wx.BLACK )
        self.t_sim_current.SetBackgroundColour((255,255,255,255))
        self.t_sim_current.SetEditable(False)
        #self.t_sim_current.SetMinSize((400,-1))

        #v_size= (self.b_load_cust.GetSize()[1] - self.l_sim_outputf.GetSize()[1])/2
        #v_size=v_size * 10
        #self.t_sim_outputf.SetSize((-1,v_size))
        #bhou= wx.StaticBox(self.panel, wx.ID_ANY, 'BHOU')
        #self.hsiz_outfold = wx.StaticBoxSizer(bhou,wx.HORIZONTAL)
        self.hsiz_outfold = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_outfold.Add( self.l_sim_outputf, 1, wx.ALIGN_LEFT ) #pylint: disable=bad-whitespace
        self.hsiz_outfold.AddSpacer(spacer_size)
        self.hsiz_outfold.Add( self.t_sim_outputf, 4, wx.ALIGN_LEFT | wx.EXPAND  ) #pylint: disable=bad-whitespace

        #bcurp= wx.StaticBox(self.panel, wx.ID_ANY, 'BCURP')
        #self.hsiz_curpfile = wx.StaticBoxSizer(bcurp,wx.HORIZONTAL)
        self.hsiz_curpfile = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_curpfile.Add( self.l_sim_current, 1, wx.ALIGN_LEFT ) #pylint: disable=bad-whitespace
        self.hsiz_curpfile.AddSpacer(spacer_size)
        self.hsiz_curpfile.Add( self.t_sim_current, 4, wx.ALIGN_LEFT | wx.EXPAND  ) #pylint: disable=bad-whitespace

        #boutcur = wx.StaticBox(self.panel, wx.ID_ANY, 'BOUTCUR')
        #self.vsiz_outcur = wx.StaticBoxSizer(boutcur,wx.VERTICAL)
        self.vsiz_outcur = wx.BoxSizer(wx.VERTICAL)
        self.vsiz_outcur.Add( self.hsiz_outfold, 0, wx.EXPAND)
        self.vsiz_outcur.AddSpacer(v_spacer_size)
        self.vsiz_outcur.Add( self.hsiz_curpfile, 0, wx.EXPAND)

        # Custom Figures x vs time
        headfont= wx.Font(14,wx.DEFAULT,wx.NORMAL,wx.BOLD)
        #self.t_cust_head = wx.StaticText(  self.panel, wx.ID_ANY, label='Custom Figures:')
        self.t_cust_note = wx.StaticText(  self.panel, wx.ID_ANY, label='Notation:\nsingle values and start:stop:step ranges\n4 9:2:17 50 => 4,9,11,13,15,50\nnegative counts from end => -1 = last value in series')
        #self.t_cust_head.SetFont( headfont )
        #self.t_cust_head.SetForegroundColour( wx.BLACK )
        self.t_cust_note.SetForegroundColour( wx.BLACK )

        self.c_matlab= [  'CO_2',      'H_2CO_3',          'HA_1',      'H^{+}',    'HCO_3^{-}',        'A_1^{-}'       ]
        self.c_ptype = [  'linear',    'linear',           'linear',    'pH',       'linear',           'linear'        ]
        self.c_python= [ u'CO\u2082', u'H\u2082CO\u2083', u'HA\u2081', u'H\u207A', u'HCO\u2083\u207B', u'A\u2081\u207B' ]
        self.c_ascii = [  'CO2',       'H2CO3',            'HA',        'H',        'HCO3',             'A'             ]
        self.c_fig_solute  = wx.Choice(self.panel, wx.ID_ANY, choices=self.c_python, name='Solute')
        self.c_fig_solute.SetSelection(0)

        self.l_fig_shells = wx.StaticText( self.panel, wx.ID_ANY, label='Shells:')
        self.t_fig_shells = wx.TextCtrl(   self.panel, wx.ID_ANY, '0 20 40 60 78:80:1' )
        
        self.l_fig_times  = wx.StaticText( self.panel, wx.ID_ANY, label='Times:')
        self.t_fig_times  = wx.TextCtrl(   self.panel, wx.ID_ANY, '0:-1')

        self.b_fig_cust_vt= wx.Button(     self.panel,  wx.ID_ANY, label='Fig vs. Time')
        self.b_fig_cust_vs= wx.Button(     self.panel,  wx.ID_ANY, label='Fig vs. Shell')

        self.l_runs       = wx.StaticText( self.panel, wx.ID_ANY, label='Run# (If applicable):')
        self.t_fig_runs   = wx.TextCtrl(   self.panel, wx.ID_ANY, '0:-1')

        self.l_fig_shells.SetForegroundColour( wx.BLACK )
        self.t_fig_shells.SetMinSize((350,-1))
        self.t_fig_shells.SetMaxSize((350,-1))
        self.l_fig_times.SetForegroundColour( wx.BLACK )
        self.t_fig_times.SetMinSize((350,-1))
        self.t_fig_times.SetMaxSize((350,-1))
        self.b_fig_cust_vt.Bind(wx.EVT_BUTTON, lambda e, figname='custom' : self.OnCreateFigure(e,figname,'vt'))
        self.b_fig_cust_vs.Bind(wx.EVT_BUTTON, lambda e, figname='custom' : self.OnCreateFigure(e,figname,'vs'))
        self.l_runs.SetForegroundColour( wx.BLACK )

        spacer_size= 10
        x_br_acv_al = wx.EXPAND | wx.RIGHT# | wx.ALIGN_LEFT
        x_bl_acv_ar = wx.EXPAND | wx.LEFT # | wx.ALIGN_RIGHT
        x_bl_acv_al = wx.EXPAND | wx.LEFT # | wx.ALIGN_LEFT

        #bcfsh = wx.StaticBox(self.panel, wx.ID_ANY, 'BCFSH')
        #self.hsiz_cust_fig_shells = wx.StaticBoxSizer(bcfsh,wx.HORIZONTAL)
        self.hsiz_cust_fig_shells = wx.BoxSizer(wx.HORIZONTAL)
        #self.hsiz_cust_fig_shells.Add( self.l_fig_shells , 0, wx.EXPAND|wx.ALIGN_LEFT ) #pylint: disable=bad-whitespace
        #self.hsiz_cust_fig_shells.Add( self.t_fig_shells , 1, wx.ALIGN_RIGHT ) #pylint: disable=bad-whitespace
        self.hsiz_cust_fig_shells.Add( self.l_fig_shells , 1, x_br_acv_al, border=10  ) #pylint: disable=bad-whitespace
        self.hsiz_cust_fig_shells.Add( self.t_fig_shells , 3, x_bl_acv_ar, border=10 ) #pylint: disable=bad-whitespace

        #bcft = wx.StaticBox(self.panel, wx.ID_ANY, 'BCFT')
        #self.hsiz_cust_fig_times = wx.StaticBoxSizer(bcft,wx.HORIZONTAL)
        self.hsiz_cust_fig_times  = wx.BoxSizer(wx.HORIZONTAL)
        #self.hsiz_cust_fig_times.Add( self.l_fig_times   , 0, wx.EXPAND|wx.ALIGN_LEFT  ) #pylint: disable=bad-whitespace
        #self.hsiz_cust_fig_times.Add( self.t_fig_times   , 1, wx.ALIGN_RIGHT ) #pylint: disable=bad-whitespace
        self.hsiz_cust_fig_times.Add( self.l_fig_times   , 1, x_br_acv_al, border=10  ) #pylint: disable=bad-whitespace
        self.hsiz_cust_fig_times.Add( self.t_fig_times   , 3, x_bl_acv_ar, border=10 ) #pylint: disable=bad-whitespace

        self.hsiz_cust_fig_run    = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_cust_fig_run.Add( self.l_runs          , 3, x_br_acv_al, border=10  ) #pylint: disable=bad-whitespace
        self.hsiz_cust_fig_run.Add( self.t_fig_runs      , 1, x_bl_acv_al, border=10 ) #pylint: disable=bad-whitespace

        self.hsiz_fig_cust    = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_fig_cust.Add( self.b_fig_cust_vt       , 0, x_br_acv_al, border=10  ) #pylint: disable=bad-whitespace
        self.hsiz_fig_cust.Add( self.b_fig_cust_vs       , 0, x_br_acv_al, border=10  ) #pylint: disable=bad-whitespace
        
        bcfig = wx.StaticBox(self.panel, wx.ID_ANY, 'Custom Figures ')
        bcfig.SetForegroundColour(wx.BLACK)
        bcfig.SetFont( headfont )
        self.vsiz_cust_fig = wx.StaticBoxSizer(bcfig,wx.VERTICAL)
        #self.vsiz_cust_fig = wx.BoxSizer(wx.VERTICAL)
        x_lr_al = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.ALIGN_LEFT
        #self.vsiz_cust_fig.Add( self.t_cust_head         , 0, x_lr_al, border=5 ) #pylint: disable=bad-whitespace
        self.vsiz_cust_fig.Add( self.t_cust_note         , 0, x_lr_al, border=5 ) #pylint: disable=bad-whitespace
        self.vsiz_cust_fig.AddSpacer(v_spacer_size)
        self.vsiz_cust_fig.Add( self.c_fig_solute        , 0, x_lr_al, border=5 ) #pylint: disable=bad-whitespace
        self.vsiz_cust_fig.AddSpacer(v_spacer_size)
        self.vsiz_cust_fig.Add( self.hsiz_cust_fig_shells, 0, x_lr_al, border=5 ) #pylint: disable=bad-whitespace
        self.vsiz_cust_fig.AddSpacer(5)
        self.vsiz_cust_fig.Add( self.hsiz_cust_fig_times , 0, x_lr_al, border=5 ) #pylint: disable=bad-whitespace
        self.vsiz_cust_fig.AddSpacer(5)
        self.vsiz_cust_fig.Add( self.hsiz_cust_fig_run   , 0, x_lr_al, border=5 ) #pylint: disable=bad-whitespace
        self.vsiz_cust_fig.AddSpacer(v_spacer_size)
        self.vsiz_cust_fig.Add( self.hsiz_fig_cust       , 0, x_lr_al, border=5 ) #pylint: disable=bad-whitespace

        bpm= wx.StaticBox(self.panel, wx.ID_ANY, 'Parameters')
        bpm.SetForegroundColour(wx.BLACK)
        bpm.SetFont( headfont )
        self.hsiz_param_main = wx.StaticBoxSizer(bpm,wx.HORIZONTAL)
        self.hsiz_param_main.name='hsiz_param_main'
        #self.hsiz_param_main = wx.BoxSizer(wx.HORIZONTAL)

        ### Main Sizer Layout ###
        bsim = wx.StaticBox(self.panel, wx.ID_ANY, 'Simulation ')
        bsim.SetForegroundColour(wx.BLACK)
        bsim.SetFont( headfont )
        self.vsiz_sim = wx.StaticBoxSizer(bsim,wx.VERTICAL)
        #self.vsiz_sim = wx.BoxSizer(wx.VERTICAL)
        self.vsiz_sim.Add(self.hsiz_sim_load          , 0, wx.ALL, border=5 )
        self.vsiz_sim.Add(self.vsiz_save_run          , 0, wx.ALL, border=5 )
        self.vsiz_sim.Add(self.vsiz_outcur            , 0, wx.ALL | wx.EXPAND, border=5 )

        #bscf = wx.StaticBox(self.panel, wx.ID_ANY, 'BSCF')
        #self.hsiz_sim_cust_fig = wx.StaticBoxSizer(bscf,wx.HORIZONTAL)
        self.hsiz_sim_cust_fig = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_sim_cust_fig.Add( self.vsiz_sim     , 0, wx.LEFT | wx.RIGHT | wx.EXPAND, border=5 )
        self.hsiz_sim_cust_fig.Add( self.vsiz_cust_fig, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, border=5 )

        #bpc = wx.StaticBox(self.panel, wx.ID_ANY, 'BPC')
        #self.hsiz_param_cell = wx.StaticBoxSizer(bpc,wx.HORIZONTAL)

#VERITCAL_ALIGHN is problem
#in mgui2
        self.equations= collections.OrderedDict()
        self.equations['show_co2_k1'] = \
            { 'bm':wx.Bitmap('latex_stuff/co2_k1_fromweb_150.png'   , wx.BITMAP_TYPE_PNG), 'visible':False, 'storage':None }
        self.equations['show_h2co3_pk2'] = \
            { 'bm':wx.Bitmap('latex_stuff/h2co3_pk2_fromweb_150.png', wx.BITMAP_TYPE_PNG), 'visible':False, 'storage':None }
        self.equations['show_ha1_pk3'] = \
            { 'bm':wx.Bitmap('latex_stuff/ha1_pk3_fromweb_150.png'  , wx.BITMAP_TYPE_PNG), 'visible':False, 'storage':None }

        self.hsiz_param_cell = wx.BoxSizer(wx.HORIZONTAL)
        self.hsiz_param_cell.Add( self.hsiz_param_main, 0, wx.ALL | wx.EXPAND, border=5 )

        self.vsiz_main = wx.BoxSizer(wx.VERTICAL)
        self.vsiz_main.Add( self.hsiz_sim_cust_fig    , 0, wx.LEFT | wx.RIGHT | wx.EXPAND, border=5 )
        self.vsiz_main.Add( self.hsiz_param_cell      , 0, wx.LEFT | wx.RIGHT | wx.EXPAND, border=5 )

        #self.set_sim_dirs('def_sim_dir')

        # DEFAULT TO LOAD
        self.OnSelectSimType(None,simtype=myargs.simtype,paper=myargs.paper,fig=myargs.figure)
        #print('\n'*4, 'HERE\n'*10)

        self.panel.SetSizer(self.vsiz_main)
        self.panel.SetupScrolling()
        self.panel.SetAutoLayout(True)
#        self.vsiz_main.Fit(self.panel)
#        self.panel.Layout()

        ''' HERE TO SET DEF SPECIES '''
        #wx.CallLater(500, self.set_Species, 3)

        #self.panel.Bind(wx.EVT_SIZE, self.p_cell.Render())
        self.reset_run_data()

        self.frame.Show(True)

        if myargs.dosim:
            self.OnRunSim(None)
        elif myargs.sdp:
            self.loadSimData(myargs.sdp)

        if self.myargs.dofig:
            self.OnCreateFigure(None,self.myargs.dofig)

            #'/home/dhuffman/data/ProjectsW/modelling/rbc2024_find4p156/run_params_RBCO2_Fig_5PERMS.p')
        if INSPECT:
            wx.lib.inspection.InspectionTool().Show()

        self.wxapp.MainLoop()

    def set_Species(self, s):
        c= self.cur_params['Species'].wx_item
        print('ccccccccccccccccccccccccccccccccccccccccccccccccccccccc=\n  ',c)
        c.Selection= s
        wx.PostEvent(c, wx.CommandEvent(wx.wxEVT_CHOICE))

    def reset_run_data(self):
        self.run_data=[]
        self.run_time=[]
        self.run_params={}

    def sel_idx(self, seltype, arg, guichoice):
        hprint('sel_idx:',arg,guichoice)
        if arg != None:
            try: # an integer
                idx= int(arg)
                print(f'  sel_idx: from int={idx}')
            except ValueError: # a string
                idx= guichoice.FindString(arg)
                print(f'  sel_idx: found from choice list={idx}')
        else: # get it from gui
            try:
                idx= guichoice.GetSelection()
                print(f'  sel_idx: from selection= {idx}')
            except:
                idx= 0
                print(f'  sel_idx: defaulting to {idx}')

        nchoices=guichoice.GetCount()
        print(f'  sel_idx: gui nchoices= {nchoices}')
        if idx < nchoices:
            print('  selidx')
            print(f'   idx={idx}')
            print(f'   guich={guichoice}')
            guichoice.SetSelection(idx) 
            return guichoice.GetString(guichoice.GetCurrentSelection())
        else:
            print(f'Incorrect {seltype} selection index, choices are:')
            for i,idx in enumerate(range(nchoices)):
                print(f'  {i:2}: {guichoice.GetString(idx)}')


    def OnSelectSimType(self,e,simtype=None,paper=None,fig=None):
        ''' simtype is name from dropdown or index number '''
        pprint.pp(Figs)
        print(f'\nOnSelectSimType e={e}, st={simtype}, p={paper}, f={fig}')
        print('avail sime=', self.sims('n','l'))

        self.cur_sim_type= new_sim_type= self.sel_idx('Sim',simtype,self.c_sim_type)
        print(f'         : cur_sim_type set to {self.cur_sim_type}')
        
        self.c_load_def_paper.Clear()
        self.c_load_def_paper.AppendItems( self.papers('n','l',new_sim_type) )
        self.c_load_def_paper.SetSelection(0)


        try:
            self.hsiz_param_cel.Remove( self.p_cell.vs )
        except AttributeError: # On initial run
            pass

        self.OnSelectPaper(e, paper, fig, newPanel=True)
        self.setup_cell_panel()
        self.hsiz_param_cell.Add( self.p_cell.vs, 0, wx.ALL , border=5 )


    def OnSelectPaper(self,e, paper=None, fig=None, newPanel=False):
        print(f'\nOnSelectPaper: paper={paper}')
        print('cur papers=', self.papers('n','l') )

        print('OnPaperTypeCalling')
        self.cur_paper= new_paper= self.sel_idx('Paper',paper,self.c_load_def_paper)
        print(f'         : cur_paper = {self.cur_paper}')

        self.c_load_def_fig.Clear()
        self.c_load_def_fig.AppendItems(self.figures('n','l',None,new_paper))
        self.c_load_def_fig.SetSelection(0)

        self.OnSelectFigure(e,fig,newPanel)


    def OnSelectFigure(self,e,fig=None,newPanel=False):
        print(f'\nOnSelectFigure: fig={fig}')
        print('cur figs=', self.figures('n','l',None) )

        print('OnFigureTypeCalling')
        self.cur_fig= new_fig= self.sel_idx('Figure',fig,self.c_load_def_fig)
        print(f'         : cur_fig = {self.cur_fig}')

        for b in self.fig_buttons.values():
            self.hsiz_cur_button.Hide(b)

        cur_pg              = myParams[self.cur_sim_type][self.cur_paper][self.cur_fig]
        self.cur_params     = cur_pg['params']
        self.cur_params_f   = cur_pg['fname']
        self.cur_valid_figs = cur_pg['valid_figs']

        self.cur_params_tb_outs= [ p for p in self.cur_params.values() if (p.is_textbox and     p.is_output) ]
        self.cur_params_tb_ins=  [ p for p in self.cur_params.values() if (p.is_textbox and not p.is_output) ]

        self.make_param_groups()

        self.t_sim_current.SetValue( '%s'%self.cur_params_f)

        for fn in self.cur_valid_figs:
            self.hsiz_cur_button.Show(self.fig_buttons['%s %s'%(self.cur_paper,fn)])

        try:
            self.hsiz_param_main.Layout()
            self.vsiz_main.Layout()

            s=self.panel.GetSizer()
            w,h = s.GetMinSize()
            self.panel.SetVirtualSize((w,h))
            #self.frame.Layout()
            #self.frame.Refresh()
            #self.frame.Update()

            if not newPanel:
                self.p_cell.Refresh()

        except AttributeError:
            pass

    def make_param_groups(self):
        self.dialogs = {}
        self.vc_sizers_d = {}
        self.group_gbs_od = collections.OrderedDict()
        rows={}
        for param in self.cur_params.values():
            print('\nmake_param_groups:PARAM:',param.human_name,param.mlvar_name)
            if param.is_in_dialog:
                #TRYCLEARtry:
                #TRYCLEAR    param.dialog
                #TRYCLEAR    continue
                #TRYCLEARexcept AttributeError: pass
                self.make_set_dialog( param )
                vcs= param.dialog.dlg_vcs
                parent= param.dialog
            else:
                #TRYCLEARtry:
                #TRYCLEAR    param.gbs
                #TRYCLEAR    continue
                #TRYCLEARexcept AttributeError: pass
                vcs= self.make_vcs( param ) # vertical BoxSizer
                parent= self.panel

            if self.make_set_param_group_gbs( parent, param, vcs ): # Created New GBS
                rows[param.disp_grp] = 1

            try:
                param.row = rows[param.disp_grp]
            except KeyError:
                param.row= 0 # Hidden

            if param.is_button:
                #self.make_fancy_label( param )
                #param.wx_button= wx.Button(self.panel, wx.ID_ANY, label=param.wx_label)
                param.wx_button= wx.Button(parent, wx.ID_ANY, label=param.human_name)
                #print('%s,%s',param.mlvar_name,param.validator)
                #print('GA=',getattr(self, param()))
                param.wx_button.Bind(wx.EVT_BUTTON, getattr(self, param()[0]))
                param.gbs.Add(param.wx_button, (param.row, 0), (1, 1))#, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
            else:
                if param.is_output:
                    self.make_output( parent, param )
                    #param.gbs.Add(param.wx_item,   (param.row, 1), (1, 1))
                elif param.is_textbox:
                    self.make_tb( parent, param )
                    #param.gbs.Add(param.wx_item,   (param.row, 1), (1, 1), wx.EXPAND | wx.ALIGN_LEFT)
                    #param.gbs.Fit(param.wx_item)
                    #param.gbs.Layout()
                elif param.is_checkbox:
                    self.make_cb( parent, param )
                elif param.is_choice:
                    self.make_ch( parent, param )
                    #param.gbs.Add(param.wx_item,   (param.row, 1), (1, 1))
                #print('trying to add to gbs:',param.row,param.disp_grp, param.mlvar_name)
                #param.gbs.Add(param.wx_label,  (param.row, 0), (1, 1), wx.LEFT  | wx.ALIGN_LEFT  | wx.ALIGN_CENTER_VERTICAL, border=10)
                #param.gbs.Add(param.wx_item,   (param.row, 1), (1, 1), wx.LEFT|wx.RIGHT | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, border=1)
                #vs=wx.BoxSizer(wx.HORIZONTAL)
                #vs.Add(param.wx_item, wx.EXPAND|wx.GROW)
                if not param.is_hidden:
                    param.gbs.Add(param.wx_label,  (param.row, 0), (1, 1), wx.ALIGN_LEFT)#|            wx.ALIGN_CENTER_VERTICAL)
                    param.gbs.Add(param.wx_item,   (param.row, 1), (1, 1), wx.LEFT|wx.RIGHT|wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, border=5)
                    param.gbs.Layout()

                    rows[param.disp_grp] = param.row + 1

            if param.onval:
                print('\nmake_param_groups: calling onval:')
                self.on_val_funcs[ param.onval ](new_wx_item=True)

        for d in self.dialogs.values():
            d.Fit()
            d.Layout()

        self.hsiz_param_main.Clear(delete_windows=True)

        for i,(k,vcs) in enumerate(self.vc_sizers_d.items()):
            ''' SP VCS SP VCS CELL OUT '''
            vcs.Layout()
            self.hsiz_param_main.InsertSpacer(i*2,20)
            self.hsiz_param_main.Insert(i*2+1,vcs)
            #self.hsiz_param_main.Insert(i*2,vcs, wx.LEFT | wx.ALIGN_RIGHT, border=30)
            self.hsiz_param_main.Show(vcs)

    def make_vcs(self, param):
        # Vertical Column Sizer for Param Columns
        try:
            return self.vc_sizers_d[param.disp_col]
        except KeyError:
            self.vc_sizers_d[param.disp_col] = wx.BoxSizer(wx.VERTICAL)
            return self.vc_sizers_d[param.disp_col]

    def make_set_dialog(self, param):
        try:
            dlg = self.dialogs[ param.disp_grp ]
        except KeyError:
            #print('param.disp_grp', param.disp_grp)
            dlg = wx.Dialog(None, wx.ID_ANY, 'the '+param.disp_grp[2:])#, style=wx.RESIZE_BORDER)
            dlg.dlg_vcs= wx.BoxSizer(wx.VERTICAL)
            dlg.SetSizer(dlg.dlg_vcs)
            dlg.SetAutoLayout(True)
            dlg.SetMinSize(( 400, 400 )) #TODO move this to after - ceanup with setminsize

            ok_button = wx.Button(dlg, wx.ID_ANY, label='Close')
            ok_button.Bind(wx.EVT_BUTTON, lambda e,dlg=dlg:self.OnDoneEditing(e,dlg))

            self.dialogs[ param.disp_grp ] = dlg

        param.dialog= dlg

    def OnDoneEditing(self,e,dlg):
        dlg.Show(False)

    def make_set_param_group_gbs(self, parent, param, vcs):
        #print('  make_set_param_group_gbs "%s" '%(param.human_name), end='')
        col,group = param.disp_col, param.disp_grp
        if col==None or group==None:
            return False

        try:
            self.group_gbs_od[col] #print(' >>> "col" OK:', end='' )
        except KeyError:
            self.group_gbs_od[col] = collections.OrderedDict() #print(' >>> made NEW col "%s"'%(col), end='')

        try:
            param.gbs = self.group_gbs_od[col][group] #print(' >>> "group" OK:' )
        except (KeyError, NameError):
            param.gbs= self.group_gbs_od[col][group] = wx.GridBagSizer(hgap=15, vgap=2) #print(' >>> made NEW group "%s"'%(group))
            #print('made gbs:',col, group,param.gbs)
            if not param.is_in_dialog:
                param.gbs.Add(fancytext.StaticFancyText( parent, wx.ID_ANY,
                    u'<font weight="bold" color="black" size="12">%s</font>'%param.disp_grp, name=f'SFT:{param.disp_grp}'), #HERE why d_ in disp_grp for dialog stuff ???
                        (0, 0), (1, 2), wx.ALIGN_LEFT | wx.ALIGN_TOP )
                #param.gbs.AddGrowableCol(1)

            vcs.Add(param.gbs, 0, wx.TOP | wx.EXPAND | wx.GROW, border=5)
            vcs.AddSpacer(5)
            return True # New GBS Created
        return False

    def make_fancy_label(self, parent, param, db=False):
        if db:
            print('  makefl parent=', parent, 'param=', param)
        param.wx_label = fancytext.StaticFancyText(parent, wx.ID_ANY, ('%s'%param.human_name),
             background=wx.Brush((249,249,248,255),wx.SOLID), name=f'SFT:{param.mlvar_name}')
             #background=wx.Brush(wx.NullColour,wx.SOLID))#249,249,248,255))
             #background=wx.RED_BRUSH)#249,249,248,255))

    def update_buffs(self,new_wx_item=False):
        n_buffs= self.cur_params['n_buff']()[0]
        self.show_eq('show_co2_k1'   , True )
        self.show_eq('show_h2co3_pk2', True )
        self.show_eq('show_ha1_pk3'  , n_buffs >= 3)

    def sel_newspecies(self, new_wx_item=False):
        print('sel_newspecies -> update GENBKG')
        sp_p= self.cur_params['Species'    ]
        gb_p= self.cur_params['Genetic_Bkg']
        gt_p= self.cur_params['Genotype'   ]
        sp= sp_p()[0]
        gb= gb_p()[0]
        gt= gt_p()[0]
        print(f'  sp:{sp}  gb:{gb}  gt:{gt}')

        genbks= list(RBCO2_LUT[sp].keys())
        print('  genbks from LUT=',genbks)
        gb_p.choices=genbks

        if gb in gb_p.choices:
            gb_p.set_valstore([gb])
            gb_index=genbks.index(gb)
        else:
            gb_p.set_valstore([gb_p.choices[0]])
            gb_index=0
        print('  new gb=',gb_p())

        try:
            gb_p.wx_item
            gb_p.wx_item.Clear()
            gb_p.wx_item.AppendItems(genbks)
            gb_p.wx_item.SetSelection(gb_index)
        except AttributeError as e:
            print('  wx_item not yet made - dont care -should update on creation')
            print(f'  Exc={e}')

        self.sel_newgenbkg()
        print('  sel_newspecies -> SET')

    def sel_newgenbkg(self, new_wx_item=False):
        print('sel_newgenbkg -> update Genotypes')
        sp_p= self.cur_params['Species'    ]
        gb_p= self.cur_params['Genetic_Bkg']
        gt_p= self.cur_params['Genotype'   ]
        sp= sp_p()[0]
        gb= gb_p()[0]
        gt= gt_p()[0]
        print(f'  sp:{sp}  gb:{gb}  gt:{gt}')

        gts=list(RBCO2_LUT[sp][gb].keys())
        print('  gts from LUT=', gts)
        gt_p.choices=gts

        if gt in gt_p.choices:
            gt_p.set_valstore([gt])
            gt_index=gts.index(gt)
        else:
            gt_p.set_valstore([gt_p.choices[0]])
            gt_index=0

        try:
            gt_p.wx_item
            gt_p.wx_item.Clear()
            gt_p.wx_item.AppendItems(gts)
            gt_p.wx_item.SetSelection(gt_index)
        except AttributeError as e:
            print('  wx_item not yet made - dont care -should update on creation')
            print(f'  Exc={e}')

        self.sel_newgenotype()
        print('sel_newgenbkg -> SET')

    def sel_newgenotype(self, new_wx_item=False):
        #if new:
        #    print('sel_newgenotype -> NEW Return')
        #    return

        print('sel_newgenotype -> update D, MCH, MCV and others')
        sp_p= self.cur_params['Species'    ]
        gb_p= self.cur_params['Genetic_Bkg']
        gt_p= self.cur_params['Genotype'   ]
        sp= sp_p()[0]
        gb= gb_p()[0]
        gt= gt_p()[0]
        print(f'  sp:{sp}  gb:{gb}  gt:{gt}')

        mchLUTval      = RBCO2_LUT[sp][gb][gt]['MCH']
        mcvLUTval      = RBCO2_LUT[sp][gb][gt]['MCV']
        dLUTval        = RBCO2_LUT[sp][gb][gt]['Dµm']
        klysLUTval     = RBCO2_LUT[sp][gb][gt]['kHbO2_lysate']
        ko2targetLUTval= RBCO2_LUT[sp][gb][gt]['kHbO2_RBC_target']
        pmo2LUTval     = RBCO2_LUT[sp][gb][gt]['PmO2']
        print(f'  mchLUTval:{mchLUTval}  mcvLUTval:{mcvLUTval}  dLUTval:{dLUTval}  klysLUTval:{klysLUTval} PmO2:{pmo2LUTval}' )

        mchp=      self.cur_params['MCH']
        mcvp=      self.cur_params['MCV']
        dp  =      self.cur_params['Dµm'  ]
        klys=      self.cur_params['kHbO2_lysate']
        ko2target= self.cur_params['kHbO2_RBC_target']
        pmo2=      self.cur_params['Pm_O2']

        def ifLUT(p,v):
            if p.allow_LUTs:
                p.set_valstore(v)

        ifLUT(mchp     ,[mchLUTval      ])
        ifLUT(mcvp     ,[mcvLUTval      ])
        ifLUT(dp       ,[dLUTval        ])
        ifLUT(klys     ,[klysLUTval     ])
        ifLUT(ko2target,[ko2targetLUTval])
        ifLUT(pmo2     ,[pmo2LUTval     ])
        print('sel_newgenotype -> DONE')

    def show_eq(self, eq, s):
        eq= self.equations[eq]
        eq['visible'] = s

    def make_cb(self, parent, param ):
        #print('  make_cb parent=', parent, 'param=', param)
        self.make_fancy_label(parent, param)
        param.wx_item= wx.CheckBox( parent, wx.ID_ANY, '' )
        #print('make_cb:',param.mlvar_name,param(0))
        param.wx_item.SetValue(param()[0])
        param.wx_item.Bind(wx.EVT_CHECKBOX, lambda e, param=param: self.OnValChange(e, param))

    def make_ch(self, parent, param ):
        self.make_fancy_label(parent, param)#, db=True)
        #if param.human_name in ['Species','Genetic_Bkg','Genotype']:
        print(f'make_ch: {param.human_name}')
        print('make_ch: p.choices=',param.choices)
        print('make_ch: p()=', param())
        param.wx_item= wx.Choice( parent, wx.ID_ANY, choices=param.choices, name='HI' )
        #init_val= param()
        #print('init_val=', init_val)
        #param.set_valstore(init_val)
        #print('then_vals=', param())
        #print('then_val=', param()[0])
        #print('then_val=', str(param()[0]))

        param.wx_item.SetSelection(param.choices.index(str(param()[0])))
        param.wx_item.Bind(wx.EVT_CHOICE, lambda e, param=param: self.OnValChange(e, param))
        def GV():
            return param.wx_item.GetString(param.wx_item.GetSelection())
        param.wx_item.GetValue= GV


    def format_param_list(self, param):
        #print(f'fpl:formatter={param.formatter}')
        print(f'fpl: {param()}')
        #print('fpl:',[ v for v in param()] )
        #print('fpl:',', '.join( [ param.formatter.format(v) for v in param()] ))
        if param.formatter == '{}' and param.validator in [pos_float, sci_float, reg_float]:
            #print('fpl:================================')
            #print('fpl:param()=', param())
            #TODO OOPS delete/comment this line
            #TODO Use this func in create_param_files - needs single versus list - maybe func???
            #TODO move formatter/validator to the param itself and avoid any tests here
            l = [ np.format_float_positional(v) for v in param() ]
            #print('fpl:[val,formatval]',['%f  %s'%(v,np.format_float_positional(v,fractional=False,trim='0')) for v in param()])
            l = [ np.format_float_positional(v,fractional=False,trim='0') for v in param() ]
        else:
            l = [ param.formatter.format(v)     for v in param() ]
        rv= ', '.join( l )
        return rv

    def make_tb(self, parent, param ):
        self.make_fancy_label(parent, param)
        # SAVE THIS
        #defval= '{:0.4e}'.format(1234.0000e+10)
        #print('val=',defval)
        #te= param.wx_item.GetTextExtent( defval )
        #print('TE=',te)
        #self.default_tc_size= tuple(map(add,param.wx_item.GetSizeFromTextSize( te ),(20,0)))
        #print('S=',self.default_tc_size)
        #param.wx_item.SetInitialSize( s )
        # RESULT was (100,28) so just use (100,-1)
        # NOTE - doesn't seem to be a way to do this calc before the TC exists as all the functions
        #   are methods of the tc - tried making a generic one at beginning - it didn't work.
        #   so - just hardcoding the size for now.  Oh Well...
        #param.wx_item= wx.TextCtrl( parent, wx.ID_ANY, param.formatter.format(param.val), size=(100,-1), style= wx.TE_PROCESS_ENTER )
        #param.wx_item.SetInitialSize(
        #    param.wx_item.GetSizeFromTextSize(
        #        param.wx_item.GetTextExtent( val ) ) )
        #print('param=',param, param.mlvar_name)
        sz=param.wx_label.GetSize()
        #print('sz=',sz)
        param.wx_item = ColChangeInput(
            parent,
            wx.ID_ANY,
            cci_def_text= self.format_param_list(param),
            cci_size=(300,sz[1]),
            on_enter_func=lambda e, param=param: self.OnValChange(e, param),
            name=f'TC:{param.mlvar_name}',
            linspace=True,
            param=param,
        )
        #param.wx_item.SetMinSize((100,50))

    def set_modified_bg(self,param):
        param.wx_item.SetBackgroundColour('orange')

    def set_regular_bg(self,param):
        param.wx_item.SetBackgroundColour(param.wx_item.def_text_bg_color) # def_text set in CCI input and make_output for outs

    def make_output(self, parent, param ):
        #print('  make_output parent=', parent, 'param=', param)
        self.make_fancy_label(parent,param)
        if param.is_textbox:
            sz=param.wx_label.GetSize()
            param.wx_item = wx.TextCtrl( parent, wx.ID_ANY, self.format_param_list(param), size=(200,sz[1]))
        elif param.is_checkbox:
            param.wx_item= wx.CheckBox( parent, wx.ID_ANY, self.format_param_list(param))
        param.wx_item.SetEditable(False)
        param.wx_item.def_text_bg_color = (232,232,232)
        param.wx_item.SetBackgroundColour(param.wx_item.def_text_bg_color)
        param.wx_item.SetForegroundColour((0,0,0))
        param.wx_item.set_modified_bg= lambda param=param: self.set_modified_bg(param)
        param.wx_item.set_regular_bg = lambda param=param: self.set_regular_bg(param)

    def OnMobilities(self,e):
        #print('OM', self.dialogs)
        if self.dialogs['d_Mobilities'].Show():
            pass
        
    def OnBufferReactions(self,e):
        #print('OC')
        if self.dialogs['d_Buffer Reactions'].Show(): # Get these from the name in the file
            pass

    def OnPermeabilities(self,e):
        #print('OP')
        if self.dialogs['d_Permeability Across PM'].Show():
            pass

    def mark_modified(self,param):
        try:
            param.wx_item.set_modified_bg()
        except AttributeError:
            pass # not all have this method

    def mark_bad_lengths(self,ps=None):
        ''' list lengths for batch runs '''
        print('MBL:::')
        if ps == None:
            ps= self.cur_params_tb_ins
        #print('MBL::: ps=',ps)
        pvals= [ p() for p in ps ]
        print('MBL::: pvals=',len(pvals),pvals)
        lens = set([1])
        [lens.add(len(vl)) for vl in pvals]
        print('MBL::: lens=', lens)

        if len(lens) not in [1,2]: # should only be 2 lengths 1 and some higher batch_len
            for i,p in enumerate(ps):
                print('  MBL:%d:p= %s'%(i, p.mlvar_name))
                if len(p.valstore) != 1:
                    print('  MBL:==> Not1 %s'%p.mlvar_name)
                    self.mark_modified(p)
            raise InputError('!!!! Wrong number of params!!!!!!!')
        else:
            for i,p in enumerate(ps):
                print('  MBL:call set_regular_bg',p.mlvar_name)
                try: p.wx_item.set_regular_bg()
                except AttributeError: pass
        print('MBL::: DONE')
        return lens

    def update_deps_and_outs(self,param):
        #print('DEPS OUTS DEPS OUTS DEPS OUTS DEPS OUTS DEPS DEPS DEPS DEPS DEPS DEPS DEPS DEPS')
        print('deps=',[p.mlvar_name for p in param.dependents])
        print('tb_outs=',[p.mlvar_name for p in self.cur_params_tb_outs])
        for p in set( param.dependents  + self.cur_params_tb_outs ):
            dprint(DDEPS,( 'DEPS: doin: %s'%p.mlvar_name, ))
            if p.set_valstore(p()):
                p.wx_item.SetEditable(True)
                print('update_deps: setting text')
                p.wx_item.SetValue(self.format_param_list(p))
                p.wx_item.SetEditable(False)
                p.wx_item.set_regular_bg()
            else:
                print('update_deps:call mark modified')
                self.mark_modified(p)
                self.mark_modified(param)

    def OnValChange(self, e, param):
        ''' event handler for user hitting enter on a field '''
        in_vals = param.wx_item.GetValue()
        dprint(DDEPS,( f'\nOVC: {param.mlvar_name} in_vals={in_vals} {type(in_vals)}', ))
        if param.is_textbox:
            in_val_l= [ v.strip() for v in in_vals.split(',') ]
        elif param.is_checkbox:
            in_val_l= [ in_vals ] #for v in in_vals ] #bool # Only singles now
        elif param.is_choice:
            in_val_l= [ in_vals ]

        print('OVC1')
        print('OVC1a: param=',param())
        bad = True if not param.set_valstore( in_val_l ) else False
        print('OVC1b: param=',param())

        self.mark_bad_lengths()

        print('OVC2')
        if bad:
            self.mark_modified(p)
        else:
            if param.onval:
                self.on_val_funcs[ param.onval ](new_wx_item=False)

            self.update_deps_and_outs(param)
        print('OVC3')

        self.p_cell.Refresh()

    def setup_cell_panel(self):
        print(f'setup_cell_panel CurSimType: {self.cur_sim_type}' )
        #TODO Make decision - either DONT destroy like this below, just hide.
        # or - recreate all params etc.  Hiding is a memory hog.  Recreating is ???
        try:
            print(f'SCP: predestroy')# p_cell={self.p_cell}')
            self.p_cell.Destroy()
            print(f'SCP: postdestroy p_cell={self.p_cell}')
        except Exception as e:#AttributeError:
            print(f'SCP: e={e}')
            pass
        if self.cur_sim_type in ['AJP', 'JTB']:
            self.p_cell = CellPanel_Oocyte(self)
        elif self.cur_sim_type in ['RBCO2']:
            #self.p_cell = CellPanel_RBC(self)
            self.p_cell = CellPanel_RBCOPENGL(self)
        print(f'SCP: end p_cell={self.p_cell}')

        #try:
        #    self.hsiz_param_cell.Add( self.p_cell, 0, wx.ALL | wx.EXPAND, border=5 )
        #except AttributeError:
        #    pass

    def add_shape(self,shape,x,y,pen=None,brush=None,text=None):
        shape.SetX( x )
        shape.SetY( y )
        if pen: shape.SetPen( pen )
        if brush: shape.SetBrush( brush )
        if text:
            for line in text.split('\n'):
                shape.AddText(line)
        self.sc.AddShape(shape)

    def add_lineshape(self,lineshape,ends,pen=None,brush=None,arrow=None):
        lineshape.MakeLineControlPoints(2)
        lineshape.SetEnds( ends[0], ends[1], ends[2], ends[3] )
        if pen: lineshape.SetPen( pen )
        if brush: lineshape.SetBrush( brush )
        if arrow: lineshape.AddArrow( arrow )
        self.sc.AddShape(lineshape)

    def OnSaveCurParams(self, e):
        ''' event-handler - create a parameter file to be stored in the sim directory '''
        self.create_param_files()

    def set_sim_dirs(self,fullpath):
        print('set_sim_dirs: fullpath=', fullpath)
        ''' fullpath default is def_sim_dir, but status is used to ask user '''
        newdir=False

        if not fullpath:
            dlg = wx.DirDialog(self.panel,
                    message="Create/Select Simulation Output Directory",
                    defaultPath='.',
                    style=wx.DD_DEFAULT_STYLE)
            if dlg.ShowModal() == wx.ID_OK:
                fullpath=dlg.GetPath()
            else:
                fullpaht='def_sim_dir'

        if not os.path.isdir(fullpath):
            os.mkdir(fullpath)
            newdir=True

        self.sim_dir_path= fullpath
        if fullpath.endswith(os.sep):
            bn=fullpath[:-1]
        else:
            bn=fullpath
        self.sim_base_name= os.path.basename( bn )
        dprint(DBG_DIRS,'  sim_dir_path :', self.sim_dir_path)
        dprint(DBG_DIRS,'  sim_base_name:', self.sim_base_name)
        self.t_sim_outputf.SetValue( os.path.relpath(self.sim_dir_path) )
        self.t_sim_current.SetValue( self.sim_base_name )
        return newdir

    def create_param_files(self):
        ''' create a parameter file to be stored in the sim directory '''
        #TODO - possible rename this to indicate ".m" file
        #TODO - maybe an option since matlab is only 1 version - octave, sundials
        batch_len = max(self.mark_bad_lengths()) # mbl returns a set with { 1, numbatchvars } Ex. batch_len= {1, 3}
        dprint(DBG_DIRS,('batch_len=',batch_len))

        #for run_idx in range(self.mark_bad_lengths):
        self.fnl=[]
        for ri in range(batch_len): # ri = run_idx
            name_parts=[]
            vals=[]
            for p in self.cur_params.values():
                print(f'  ri:{ri}: p:{p.mlvar_name}   {p()}')
                pvals = p()

                try:
                    v=pvals[ri]
                except IndexError:
                    print('  IndexError: using 0th')
                    v=pvals[0]

                if not p.is_button:
                    if p.is_choice:
                        if p.is_string:
                            vals.append( '%s = \'%s\''%(p.mlvar_name,v) )
                        else:
                            vals.append( '%s = %s'%(p.mlvar_name,v) )
                    elif p.is_checkbox:
                        vals.append( '%s = %s'%(p.mlvar_name,{ True : 'true', False: 'false' }[v]) )
                    else:
                        if p.formatter == '{}' and p.validator in [pos_float, sci_float, reg_float]:
                            s = np.format_float_positional(v,fractional=False,trim='0')
                        else:
                            s = p.formatter.format(v)
                        if p.is_string:
                            vals.append( '%s = \'%s\''%(p.mlvar_name,s) )
                        else:
                            vals.append( '%s = %s'%(p.mlvar_name,s) )
                    if len(pvals) > 1 and not p.is_output:
                        name_parts.append( '__%s_%s'%(p.mlvar_name,s.replace('.','_')) )

                print(f'     vals[-1]: {vals[-1]}')
            name_parts = ''.join(name_parts)
            dprint(DBG_DIRS,('nameparts=',name_parts))

            fn=f'{self.sim_base_name}{name_parts}' # Matlab Funcs want the base name only - no path or '.m'
            print('fn=',len(fn),fn)

            # Matlab limit 63 char for variable name, which file becomes
            name_end='paramsIn'
            if len(fn)+len(name_end)+1 > 60:
                with open( f'LOG_long_{name_end}.txt', 'a') as logfn:
                    shortfn=fn[:30] +datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
                    logfn.write(f'SHORTFILE:{shortfn},FILE:{fn}\n')
                    fn=shortfn
            print('fn(short)=',len(fn),fn)

            fp= os.path.join( self.sim_dir_path, f'{fn}_{name_end}.m' )
            print('fp=',len(fp),fp)

            if os.path.exists(fp):
                dlg = wx.MessageDialog(None,
                                       "Simulation %s exists do you want to overwrite it?"%fp,
                                       'Overwrite!',
                                       wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
                result = dlg.ShowModal()
                if result == wx.ID_NO:
                    return False

            f = open(fp, 'w')
            flen = len(fp)+7
            f.write('''fprintf(' -> %s\\n')\n'''%('*'*flen))
            f.write('''fprintf('    * In %s *\\n')\n'''%fp)
            f.write('''fprintf('    %s\\n')\n'''%('*'*flen))
            text= ';\n'.join( vals ) + ';\n'
            print( text )
            f.write( text )
            f.close()

            self.fnl.append( fn )

        self.panel.Update()

        return True

    def OnRunSim(self, e):
        ''' run the sim event handler '''
        self.set_sim_dirs( self.myargs.sdp )
        if self.create_param_files():
            self.run_sims()

    def get_run_param(self,ri,pname):
        pvals = self.cur_params[pname]()
        print(f'pvals for {pname} = {pvals}')
        #print('rp=\n',self.run_params)

        if pname not in self.run_params:
            self.run_params[pname]=[]

        try:
            self.run_params[pname].append( pvals[ri] )
        except IndexError: # occurs when only 1 value for this but many for another prarm
            self.run_params[pname].append( pvals[0] )

    SAVETESTFILES= False
    SAVETESTFILES= True 
    def run_sims(self):
        ''' run the sim '''

        if USE_MATLAB:
            if not self.matlab_eng:
                self.matlab_eng = matlab.engine.start_matlab("-desktop")

        self.reset_run_data()
        time.sleep(1)
        totruns= len(self.fnl)
        for ri,fn in enumerate(self.fnl):
            self.t_sim_current.SetValue( '%s ( %s )'%(self.sim_base_name,fn) )
            self.panel.Update()

            progress_title= 'Simulation Time: (Run %d/%d)'%(ri+1,totruns)
            #ret_time,ret_data= self.matlab_eng.Simulate_CO2_JTB_type1_addition_only(progress_title, self.sim_dir_path, fn, nargout=2)
            
            if USE_MATLAB:
                #ret_time,ret_data= self.matlab_eng.Simulate_CO2_All(self.cur_sim_type,progress_title, self.sim_dir_path, fn, nargout=2)
                ret_time,ret_data= self.matlab_eng.Simulate(self.cur_sim_type,progress_title, self.sim_dir_path, fn, nargout=2)
            elif USE_OCTAVE:
                #ret_time,ret_data= self.oc.Simulate_CO2_All(self.cur_sim_type,progress_title, self.sim_dir_path, fn, nargout=2)
                #(ret_time,ret_data)= self.oc.feval('Simulate_CO2_All',self.cur_sim_type,progress_title, self.sim_dir_path, fn, nout=2, stream_handler=None)# verbose=False)
                (ret_time,ret_data)= self.oc.feval('Simulate',self.cur_sim_type,progress_title, self.sim_dir_path, fn, nout=2, stream_handler=None)# verbose=False)
            # OCTAVE - wait for octave 5.2 with built in ode15s is available native
            #v=octave.ones(3,3)
            #print(v)
            # tried 4.2 - no ode15s package that would work
            # tried snap verision - wouldn't work together with conda
            # gave up - didn't try flatpack
            #ret_time,ret_data= octave.Simulate_CO2_All(self.cur_sim_type, progress_title, self.sim_dir_path, fn)

            self.run_time.append(np.asarray(ret_time))
            self.run_data.append(np.asarray(ret_data))
            if self.cur_sim_type in ['AJP', 'JTB']:
                desired_run_params = [\
                    'n_in', 'n_out',
                    'D', 'D_inf',
                    'n_buff', 'pH_out', 'pH_in_init', 'Pm_CO2_input', 'cust_plot_title',
                    'CAII_in_flag' , 'CAII_in' , 'A_CAII',
                    'CAIV_out_flag', 'CAIV_out', 'A_CAIV',
                    'A1tot_in', 'A2tot_in',
                    'Buff_pc', 'oos_tort_lambda', 'tort_gamma',
                    'tf_CO2on','PlotTitle','OutFile','OutCol','FigProps','Panel', 'SweepVar'
                ]
            elif self.cur_sim_type in ['RBCO2']:
                # see paramsOut files for available
                #desired_run_params =[ cp.mlvar_name for cp in self.cur_params.values() ]
                desired_run_params = list(self.cur_params.keys())
                ''' ['Species', 'Genetic_Bkg', 'Genotype', 'MCH', 'MCV', 'Dµm', 'Dcm', 'rµm', 'rcm', 'nomat_R_TOR', 'Hbtot_in', 'tmax', 'r_sphere', 'd_euf_um', 'd_euf_cm', 'R_infcm', 'R_infµm', 'n_in', 'n_out', 'T', 'PB', 'PH2O', 'O2_pc', 'PO2', 'sO2', 'O2', 'PO2_50', 'Pm_O2', 'k_lysate', 'D_O2out', 'D_HbO2out', 'D_Hbout', 'D_O2in', 'D_HbO2in', 'D_Hbin', 'plottitle']
                '''
                desired_run_params.extend(['N', 'k37', 't37'])

            print('self.cur_params=', self.cur_params)
            didntgetlist=[]
            for rp in desired_run_params:
                print('rp=',rp)
                try:
                    self.get_run_param(ri,rp)
                except KeyError: # only in 11 12
                    didntgetlist.append(rp)
                    print('Didn\'t get %s'%rp)
            print('\n\nDIDNTGETLIST',didntgetlist)
            print(progress_title)
           
            #print(type(self.run_time))
            #print(type(self.run_time[ri]))

            dl= len(self.run_time[ri])
            f=open(os.path.join( self.sim_dir_path, f'{fn}.csv'),'w')
            [ f.write('%f,%s\n'%(self.run_time[ri][i][0],
                             ','.join(['%f'%v for v in self.run_data[ri][i]]))) for i in range(dl) ]
            f.close()
            
            pickle.dump(self.run_time  , open(self.build_fn('run_time_'  ), 'wb'))
            pickle.dump(self.run_data  , open(self.build_fn('run_data_'  ), 'wb'))
            pickle.dump(self.run_params, open(self.build_fn('run_params_'), 'wb'))

        self.t_fig_runs.Clear()
        numruns = ri+1
        self.t_fig_runs.SetValue('[' + ' '.join([ '%d'%v for v in range(numruns) ]) + ']')

        print('Simulation Completed.')

        if self.myargs.dofig:
            self.OnCreateFigure(None,self.myargs.dofig)

    def build_fn(self, prefix, includepath=True):
        ''' prefix = 'run_time_', 'run_data_', 'run_params_'
        '''
        # Example fn= 'RBCO2_Fig_5PSIGMOIDstrain'
        fn  = f'{prefix}{self.cur_sim_type}_{self.cur_fig}.p'.replace(' ','_').replace(',','_')
        if includepath:
            rfn= os.path.join( self.sim_dir_path, fn )
            print(f'build_fn: {rfn}') 
            return rfn
        else:
            print(f'build_fn: {fn}') 
            return fn

    def extract_fn(self, fn, prefix, includesPath=False):
        ''' prefix = 'run_time_', 'run_data_', 'run_params_'
        '''
        print(f'extract_fn: fn={fn}')
        pgkey=fn.replace(prefix,'').split('.')[0]
        print('  pgkey  :',pgkey)
        simtype = pgkey.split('_Fig')[0]
        print('  simtype:',simtype)
        fig=pgkey.replace(f'{simtype}_','')
        print('  figure :',fig)
        return pgkey, simtype, fig

    def load_sim_data(self):
        self.run_time  = pickle.load( open(self.build_fn('run_time_'  ), 'rb') )
        self.run_data  = pickle.load( open(self.build_fn('run_data_'  ), 'rb') )
        self.run_params= pickle.load( open(self.build_fn('run_params_'), 'rb') )

    def OnLoadSimData(self,e):
        dlg=wx.FileDialog(None, 'Choose Sim Data (run_data) File', wildcard='Sim .p files (*.p)|*.p',
            style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_CANCEL:
            return
        pathname = dlg.GetPath()
        print('OLSD: pathname=',pathname)
        self.loadSimData(pathname)

    def loadSimData(self,pathname):
        print('loadSimData:\n  pathn:',pathname)
        dirn,fn= os.path.split(pathname)
        if not fn:
            fns= glob.glob(f'{dirn}/run_data_*')
            l= len(fns)
            if l != 1:
                if l == 0:
                    msg=f'Did not find run_data_ file in {dirn}'
                elif l > 1:
                    msg=f'Found multiple run_data_ files in {dirn}'
                dlg = wx.MessageDialog(None, msg, "Sim Data Load Error!", wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
                return

            fn=fns[0] 
        print('  dirn :',dirn,'\n  filen:',fn)
       
        # TODO - why calling this , get interrupted
        # TODO pgkey, simtype, fig= self.extract_fn(fn, 'run_data_', False)
        self.set_sim_dirs(dirn)
        print('loadSimData:\n  sdp=',self.sim_dir_path)

        self.load_sim_data()

    def OnLoadParamFile(self, e):
        ''' event_handler - load a parameter file to run NOT IMPLEMENTED '''
        dlg=wx.FileDialog(None, 'Open Custom Parameter File', wildcard='Matlab .m files (*.m)|*.m',
            style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_CANCEL:
            return
        pathname = dlg.GetPath()
        with open(pathname,'r') as pfile:
            pflines= pfile.readlines()
            for l in pflines:
                #print(l)
                try:
                    mlvar,val = [ v.strip().strip(';') for v in l.split('=') ]
                    #print('mlvar=',mlvar,'val=',val)
                except ValueError: 
                    #print('Skipped line:',l)
                    continue
                #pdb.set_trace()
                try:
                    p=self.cur_params[mlvar]
                except KeyError: continue

                if (p.is_textbox or p.is_checkbox) and not p.is_output:
                    #copy from OnValChange - make generic
                    bad = True if not p.set_valstore( [val] ) else False
                    if bad:
                        #print('BAD !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                        self.mark_modified(p)
                    else:
                        self.update_deps_and_outs(p)
                    try:
                        val= { 'true':True, 'false':False }[val]
                    except KeyError: pass

                    if p.is_checkbox:
                        #print('cb',val)
                        p.wx_item.SetValue( val )
                    elif p.is_textbox:
                        #print('tb', self.format_param_list(p))
                        p.wx_item.SetValue(self.format_param_list(p))

        self.mark_bad_lengths()
        self.t_sim_current.SetValue( '%s'%(os.path.relpath(pathname)))

    def pH_from_Hplus(self, v):
        pH      = 3-np.log10(v)
        return pH

#    def electrode_index_from_um(self, um, R_cm, n_in ):
#        depth = um * 1e-4               # depth electrode in centimeters from microns
#        radii_in = (R_cm/n_in)*np.array(range(0,n_in))
#        #print('depth=',depth)
#        #print('radii_in=',radii_in)
#        electrode_idx = np.nonzero(radii_in >= R_cm-depth)[0][0] # nonzero returns tuple of arrays for each dimension of input
#        print('electrode_idx=',electrode_idx, '  rad[elec_idx]=',radii_in[electrode_idx])
#        return electrode_idx

#    def get_subst_idxs(self,sol_order,n_buff,N,n_in,n_out):
#        sol_start = sol_order * N
#        sol_memb  = sol_start + n_in
#        sol_end   = sol_memb + n_out
#        print('ss:',sol_start,'sm:',sol_memb,'se:',sol_end)
#        return sol_start, sol_memb, sol_end
#        #electrode_idx = self.electrode_index_from_um( depth, R_cm, n_in )
#        #sol = data[:, sol_start + electrode_idx ] )
#        #pHs = self.pH_from_Hplus( data[:, pH_memb + 1 ] )
#        #return pHi,pHs
#

#    def get_pH(self,data,n_buff,N,n_in,n_out,R_cm,depth_um=50):
#        pH_order = self.substances['pH'].order + (n_buff - 2)
#        ss,sm,se = self.get_subst_idxs(pH_order,n_buff,N,n_in,n_out)
#        electrode_idx = self.electrode_index_from_um( depth_um, R_cm, n_in )
#        print('eidx:',electrode_idx)
#        pHi = self.pH_from_Hplus( data[:, ss + electrode_idx ] )
#        pHs = self.pH_from_Hplus( data[:, sm + 1 ] )
#        return pHi,pHs

#    def get_ddata_dt(self,data,t):
#        dt    = np.ediff1d( t )
#        dd    = np.ediff1d( data )
#        dd_dt = dd/dt
#        max_dd_idx  = np.argmax(np.absolute(dd_dt))
#        max_dd      = dd_dt[max_dd_idx]
#        print('max_dd=',max_dd)
#        return dd_dt, max_dd_idx, max_dd
#
#    def radii_in_out(self,R_cm,R_inf_cm,n_in,n_out):
#        radii_in   =           (       R_cm / n_in  ) * np.array(range(0,n_in+1 ))
#        radii_out  = R_cm + ((R_inf_cm-R_cm)/(n_out)) * np.array(range(1,n_out+1)) # Eliminate .650 from r_out
#        return radii_in,radii_out

#    # NEW version shapes to (n,1) instead of (n,)
#    def radii_in_outNEW(self,R_cm,R_inf_cm,n_in,n_out):
#        radii_in   =           (       R_cm / n_in  ) * np.array(range(0,n_in+1 ))
#        radii_out  = R_cm + ((R_inf_cm-R_cm)/(n_out)) * np.array(range(1,n_out+1)) # Eliminate .650 from r_out
#        ishape=len(radii_in)#.shape[0]
#        oshape=len(radii_out)#.shape[0]
#        return radii_in.reshape(1,ishape) ,radii_out.reshape(1,oshape)

    ### Figure related support ###
#    shades = [\
#        ( 102/255,  51/255,       0),#  brown
#        (       0,  0.5000,       0),#  green
#        (  1.0000,       0,       0),#  red
#        (       0,  0.7500,  0.7500),#  cyan
#        (  0.7500,       0,  0.7500),#  magenta
#        ( 204/255, 153/255,       0)]#  gold
#    shades_6 = [\
#        (       0,  0.5000,       0), # green
#        (       0,       0,  1.0000), # blue
#        (  1.0000,       0,       0), # red
#        (       0,  0.7500,  0.7500), # cyan
#        (  0.7500,       0,  0.7500), # magenta
#        ( 162/255, 120/255,       0), # gold
#        (  0.2500,  0.2500,  0.2500)] # black
#    shades_7 = [\
#        (      0,        0,       1), # blue
#        (      1,     0.40,       0), # orange
#        (   0.40,     0.20,       0), # brown
#        (      0,     0.75,    0.75), # cyan
#        (   0.75,        0,    0.75), # magenta
#        ( 0.7500,   0.7500,       0), # yellow
#        ( 0.2500,   0.2500,  0.2500), # black
#        (   1.00,        0,       0), # red
#        (      0,     0.50,       0)] # green 
#    shades_8 = [\
#        ( 150/255,  75/255,       0), # brown     
#        (       0,  0.5000,       0), # green
#        (  1.0000,       0,       0), # red
#        (       0,  0.7500,  0.7500), # cyan
#        (  0.7500,       0,  0.7500), # magenta
#        ( 204/255, 153/255,       0), # gold
#        (  0.2500,  0.2500,  0.2500)] # black
#    shades_9 = [\
#        (       0,  0.5000,       0), # green
#        ( 204/255, 153/255,       0), # gold
#        (  1.0000,       0,       0), # red
#        (       0,       0,  1.0000)] # blue         
#    shades_10 = [\
#        (    0.75,    0   ,    0.75), # magenta
#        (    0   ,    0.75,    0.75), # cyan
#        (    1.00,    0   ,    0   ), # red
#        (    0   ,    0   ,    1   ), # blue
#        (    0   ,    0.50,    0   ), # green  
#        (    0   ,    0   ,    0   )] # black
#    shades_11 = [\
#        ( 0      ,       0,       1), # blue
#        ( 0      ,    0.50,       0), # green 
#        ( 1      ,    0.40,       0), # orange
#        ( 0.40   ,    0.20,       0), # brown
#        ( 204/255, 153/255,       0), # gold
#        ( 0      , 153/255, 204/255), # cyan
#        ( 0.75   ,       0,    0.75)] # magenta
#    shades_12a = [\
#        ( 0      ,       0,       0), # black (10um)
#        ( 0.75   ,       0,    0.75), # magenta(50um) 
#        ( 70/255 ,  70/255,  70/255), # (150um)
#        ( 90/255 ,  90/255,  90/255), # (250um)
#        ( 110/255, 110/255, 110/255), # (350um)
#        ( 130/255, 130/255, 130/255), # (450um)
#        ( 160/255, 160/255, 160/255), # (550um)
#        ( 190/255, 190/255, 190/255)] # (150um)       
#    shades_12b = [\
#        (       0,       0,       0), # black (10um)
#        ( 204/255, 153/255,       0), # gold  (50um)
#        ( 70/255 ,  70/255,  70/255), # (150um)
#        ( 90/255 ,  90/255,  90/255), # (250um)
#        ( 110/255, 110/255, 110/255), # (350um)
#        ( 130/255, 130/255, 130/255), # (450um)
#        ( 160/255, 160/255, 160/255), # (550um)
#        ( 190/255, 190/255, 190/255)] # (150um)  
#
#    shades_ajp4 = plt.cm.bwr(np.linspace(0.6, 0.95, 10))
    shades_ajp4 = plt.cm.bwr(    np.linspace(0.95, 0.4, 10))

    shades_ajp5g = plt.cm.Greens(np.linspace(0.8 , 0.3, 10))
    shades_ajp5r = plt.cm.bwr(   np.linspace(0.95, 0.4, 10))

    shades_ajp6g = plt.cm.Greens(np.linspace(0.8 , 0.3, 10))
    shades_ajp6r = plt.cm.bwr(   np.linspace(0.95, 0.4, 10))

    shades_ajp8o = plt.cm.YlOrRd(np.linspace(0.9 , 0.5, 10))
    shades_ajp8b = plt.cm.BuPu(  np.linspace(0.8 , 0.4, 10))

    boronblue  = (178/255, 220/255,     1.0)

    borongreen = (169/255, 207/255, 161/255)


    # DEL once SimFigure works
    def make_space_above(self, axes, topmargin=1):
        """ increase figure size to make topmargin (in inches) space for 
            titles, without changing the axes sizes"""
        fig = axes.flatten()[0].figure
        s = fig.subplotpars
        #print(s.top)
        w, h = fig.get_size_inches()
        #print(w,h)
        figh = h - (1-s.top)*h  + topmargin
        print('make_space_above',figh)
        #figh=7.0
        fig.subplots_adjust(bottom=s.bottom*h/figh, top=1-topmargin/figh)
        fig.set_figheight(figh)

    # DEL once SimFigure works
    def fig_makefig(self, nr=1, nc=1, size=None, title='', plot_d={} ):
        ''' size = tuple (x,y) '''
        if not size:
            size=(8*nc,5*nr)
        fig, axs=plt.subplots(nr,nc,squeeze=0,figsize=size)
        #if nr == 1:
        #    plt.subplots_adjust( left=0.1, right=0.92, top=0.92, bottom=0.08, hspace=0.3, wspace=0.4)
        #if nr == 2:
        #    plt.subplots_adjust( left=0.1, right=0.92, top=0.92, bottom=0.08, hspace=0.4, wspace=0.4)
        plt.subplots_adjust( left=0.1, right=0.92, top=0.9, bottom=0.08, hspace=0.4, wspace=0.4)

        #title='AJP 2014 Fig 6' '\n' 'Addition and Removal 1.5\% CO_2 / 10 mM HCO^-_3' '\n'
        #title='AJP 2014 Fig 6 Addition and Removal 1.5\% CO_2 / 10 mM HCO3'
        #print('title=',title)
        #title=title.replace(' ','\ ')
        #print('title=',title)
        fig.suptitle(rf'$\mathrm{{{title}}}$', size=20, style='normal')

        title=title.replace(' ',r'\ ')
        titlelines=title.split('\n')
        title= "\n".join([rf'$\mathrm{{{tl}}}$' for tl in titlelines])
        fig.suptitle(title, size=20, style='normal')
        #fig.suptitle(rf'$\mathrm{{{title}}}$', size=20, style='normal')

        self.fig_setaxesdefs(fig.axes, plot_d)
        
        return fig,axs

    # DEL once SimFigure works
    def fig_setaxesdefs(self,axs_1d,plot_d={},prop_d={}):
        ''' axs single list of axs - note fig.axes provides 1d list
            prop_d is dict of props
        '''
        fmtr= ScalarFormatter(useOffset=True,useMathText=True)# '%.4f' )
        fmtr.set_powerlimits((-3,4))

        for figpan,ax in enumerate(axs_1d):
            ax.tick_params( direction='in', width=2.0)
            ax.yaxis.set_tick_params(labelsize=20) # 2 ways to set label size
            ax.xaxis.set_tick_params(labelsize=20) # 2 ways to set label size
            try:
                ax.xaxis.set_ticks_position(plot_d['tickspos']) # 2 ways to set label size
            except KeyError: pass

            ax.yaxis.set_major_formatter(fmtr)
            ax.yaxis.offsetText.set_fontsize(20)

            try:
                ax.set_prop_cycle(color=plot_d['colors'][figpan])
            except KeyError:
                ax.set_prop_cycle(color=self.shades)

            bs = [ "bottom", "left", "top", "right" ]
            try:
                rembs= plot_d['remborder']
                for remb in rembs:
                    ax.spines[remb].set_visible(False)
                    bs.remove(remb)
                for b in bs:
                    ax.spines[b].set_linewidth(2.0)
            except KeyError:
                pass

            ## 2nd
            #if prop_d:
            #    ax.update( prop_d )

    ### Paper Specific Figures from RXO data ###
    def jtb2012_fig3_expected(self):
        d={81: {'min_CO2': 0.0555129459526073, 'min_H2CO3':0.00127346792900956, 'min_HCO3m':9.86959970613359, 'max_pH':7.50768186739958, 'min_HA':2.47789038475807, 'max_Am':2.52210961524159 },
          101: {'min_CO2': 0.263385093489674 , 'min_H2CO3':0.00127672861410357, 'min_HCO3m':9.873347438998  , 'max_pH':7.50673521857578, 'min_HA':2.48061487116315, 'max_Am':2.51938512883652 },
          121: {'min_CO2': 0.321327978977117 , 'min_H2CO3':0.00128154810095557, 'min_HCO3m':9.87887075667718, 'max_pH':7.5053397158173 , 'min_HA':2.48463125605608, 'max_Am':2.51536874394368 },
          141: {'min_CO2': 0.37493482762637  , 'min_H2CO3':0.00128737268003665, 'min_HCO3m':9.88551956314748, 'max_pH':7.50365959821878, 'min_HA':2.48946689194544, 'max_Am':2.51053310805441 },
          161: {'min_CO2': 0.424944829490097 , 'min_H2CO3':0.00129371677565947, 'min_HCO3m':9.89272819877813, 'max_pH':7.50183781974487, 'min_HA':2.49471033745859, 'max_Am':2.50528966254132 },
          180: {'min_CO2': 0.469685719673137 , 'min_H2CO3':0.0012998299238977 , 'min_HCO3m':9.89964191556965, 'max_pH':7.50009050046522, 'min_HA':2.49973951872329, 'max_Am':2.50026048127671 },
        }
        return d,d[81].keys()

    def jtb2012_fig4_expected(self):
        # NOTE - index i50 -1 due to matlab 1 indexing vs python 0 indexing
        d={0:{ 'max_CO2':0.471960201831359, 'max_H2CO3':0.0013001063497013 , 'max_HCO3m':3.13059708641011, 'min_pH':7.0000056652852 , 'max_HA':15.2215195921725, 'min_Am':12.0910405116631,
                'i50_CO2':2432-1, 'i50_H2CO3':2433-1, 'i50_HCO3m':2398-1, 'i50_pH':2380-1, 'i50_HA':2380-1, 'i50_Am':2380},
          20:{ 'max_CO2':0.471960667818228, 'max_H2CO3':0.00130010763915841, 'max_HCO3m':3.13059948056895, 'min_pH':7.00000556667966, 'max_HA':15.221521122119 , 'min_Am':12.0910389817163,
                'i50_CO2':2428-1, 'i50_H2CO3':2429-1, 'i50_HCO3m':2392-1, 'i50_pH':2375-1, 'i50_HA':2375-1, 'i50_Am':2375},
          40:{ 'max_CO2':0.471962012040885, 'max_H2CO3':0.00130011134448762, 'max_HCO3m':3.1306063393755 , 'min_pH':7.00000528042608, 'max_HA':15.2215255635799, 'min_Am':12.0910345402552,
                'i50_CO2':2413-1, 'i50_H2CO3':2414-1, 'i50_HCO3m':2371-1, 'i50_pH':2359-1, 'i50_HA':2359-1, 'i50_Am':2359},
          60:{ 'max_CO2':0.471964176295816, 'max_H2CO3':0.00130011697184901, 'max_HCO3m':3.13061669189293, 'min_pH':7.00000483679776, 'max_HA':15.2215324468397, 'min_Am':12.0910276569953,
                'i50_CO2':2379-1, 'i50_H2CO3':2384-1, 'i50_HCO3m':2329-1, 'i50_pH':2328-1, 'i50_HA':2328-1, 'i50_Am':2328},
          79:{ 'max_CO2':0.47196865988373 , 'max_H2CO3':0.00130012193000194, 'max_HCO3m':3.13062574336164, 'min_pH':7.00000443622878, 'max_HA':15.2215386619975, 'min_Am':12.0910214418374,
                'i50_CO2':2179-1, 'i50_H2CO3':2346-1, 'i50_HCO3m':2278-1, 'i50_pH':2294-1, 'i50_HA':2294-1, 'i50_Am':2294},
          80:{ 'max_CO2':0.471969173417866, 'max_H2CO3':0.00130012198471938, 'max_HCO3m':3.13062584278149, 'min_pH':7.00000443174286, 'max_HA':15.2215387316003, 'min_Am':12.0910213722346,
                'i50_CO2':2110-1, 'i50_H2CO3':2346-1, 'i50_HCO3m':2277-1, 'i50_pH':2293-1, 'i50_HA':2293-1, 'i50_Am':2293},
        }
        return d,d[0].keys()

    def jtb2012_fig6_expected(self):
        # NOTE - index i50 -1 due to matlab 1 indexing vs python 0 indexing
        d={   '1.0':{ 'max_dpHi_dt':-0.007478936895779, 'index_dpHi_dt':1981, 'delta_pHs':1.053419283270074e-05,}, #   1
              '5.0':{ 'max_dpHi_dt':-0.006896900470081, 'index_dpHi_dt':1702, 'delta_pHs':1.756269709503044e-04,}, #   5
             '10.0':{ 'max_dpHi_dt':-0.006287857764868, 'index_dpHi_dt':1772, 'delta_pHs':3.321979971309119e-04,}, #  10
             '25.0':{ 'max_dpHi_dt':-0.004991221248820, 'index_dpHi_dt':1746, 'delta_pHs':9.249396480077721e-04,}, #  25 
             '50.0':{ 'max_dpHi_dt':-0.003834492731466, 'index_dpHi_dt':1754, 'delta_pHs':0.002450434122551,},     #  50
            '100.0':{ 'max_dpHi_dt':-0.003558638351327, 'index_dpHi_dt':1677, 'delta_pHs':0.007681867399580,},     # 100
            '150.0':{ 'max_dpHi_dt':-0.003558247383449, 'index_dpHi_dt':1677, 'delta_pHs':0.014447204858045,},     # 150
        }
        return d,d['1.0'].keys()

    def jtb2012_fig7_expected(self): #TODO - copy of 6
        d={ '34.200000':{'max_dpHi_dt':-0.003506752428296,     'index_dpHi_dt':1615, 'delta_pHs':0.007527144344197,},
             '3.420000':{'max_dpHi_dt':-0.003505135564517,     'index_dpHi_dt':1518, 'delta_pHs':0.007524824486365,},
             '0.342000':{'max_dpHi_dt':-0.003489020378579,     'index_dpHi_dt':1341, 'delta_pHs':0.007501830984722,},
             '0.034200':{'max_dpHi_dt':-0.003335248200498,     'index_dpHi_dt':1071, 'delta_pHs':0.007279239637294,},
             '0.003420':{'max_dpHi_dt':-0.002316370744425,     'index_dpHi_dt': 862, 'delta_pHs':0.005612072954587,},
             '0.001368':{'max_dpHi_dt':-0.001546856232544,     'index_dpHi_dt': 783, 'delta_pHs':0.004061499874566,},
             '0.000684':{'max_dpHi_dt':-0.001001660863247,     'index_dpHi_dt': 726, 'delta_pHs':0.002782170645465,},
             '0.000456':{'max_dpHi_dt':-0.0007420376021053291, 'index_dpHi_dt': 692, 'delta_pHs':0.002116484359663,},
             '0.000342':{'max_dpHi_dt':-0.0005896402490194736, 'index_dpHi_dt': 662, 'delta_pHs':0.001708171249300,},
        }
        return d,d['34.200000'].keys()

    def jtb2012_fig10_expected(self):
        d={\
#                THIS IS CRAPlllllllllllllllllllllllllllllllll
               '0.000000' :{'max_dpHi_dt':-19.392585307131295,    'index_dpHi_dt':1404, 'max_dpHs_dt':-2.297106351233432e-04, 'index_dpHs_dt':2653},
              '13.656280' :{'max_dpHi_dt':-0.007110703434606,     'index_dpHi_dt':1676, 'max_dpHs_dt':-5.822660631798852e-05, 'index_dpHs_dt':2067},
              '27.312560' :{'max_dpHi_dt':-0.003558638351327,     'index_dpHi_dt':1677, 'max_dpHs_dt':-5.211395772192485e-05, 'index_dpHs_dt':2063},
              '54.625120' :{'max_dpHi_dt':-0.001780151731670,     'index_dpHi_dt':1677, 'max_dpHs_dt':-4.916942977895226e-05, 'index_dpHs_dt':2062},
             '136.562800' :{'max_dpHi_dt':-7.122618602379572e-04, 'index_dpHi_dt':1677, 'max_dpHs_dt':-4.743866457258756e-05, 'index_dpHs_dt':2061},
           '27312.560103' :{'max_dpHi_dt':-3.561979254444374e-06, 'index_dpHi_dt':1677, 'max_dpHs_dt':-4.630549927141518e-05, 'index_dpHs_dt':2060},
        }
        return d,d['0.000000'].keys()

    def jtb2012_fig12_expected(self): #TODO - copy of 6
        d={ ( 90, 10):{'max_dpHi_dt':-0.006753951105073, 'index_dpHi_dt':1545},
            ( 90, 50):{'max_dpHi_dt':-0.003564317487987, 'index_dpHi_dt':1783},
            ( 90,150):{'max_dpHi_dt':-0.001301037006802, 'index_dpHi_dt':2180},
            ( 90,250):{'max_dpHi_dt':-0.000848564767062, 'index_dpHi_dt':2338},
            ( 90,350):{'max_dpHi_dt':-0.000672649194748, 'index_dpHi_dt':2514},
            ( 90,450):{'max_dpHi_dt':-0.000624536273669, 'index_dpHi_dt':2601},
            ( 90,550):{'max_dpHi_dt':-0.000618512717957, 'index_dpHi_dt':2628},
            ( 90,650):{'max_dpHi_dt':-0.000619791590727, 'index_dpHi_dt':2635},
            (100, 10):{'max_dpHi_dt':-0.007013619989054, 'index_dpHi_dt':1619},
            (100, 50):{'max_dpHi_dt':-0.003058164437665, 'index_dpHi_dt':1771},
            (100,150):{'max_dpHi_dt':-0.000728711167768, 'index_dpHi_dt':2402},
            (100,250):{'max_dpHi_dt':-0.000436691382475, 'index_dpHi_dt':2525},
            (100,350):{'max_dpHi_dt':-0.000313432805670, 'index_dpHi_dt':2617},
            (100,450):{'max_dpHi_dt':-0.000274421796955, 'index_dpHi_dt':2677},
            (100,550):{'max_dpHi_dt':-0.000266594644560, 'index_dpHi_dt':2712},
            (100,650):{'max_dpHi_dt':-0.000266441587756, 'index_dpHi_dt':2727},
        }
        return d,d[(90,10)].keys()

    def ajp2014_fig4_expected(self):
        # key is (tiny) oos_tort_lambda
        d={\
            '0.0300' :{'index_dpHi_dt': 1140, 'max_dpHi_dt': -7.946145530562044e-04, 'time_delay': 8.180964403022108},
            '0.0600' :{'index_dpHi_dt': 1080, 'max_dpHi_dt': -0.001059333959789,     'time_delay': 6.367660564922810},
            '0.1200' :{'index_dpHi_dt': 1037, 'max_dpHi_dt': -0.001290096385661,     'time_delay': 5.187762916749420},
            '0.2500' :{'index_dpHi_dt': 1010, 'max_dpHi_dt': -0.001464587992188,     'time_delay': 4.385014997219773},
            '0.5000' :{'index_dpHi_dt':  996, 'max_dpHi_dt': -0.001575302974146,     'time_delay': 3.976995874138807},
            '1.0000' :{'index_dpHi_dt':  988, 'max_dpHi_dt': -0.001656801480418,     'time_delay': 3.729320483073511},
        }
        return d,d['1.0000'].keys()

    def ajp2014_fig5_expected(self):
        # key is (tiny) oos_tort_lambda
        d={\
            '0.0300' :{'delta_pHs': 0.030651992694172    , 'index_peak_pHs': 1026, 'time_delay': 14.256549986442602, 'max_dpHi_dt': -0.001235136128688 },
            '0.0600' :{'delta_pHs': 0.012276975227814    , 'index_peak_pHs': 1013, 'time_delay': 13.604847715863277, 'max_dpHi_dt': -0.001509040550576 },
            '0.1200' :{'delta_pHs': 0.004450075449465    , 'index_peak_pHs':  997, 'time_delay': 13.024684532681826, 'max_dpHi_dt': -0.001742545289639 },
            '0.2500' :{'delta_pHs': 0.001470790959154    , 'index_peak_pHs':  982, 'time_delay': 12.621790000970483, 'max_dpHi_dt': -0.001917183595621 },
            '0.5000' :{'delta_pHs': 5.518242762141412e-04, 'index_peak_pHs':  973, 'time_delay': 12.439159668326276, 'max_dpHi_dt': -0.00201735545014  },
            '1.0000' :{'delta_pHs': 2.417989133078891e-04, 'index_peak_pHs':  969, 'time_delay': 12.258224964318998, 'max_dpHi_dt': -0.002073504545284 },
        }
        return d,d['1.0000'].keys()

    def test_results(self,expepcted_res,tested_res,test_outfile_name='test_output'):
        #error_sign='''
        #       !!!!!!!!!!!!!!!!!!!!!!!!!!!
        #       !!!!!!!!!! ERROR !!!!!!!!!!
        #       !!!!!!!!!!!!!!!!!!!!!!!!!!!'''
        error_sign='!!!!!!!!!! ERROR !!!!!!!!!!'

        with open(test_outfile_name,'w') as tof:
            for exp_run_key,exp_run_vd in expepcted_res.items(): # shells
                #print(f'   EXP:run_key={exp_run_key}')
                for exp_test_key, exp_val in exp_run_vd.items():
                    #print(f'   EXP:test_key={exp_test_key}  exp_val={exp_val}')
                    #print('tested_res=',tested_res)
                    test_val,extra_print= tested_res[exp_run_key][exp_test_key]
                    exp_test= exp_test_key.split('_')[0]
                    if exp_test in ['min','max','delta','time']:
                        evstr = f'{exp_val:18.18f}'
                        tvstr = f'{test_val:18.18f}'
                        error = 'OK tol<e-8' if abs(exp_val-test_val) < 1e-8 else error_sign
                    elif exp_test in ['i50','index']:
                        evstr = f'{exp_val:18d}'
                        tvstr = f'{test_val:18d}'
                        error = 'OK tol<1' if abs(exp_val-test_val) < 2 else error_sign
                    ss=f'{exp_run_key}: {exp_test_key:11s}:'
                    sp= ' ' * len(ss)
                    print()
                    print(    f'{ss} EXP: {evstr}    {error}')
                    tof.write(f'{ss} EXP: {evstr}    {error}')
                    print(    f'{sp} RES: {tvstr} => Diff:{exp_val-test_val}')
                    tof.write(f'{sp} RES: {tvstr} => Diff:{exp_val-test_val}')
                    if extra_print:
                        print(    f'{sp}     {extra_print}')
                        tof.write(f'{sp}     {extra_print}')

    def i50(self,f):
        return np.argmin(abs(f-(min(f)+(max(f)-min(f))/2)))

    def test_mfiles(self):
        # TODO - maybe don't want to bother with this in the code here - just do by hand in shell ???
        #HERE and below - started tests folder with rxo output m file - sed to modify to valid python
        #1 finish the sed - line endings,
        #https://www.grymoire.com/Unix/Sed.html#toc-uh-23
        #@ Using 'sed /pattern/' about 1/4- 1/3 way down
        #Then write comparator for the 2 mfiles.
        #See about dumping the .mat file from my runs and running that through the sed, and do a really good compare.
        #Will need to change rxo Atot to Atot1 - etc - lots of them.
        #See HERE below
        pass

#TODO DEL THIS after JTB cleanup
    def update_xylims(self, mmstore, data_list):
        if mmstore[0] is not None:
            if mmstore[0] > min(data_list):
                mmstore[0] = None
        if mmstore[1] is not None:
            if mmstore[1] < max(data_list):
                mmstore[1] = None

    def setup_axes(self, ax, xl, yl, xlims, ylims, **kwargs ):
        ax.set_xlabel(xl, size=20)
        ax.set_ylabel(yl, size=20)

        axes_title= kwargs.pop('axtit',None)
        if axes_title:
            ax.set_title(axes_title,size=20)
        
        paneltate = kwargs.pop('paneltate',None)
        if paneltate:
            ax.annotate( paneltate, xy=(0.0, 0.0), xytext=(-0.05,1.05), xycoords="axes fraction", size=20)

        if kwargs.pop('leg', None):
            # Defaults
            leg_props = { 'loc'       : 'best',
                          'framealpha': 0.5,
                          'edgecolor' : (0,0,0),
                          'linewidth' : (2.0),
                          'fontsize'      : 15,
                        }
            # update w/ custom params
            leg_props.update( kwargs.pop('leg_props', {}) )

            # Remove non keywords
            leglinewidth= leg_props.pop('linewidth')

            legend=ax.legend( **leg_props )

            #legend.set_title()
            for l in legend.get_lines():
                l.set_linewidth(leglinewidth)

        if xlims:
            ax.set_xlim(xlims[0],xlims[1])
        if ylims:
            ax.set_ylim(ylims[0],ylims[1])

    def fig__custom(self, fp):
        solute_idx      = fp.solute_idx
        shell_str       = fp.shell_str
        time_str        = fp.time_str
        run_str         = fp.run_str
        print('solute_idx:%d  shell_str:%s  time_str:%s  run_str:%s'%(solute_idx, shell_str, time_str, run_str))
        mat_solute_name = self.c_matlab[solute_idx]
        chart_data_type = self.c_ptype[solute_idx]
        sol_vs_X        = fp.versusX

        plot_rows=1
        plot_cols=1
        plot_d={ 'colors'   : (fp.shades,)*plot_rows * plot_cols,
                 'remborder': []  ,} #'tickspos' : 'both', }

        title= '%s vs. %s'%(mat_solute_name,sol_vs_X)
        fig,axs = self.fig_makefig(plot_rows, plot_cols, size=None, title=title, plot_d=plot_d )

        def slice_from_s( str_in, last_idx ):
            print('last_idx=',last_idx)
            ss=re.split(r'[,\s]', str_in)
            ss= [ v for v in ss if v != '' ]
            l=[]
            for vv in ss:
                vs= [int(u) for u in vv.split(':')]
                c=len(vs)
                if c == 3:
                    start,stop,step=vs#[int(u) for u in v.split(':')]
                    print('    ',start,stop,step)
                    l.append(np.arange(start,stop+1,step)) # NOTE: Users??? +1 to make inclusive
                elif c == 2:
                    start,stop=vs#[int(u) for u in v.split(':')]
                    print('    ',start,stop)
                    if start < 0:
                        start=last_idx + start
                    if stop < 0:
                        stop=last_idx + stop
                    print('    ',start,stop)
                    l.append(np.arange(start,stop+1,1)) # NOTE:: Users??? +1 to make inclusive
                elif c == 1:
                    start,=vs
                    print('    ',start)
                    l.append(np.arange(start,start+1))
            print('    l=',l)
            return np.concatenate(l)

        for ri in [0]:#runs:
            print('ri=',ri)
            np_time  = np.array(fp.run_time[ri])[:,0] 
            np_data  = np.array(fp.run_data[ri])
            N        = fp.Ns[ri]
            n_in     = fp.n_ins[ri]
            n_out    = fp.n_outs[ri]
            n_buff   = fp.n_buffs[ri]
            R_cm     = fp.Rs_cm[ri]
            R_inf_cm = fp.R_infs_cm[ri]
            n_runs   = fp.n_runs
            #print(np_time.shape)
            #print(np_data.shape)

            radii_in,radii_out= self.radii_in_out(R_cm,R_inf_cm,n_in,n_out)
            r_plot  = np.concatenate((radii_in,radii_out))
            x_radii=r_plot/10
            # 0:180:1
            # 0:3000:610
            print('shells=')
            shells=slice_from_s(shell_str,None)
            print('    ',shells)
            print('times=')
            times =slice_from_s(time_str, len(np_time))
            print('    ',times)
            print('runs=')
            runs  =slice_from_s(run_str, n_runs)
            print('    ',runs)


            sol_start = N * solute_idx
            sol_memb  = sol_start + n_in
            sol_end   = sol_memb + n_out

            electrode_idx = self.electrode_index_from_um( 50, R_cm, n_in )

            print('np_time=',np_time)
            plot_t = np_time[ times ]
            print('plot_t=',plot_t)
            plot_t = np.insert(np_time,0,-100) # add first point to -infinity (-100)
            #dt     = np.ediff1d( np_time ) #The differences between consecutive elements of an array.

            shells= [ v + sol_start for v in shells ]
            print(shells)

            ax = axs[0,0]
            ax.set_ylabel(mat_solute_name)
            if sol_vs_X=='vt': # vs Time
                print('VTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVTVT')
                ax.set_xlabel('Time(s)')
                for shell in shells:
                    print('shell=',shell)
                    sol_plot= np_data[times,shell]
                    sol_plot= np.insert(sol_plot,0,sol_plot[0])
                    if chart_data_type == 'pH':
                        sol_plot= self.pH_from_Hplus( sol_plot )

                    ax.plot(plot_t,sol_plot,label='run:%d shell:%d'%(ri,shell))
            if sol_vs_X == 'vs': # vs Shell
                print('VSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVSVS')
                ax.set_xlabel('Distance(shell)')
                for t in times:
                    print('time=',t)
                    sol_plot= np_data[t,shells]
                    if chart_data_type == 'pH':
                        sol_plot= self.pH_from_Hplus( sol_plot )
                    ax.plot(x_radii,sol_plot,label='run:%d time:%d'%(ri,t))

            ax.legend()
        plt.show()

    # IS THIS OLD OR STILL VALID
    # NOTE WARNING Stupid MATLAB   int64 * double ===> int64  ???WTF???
    # Need to make ints into floats before sending to matlab (even indexes --- WTF ???)
    #def fig__JTB_fig_9(self, fignum, fp):


           



    def OnCreateFigure(self,e,fig_name,*args):
        print('OnCreateFigure, fig_name=', fig_name, 'args=', args)

        if self.TESTING:
            self.run_time  = pickle.load( open(self.build_fn('run_time_'  ), 'rb') )
            self.run_data  = pickle.load( open(self.build_fn('run_data_'  ), 'rb') )
            self.run_params= pickle.load( open(self.build_fn('run_params_'), 'rb') )

        #else:
        #    if USE_MATLAB:
        #        if not self.matlab_eng:
        #            print( 'no eng yet')
        #            return
        
        # NEW STUFF
        sim_results= SimResults(self.run_time,self.run_data,self.run_params,self.cur_params)

#FPGONE        class FP: # Figure Params
#FPGONE            run_time = self.run_time
#FPGONE            run_data = self.run_data
#FPGONE
#FPGONE            n_runs = len(self.run_time)
#FPGONE
#FPGONE            #n_ins  = [ int(v) for v in self.run_params['n_in' ] ]
#FPGONE            #n_outs = [ int(v) for v in self.run_params['n_out'] ]
#FPGONE
#FPGONE            #ds     = self.run_params['D'    ]
#FPGONE            #d_infs = self.run_params['D_inf']
#FPGONE           
#FPGONE            if self.cur_sim_type in ['AJP', 'JTB']:
#FPGONE                l = [ ('n_ins'           , 'n_in'           ,        int),
#FPGONE                      ('n_outs'          , 'n_out'          ,        int),
#FPGONE                      ('n_buffs'         , 'n_buff'         ,        int),
#FPGONE                      ('ds'              , 'D'              , lambda x:x),
#FPGONE                      ('d_infs'          , 'D_inf'          , lambda x:x),
#FPGONE                      ('pH_outs'         , 'pH_out'         ,      float),
#FPGONE                      ('pH_in_inits'     , 'pH_in_init'     ,      float),
#FPGONE                      ('Pm_CO2s'         , 'Pm_CO2_input'   ,      float),
#FPGONE                      ('cust_plot_titles', 'cust_plot_title', lambda x:x),
#FPGONE                      ('CAII_in_flags'   , 'CAII_in_flag'   ,       bool),
#FPGONE                      ('CAIV_out_flags'  , 'CAIV_out_flag'  ,       bool),
#FPGONE                      ('CAII_ins'        , 'CAII_in'        ,      float),
#FPGONE                      ('CAIV_outs'       , 'CAIV_out'       ,      float),
#FPGONE                      ('A_CAIIs'         , 'A_CAII'         ,      float),
#FPGONE                      ('A_CAIVs'         , 'A_CAIV'         ,      float),
#FPGONE                      ('Buff_pcs'        , 'Buff_pc'        ,      float),
#FPGONE                      ('A1tot_ins'       , 'A1tot_in'       ,      float),
#FPGONE                      ('A2tot_ins'       , 'A2tot_in'       ,      float),
#FPGONE                      ('oos_tort_lambdas', 'oos_tort_lambda',      float),
#FPGONE                      ('tort_gammas'     , 'tort_gamma'     ,      float),
#FPGONE                      ('tf_CO2ons'       , 'tf_CO2on'       ,      float),
#FPGONE                      ('PlotTitles'      , 'PlotTitle'      , lambda x:x),
#FPGONE                      ('OutFiles'        , 'OutFile'        , lambda x:x),
#FPGONE                      ('FigPropss'       , 'FigProps'       , lambda x:x),
#FPGONE                      #('', '', float),
#FPGONE                ]
#FPGONE
#FPGONE                cvars= vars() # class vars - used to dynamically add
#FPGONE                # Equavalent but cleaner way to repeat with exceptions where vars don't exist
#FPGONE                # try:
#FPGONE                #   n_buffs     = [   int(v) for v in self.run_params['n_buff'      ] ]
#FPGONE                # except KeyError: pass
#FPGONE                for ns,n,t in l:
#FPGONE                    try:
#FPGONE                        cvars[ns]=[ v for v in self.run_params[n] ]
#FPGONE                    except KeyError as ke:
#FPGONE                        #print(sys.exc_info())#ke.__traceback__.print_tb)
#FPGONE                        print('NO Key:',ke)
#FPGONE
#FPGONE# TODO move all this to Gen AJP or JTB Figure - then factory
#FPGONE            
#FPGONE            if self.cur_sim_type in ['AJP', 'JTB']:
#FPGONE                Ns        = [ nin + nout +1 for nin,nout in zip(n_ins,n_outs) ]
#FPGONE                # divide by 10 couldn't use class variable cm_to_mm=10 due to scope issues UGH.
#FPGONE                Rs_cm     = [ (v / 10 ) /2     for v        in ds     ] # in cm not mm
#FPGONE                R_infs_cm = [ (v / 10 ) /2     for v        in d_infs ] # in cm not mm
#FPGONE            #elif self.cur_sim_type in ['RBCO2']:
#FPGONE
#FPGONE            #n_buffs     = [   int(v) for v in self.run_params['n_buff'      ] ]
#FPGONE            #pH_outs     = [ float(v) for v in self.run_params['pH_out'      ] ]
#FPGONE            #pH_in_inits = [ float(v) for v in self.run_params['pH_in_init'  ] ]
#FPGONE            #Pm_CO2s     = [ float(v) for v in self.run_params['Pm_CO2_input'] ]
#FPGONE            #CAII_flags  = [  bool(v) for v in self.run_params['CAII_flag'   ] ]
#FPGONE            #CAIV_flags  = [  bool(v) for v in self.run_params['CAIV_flag'   ] ]
#FPGONE            #CAII_ins    = [ float(v) for v in self.run_params['A_CAII'      ] ]
#FPGONE            #CAIV_outs   = [ float(v) for v in self.run_params['A_CAIV'      ] ]
#FPGONE            #try:
#FPGONE            #    Buff_pcs = [ float(v) for v in self.run_params['Buff_pc'] ]
#FPGONE            #except KeyError: pass
#FPGONE            #try:
#FPGONE            #    A1tot_ins  = [ float(v) for v in self.run_params['A1tot_in' ] ]
#FPGONE            #except KeyError as e:
#FPGONE            #    pass
#FPGONE            #try:
#FPGONE            #    A2tot_ins  = [ float(v) for v in self.run_params['A2tot_in' ] ]
#FPGONE            #except KeyError: pass
#FPGONE            #try:
#FPGONE            #    tort_lambdas = [ float(v) for v in self.run_params['tort_lambda'] ]
#FPGONE            #except KeyError: pass
#FPGONE            #try:
#FPGONE            #    tort_gammas = [ float(v) for v in self.run_params['tort_gammas'] ]
#FPGONE            #except KeyError: pass

        exitafter= self.myargs.doexit

        #def testnewfig(rp):
        #    Figs['RBCO2']['3a'](self.run_time,self.run_data,self.run_params)

        CHART_DEBUGGING=True
        CHART_DEBUGGING=False
        pprint.pp(Figs)
        print('fig_name=',fig_name)
        if fig_name=='custom':
            #self.matlab_eng.create_fig_t_v_x(args[0],args[1],args[2],nargout=0)
            #self.matlab_eng.create_fig_t_v_x(*args,nargout=0)
            FP.versusX=args[0]

            FP.shades= self.shades

            FP.solute_idx = self.c_fig_solute.GetSelection()
            FP.shell_str  = self.t_fig_shells.GetValue()
            FP.time_str   = self.t_fig_times.GetValue()
            FP.run_str    = self.t_fig_runs.GetValue()

            self.fig__custom(FP)

        else:
            if fig_name.startswith('Fig '):
                fig_name=fig_name.removeprefix('Fig ')
            print(f'{self.cur_sim_type}, *** {self.cur_paper}, ### {fig_name}')
            #Figs[self.cur_sim_type][self.cur_paper][fig_name](self.run_time,self.run_data,self.run_params, CHART_DEBUGGING)
            print('Figlist=\n')
            pprint.pp(Figs)
            Figs[self.cur_sim_type][self.cur_paper][fig_name](sim_results, CHART_DEBUGGING)
#            {\
#            #'JTB_2012 Fig 3'       : lambda: self.fig__JTB_fig_3_4(  3, FP),
#            #'JTB_2012 Fig 4'       : lambda: self.fig__JTB_fig_3_4(  4, FP),
#            #'JTB_2012 Fig 5'       : lambda: self.fig__JTB_fig_5  (  5, FP),
#            #'JTB_2012 Fig 6'       : lambda: self.fig__JTB_fig_6_7(  6, FP),
#            #'JTB_2012 Fig 7'       : lambda: self.fig__JTB_fig_6_7(  7, FP),
#            #'JTB_2012 Fig 8'       : lambda: self.fig__JTB_fig_8  (  8, FP),
#            #'JTB_2012 Fig 9'       : lambda: self.fig__JTB_fig_9  (  9, FP),
#            #'JTB_2012 Fig 10'      : lambda: self.fig__JTB_fig_10 ( 10, FP),
#            #'JTB_2012 Fig 11'      : lambda: self.fig__JTB_fig_11 ( 11, FP),
#            #'JTB_2012 Fig 12'      : lambda: self.fig__JTB_fig_12 ( 12, FP),
#
#            #'AJP_2014 Fig 4'       : lambda: self.fig__AJP_fig_4  (  4, FP),
#            #'AJP_2014 Fig 5'       : lambda: self.fig__AJP_fig_5  (  5, FP),
#            ##'AJP_2014 Fig 6'       : lambda: self.fig__AJP_fig_6  (  6, FP),
#            #'AJP_2014 Fig 6'       : lambda: fig__AJP_fig_6New  (  6, sim_results),
#            #'AJP_2014 Fig 8'       : lambda: self.fig__AJP_fig_8  (  8, self.run_params),
#            #'AJP_2014 Fig 13'      : lambda: self.fig__AJP_fig_8  (  8, self.run_params),
#            #'AJP_2014 Fig DKPmCO2Sweep': lambda: self.fig__AJP_fig_PmCO2Sweep('PMCO2', FP),
#            #'AJP_2014 Fig GenSweeps'   : lambda: fig__AJP_fig_GenSweep  ('PMCO2', sim_results, exitafter),
#            #'AJP_2014 Custom Fig 5': lambda: self.fig__AJP_fig_5  (5.1, FP),
#
#            #'RBCO2 Fig 5'          : lambda: self.fig__RBCO2_fig_5( 5            , self.run_params),
#            'RBCO2 Fig 5'          : Figs['RBCO2']['RBCO2']['5'],
#            #'RBCO2 Fig 5PERMS'     : lambda: self.fig__RBCO2_fig_5( '5PERMS'     , self.run_params),
#            'RBCO2 Fig 5PERMS'     : Figs['RBCO2']['RBCO2']['5PERMS'],
#            #'RBCO2 Fig 5PERMSSweep': lambda: self.fig__RBCO2_fig_5( '5PERMSSweep', self.run_params),
#            'RBCO2 Fig 5PERMSSweep': Figs['RBCO2']['RBCO2']['5PERMSSweep'],
#            #'RBCO2 Fig 5PSIGMOID'  : lambda: self.fig__RBCO2_fig_5( '5PSIGMOID'  , self.run_params),
#            'RBCO2 Fig 5PSIGMOID'  : Figs['RBCO2']['RBCO2']['5PSIGMOID'],
#            #'RBCO2 Fig 6 Bar'      : lambda: self.fig__RBCO2_fig_6bar( '6'  , self.run_params),
#            ##'RBCO2 Fig 3a New'     : lambda: testnewfig(self.run_params),
#            'RBCO2 Fig 3a'         : Figs['RBCO2']['RBCO2']['3a'],
#            'RBCO2 Fig 3b'         : Figs['RBCO2']['RBCO2']['3b'],
#            'RBCO2 Fig 3c'         : Figs['RBCO2']['RBCO2']['3c'],
#            'RBCO2 Fig 3d'         : Figs['RBCO2']['RBCO2']['3d'],
#            }[fig_name](self.run_time,self.run_data,self.run_params, CHART_DEBUGGING)

        print('OUT OnCreateFigure, fig_name=', fig_name, 'args=', args)
        if exitafter:
            sys.exit()

#class FigPanelProps():
#    pass

class Substance():
    def __init__(self,t):
        self.order       = t[0]  # order in X
        self.matht       = t[1]  # math text string
        self.yunits      = t[2]  # units for y axis
        self.fconv       = t[3]  # conversion function
        self.fig345panel = t[4]  # figure 3 and 4 panel

class ExtractedData:
    ''' single simulation run extracted data storage class '''
    pass

class SimResults():
    def __init__(self,sim_time,sim_data,sim_runparams,curparams):
        self.t = sim_time # from matlab time
        self.d = sim_data # from matlab X
        self.n_runs = len(self.t)
        self.rp= sim_runparams
        self.cp= curparams
        self.edclass=ExtractedData

        self.substances={\
            'CO2'   : Substance((0, 'CO_2'    , 'Concentration (mM)' , lambda x:x        , 0  )),
            'H2CO3' : Substance((1, 'H_2CO_3' , 'Concentration (mM)' , lambda x:x        , 1  )),
            'HA'    : Substance((2, 'HA_1'    , 'Concentration (mM)' , lambda x:x        , 4  )),
            'pH'    : Substance((3, 'pH'      , 'pH'                 , self.pH_from_Hplus, 3  )),
            'HCO3m' : Substance((4, 'HCO_3^-' , 'Concentration (mM)' , lambda x:x        , 2  )),
            'Am'    : Substance((5, 'A^-_1'   , 'Concentration (mM)' , lambda x:x        , 5  )),
        }


        self.eds=[]

    def make_output(self,outfile,indexvarname,indexvar,datadict): # SimResults
        # Output batch data to file
        thisdf= pd.DataFrame( datadict, 
                #{'dpHi'  :dphis,
                # 'delpHs':dphss,
                #},
            index=indexvar,
        )
        print('thisdf=',thisdf)
        thisdf.to_csv(outfile, index=True,index_label=indexvarname)


    def extract(self,extractors,alist=[],klist=[]):# SimResults
        ''' extract time x shell data matrix for a single species from raw sim data
            and store it in an ExtractedData (ed) class for each run

            call with list of extractors and
                      list of lists of args to pass to each extractor and
                      list of dicts of kwargs 
            example:
            sr.extract( [sr.get_solutes], [[shell_depth,3.15]], [{'over':'time'}] )
        '''
        # example call sr.extract( [ sr.get_pH, sr.get_dpHi_dt, sr.get_delpHs ])
        #hprint('extract1')
        for ri in range(self.n_runs):
            print('ri=',ri)
            self.eds.append( ExtractedData() )
            ed=self.eds[-1]
            ed.np_time = np.array(self.t[ri])[:,0]
            ed.np_data = np.array(self.d[ri])

            for ex,args,kwargs in zip_longest(extractors,alist,klist):
                print(f'->ex {ex}\n  a:{args}\n  k:{kwargs}')
                ex(ri,self.eds[-1],args,kwargs)

    # Data Extractor methods
    def pH_from_Hplus(self, v): # SimResults
        pH      = 3-np.log10(v)
        return pH

    def index_from_R_um(self, ri, R_um):
        ''' R_um is desired radius to return index into X '''

        R_cm = R_um * 1e-4
        radii,radii_in,radii_m,radii_out= self.radii_in_out(ri)
        rad_idx = int(np.nonzero(radii >= R_cm)[0][0]) # nonzero returns tuple of arrays for each dimension of input
        print('rad_idx=',rad_idx, '  rad[elec_idx]=',radii[rad_idx])
        print('RI:\n',radii_in)
        print('RO:\n',radii_out)
        return rad_idx

    def radii_in_out(self,ri=0): # SimResults
        n_in     = self.rp['n_in'      ][ri]
        n_out    = self.rp['n_out'     ][ri]
        N        = n_in + n_out +1
        D        = self.rp['D'         ][ri]
        D_inf    = self.rp['D_inf'     ][ri]
        R_m_cm   = (D/10) / 2
        R_inf_cm = (D_inf/10) / 2

        radii_in = (R_m_cm/n_in)            *np.array(range(0,n_in))
        radii_m  =  R_m_cm                  *np.array([1])
        radii_out= ((R_inf_cm-R_m_cm)/n_out)*np.array(range(1,n_out+1)) + R_m_cm
        radii     = np.concatenate((radii_in,radii_m,radii_out))
        return radii,radii_in,radii_m,radii_out

    def get_subst_idxs(self,sol_order,n_buff,N,n_in,n_out): # SimResults
        sol_start = sol_order * N
        sol_memb  = sol_start + n_in
        sol_end   = sol_memb + n_out
        #print('ss:',sol_start,'sm:',sol_memb,'se:',sol_end)
        return sol_start, sol_memb, sol_end


    #def get_pH(self,data,n_buff,N,n_in,n_out,R_cm,depth_um=50):
    def get_run_var(self,ri,vname): # SimResults
        if ri == -1:
            return self.rp[vname]
        else:
            return self.rp[vname][ri]

    def get_soluteSSSSs(self,ri,ed,*args,over='time',**kwargs): # SimResults
        print(f'get_solutes ri={ri} args={args} over={over} kwargs={kwargs}')
        n_buff   = self.rp['n_buff'    ][ri]
        n_in     = self.rp['n_in'      ][ri]
        n_out    = self.rp['n_out'     ][ri]
        D        = self.rp['D'         ][ri]
        D_inf    = self.rp['D_inf'     ][ri]
        N        = n_in + n_out +1
        R_cm     = (D/10) / 2
        R_inf_cm = (D_inf/10) /2

        try:
            tf_CO2on = self.rp['tf_CO2on'  ][ri]
            ed.idx_tfCO2on= np.nonzero(ed.np_time >= tf_CO2on)[0][0]
        except KeyError:
            pass
        
        #hprint('solutes')
        ed.solutes={}

        if over=='time':
            R_um=args[0]
        elif over=='radius':
            timearg=args[0]

        for soln,solv in self.substances.items():
            sol_order = solv.order + (n_buff - 2)
            ss,sm,se = self.get_subst_idxs(sol_order,n_buff,N,n_in,n_out)
            #hprint('ss=',ss,'sm=',sm,'se=',se)
            #'CO2'  
            #'H2CO3'
            #'HA'   
            #'pH'   
            #'HCO3m'
            #'Am'   
            #hprint('soln=',soln,'ss+idx=',ss+idx)
            if over=='time':
                #R_um=args[0]
                shellidx = self.index_from_R_um( ri )#R_um, R_inf_cm, R_cm, N, n_in, n_out )
                ed.solutes[soln]= solv.fconv( ed.np_data[:, ss + shellidx ] )
            elif over=='radius':
                #timearg=args[0]
                timeidx= np.nonzero(ed.np_time >= timearg)[0][0]
                hprint(f'get_solutes:{soln:5} timeidx={timeidx}  ss={ss}  se={se}')
                ed.solutes[soln]= solv.fconv( ed.np_data[timeidx, ss : se+1 ] )

    def get_substance(self,ri,ed,substance,*args,**kwargs): # SimResults
        print('subs:',substance)
        print('args:',args)
        
        n_buff   = self.rp['n_buff'    ][ri]
        n_in     = self.rp['n_in'      ][ri]
        n_out    = self.rp['n_out'     ][ri]
        N        = n_in + n_out +1

        try:
            tf_CO2on = self.rp['tf_CO2on'  ][ri]
            ed.idx_tfCO2on= np.nonzero(ed.np_time >= tf_CO2on)[0][0]
        except KeyError:
            pass
        ed.substance={}
        #if over=='time':
        #    R_um=args[0]
        #elif over=='radius':
        #    timearg=args[0]

        for sp in substance:
            solv= self.substances[sp]
            sol_order = solv.order + (n_buff - 2)
            ss,sm,se = self.get_subst_idxs(sol_order,n_buff,N,n_in,n_out)

            ed.substance[sp]= solv.fconv( ed.np_data[:, ss : se+1 ] )
         #   if over=='time':
         #       #R_um=args[0]
         #       shellidx = self.index_from_R_um( R_um, R_inf_cm, R_cm, N, n_in, n_out )
         #       ed.solutes[sp]= solv.fconv( self.np_data[:, ss + shellidx ] )
         #   elif over=='radius':
         #       #timearg=args[0]
         #       timeidx= np.nonzero(ed.np_time >= timearg)[0][0]
         #       hprint(f'get_solutes:{sp:5} timeidx={timeidx}  ss={ss}  se={se}')
         #       ed.solutes[sp]= solv.fconv( self.np_data[timeidx, ss : se+1 ] )
#NOTE Here break these
#    get_solute ('ph')
#
#    get_depth
#    get_time
#    get_I
#    get_E

    
    def get_pHi(self,ri,ed,depth_um=50,timelo=None,timehi=None):
        D        = self.rp['D'         ][ri]
        R_cm     = (D/10) / 2
        n_in     = self.rp['n_in'      ][ri]

        ed.pHi= ed.substance['pH'][:,0:n_in]

        R_um= (R_cm*10000) - depth_um
        shellidx = self.index_from_R_um( ri, R_um )
        hprint('pHi:',ri,shellidx)
        return ed.pHi[:,shellidx]

    def get_pHs(self,ri,ed,depth_um=0):
        D        = self.rp['D'         ][ri]
        R_cm     = (D/10) / 2
        n_in     = self.rp['n_in'      ][ri]
        n_out    = self.rp['n_out'     ][ri]
        N        = n_in + n_out +1

        ed.pHs= ed.substance['pH'][:,n_in+1:N]

        R_um= (R_cm*10000) - depth_um
        shellidx = self.index_from_R_um( ri, R_um )
        shellidxpHs= shellidx - n_in
        hprint('pHs:',ri,shellidxpHs)
        return ed.pHs[:,shellidxpHs]

    def get_pHiiiiii(self,ri,ed,depth_um=50,timelo=None,timehi=None):
        D        = self.rp['D'         ][ri]
        D_inf    = self.rp['D_inf'     ][ri]
        R_cm     = (D/10) / 2
        R_inf_cm = (D_inf/10) /2
        n_in     = self.rp['n_in'      ][ri]
        n_out    = self.rp['n_out'     ][ri]
        N        = n_in + n_out +1

        depthidx = self.index_from_R_um( depth_um, R_inf_cm, R_cm, N, n_in, n_out )
        hprint('depthidx=',depthidx)

        if depth_um:
            ed.pHi= ed.pHi[:,depthidx]

        if timelo:
            timeidxlo= np.nonzero(self.np_time >= timearg)[0][0]
        else:
            timedxlo= 0

        if timehi:
            timeidxlo= np.nonzero(self.np_time >= timearg)[0][0]
        else:
            timedxlo= 0

        if over=='time':
            #R_um=args[0]
            shellidx = self.index_from_R_um( R_um, R_inf_cm, R_cm, N, n_in, n_out )
            ed.pHisolutes[sp]= solv.fconv( self.np_data[:, ss + shellidx ] )
        elif over=='radius':
            #timearg=args[0]
            timeidx= np.nonzero(self.np_time >= timearg)[0][0]
            hprint(f'get_solutes:{sp:5} timeidx={timeidx}  ss={ss}  se={se}')
            ed.solutes[sp]= solv.fconv( self.np_data[timeidx, ss : se+1 ] )

    def get_pHHHHHH(self,ri,ed,*args,**kwargs): # SimResults
        ''' extractor for basic pH related data
            usually required for all following extractors 
            ri= run number
            ed= ExtractedData 
        '''
        hprint(f'get_pH ri={ri} args={args}  kwargs={kwargs}')
        try:
            depths_um = kwargs['depths_um']
        except KeyError:
            depths_um = [50]

        n_buff   = self.rp['n_buff'    ][ri]
        n_in     = self.rp['n_in'      ][ri]
        n_out    = self.rp['n_out'     ][ri]
        D        = self.rp['D'         ][ri]
        D_inf    = self.rp['D_inf'     ][ri]
        N        = n_in + n_out +1
        R_cm     = (D/10) / 2
        R_inf_cm = (D_inf/10) / 2

        R_um     = R_cm * 10000

        try:
            tf_CO2on = self.rp['tf_CO2on'  ][ri]
            ed.idx_tfCO2on= np.nonzero(self.np_time >= tf_CO2on)[0][0]
        except KeyError:
            pass
 
        pH_order = self.substances['pH'].order + (n_buff - 2)
        ss,sm,se = self.get_subst_idxs(pH_order,n_buff,N,n_in,n_out)
        #electrode_idx = self.electrode_index_from_um( depth_um, R_cm, n_in )
       
        ed.pHi={}
        ed.pHs={}
        for depth_um in depths_um:
            R_depth_um = R_um - depth_um
            idx = self.index_from_R_um( R_depth_um, R_inf_cm, R_cm, N, n_in, n_out )
            hprint('idx:',idx)
            print(ss,sm,se)
            #ed.pHi= self.pH_from_Hplus( self.np_data[:, ss + electrode_idx ] )
            ed.pHi[depth_um]= self.pH_from_Hplus( self.np_data[:, ss + idx ] )
            ed.pHs[depth_um]= self.pH_from_Hplus( self.np_data[:, sm + 1   ] )


    def get_dpHi_dt(self,ri,ed,pHi,*args,**kwargs): # SimResults
        ''' extractor for dpHi/dt related data
            data is broken into 2 parts
            pHi_I = CO2 Influx ( see ModelParams )
            pHi_E = CO2 Efflux ( see ModelParams )
        '''
        print(f'get_dpHi_dt ri={ri} args={args}  kwargs={kwargs}')
        try:
            idx= ed.idx_tfCO2on                   # 1873
        except AttributeError:
            idx=-1

        t_I   = ed.np_time[   0 : idx ]  # 0 - 1872 ( t= 0 - 1195.148
        t_E   = ed.np_time[ idx :  -1 ]  # 1873

        pHi_I = pHi[   0 : idx ]           #
        pHi_E = pHi[ idx :  -1 ]           #

        if pHi_I.size: # not empty
            dpHi_dt_I, max_dpHi_dt_idx_I, max_dpHi_dt_I= self.get_ddata_dt(pHi_I, t_I)
            ed.max_dpHi_dt_I     =       max_dpHi_dt_I
            ed.max_dpHi_dt_idx_I =       max_dpHi_dt_idx_I
            ed.max_dpHi_dt_t_I   =   t_I[max_dpHi_dt_idx_I]
            ed.pH_at_max_dpHi_I  = pHi_I[max_dpHi_dt_idx_I]

            y1= pHi_I[0]
            y2= ed.pH_at_max_dpHi_I
            t2= ed.max_dpHi_dt_t_I
            m = ed.max_dpHi_dt_I
            #(y2 - y1) = m * (t2 - t1)
            t1 = ((y2 - y1) /  m) - t2
            ed.time_delay_pHi= t1

        if pHi_E.size: # not empty
            dpHi_dt_E, max_dpHi_dt_idx_E, max_dpHi_dt_E= self.get_ddata_dt(pHi_E, t_E)
            ed.max_dpHi_dt_E     =       max_dpHi_dt_E
            ed.max_dpHi_dt_idx_E =       max_dpHi_dt_idx_E
            ed.max_dpHi_dt_t_E   =   t_E[max_dpHi_dt_idx_E]
            ed.pH_at_max_dpHi_E  = pHi_E[max_dpHi_dt_idx_E]

    def get_delpHs(self,ri,ed,pHs,*args,**kwargs): # SimResults
        ''' extractor for delta pHs related data
            data is broken into 2 parts, Influx and Efflux
        '''
        try:
            idx= ed.idx_tfCO2on
        except AttributeError:
            idx= -1
        t_I   = ed.np_time   [   0 : idx ]
        t_E   = ed.np_time   [ idx :  -1 ]
        pHs_I = pHs[   0 : idx ]
        pHs_E = pHs[ idx :  -1 ]

        if pHs_I.size:
            ed.max_pHs_I= max(pHs_I)
            ed.min_pHs_I= pHs_I[0]
            ed.del_pHs_I= ed.max_pHs_I - ed.min_pHs_I
            #print(f'max  {ed.max_pHs_I}  min {ed.min_pHs_I}  del: {ed.del_pHs_I}')

            ed.max_pHs_idx_I = np.argmax(pHs_I)
            startingpoint= 0.0
            ed.time_to_peak_pHs= ed.np_time[ed.max_pHs_idx_I] - startingpoint

        if pHs_E.size:
            ed.max_pHs_E= pHs_E[0]
            ed.min_pHs_E= min(pHs_E)
            ed.del_pHs_E= ed.max_pHs_E - ed.min_pHs_E

    def get_ddata_dt(self,data,t): # SimResults
        dt    = np.ediff1d( t )
        dd    = np.ediff1d( data )
        dd_dt = dd/dt
        max_dd_idx  = np.argmax(np.absolute(dd_dt))
        max_dd      = dd_dt[max_dd_idx]
        print('max_dd=',max_dd)
        return dd_dt, max_dd_idx, max_dd

    def get_Hb_Sat(self,ri,ed,*args,**kwargs): # SimResults
        R     = self.rp['rcm'    ][ri]
        R_inf = self.rp['R_infcm'][ri]
        n_in  = self.rp['n_in'   ][ri]
        n_out = self.rp['n_out'  ][ri]
        N= n_in + n_out + 1

        self.calc_hb_sat(ri,ed,N,n_in,n_out,R,R_inf)
        self.calc_37s(ri,ed)
    
    # NEW version shapes to (n,1) instead of (n,)
    def radii_in_outNEW(self,R_cm,R_inf_cm,n_in,n_out):
        radii_in   =           (       R_cm / n_in  ) * np.array(range(0,n_in+1 ))
        radii_out  = R_cm + ((R_inf_cm-R_cm)/(n_out)) * np.array(range(1,n_out+1)) # Eliminate .650 from r_out
        ishape=len(radii_in)#.shape[0]
        oshape=len(radii_out)#.shape[0]
        return radii_in.reshape(1,ishape) ,radii_out.reshape(1,oshape)

    def calc_hb_sat(self,ri,ed,N,n_in,n_out,R,R_inf):
        X=self.d[ri]
        radii_in,radii_out= self.radii_in_outNEW(R,R_inf,n_in,n_out)
        #print('RDS',self.run_data[0])

        # Extract concentration of solutes (mM) from output matrix X
        #X_O2     = X     (:,1:N);     % O2  (time,space)
        #X_HbO2   = X     [:,N+1:2*N]   # HbO2[time,space]
        #X_Hb     = X     [:,2*N+1:3*N] # HbO2[time,space]
        #X_HbO2_in= X_HbO2[:,0:n_in]
        #X_Hb_in  = X_Hb  [:,0:n_in]
        # More efficient way
        start=N+1   # N=202 n_in=101  start=203 : 304
        X_HbO2_in=X[:, start: start+n_in+1]
        start=2*N+1 #                       405 : 506
        X_Hb_in  =X[:, start: start+n_in+1]
        #Vshell(j+1) = ((4/3)*pi)*((r_in(j+1)^3)-(r_in(j)^3)); # units of cm^3
        ftpi=4/3 * np.pi
        Vri=ftpi * np.power(radii_in,3)[0]
        #print('Vri',Vri)
        Vshell= Vri[1:] - Vri[:-1]
        Vshell=np.insert(Vshell,0, 0.0)
        Vshell=Vshell.reshape(1,len(Vshell))
        #print('Vshell',Vshell)

#See 3_Occhipinti--2024JP--Modeling_Text.docx
        # mM x cm^3 = umol. Remember that 1 mM = 1 umol/cm^3  
        #moles_HbO2_pershell(:,j+1) = X_HbO2_in(:,j+1).*Vshell(j+1);
        # mM x cm^3 = umol. Remember that 1 mM = 1 umol/cm^3  
        #moles_Hb_pershell(:,j+1) = X_Hb_in(:,j+1).*Vshell(j+1);
        moles_HbO2_pershell= X_HbO2_in * Vshell
        #print('moles_HbO2_pershell',moles_HbO2_pershell)
        moles_Hb_pershell  = X_Hb_in   * Vshell
        #print('moles_Hb_pershell',moles_Hb_pershell)
        # Calculate total moles of HbO2 in the RBC....this is a column vector with
        # length equal to the rows of X ....that is equal to the discretization of
        # time (i.e, it is time-dependent). Do the same for total moles of Hb

        #moles_HbO2_total = sum(moles_HbO2_pershell,2); # units of umol
        moles_HbO2_total = np.sum(moles_HbO2_pershell,1) # units of umol
        #moles_Hb_total = sum(moles_Hb_pershell,2); # units of umol
        moles_Hb_total = np.sum(moles_Hb_pershell,1) # units of umol

        Vsphere = ftpi* np.power(radii_in[0][-1],3) # cm^3

        #total_HbO2_conc = moles_HbO2_total./Vsphere; # units mM
        #total_Hb_conc = moles_Hb_total./Vsphere; # units mM
        total_HbO2_conc = moles_HbO2_total/Vsphere # units mM
        total_Hb_conc = moles_Hb_total/Vsphere # units mM
        
         
        ed.Hb_Sat = total_HbO2_conc/(total_HbO2_conc+total_Hb_conc)
#        b= self.shades_ajp8o
#        o= self.shades_ajp8b
#        plot_d={ 'colors'   : (b,b,b,o,o,o),#fp.shades,
#                 'remborder': []  ,
#                 'tickspos' : 'both', }
        #return Hb_Sat

    def calc_37s(self,ri,ed):#t,Hb_Sat):
        '''see sf_analysis.py line 191 - for full step by step
           from linear interp to this func

        dy/dt = (y2 - y1) / (t2 - t1)

        t_37 = (y_37*(t2-t1)-(t2*y1-t1*y2))/(y2-y1)
        yrange= y2-y1
        xrange= t2-t1
        t_37 = y_37*(xrange)-(t2*y1-t1*y2)
                ---------------
                 yrange
        #t_37 * (y2-y1)= t2(y_37 - y1)   + t1(y2 - y_37)
        '''

        t=ed.np_time
        try:
            y_37= ed.y_37= y_37= np.exp(-1)*ed.Hb_Sat[0] # this is the "exact" value of y at time t = t37
            idx1=          np.where(ed.Hb_Sat>= y_37)[0][-1]
            t1  = ed.t1  = t[idx1]#,0]
            y1  = ed.y1  = ed.Hb_Sat[idx1]
            t2  = ed.t2  = t[idx1+1]#,0]
            y2  = ed.y2  = ed.Hb_Sat[idx1+1]
            t_37= ed.t_37= (y_37*(t2-t1)-(t2*y1-t1*y2))/(y2-y1)
            k_37=          1/t_37
            k_37= ed.k_37= np.real(k_37)

            if t_37 < 0.0:
                dlg = wx.MessageDialog(None,
                    'You PROBALBY need to set "Max Time" (tmax) to a higher value\nto run the simulation longer\ndue to a low PmO2\nto allow KHbO2 to cross the t_37 theshold.',
                    "T_37 Calculation Error!",
                    wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()

        except IndexError as e:
            hprint(e)
            ed.k_37=0
            ed.t_37=-0.02
            ed.y_37=0
            ed.t1=0
            ed.t2=0
            ed.y1=0
            ed.y2=0





#class fig__AJP_fig_GenSweep():
#    def __init__(self,figid,sim_results,exitafter=False):
#
#        sfp= SimFigProps()
#        sfp.plot_rows=2
#        sfp.plot_cols=3
#        sfp.plot_d={ 'remborder': ['top','right']  ,
#                          'tickspos' : 'bottom', }
#        sfp.title='AJP 2014 Fig 13ish (Sweep)'
#        sfp.shades = sfp.shades_ajp5g    # WAS "shades"
#
#        super().__init__(figid,sim_results,sfp)
#        self.make_fig()
#        ax_ph     = self.axs[0,0]
#        ax_dphidt = self.axs[0,1]
#        ax_delphs = self.axs[0,2]
#        ax_tdelayphi = self.axs[1,1]
#        ax_ttpeakphs = self.axs[1,2]
#
#        sr=sim_results
#        n_runs = len(self.sr.t)
#        #n_runs=1
#        sr.extract( [ sr.get_pH, sr.get_dpHi_dt, sr.get_delpHs ])
#
#        for ri in range(n_runs):
#            fpp=FigPanelProps() 
#            fpp.xvar= np.array(sr.t[ri])[:,0] # was np_time
#            self.plot_pHipHs(ax_ph,sr.eds[ri],fpp)
#        ph_ylims=(6.8,7.8)
#        ax_ph.set_ylim(ph_ylims)#0.0,0.007)
#
##There is proabbly a line of lambda and gamma that fit the dphi and dphs points
##see if you can figure that.
#
#        sweepvarname= self.sr.get_run_var(-1, 'SweepVar')[0] # 'tort_gamma'
#        sweepvars= self.sr.rp[sweepvarname]
#        xlabel= self.sr.cp[sweepvarname].human_name
#        titlerunpart = self.sr.get_run_var(0, 'PlotTitle')
#
#        if sweepvarname == 'Pm_CO2_input':
#            logx=True
#        else:
#            logx=False
#
#        fpp1=FigPanelProps() 
#        fpp1.title=f'-dphi/dt\n{titlerunpart}'
#        fpp1.xvar= sweepvars
#        fpp1.logx= logx
#        # negate for plot
#        fpp1.yvar= dphidts= [ -ed.max_dpHi_dt_I for ed in sr.eds ]
#        fpp1.xlabel=xlabel
#        fpp1.pkwargs={ 'color': 'red', 'linestyle':'-', 'marker':'o',
#                'label':'-(dphi/dt)max' }
#        self.plot_dpHidt(ax_dphidt,fpp1)
#
#        fpp2=FigPanelProps() 
#        fpp2.title=f'ΔpHs\n{titlerunpart}'
#        fpp2.xvar= sweepvars
#        fpp2.logx= logx
#        fpp2.yvar= delphss= [ ed.del_pHs_I for ed in sr.eds ]
#        fpp2.xlabel=xlabel
#        fpp2.pkwargs={ 'color': 'green', 'linestyle':'-', 'marker':'o',
#                'label':'ΔpHs' }
#        self.plot_delpHs(ax_delphs, fpp2)
#
#        fpp4=FigPanelProps() 
#        fpp4.title=f'TimeDelay pHi (I)\n{titlerunpart}'
#        fpp4.xvar= sweepvars
#        fpp4.logx= logx
#        # negate for plot
#        fpp4.yvar= delays= [ -ed.time_delay_pHi for ed in sr.eds ]
#        fpp4.xlabel=xlabel
#        fpp4.ylabel='delay (s)'
#        fpp4.pkwargs={ 'color': 'blue', 'linestyle':'-', 'marker':'o',
#                'label':'TimeDelay (s)' }
#        self.plot_t(ax_tdelayphi,fpp4)
#        ax_tdelayphi.legend()
#
#        tds= { 'CTRL and CAII':( 9.0, 0.0, 'grey'  ),
#             #  'caii':( 9.0, 0.0, 'purple'),
#             #  'caiv':( 9.0, 0.0, 'green' ),
#        }
#        for k, (y,yd,color) in tds.items():
#            ax_tdelayphi.fill_between( fpp4.xvar, y-yd, y+yd, color=color,alpha=0.2)
#            ax_tdelayphi.annotate(f'Paper {k} td= {y}±{yd}', color=color,
#                    xy=(fpp4.xvar[-1],y), xycoords="data", size=14,
#                    xytext=(-220,0), textcoords='offset pixels')
#
#        fpp5=FigPanelProps() 
#        fpp5.title=f'TimeToPeak pHs (I)\n{titlerunpart}'
#        fpp5.xvar= sweepvars
#        fpp5.logx= logx
#        # negate for plot
#        fpp5.yvar= delays= [ ed.time_to_peak_pHs for ed in sr.eds ]
#        fpp5.xlabel=xlabel
#        fpp5.ylabel='time to peak (s)'
#        fpp5.pkwargs={ 'color': 'red', 'linestyle':'-', 'marker':'o',
#                'label':'TimeToPeak (s)' }
#        self.plot_t(ax_ttpeakphs,fpp5)
#        ax_ttpeakphs.legend()
#       
#        ttps= { 'CTRL':(11.2, 3.7, 'grey'  ),
#                'CAII':( 7.6, 2.7, 'purple'),
#                'CAIV':( 6.5, 0.8, 'green' ),
#        }
#        for k, (y,yd,color) in ttps.items():
#            ax_ttpeakphs.fill_between( fpp5.xvar, y-yd, y+yd, color=color,alpha=0.2)
#            ax_ttpeakphs.annotate(f'Paper {k} tp= {y}±{yd}', color=color,
#                    xy=(fpp5.xvar[-1],y), xycoords="data", size=14,
#                    xytext=(-220,0), textcoords='offset pixels')
#
#
#        dphidt_ylims=(0.0,0.007)
#        ax_dphidt.set_ylim(dphidt_ylims)#0.0,0.007)
#
#        delphs_ylims=(0.0,0.5)
#        ax_delphs.set_ylim(delphs_ylims)
#
##sim was stuck on 0.03
##fix figs first
#
#
#        for v,n,c in ((0.0012,'Raif','blue'),
#                      (0.0009,'DK','green')):
#            x=fpp2.xvar[-1]
#            ax_dphidt.axhline(v,color=c, alpha=0.5)
#            ax_dphidt.annotate(f'{n}= {v}', color=c,
#                    xy=(x,v), xycoords="data", size=14,
#                    xytext=(20,0), textcoords='offset pixels')
#
#        if sweepvarname == 'Pm_CO2_input':
#            pmco2h2o=0.00342
#
#            ax_dphidt.axvline(pmco2h2o)
#            y=(dphidt_ylims[1]-dphidt_ylims[0])*0.25
#            x=pmco2h2o
#            ax_dphidt.annotate(f'PmCO2H2O= {pmco2h2o}',
#                    xy=(x,y), rotation=90, xycoords="data", size=14,
#                    xytext=(20,0), textcoords='offset pixels')
#
#            ax_delphs.axvline(pmco2h2o)
#            y=(delphs_ylims[1]-delphs_ylims[0])*0.25
#            x=pmco2h2o
#            ax_delphs.annotate(f'PmCO2H2O= {pmco2h2o}',
#                    xy=(x,y), rotation=90, xycoords="data", size=14,
#                    xytext=(20,0), textcoords='offset pixels')
#
#
#        self.fig.tight_layout()
#
#        outfilebase= f'{self.sr.rp["OutFile"][0]}'.replace('/','_').replace(' ','_')
#        outcol= f'{self.sr.rp["OutCol"][0]}'.replace('/','_').replace(' ','_')
#
#        self.make_output(f'{outfilebase}.csv',outcol,sweepvars,
#                         {'dphidt':fpp1.yvar,
#                          'delphs':fpp2.yvar,
#                          'tdphi' :fpp4.yvar,
#                          'ttpphs':fpp5.yvar})
#
#        self.fig.savefig(f'{outfilebase}.png')
#
#        if not exitafter:
#            plt.show()
#

        
import argparse
def doit():
    ''' dummy startup function '''
    parser=argparse.ArgumentParser(
        prog='mgui.py',
        description='Modelling GUI',
        epilog='''Run Simulations, Generate Data, Create standard graphs from papers
Example for RBCs:python mgui.py --simtype 2 --paper 2 --figure 1 .
Might NEED TO SPECIFY
PYOPENGL_PLATFORM=egl python mgui.py --simtype 2 --paper 2 --figure 1 .''')
    cwd=os.getcwd()
    parser.add_argument('--testing', action='store_true', default=False, help='Are we TESTING. (generally no)')
    parser.add_argument('--simtype', type=str, help='SimType 0:JTB 1:AJP 2:RBCO2 or name:"AJP"')
    parser.add_argument('--paper'  , type=str, help='Paper 0:JTB_2012 1:AJP_2014 2:RBCO2 or name "JTB_2012"')
    parser.add_argument('--figure' , type=str, help='Figure Number (order in dropdown) or dropdown name "Fig_6"')
    parser.add_argument('--sdp'    , type=str, help='Path to set, either new or Previous Simulation Data (run_data file) to load')
    parser.add_argument('--dosim'  , action='store_true', default=False, help='Auto Run Sim (requires --simtype --sdp and --figure)')
    parser.add_argument('--dofig'  , type=str, help='Create figure, number or Button Name (requires --sdp and --figure)')
    parser.add_argument('--doexit' , action='store_true', default=False, help='Exit after Figure generation. (generally no)')
    appargs=parser.parse_args()
    print('testing=',appargs.testing)
    print('simtype=',appargs.simtype)
    print('paper=',appargs.paper)
    print('figure=',appargs.figure)
    if appargs.sdp:
        if appargs.sdp[-1] != os.sep:
            appargs.sdp=appargs.sdp+os.sep
    print('simdatapath=',appargs.sdp)
    #print('AV:',sys.argv)

    ModelApp( appargs )

if __name__ == '__main__':
    doit()

''' Matlab 2024a
    linux:
        make venv and activate
        in /usr/local/MATLAB/R2024a/extern/engines/python
        sudo chown -R dhuffman: dist
        sudo mkdir build
        sudo chown -R dhuffman: build/
        pip install .
'''
r'''
From Matlab site http://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html
Verify Python and MATLAB Installations

First, verify that your system has the correct versions of Python and MATLAB. Then, find the path to the MATLAB folder. You need the path to the MATLAB folder to install the MATLAB Engine for Python.

    Check that Python is installed on your system and that you can run Python at the operating system prompt.

        To install Python 2.7, 3.3, or 3.4, see Install Supported Python Implementation.

    Add the folder that contains the Python interpreter to your path, if it is not already there.

    Find the path to the MATLAB folder. Start MATLAB and type matlabroot in the command window. Copy the path returned by matlabroot.

Install Engine

To install the MATLAB Engine for Python, execute the following commands where matlabroot is the path to the MATLAB folder.

Windows system:

cd "matlabroot\extern\engines\python"
python setup.py install

Mac or Linux system:

cd "matlabroot/extern/engines/python"
python setup.py install
'''
