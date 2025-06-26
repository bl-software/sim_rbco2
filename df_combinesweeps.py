import pandas as pd
import matplotlib.pyplot as plt

#df=pd.DataFrame( 
#    [ [ 4.11,4.12,4.13,4.14 ],
#      [ 4.21,4.22,4.23,4.24 ],
#      [ 4.31,4.32,4.33,4.34 ],
#      [ 4.41,4.42,4.43,4.44 ],
#    ],
#    index=[ 0.1,0.2,0.3,0.4 ],
#    columns=['r1','r2','r3','r4']
#)

indexval= 'PmO2'

#filelist=['BalbCJ.csv', 'BalbCJUP.csv',
#'C57BL6J.csv', 'C57BL6JUP.csv',
#'C57BL6CCtrl6J.csv', 'C57BL6CCtrl6JUP.csv',
#'C57BL6CCtrlBalbC.csv', 'C57BL6CCtrlBalbCUP.csv']

#sweeptype='MCH'
#sweeptype='MCV'
sweeptype='D'
note=''

''' ODER MATTERS for some reason '''
filelist=[]
if sweeptype=='MCH':
    filelist+=[('PmO2B' , 'BalbC_J_Pan_MHC_Sweep.csv'               ),
               ('PmO26C', 'C57BL_6Case_Ctrl_BalbC_Pan_MHC_Sweep.csv'),
               ('PmO26' , 'C57BL_6J_Pan_MHC_Sweep.csv'              ),
               ('PmO2BC', 'C57BL_6Case_Ctrl_6J_Pan_MHC_Sweep.csv'   ),
    ]
    filelist+=[\
        ('PmO2HF','Human_FemaleN4_MHC_Sweep.csv'),
        ('PmO2HM','Human_MaleN11_MHC_Sweep.csv' ),
        ('PmO2HA','Human_AvgN15_MHC_Sweep.csv'  ),
    ]

    filelist+=[('PmO2BV','Bovine_MHC_Sweep.csv')]

elif sweeptype in ['MCV','D']:
    if sweeptype == 'MCV':
        note='10pts'
    filelist+=[('PmO2B' , f'{sweeptype}Sweep_BalbC_J_Pan{note}.csv'               ),
               ('PmO26C', f'{sweeptype}Sweep_C57BL_6Case_Ctrl_BalbC_Pan{note}.csv'),
               ('PmO26' , f'{sweeptype}Sweep_C57BL_6J_Pan{note}.csv'              ),
               ('PmO2BC', f'{sweeptype}Sweep_C57BL_6Case_Ctrl_6J_Pan{note}.csv'   ),
    ]
    filelist+=[\
        ('PmO2HF',f'{sweeptype}Sweep_Human_FemaleN4{note}.csv'),
        ('PmO2HM',f'{sweeptype}Sweep_Human_MaleN11{note}.csv' ),
        ('PmO2HA',f'{sweeptype}Sweep_Human_AvgN15{note}.csv'  ),
    ]

    filelist+=[('PmO2BV',f'{sweeptype}Sweep_Bovine{note}.csv')]

fig,ax=plt.subplots(figsize=(14,10))
dfs=[]
toplot=[]
for pc,fn in filelist:
    dfs.append(pd.read_csv(fn).rename(columns={'PmO2':pc}))#set_index(indexval))
    toplot.append((pc,dfs[-1].columns[1]))
    print('\ngot df=\n',dfs[-1])

print('toplot=',toplot)

rdf= pd.concat(dfs, axis=1)
print('rdf=\n',rdf)

colors=['blue','orange','green','red','pink','lightblue','purple','brown']
if sweeptype=='MCH':
    balbc    =(0.1051, 3.824,'PmO2=',  10,-15, 0)
    balbcctrl=(0.1616, 4.217,'PmO2=',  10, -15, -3)
    j6       =(0.2668, 5.08 ,'PmO2=', -410, 0, 0)
    j6ctrl   =(0.1556, 4.156,'PmO2=', -410, -10, -2)
    humf     =(0.04695,1.793,'PmO2=', 200, 0, 5)
    humm     =(0.0516, 1.853,'PmO2=', 100, 0, 5)
    huma     =(0.05031,1.837,'PmO2=',  20, -5, -10)
    bovine   =(0.0409, 2.24 ,'PmO2=',  10, 0, 0)
elif sweeptype=='MCV':
    balbc    =(0.1051, 3.824,'PmO2=',  10,-0, 0)
    balbcctrl=(0.1616, 4.217,'PmO2=',  10,-0, -3)
    j6       =(0.2668, 5.08 ,'PmO2=',-110,  0, 0)
    j6ctrl   =(0.1556, 4.156,'PmO2=',-270,5, -2)
    humf     =(0.04695,1.793,'PmO2=', 10,  0, 0)
    humm     =(0.0516, 1.853,'PmO2=', 10,  0, 0)
    huma     =(0.05031,1.837,'PmO2=',  10, -0,0)
    bovine   =(0.0409, 2.24 ,'PmO2=',  10,  0, 0)
