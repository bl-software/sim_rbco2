import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import glob
import sys
import os
import argparse

'''
python combine_gamlam.py --dbglvl=3 --sweeptype=l --celltype=CTRL --celltype=CAII --celltype=CAIV --filtered=f P0034_L_log/
'''

# CMD Line args
parser=argparse.ArgumentParser(
    prog='combine_gamlam.py',
    description='''Combine results from Modelling GUI
runs on files in CWD''',
    epilog='''Example for python combine_gamlam.py --sweeptype=g --celltype=CAII --celltype=CAIV --celltype=CTRL ./P0034_G_log/''')
cwd=os.getcwd()

parser.add_argument('--dbglvl', choices=['1','2','3','4','5','6','7'], help='Debug Level')
#parser.add_argument('--filtered', action='store_true', help='Use hardcoded Filter values')
def check_filts(v):
    print(v,type(v))
    v= int(v,base=16)
    if v < 0 or v > 15:
        raise argparse.ArgumentsTypeError('invalid filter must be 0 <= v <= 7')
    return v

parser.add_argument('--filtered', type=check_filts, help='''Use hardcoded filter values
4-bit hex coded
    0x0000
       1=dphidt (dphidt)
        2=delphs (delta phs)
         4=ttp (time to peak)
          8=tdphi (dphi delay)
    ex: 0x7 for 1, 2 and 3
''')
parser.add_argument('--sweeptype', choices=['g','l'], help='g=gamma(Vitelline Membrane), l=lambda(Vesicles)')
parser.add_argument('--celltypes' , choices=['CTRL','CAII','CAIV','ALL'], action='append')
parser.add_argument('folder', type=str, default=cwd, help=f'Default is {cwd}')

args=parser.parse_args()
print('dbglvl=',args.dbglvl)
print('filtered=',args.filtered)
print('sweeptype=',args.sweeptype)
print('celltypes=',args.celltypes)
print('folder=',args.folder)
if args.folder[-1] != os.path.sep:
    print(f'!!! folder must end with {os.path.sep}')
    sys.exit()

DBGL= int(args.dbglvl)
print('DBGL=',DBGL)

def dprint(l,*args):
    if DBGL >= l:
        print(*args)

###################
# Paper Vals needed 
#
celltypes= ['CTRL', 'CAII', 'CAIV']
# Value targets and errors from RBC paper for IRL experiments
# invalid - means I just made it up - actual value not in the paper
dphi_targets= {\
        'CTRL':( 0.0012, 0.0005), # paper, invalid
        'CAII':( 0.0012, 0.0005), # invalid, invalid
        'CAIV':( 0.0012, 0.0005), # invalid, invalid
}
dphs_targets= {\
        'CTRL':( 0.046, 0.02), # paper, paper
        'CAII':( 0.046, 0.02), # invalid, invalid
        'CAIV':( 0.046, 0.02), # invalid, invalid
}
ttpphs_targets= {\
        'CTRL':( 11.2, 3.7), # paper, paper
        'CAII':(  7.6, 2.7), # paper, paper
        'CAIV':(  6.5, 0.8), # paper, paper
}
tdphi_targets=  {\
        'CTRL':( 9.0, 0.5), # paper, invalid
        'CAII':( 9.0, 0.5), # paper, invalid
        'CAIV':( 9.0, 0.5), # paper, invalid
}
celltype_colors= {\
    'CTRL':('green', mpl.colormaps['Greens'], 0.02 ),
    'CAII':('blue' , mpl.colormaps['Blues' ], 0.005),
    'CAIV':('red'  , mpl.colormaps['Reds'  ], 0.02 ),
}

fileparts= {\
    'CTRL': 'Ai_5_0_As_150_0',
    'CAII': 'Ai_1000_0_As_150_0',
    'CAIV': 'Ai_40_0_As_10000_0',
}

titleparts= {\
    'Ai_5_0_As_150_0'   : f'Ai=5.0    As=150.0',
    'Ai_1000_0_As_150_0': f'Ai=1000.0 As=150.0',
    'Ai_40_0_As_10000_0': f'Ai=40.0   As=10000.0',
}
###############
# Use Arguments
#
sweeptype={\
        'l': 'λ',
        'g': 'γ',
        }[args.sweeptype]
