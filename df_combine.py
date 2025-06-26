import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

#df=pd.DataFrame( 
#    [ [ 4.11,4.12,4.13,4.14 ],
#      [ 4.21,4.22,4.23,4.24 ],
#      [ 4.31,4.32,4.33,4.34 ],
#      [ 4.41,4.42,4.43,4.44 ],
#    ],
#    index=[ 0.1,0.2,0.3,0.4 ],
#    columns=['r1','r2','r3','r4']
#)
#p50cmap=mpl.colormaps['autumn']
p50cmap=mpl.colormaps['winter']
r=7.77 - 2.22
v=2.22
indexval= 'PmO2'
#          PmO2     KHbO2  anno     pixeloffset  color
p50_3     =(0.2668, 2.22 ,'PmO2=', (-180,-30), p50cmap((2.22-v)/r ))
p50_5     =(0.2668, 3.29 ,'PmO2=', (-180,-30), p50cmap((3.29-v)/r ))
p50_7     =(0.2668, 4.18 ,'PmO2=', (-180,-30), p50cmap((4.18-v)/r ))
p50_9     =(0.2668, 5.08 ,'PmO2=', (-180,-30), p50cmap((5.08-v)/r ))
p50_12    =(0.2668, 5.93 ,'PmO2=', (-180,-30), p50cmap((5.93-v)/r ))
p50_15    =(0.2668, 6.73 ,'PmO2=', (-180,-30), p50cmap((6.73-v)/r ))
p50_20    =(0.2668, 7.77 ,'PmO2=', (-180,-30), p50cmap((7.77-v)/r ))

aqp1low   =(0.0742 , 2.87 ,'PmO2=', (-180,-30), 'black'         )
low       =(0.0675 , 2.87 ,'PmO2=', (-180,-30), 'black'         )
cast      =(0.1107 , 4.14 ,'PmO2=', (-180,-30), 'black'         )
balbc     =(0.1051 , 3.824,'PmO2=', (-150,-20), 'green'         )
balbcctrl =(0.1616 , 4.217,'PmO2=', (-180,-20), 'lightgreen'    )
j6caseavg =(0.1586 , 4.187,'PmO2=', (-180,-20), 'red'           )
rxoWT     =(0.14979, 3.99 ,'PmO2=', (-180,-20), 'blue'          )
sphereCtrl=(0.14977, 3.9949   ,'PmO2=', (-200,20), 'blue'          )
#sphereCtrl=(0.15, 3.9949   ,'PmO2=', (-200,20), 'blue'          )
sphere    =(0.150325, 1.83313,'PmO2=', (50,-50), 'blue'          )
j6        =(0.2668 , 5.08 ,'PmO2=', (-180,-20), 'red'           )
j6ctrl    =(0.1556 , 4.156,'PmO2=', (-180,-30), 'indianred'     )
ae1wt     =(0.2039 , 4.63 ,'PmO2=', (-180,-30), 'blue'          )
ae1het    =(0.1635 , 4.41 ,'PmO2=', (-180,-20), 'cornflowerblue')
ae1wtold  =(0.2064 , 4.67 ,'PmO2=', (-200,+30), 'salmon'        )
ae1hetold =(0.162  , 4.396,'PmO2=', (-200,-50), 'orangered')
#cast      =(0.1041 , 3.691,'PmO2=', (-180,-30), 'black'         )
humm      =(0.0516 , 1.853,'PmO2=', (+80 ,-20), 'lightblue'     )
humf      =(0.04695, 1.793,'PmO2=', (+80 ,-60), 'pink'          )
huma      =(0.05031, 1.837,'PmO2=', (+80 ,-40), 'purple'        )
bovine    =(0.0878 , 2.24 ,'PmO2=', (-150,-20), 'brown'         )
bovinenew =(0.0878 , 2.24 ,'PmO2=', (-150,-20), 'orange'        )

human1    =(0.0878 , 2.24 ,'PmO2=', (-150,-20), 'orange'        )

toplot=[\
#    ae1wt, ae1het,
#    ae1wtold, ae1hetold,
#p50_3, p50_5, p50_7, p50_9, p50_12, p50_15, p50_20,
    #low,
    #aqp1low,
    j6caseavg,
#    rxoWT,
    #sphere,
    #sphereCtrl,
#    cast,
#    human1,
#    balbc,
#    balbcctrl,
#    j6,
#    j6ctrl,
#    humm,
#    humf,
#    huma,
#    bovine,
##   bovinenew,
]

