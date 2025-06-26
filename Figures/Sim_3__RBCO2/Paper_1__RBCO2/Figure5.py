import numpy as np
import pandas as pd
import matplotlib as mpl
from support import *
from Figures.Sim_3__RBCO2.Paper_1__RBCO2.RBCO2_Figs import RBCO2_Fig

class Fig5(RBCO2_Fig):
    ''' sigmoid per Species
        kHbO2(y) vs Pm_O2(x)
    '''
    def __init__(self,sim_results,fignum,*args,**kwargs):
        super().__init__(sim_results,args,kwargs)

        sr=sim_results

        extras= sr.cp['Extra']()[0]
        FIG5       = 'FIG5'        in extras
        DEBUGHBS   = 'DEBUGHBS'    in extras
        FULLSIGMOID= 'FULLSIGMOID' in extras

        ft=RBCO2_Fig.FancyText
        try:
            titlepart = sr.cp['PlotTitle']()[0]
            titlepart=titlepart.replace('_','\_')
        except KeyError:
            titlepart=''
        titlepart=f'{titlepart}\n'
        title1=f'Fig 5. {titlepart}\n{ft.title_kvperms}'
        title2=f'Fig 5. {titlepart}\n{ft.title_hbsat}'

#        b= self.shades_ajp8o
#        o= self.shades_ajp8b
        self.fp= self.FigProps(
            nrows= 1,
            ncols= 1,
            title= '',#None#f'Fig 5. {titlepart}\n{ft.title_kvperms}'
            plot_d={ 'colors'   : (self.shades_ajp8o,),
                     'remborder': ['top','right'],
                     #'tickspos' : 'both',
                   }
        )