print(f'Sweeptype: {sweeptype}')

extratitle={\
        'λ' : f'(Vesicles)',
        'γ' : f'(VitMem)',
        }[sweeptype]

############
# Setup figs
#
size=(28,20)
figdphi,  faxs1=plt.subplots(1,1,squeeze=0,figsize=size)
figdelphs,faxs2=plt.subplots(1,1,squeeze=0,figsize=size)
figtdphi, faxs3=plt.subplots(1,1,squeeze=0,figsize=size)
figttpphs,faxs4=plt.subplots(1,1,squeeze=0,figsize=size)

plt.subplots_adjust( left=0.1, right=0.92, top=0.9, bottom=0.08, hspace=0.4, wspace=0.4)
allfigs= [figdphi, figdelphs, figtdphi, figttpphs]

axi=faxs1[0,0]
axs=faxs2[0,0]
axd=faxs3[0,0]
axt=faxs4[0,0]
allaxes=[ axi, axs, axd, axt ]

title=f'AJP Sweep over {sweeptype}s{extratitle}'
figdphi.suptitle(f'{title}({args.folder})', size=20, style='normal')
figdelphs.suptitle(f'{title}({args.folder})', size=20, style='normal')
figtdphi.suptitle(f'{title}({args.folder})', size=20, style='normal')
figttpphs.suptitle(f'{title}({args.folder})', size=20, style='normal')

alltitleparts=[]
celltypelegend=[]
filtertitles={}
for fig in allfigs:
    filtertitles[fig]={}
    for ct in celltypes:
        filtertitles[fig][ct]={}