fl_d= {

    j6caseavg :['MouseC57BL_6Case_AvgWT_r1_2.csv' , 'MouseC57BL_6Case_AvgWT_r2_2.csv' ],
#    j6caseavg :['MouseC57BL_6Case_AvgWT_r1_2.csv' ,],# 'MouseC57BL_6Case_AvgWT_r2_2.csv' ],
#    sphere     :['MouseSphereWT_r1_2.csv' ,],# 'MouseC57BL_6Case_AvgWT_r2_2.csv' ],
    #sphere    :['MouseSphere647WT_r1_2.csv' ,],# 'MouseC57BL_6Case_AvgWT_r2_2.csv' ],
    #sphereCtrl :['MouseSphereCTRLWT_r1_2.csv' ,],# 'MouseC57BL_6Case_AvgWT_r2_2.csv' ],

#LAST      aqp1low :['MouseLow_AQPIWTWT_r1_2.csv' , 'MouseLow_AQPIWTWT_r2_2.csv' ],
#LAST
#LAST        ae1wtold :['MouseAE1WT_r1_2.csv' , 'MouseAE1WT_r2_2.csv' ],
#LAST        ae1hetold:['MouseAE1Het_r1_2.csv', 'MouseAE1Het_r2_2.csv'],
#LAST     ae1wt :['MouseAE1_6JBkgWT_r1_2.csv' ,'MouseAE1_6JBkgWT_r2_2.csv' ],
#LAST     ae1het:['MouseAE1_6JBkgHet_r1_2.csv','MouseAE1_6JBkgHet_r2_2.csv'],
#LAST        #ae1wt :['MouseAE1_6JBkgWT_r1_2_p50_20.0.csv' , 'MouseAE1_6JBkgWT_r2_2_p50_20.0.csv' ],
#LAST        #ae1het:['MouseAE1_6JBkgHet_r1_2_p50_20.0.csv', 'MouseAE1_6JBkgHet_r2_2_p50_20.0.csv'],
#LAST
#LAST     ae1wtold :['MouseAE1WT_r1_2_p50_20.0.csv' ,'MouseAE1WT_r2_2_p50_20.0.csv' ],
#LAST     ae1hetold:['MouseAE1Het_r1_2_p50_20.0.csv','MouseAE1Het_r2_2_p50_20.0.csv'],
#LAST        p50_3 :['MouseC57BL_6J_PanWT_r1_2_p50_3.0.csv' , 'MouseC57BL_6J_PanWT_r2_2_p50_3.0.csv'],
#LAST        p50_5 :['MouseC57BL_6J_PanWT_r1_2_p50_5.0.csv' , 'MouseC57BL_6J_PanWT_r2_2_p50_5.0.csv'],
#LAST        p50_7 :['MouseC57BL_6J_PanWT_r1_2_p50_7.0.csv' , 'MouseC57BL_6J_PanWT_r2_2_p50_7.0.csv'],
#LAST        p50_9 :['MouseC57BL_6J_PanWT_r1_2_p50_9.35.csv', 'MouseC57BL_6J_PanWT_r2_2_p50_9.35.csv'],
#LAST        p50_12:['MouseC57BL_6J_PanWT_r1_2_p50_12.0.csv', 'MouseC57BL_6J_PanWT_r2_2_p50_12.0.csv'],
#LAST        p50_15:['MouseC57BL_6J_PanWT_r1_2_p50_15.0.csv', 'MouseC57BL_6J_PanWT_r2_2_p50_15.0.csv'],
#LAST        p50_20:['MouseC57BL_6J_PanWT_r1_2_p50_20.0.csv', 'MouseC57BL_6J_PanWT_r2_2_p50_20.0.csv'],
#LAST      low     :['MouseLow_AQPIWTWT_r1_2.csv','MouseLow_AQPIWTWT_r2_2.csv'     ],
#LAST     cast     :['MouseCastall_r1_2.csv','MouseCastall_r2_2.csv'     ],
     #dale     :['HUMANSOMETHINGMouseC57BL_6Case_RXO_116WT_r0_2.csv','MouseC57BL_6Case_RXO_116WT_r1_2.csv'     ],
#     rxoWT     :['MouseC57BL_6Case_RXO_116WT_r1_2.csv',  ],
#    balbc    :['BalbCJlow.csv'          , 'BalbCJmid.csv'           , 'BalbCJup.csv'          ],
#    balbcctrl:['C57BL6CCtrlBalbClow.csv', 'C57BL6CCtrlBalbCmid.csv' , 'C57BL6CCtrlBalbCup.csv'],
#    j6       :['C57BL6Jlow.csv'         , 'C57BL6Jmid.csv'          , 'C57BL6Jup.csv'         ],
#    j6ctrl   :['C57BL6CCtrl6Jlow.csv'   , 'C57BL6CCtrl6Jmid.csv'    , 'C57BL6CCtrl6Jup.csv'   ],
#    ae1wt    :['AE1low.csv'             , 'AE1mid.csv'              , 'AE1up.csv'             ],
#    ae1het   :['AE1Hetlow.csv'          , 'AE1Hetmid.csv'           , 'AE1Hetup.csv'          ],
#    cast     :['CASTEIJlow.csv'         , 'CASTEIJmid.csv'          , 'CASTEIJup.csv'         ],
#    humm     :['HumanMalelow.csv'       , 'HumanMalemid.csv'        , 'HumanMaleup.csv'       ],
#    humf     :['HumanFemalelow.csv'     , 'HumanFemalemid.csv'      , 'HumanFemaleup.csv'     ],
#    huma     :['HumanAvglow.csv'        , 'HumanAvgmid.csv'         , 'HumanAvgup.csv'        ],
#    bovine   :['Bovine_5.5_low.csv'     , 'Bovine_5.5_mid.csv'      , 'Bovine_5.5_up.csv'     ],
#    bovinenew:['Bovine__low.csv'        , 'Bovine__mid.csv'         , 'Bovine__up.csv'        ],
}