elif sweeptype=='D':
    balbc    =(0.1051, 3.824,'PmO2=',  10, 0, 0)
    balbcctrl=(0.1616, 4.217,'PmO2=',  10, 0, 0)
    j6       =(0.2668, 5.08 ,'PmO2=', -80, 0, 0)
    j6ctrl   =(0.1556, 4.156,'PmO2=', -80, 0, 0)
    humf     =(0.04695,1.793,'PmO2=', 120, 0, 0)
    humm     =(0.0516, 1.853,'PmO2=', 200, 0, 0)
    huma     =(0.05031,1.837,'PmO2=',  30, 0, 0)
    bovine   =(0.0409, 2.24 ,'PmO2=',  10, 40, 0)

points=[balbc,balbcctrl,j6,j6ctrl,humf,humm,huma,bovine]
arrowprops={'width':0.5,'headwidth':2,'headlength':2,'shrink':0.15}
print('zip',list(zip(toplot,points)))
print('rdf=\n',rdf.columns)
for i,((x,y),(p,k,t,offx,offy,spc)) in enumerate(zip(toplot,points)):
    print('x=',x)
    print('y=',y)
    print('p=',p)
    print('k=',k)
    c=colors[i]
    ax.plot(rdf[x],rdf[y], color=c,marker='o',label=y, clip_on=False)
    ax.axhline(k,color=c,label=f'kHbO2 target = {k}')
    
    if sweeptype=='MCH':
        hbtin = f'{y.replace("_K","_hbti")}'
        hbtis = rdf[hbtin]#f'{y.replace("_K","_hbti")}']
        mchn = f'{y.replace("_K", "_mch")}'
        mchs  = rdf[mchn]
        batchlen= len(mchs)
        delta= mchs.max() - mchs.min()
        vals=zip(mchs,hbtis)
    elif sweeptype=='MCV':
        hbtin = f'{y.replace("_K","_hbti")}'
        hbtis = rdf[hbtin]#f'{y.replace("_K","_hbti")}']
        mcvn = f'{y.replace("_K", "_mcv")}'
        mcvs  = rdf[mcvn]
        batchlen= len(mcvs)
        delta= mcvs.max() - mcvs.min()
        vals=zip(mcvs,hbtis)
    elif sweeptype=='D':
        dn = f'{y.replace("_K", "_d")}'
        ds  = rdf[dn]
        batchlen= len(ds)
        delta= ds.max() - ds.min()
        vals=zip(ds)#zip(mcvs,hbtis)

    ax.set_title(f'{sweeptype} Sweeps: {batchlen} points, range {delta}')

    pmo2=rdf[x][0]
    maxk=0
    mink=1000
    #for j,(mch,hbti) in enumerate(zip(mchs,hbtis)):
    for j,v in enumerate(vals):
        k37=rdf[y][j]
        if k37 > maxk:
            maxk=k37
        if k37 < mink:
            mink=k37

        if sweeptype=='MCH':
            mch=v[0]
            hbti=v[1]
            mchc = hbti * 64316 / 40000
            print('mch',mch)
            print('hbti',hbti)
            print('mchc',mchc)
            if i not in [4,5]:
                ax.annotate(f'MCH={mch} MCHC={mchc:0.2f} HbTotIn={hbti:0.2f}',
                        xy=(pmo2,k37),xytext=(offx,offy+j*spc), textcoords='offset pixels',
                        size=14,color=c)
            deltaxy=(0.035,5.5)

        elif sweeptype=='MCV':
            mcv=v[0]
            hbti=v[1]
            #if i not in [4,5]:
            #if j==4:
            #    spc +=4
            ax.annotate(f'MCV={mcv} HbTotIn={hbti:0.2f}',
                    xy=(pmo2,k37),xytext=(offx,offy+j*spc), textcoords='offset pixels',
                    size=14,color=c)
            deltaxy=(0.045,5.0)

        elif sweeptype=='D':
            d=v[0]
            ax.annotate(f'D={d}',
                    xy=(pmo2,k37),xytext=(offx,offy+j*spc), textcoords='offset pixels',
                    size=14,color=c)
            deltaxy=(0.035,5.7)

    deltak=maxk-mink
    ax.annotate(f'Δk37={deltak}',
            xy=deltaxy,xytext=(0,-i*20), textcoords='offset pixels',
            size=16,color=c)

ax.set_xlabel('PmO2')
ax.set_ylabel('kHbO2')
ax.legend()

#ax.set_xlim(0.001,100)
##ax.set_ylim(0,6)
#ax.xaxis.set_ticks_position('bottom')
#ax.spines['left'].set_position(('data', 1))
#ax.spines['top'].set_visible(False)
#ax.spines['right'].set_visible(False)
##ax.legend()
#
##fig1.tight_layout()
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