for celltype in args.celltypes:
    filepart= fileparts[celltype] # 'Ai_5_0_As_150_0'
    print(f'Filepart: {filepart}')

    titlepart= f'{celltype} {titleparts[filepart]}' # 'CTRL Ai=5.0    As=150.0'
    print(f'Titlepart: {titlepart}')
    alltitleparts.append(titlepart)

    filename= {\
            'λ' : f'{filepart}_{sweeptype}s_γ*.csv',
            'γ' : f'{filepart}_λ*_{sweeptype}s.csv',
            }[sweeptype]
    print('filename=',filename)

    fullfilepath=f'{args.folder}{filename}'
    print('fullfilepath=', fullfilepath)

    filelist=sorted(glob.glob(fullfilepath))
    print('filelist=',filelist)

    dfs=[]
    for fn in filelist:
        df=pd.read_csv(fn)
        dprint(3,'read df=\n',df)
        df=df.set_index(df.columns[0])
        dfs.append((fn,df))
    dprint(3,'dfs=\n',dfs)
    saved_df_index=dfs[0][1].index

    cellmarker, cellmarkersize, cm={\
            'CTRL':('o', 7, mpl.colormaps['Greens']),
            'CAII':('s', 6, mpl.colormaps['Blues' ]),
            'CAIV':('*', 8, mpl.colormaps['Reds'  ]),
        }[celltype]

    for fn,df in dfs:
        endlabel=f'{celltype} {df.index.name.split("_")[-1]}'
        dotidx= endlabel.find('.')
        endlabel=endlabel[:dotidx+4]

        dprint(3,'\nn=   ',df.index.name)
        dprint(3,'ns=  '  ,df.index.name.split('='))
        dprint(3,'ns-1='  ,df.index.name.split('=')[-1])
        try:
            v=float(df.index.name.split('=')[-1])
            cmc= cm((v+0.4)/1.6)
        except:
            print('Error (float conv) in fn=',fn,'df=\n',df)
            sys.exit()

        if df.index.name in [ 'gamma_at_lam=0.1', 'lambda_at_gam=0.03' ]:
            endlabel=f'RXO {endlabel}'
            plotkwargs={
                'marker':cellmarker,
                'markersize':cellmarkersize+4,
                'linewidth':3,
                'color':cmc,#'red',
            }
        else:
            plotkwargs={
                'marker':cellmarker,
                'markersize':cellmarkersize,
                'color':cmc,
            }
        
        if celltype not in celltypelegend:
            celltypelegend.append(celltype)
            plotkwargs['label']=celltype

        if 1 & args.filtered:
            col = 'dphidt'
            y,yd= dphi_targets[celltype]
            minval,maxval= y-yd, y+yd
            df= df[  (df[col] >= minval  ) & (df[col] <= maxval  )  ]
            filtertitles[figdphi][celltype].update({'min':minval, 'max':maxval, 'name':col})

        if 2 & args.filtered:
            col= 'delphs'
            y,yd= dphs_targets[celltype]
            minval,maxval= y-yd, y+yd
            df= df[  (df[col] >= minval) & (df[col] <= maxval)  ]
            filtertitles[figdelphs][celltype].update({'min':minval, 'max':maxval, 'name':col})

        if 4 & args.filtered:
            col= 'ttpphs'
            y,yd= ttpphs_targets[celltype]
            minval, maxval = y-yd, y+yd
            df= df[  (df[col] >= minval   ) & (df[col] <= maxval   )  ]
            filtertitles[figttpphs][celltype].update({'min':minval, 'max':maxval, 'name':col})
            print('SSSSSSSSS\n',{'min':minval, 'max':maxval, 'name':col})
            print(filtertitles[figttpphs][celltype])

        if 8 & args.filtered:
            col= 'tdphi'
            y,yd= tdphi_targets[celltype]
            minval,maxval= y-yd, y+yd
            df= df[  (df[col]  >= minval ) & (df[col]  <= maxval )  ]
            filtertitles[figtdphi][celltype].update({'min':minval, 'max':maxval, 'name':col})

        axi.plot( df.index, df['dphidt'].values,**plotkwargs)
        axs.plot( df.index, df['delphs'].values,**plotkwargs)
        axd.plot( df.index, df['tdphi' ].values,**plotkwargs)
        axt.plot( df.index, df['ttpphs'].values,**plotkwargs)

        try:
            pointidx={\
                'CTRL':-3,
                'CAII':-1,
                'CAIV':-2,
               }[celltype]

            x= df.index[pointidx]
            # Anno end of lines - better than legend
            y=df['dphidt'].values[pointidx]
            axi.annotate(f'{endlabel}', color=cm(0.8),
                    xy=(x,y), xycoords="data", size=10,
                    xytext=(20,5), textcoords='offset pixels')

            y=df['delphs'].values[pointidx]
            axs.annotate(f'{endlabel}', color=cm(0.8),
                    xy=(x,y), xycoords="data", size=10,
                    xytext=(20,5), textcoords='offset pixels')


            y=df['tdphi'].values[pointidx]
            axd.annotate(f'{endlabel}', color=cm(0.8),
                    xy=(x,y), xycoords="data", size=10,
                    xytext=(20,5), textcoords='offset pixels')

            y=df['ttpphs'].values[pointidx]
            axt.annotate(f'{endlabel}', color=cm(0.8),
                    xy=(x,y), xycoords="data", size=10,
                    xytext=(20,5), textcoords='offset pixels')

        except IndexError:
            pass

dphilist=((0.0012,'Raif'    ,'blue' ),
          (0.0009,'DK'      ,'green'),
          (0.0045,'DK BLUE' ,'blue' ),
          (0.0067,'DK RED'  ,'red'  ),
          (0.0064,'DK GREEN','green'))

for v,n,c in dphilist:
    #breakpoint()
    x=axi.get_xlim()[1]
    axi.axhline(v,color=c, alpha=0.5)
    # 5 physiological lines Raif, DK blue red green
    axi.annotate(f'{n}= {v}', color=c,
            xy=(0,v), xycoords="data", size=14,
            xytext=(-120,0), textcoords='offset pixels')