filelist=[]
for p in toplot:
    print('p=',p)
    filelist+=fl_d[p]
print('fl=',filelist)

dfs=[]
for fn in filelist:
    dfs.append(pd.read_csv(fn).set_index(indexval))
    print('\ngot df=\n',dfs[-1])

dfd={}
for df in dfs:
    coln= df.columns[0]
    if coln in dfd.keys():
        dfd[coln]=pd.concat((dfd[coln],df))
    else:
        dfd[coln]=df

rdf= pd.concat(dfd.values(), axis=1)
#print(rdf.to_string())
rdf.to_csv('AllVals.csv')

colors=[c for x,y,t,(px,py),c in toplot]
p50cmap=mpl.colormaps['tab10']
colors=[p50cmap(i) for i,(x,y,t,(px,py),c) in enumerate(toplot)]
#print('color=',colors)
ax=rdf.plot(figsize=(14,10),logx=True,ylabel='KHbo2',linewidth=3,legend=True,color=colors,style='',marker='.',markersize=1)

arrowprops={'width':0.5,'headwidth':2,'headlength':2,'shrink':0.15}
for i,(x,y,t,(px,py),c) in enumerate(toplot):
    if x:
        c=p50cmap(i)
        # Dots
        ax.plot(x,y,marker='o',linewidth=3,markersize=6,color=c)
        ax.annotate(f'{t}{x}',(x,y),xytext=(x+px,y+py),xycoords='data',textcoords='offset pixels',
                arrowprops=arrowprops, **{'color':c})
        EXTRAANNO= True
        EXTRAANNO= False
        if EXTRAANNO:
            (ox,oy,ot,(opx,opy),oc)= [ae1wtold,ae1hetold][i]
            ax.plot(ox,oy,marker='o',markersize=6,color='red')
            ax.annotate(f'OLD {ot}{ox}',(ox,oy),xytext=(ox+opx,oy+opy),
                    xycoords='data',textcoords='offset pixels',
                    arrowprops=arrowprops, **{'color':'red'})
        ax.axhline(y,color=c)
        print(f'x={x} y={y}')
        ax.annotate(f'KHbo2={y}',(1,y),xytext=(2.5,y),xycoords='data',textcoords='offset pixels',
                **{'color':c})
    else:
        ax.axhline(y,color=c)

if sphere in toplot:
    y=1.85189
    x=0.15616
    c='r'
    ax.axhline(y,color='r')
    ax.plot(x,y,marker='o',markersize=6,color=c)
    ax.annotate(f'PmO2={x}',(x,y),xytext=(x-80,y+30),xycoords='data',textcoords='offset pixels',
                arrowprops=arrowprops, **{'color':c})
    ax.annotate(f'KHbo2={y}',(1,y),xytext=(2.5,y+20),xycoords='data',textcoords='offset pixels',
            **{'color':c})


#ax.set_xscale('log')
ax.set_xlim(0.001,100)
#ax.set_ylim(0,7.0)
ax.xaxis.set_ticks_position('bottom')
ax.spines['left'].set_position(('data', 1))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
#ax.legend()

ax.spines['bottom'].set_linewidth(3)
ax.spines['left'].set_linewidth(3)
ax.figure.savefig('P50Sigs.svg', format='svg')

#fig1.tight_layout()
plt.show()

'''
             BalbCJ   C57BL6J  C57BL6CCtrl6J  C57BL6CCtrlBalbC
PmO2                                                          
0.003162   0.231761  0.224749       0.216743          0.218615
0.010000   0.688566  0.668140       0.643362          0.648466
0.031623   1.821204  1.768684       1.697493          1.707859
0.100000   3.736633  3.624166       3.466165          3.475588
0.316228   5.461099  5.267964       5.040331          5.037311
1.000000   6.314444  6.062464       5.812372          5.799129
3.162278   6.625426  6.347417       6.092534          6.074935
10.000000  6.727898  6.440422       6.184922          6.165600
31.622777  6.760716  6.470364       6.214496          6.194849
'''
#balbc,0.1051,3.824
#balbcctrl,0.1616,4.217
#j6,0.2668,5.08
#j6ctrl,0.1556,4.156
#ae1wt,0.2064,4.67
#ae1het,0.16196,4.396
#cast,0.1041,3.691
#humf,0.04695,1.793
#humm,0.0516,1.853
#huma,0.05031,1.837
#bovine,0.0878,2.24