#        self.fp.plot_d={ 'colors'   : (b,)*self.fp.plot_rows * self.fp.plot_cols,
#                         'remborder': ['top','right'],
#                         #'tickspos' : 'both',
#                       }
        self.make_fig(n=2)

        fig1,axs1= self.figaxpairs[0]
        fig2,axs2= self.figaxpairs[1]
        fig1.suptitle(title1, size=20, style='normal')
        fig2.suptitle(title2, size=20, style='normal')

        ax_sig  = axs1[0,0]
        ax_hbsat= axs2[0,0]
        axs= (ax_sig,ax_hbsat)
       
        xlabels= [ft.xaxis_perms, r'$Time(s)$']
        ylabels= [ft.yaxis_khbo2, r'$Hb_{Sat}$']
        logx=['log', 'linear']
        fpp=self.FigPanelProps() # 1 FPP is sufficient here to reuse for all panels

        for ax,xl,yl,lx in zip(axs,xlabels,ylabels,logx):
            fpp.axtitle   = None
            fpp.ylabel    = yl
            fpp.xlabel    = xl
            fpp.logx= lx
            fpp.plotkwargs= { 'linestyle':'-', 'linewidth':3.0, 'marker':'' }
            self.setup_axes( ax, fpp )

        sr.extract( [ sr.get_Hb_Sat, ], [(),], [{}] )

        pm_o2s= sr.cp['Pm_O2']()
        k_37s= [ed.k_37 for ed in sr.eds]

        for ri in range(sr.n_runs):#,(hbsat,) in enumerate(zip(pmco2s,labels)):
            ed= sr.eds[ri]

            fpp.xvar= np.array(sr.t[ri])[:,0]

            fpp.yvar= ed.Hb_Sat
            self.plot_HbSat(ax_hbsat,fpp)

            if DEBUGHBS:
                pm_o2=pm_o2s[ri]
                pm_o2p= f'{pm_o2:0.6}'
                # Mark ts and ys used in interpolation
                #ax_hbsat.plot(t[0,0],Hb_Sat[0], marker='x',markersize=15)
                ax_hbsat.plot(ed.t1,ed.y1, marker='o',markersize=15, label='t1,y1')
                ax_hbsat.plot(ed.t2,ed.y2, marker='v',markersize=15, label='t2,y2')
                ax_hbsat.annotate(f'pmo2:{pm_o2p} (t1:{ed.t1:5f},y1:{ed.y1:5f})',
                    xy=(ed.t1,ed.y1), xycoords="data",
                    xytext=(20,20), textcoords='offset pixels', size=20)
                ax_hbsat.annotate(f'pmo2:{pm_o2p} (t2:{ed.t2:5f},y2:{ed.y2:5f})',
                    xy=(ed.t2,ed.y2), xycoords="data",
                    xytext=(20,20), textcoords='offset pixels', size=20)

                ax_hbsat.plot(ed.t_37,ed.y_37, marker='x',markersize=15)
                #ax_hbsat.axhline(y_37+(0.0001*i))
                ax_hbsat.axvline(ed.t_37)
                ax_hbsat.annotate( f't_37 pmo2={pm_o2p}',
                        xy=(ed.t_37,ed.y_37), xycoords="data",
                        xytext=(2,28*ri), textcoords='offset pixels', size=20)
            self.set_legend(ax_hbsat) 

        #fpp.logx= 'log'
        if fignum == '5':
            hprint('FN=5')
            fpp.xvar= pm_o2s
            fpp.yvar= k_37s
            self.plot_t(ax_sig,fpp)

            ax_sig.set_xscale('log')
            if FULLSIGMOID:
                ax_sig.set_xlim(0.001,100)
                #ax_sig.set_ylim(0,6)
            ax_sig.xaxis.set_ticks_position('bottom')
            ax_sig.spines['left'].set_position(('data', 1))
            ax_sig.spines['bottom'].set_linewidth(3)
            ax_sig.spines['left'].set_linewidth(3)

            if FIG5:
                f5_pmo2=  [     0.0143,     0.0281,     0.0376,    0.0673,  0.0693,    0.0983,     0.1213, 0.1546,         26.63 ]
                f5_name=  ['dKO+pCMBS', 'WT+pCMBS', 'dKO+DIDS', 'WT+DIDS',   'dKO', 'RHag-/-', 'Aqp1 -/-',   'WT', 'H20 Membrane']
                f5_k37=   [     0.8688,     1.5282,     1.8938,    2.7533,  2.7989,    3.3582,     3.6828, 4.0358,         5.9953]
                #f5_k37=   [     0.6877,     1.2023,     1.4937,    2.1783,  2.2151,    2.6579,     2.9191, 3.2059,         4.8297]
                f5colors= [   'purple',        'g',   'purple',       'g', 'purple',      'b',        'r',    'g',    'steelblue']
                f5extraxy=[       None,       None,       None,      None,   (0,15),     None,       None,   None,           None]
                #This is for the colored markers from manuscript
                for p,k,c,exy,n in zip(f5_pmo2,f5_k37,f5colors,f5extraxy,f5_name):
                    ax_sig.plot(p,k,color=c,marker='o',markersize=15, clip_on=False)
                    #extray=0
                    #if (k - last_k) < 0.1:
                    #    print('EXTRA_Y', k, last_k)
                    #    extray= 20
                    if exy:
                        ex,ey=exy
                    else:
                        ex,ey=0,0
                    ax_sig.annotate( f'{n} ({p})', xy=(p,k), xycoords="data",
                            xytext=(20+ex,-20+ey), textcoords='offset pixels', color=c)# size=20)

        elif fignum=='SigPLocator':
            hprint('FN=SigPLoc')
            khbo2_target = sr.cp['kHbO2_RBC_target']()[0]

            fpp.xvar= pm_o2s
            fpp.yvar= k_37s
            fpp.plotkwargs['marker']='o'
            self.plot_t(ax_sig,fpp)

            ax_sig.axhline(khbo2_target, label=f'kHbO2 target = {khbo2_target}')

            ax_sig.annotate(f'kHbO2 target={khbo2_target}',
                    xy=(fpp.xvar[0],khbo2_target),xytext=(10,10),
                    textcoords='offset pixels',size=14)

        elif fignum=='SigmoidSweep':
            hprint('FN=SigSweep')
            batchparams = sr.cp['BatchParams' ]()[0] # Comma sep list from Param File
            sweeptype = sr.cp['SweepType' ]()[0]
            print('BATCHPARAMS:',batchparams)
            print('SWEEPTYPE:',sweeptype)
            bps= batchparams.split(',')

            batchd={ bp : sr.cp[bp]() for bp in bps } 
            #batchlist=[]
            #for ri in range(sr.n_runs):
                #batchlist.append([sr.cp[bp]()[ri] for bp in bps])
                #batchlist.append((sr.cp['MCH'][ri],sr.cp['Hbtot_in'][ri]))
                #print(f'batchlist:{batchlist}')
            if len(pm_o2s) == 1:
                pm_o2s= pm_o2s* sr.n_runs

            if sweeptype == 'MCH':
                #for pmo2,k37,(mch,hbtotin) in zip(pm_o2s,k_37s,batchlist):
                for pmo2,k37,*args in zip(pm_o2s,k_37s,*batchd.values()):
                    # from spreadsheet
                    #hbtotin=4* 1000 * (mchc*10/64316)
                    mch    = args[0]
                    hbtotin= args[1]
                    mchc = hbtotin * 64316 / 40000
                    ax_sig.annotate(f'MCH={mch} MCHC={mchc:0.2f} HbTotIn={hbtotin:0.2f}',
                            xy=(pmo2,k37),xytext=(10,0), textcoords='offset pixels',size=14)
            elif sweeptype == 'MCV':
                #for pmo2,k37,(mcv,hbtotin) in zip(pm_o2s,k_37s,batchlist):
                for pmo2,k37,*args in zip(pm_o2s,k_37s,*batchd.values()):
                    mcv    = args[0]
                    hbtotin= args[1]
                    ax_sig.annotate(f'MCV={mcv} HbTotIn={hbtotin:0.2f}',
                            xy=(pmo2,k37),xytext=(10,0), textcoords='offset pixels',size=14)
            elif sweeptype == 'D':
                #for pmo2,k37,(d,) in zip(pm_o2s,k_37s,batchlist):
                for pmo2,k37,*args in zip(pm_o2s,k_37s,*batchd.values()):
                    d    = args[0]
                    ax_sig.annotate(f'D={d}',
                            xy=(pmo2,k37),xytext=(10,0), textcoords='offset pixels',size=14)
            elif sweeptype == 'P50':
                #for i,(pmo2,k37,(p50,)) in enumerate(zip(pm_o2s,k_37s,batchlist)):
                for pmo2,k37,*args in zip(pm_o2s,k_37s,*batchd.values()):
                    p50    = args[0]
                    ax_sig.annotate(f'P50={float(p50)}, k37={k37:0.4f}',
                            xy=(pmo2,k37),xytext=(10,0),
                            textcoords='offset pixels',size=14)

            sweepcolors=mpl.colormaps['tab10']
            ax_sig.plot(pm_o2s,k_37s, marker='o')#,color=sweepcolors,linewidth=3)

            yl,yh=ax_sig.get_ylim()
            yr=yh-yl
            y10=yr*0.1
            ax_sig.set_ylim(yl-y10,yh+y10)
            ax_sig.legend(loc='upper left')

        fig1.tight_layout()
        fig2.tight_layout()
        #fig1.savefig('P50Sigs.svg', format='svg')
        fig2.savefig('HbSat.svg', format='svg')
        fig1.savefig('P50Points.svg', format='svg')

        outfile= f'{sr.cp["OutFile"]()[0]}.csv'.replace('/','_').replace(' ','_')
        outcol = sr.cp['OutCol']()[0]
        outd= {f'{outcol}_K37':k_37s}
        
        if fignum in ['5','SigPLocator']:
            thisdf= pd.DataFrame(
                outd,
                index=pm_o2s,
            )
        elif fignum == 'SigmoidSweep':
            outd.update( {f'{outcol}_{v}' : batchd[v] for v in bps} )
            thisdf= pd.DataFrame(\
                outd,
                index=pm_o2s,
            )

        #elif sweeptype == 'MCH':
        #    #mchs=batchd['MCH']#[b[0] for b in batchlist]
        #    #hbtis=batchd['Hbtot_in']#[b[1] for b in batchlist]
        #    outd.update( {f'{outcol}_{v}' : batchd[v] for v in bps} )
        #    thisdf= pd.DataFrame(\
                #        outd,
                ##{f'{outcol}_K'   :k_37s,
                ##                 f'{outcol}_mch' :mchs ,
                ##                 f'{outcol}_hbti':hbtis,
                ##                },
                #index=pm_o2s,
            #)
        #elif sweeptype == 'MCV':
        #    mcvs=(b[0] for b in batchlist)
        #    hbtis=(b[1] for b in batchlist)
        #    thisdf= pd.DataFrame(\
                #        {f'{outcol}_K'   :k_37s,
                # f'{outcol}_mcv' :mcvs,
                # f'{outcol}_hbti':hbtis,
                #},
                #index=pm_o2s,
            #)
        #elif sweeptype == 'D':
        #    ds=(b[0] for b in batchlist)
        #    thisdf= pd.DataFrame(\
                #        {f'{outcol}_K'   :k_37s,
                # f'{outcol}_d'   :ds,
                #},
                #index=pm_o2s,
            #)
        #elif sweeptype == 'P50':
        #    p50s=(b[0] for b in batchlist)
        #    thisdf= pd.DataFrame(\
                #        {f'{outcol}_K'   :k_37s,
                # f'{outcol}_P50' :p50s,
                #},
                #index=pm_o2s,
            #)

        thisdf.to_csv(outfile, index=True,index_label='PmO2')

        self.show_fig()

        return
        # OLDER STUFF 
        colors_to_pop=[]
        for i,ri in enumerate(range(n_runs)):
            if not colors_to_pop:
                colors_to_pop= f5colors.copy()

            cur_color=colors_to_pop.pop(0)
            cur_coloralpha=mpl.colors.to_rgba(cur_color, 0.5)

        ''' from plan doc in case it gets modded
        If PM,O2 = 0.1546 & rtorus= 1.01 μm → kHbO2 = 4.0377 s−1 
            Now assume new rtorus = 1.007006… (result of the calc) 
        Then what must PM,O2 be (1.007006) to give kHbO2 = 4.156 s−1. 
        Result => 0.1667080345
        '''