di=saved_df_index
dil=di.tolist()
print('dil=',dil)
ttps_plot= { 'CTRL':( ttpphs_targets['CTRL'][0], ttpphs_targets['CTRL'][1], 0.02 ),
             'CAII':( ttpphs_targets['CAII'][0], ttpphs_targets['CAII'][1], 0.005),
             'CAIV':( ttpphs_targets['CAIV'][0], ttpphs_targets['CAIV'][1], 0.02 ),
}
tds_plot= { 'CTRL and CAII':( 9.0, 0.0, 'black', 0.1  ),
     #  'caii':( 9.0, 0.0, 'purple'),
     #  'caiv':( 9.0, 0.0, 'green' ),
}
for k, (y,yd,ext) in ttps_plot.items():
    c=celltype_colors[k][0]
    paddedidx= [-0.01-ext] +dil +[dil[-1]+ext]
    axt.fill_between( paddedidx, y-yd, y+yd, color=c,alpha=0.05)#, zorder=1000)
    axt.annotate(f'Paper {k} tp= {y}±{yd}', color=c,
            xy=(di[0],y), xycoords="data", size=14,
            xytext=(-240,0), textcoords='offset pixels')

for k, (y,yd,c,ext) in tds_plot.items():
    axd.fill_between( dil, y-yd, y+yd, color=c,alpha=1.0)
    axd.annotate(f'Paper {k} td= {y}±{yd}', color=c,
            xy=(di[0],y), xycoords="data", size=14,
            xytext=(-240,0), textcoords='offset pixels')



rxo_lam=0.1
rxo_gam=0.03

if sweeptype=='λ':
    v=rxo_lam
    axi.axvline(v, color=c, linestyle='--', alpha=0.5)
    axi.annotate(f'RXO λ={v}', color=c, rotation=90,
            xy=(v,0.0), xycoords="data", size=14,
            xytext=(15,0), textcoords='offset pixels')
elif sweeptype=='γ':
    v=rxo_gam
    axi.axvline(v, color=c, linestyle='--', alpha=0.5)
    axi.annotate(f'RXO γ={v}', color=c, rotation=90,
            xy=(v,0.0), xycoords="data", size=14,
            xytext=(15,0), textcoords='offset pixels')

#    if celltype == 'CTRL':
#        axi.set_ylim((0.0,0.004))
#    elif celltype == 'CAII':
#        axi.set_ylim((0.0,0.007))
#    elif celltype == 'CAIV':
#        axi.set_ylim((0.0,0.007))
#axi.set_ylim((0.0,0.007))

'''
FTS={<Figure size 2800x2000 with 1 Axes>:
      {'CTRL': {'min': 0.0006999999999999999, 'max': 0.0017, 'name': 'dphidt'},
       'CAII': {'min': 0.0006999999999999999, 'max': 0.0017, 'name': 'dphidt'},
       'CAIV': {'min': 0.0006999999999999999, 'max': 0.0017, 'name': 'dphidt'}
      },
     <Figure size 2800x2000 with 1 Axes>:
      {'CTRL': {'min': 0.026, 'max': 0.066, 'name': 'delphs'},
       'CAII': {'min': 0.026, 'max': 0.066, 'name': 'delphs'},
       'CAIV': {'min': 0.026, 'max': 0.066, 'name': 'delphs'}
      },
     <Figure size 2800x2000 with 1 Axes>:
      {'CTRL': {},
       'CAII': {},
       'CAIV': {}
      },
     <Figure size 2800x2000 with 1 Axes>:
      {'CTRL': {'min': 7.499999999999999, 'max': 14.899999999999999, 'name': 'ttpphs'},
       'CAII': {'min': 4.8999999999999995, 'max': 10.3, 'name': 'ttpphs'},
       'CAIV': {'min': 5.7, 'max': 7.3, 'name': 'ttpphs'}
      }
    }
allfigs= [135124330361760, 135124256277984, 135124485366752, 135124256844592]
'''

titlepart= '\n'.join(alltitleparts)
xlabel= f'(1/{sweeptype}^2) {extratitle}'

print('FTS=',filtertitles)
def docelltypes(figfilts,plotfig,textfig ):
    #print('figfilts=',figfilts)
    for ct,ft in figfilts.items():
        cm= celltype_colors[ct][1]
        #print('ct=',ct,'ft=',ft, 'cm',cm)
        try:
            #print(ft["name"], ct, f'{ft["min"]:.2e}', f'{ft["max"]:.2e}')
            tablevals.append([ft["name"],ct,f'{ft["min"]:.2e}',f'{ft["max"]:.2e}'])
        except KeyError:
            continue

        if plotfig == textfig:
            cellColours.append([cm(0.5)]*4)
        else:
            cellColours.append([cm(0.1)]*4)

for plotfig,plotax in zip(allfigs,allaxes):
    tablevals=[]
    tablerowcolors=[]
    cellColours=[]
    #print('allfigs ids=',[id(f) for f in allfigs])
    #print('\n\nplotfig=',id(plotfig),plotfig)
    try:
        figfilts= filtertitles[plotfig]
    except KeyError:
        continue
    
    docelltypes(figfilts,plotfig,plotfig )
    for textfig in [ f for f in allfigs if f != plotfig ]:
        print('\n  textfig', id(textfig))
        try:
            figfilts= filtertitles[textfig]
        except KeyError:
            continue
 
        docelltypes(figfilts,plotfig,textfig )

    col_labels = ['Param', 'CellType','Min','Max']
    #row_labels = ['Row1','Row2','Row3']
    #table_vals = [[10, 9, 8], [20, 19, 18], [30, 29, 28]]
    #row_colors = ['red', 'blue', 'yellow']
    print('tablevals=',tablevals)
    print('cellcolors=',cellColours)
    print('collabels=',col_labels)
    #print('tablrowcols=',tablerowcolors)
    nrows= len(tablevals)
    if args.filtered:
        my_table = plotax.table(cellText=tablevals,
                             cellColours=cellColours,
                             colWidths=[0.05] * 4,
                             #rowLabels=row_labels,
                             colLabels=col_labels,
                             #rowColours=tablerowcolors,
                             bbox=[0.7,1.0,0.2,0.02*nrows],
                                #loc='upper right',
                             )

        #tbb=my_table._bbox 
        #print(tbb)
        #yloc= tbb[1] - tbb[3]
        plotax.text(0.66,1.01,'Filters:',transform=plotax.transAxes, fontweight='bold')

figdhpi_title  ='-dphi/dt'
figdhpi_titlefn='dphi_dt'
axi.set_title(f'{figdhpi_title}\n{titlepart}')
axi.set_xlabel(xlabel)
axi.set_ylabel(f'-dphi/dt_max',size=20)
axi.set_ylim(0.0,0.012)

figdelphs_title  ='ΔpHs'
figdelphs_titlefn='delpHs'
axs.set_title(f'{figdelphs_title}\n{titlepart}')
axs.set_ylabel(f'ΔpHs',size=20)
axs.set_xlabel(xlabel)
axs.set_ylim(0.0,0.40)

figtdphi_title  ='time delay pHi'
figtdphi_titlefn='time_delay_pHi'
axd.set_title(f'{figtdphi_title}\n{titlepart}')
axd.set_xlabel(xlabel)
axd.set_ylabel(f'td(s)',size=20)
axd.set_ylim(0.0,18.0)

figttpphs_title  ='time to peak pHs'
figttpphs_titlefn='time_to_peak_pHs'
axt.set_title(f'{figttpphs_title}\n{titlepart}')
axt.set_xlabel(xlabel)
axt.set_ylabel(f'tp(s)',size=20)
axt.set_ylim(0.0,20.0)

axi.legend()
axs.legend()
axt.legend()
axd.legend()
plt.show()


perm= {'P0068':'p0068',
       'P0034':'p0034'
       }[args.folder.replace('./','').split('_')[0]]

figdphi.savefig( f'F1_{sweeptype}_sweep_Perm_{perm}_{figdhpi_titlefn}' )
figdelphs.savefig( f'F2_{sweeptype}_sweep_Perm_{perm}_{figdelphs_titlefn}' )
figtdphi.savefig( f'F3_{sweeptype}_sweep_Perm_{perm}_{figtdphi_titlefn}' )
figttpphs.savefig( f'F4_{sweeptype}_sweep_Perm_{perm}_{figttpphs_titlefn}' )



