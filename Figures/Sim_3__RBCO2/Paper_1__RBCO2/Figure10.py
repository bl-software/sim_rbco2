import numpy as np
import matplotlib.pyplot as plt
from Figures.Sim_3__RBCO2.Paper_1__RBCO2.RBCO2_Figs import RBCO2_Fig
from support import *

class Fig10(RBCO2_Fig):
    def rbc_styles(self,n=1):
        p='purple'
        m='mediumpurple'
        y='yellowgreen'
        return {
                 'WT': {'c':'g', 'v':4.0358, 'mfc':'none' },
            'Aqp1-/-': {'c':'r', 'v':3.6828, 'mfc':'none' },
            'RHag-/-': {'c':'b', 'v':3.3582, 'mfc':'none' },
                'dKO': {'c': p , 'v':2.7989, 'mfc':'none' },
            'WT+DIDS': {'c': y , 'v':2.7533, 'mfc': y     },
           'dKO+DIDS': {'c': m , 'v':1.8938, 'mfc': m     },
           'WT+pCMBS': {'c':'g', 'v':1.5282, 'mfc':'g'    },
          'dKO+pCMBS': {'c': p , 'v':0.8688, 'mfc': p     },
        }
    
    def diffusion_stdlines(self, ax, rs):
        for k,v in rs.items():
            ax.axhline(y=v['v'],color=v['c'],linestyle='--',alpha=0.3)
            ax.plot(104,v['v'],color=v['c'],marker='o',markerfacecolor=v['mfc'],label=k,clip_on=False)

    def __init__(self,sim_results,fignum,*args,**kwargs):
        super().__init__(sim_results,args,kwargs)

        sr=sim_results

        ptext,atext={
            '10a': ('A', r'Fig 10a. 𝑘_{HbO_2} vs. (D_{O_2})_o'  ),
            '10b': ('B', r'Fig 10b. 𝑘_{HbO_2} vs. (D_{O_2})_i'  ),
            '10c': ('C', r'Fig 10c. 𝑘_{HbO_2} vs. (D_{HbO_2})_i'),
            '10d': ('D', r'Fig 10d. 𝑘_{HbO_2} vs. (D_{Hb})_i'   ),
        }[fignum]

        self.fp= self.FigProps(
            nrows= 1,
            ncols= 1,
            title= atext,
            plot_d={ 'colors'   : (self.shades_rbc_b,),
                     'remborder': ['top','right'],
                     #'tickspos' : 'both',
                   }
        )

       
        self.make_fig(n=1)
        fig1,axs1= self.figaxpairs[0]
        ax=axs1[0][0]

        sr.extract( [ sr.get_Hb_Sat, ], [(),], [{}] )

        k_37s= [ed.k_37 for ed in sr.eds]

        ylabel= r'$ 1/t_{37} = k_{HbO_2}$'
        xlabel= '% of Control'

        fpp=self.FigPanelProps()
        fpp.paneltate = ptext
        #fpp.axtitle   = atext
        fpp.ylabel    = ylabel
        fpp.xlabel    = xlabel
        fpp.xlims = (0,100)
        fpp.ylims = (0,5)
        self.setup_axes( ax, fpp )

        do2o_ctrl  =1.3313e-5  
        do2i_ctrl  =2.7745e-6
        dhbo2i_ctrl=6.07e-8
        dhbi_ctrl  =6.07e-8
        diffusion,diffctrl= {
            '10a': (sr.rp['D_O2out'  ], do2o_ctrl  ),
            '10b': (sr.rp['D_O2in'   ], do2i_ctrl  ),
            '10c': (sr.rp['D_HbO2in' ], dhbo2i_ctrl),
            '10d': (sr.rp['D_Hbin'   ], dhbi_ctrl  ),
        }[fignum]

        hprint(diffusion)

        y=(np.array(diffusion)/diffctrl)*100
        hprint(y)
        ax.plot( y, k_37s, marker='x')

        rs= self.rbc_styles()
        self.diffusion_stdlines(ax,rs)

        ax.legend()
        self.show_fig()

        return

        for ri in range(sr.n_runs):
            ed= sr.eds[ri]

            fpp.yvar= ed.Hb_Sat

            #titk= 'Fig 9a. 𝑘_{HbO_2} vs. (D_{O_2})_O'
            ax=axs['A']

            #plotvals=(np.array(do2_outs)/do2o_ctrl)*100

            xticks = np.arange(0, 101, 20)
            xlabels = [f'{x:d}%' for x in xticks]
            ax.set_xticks(xticks, labels=xlabels)
            ax.set_yticks(np.arange(1,6))#xticks, labels=xlabels)
            ax.margins(x=120)

            #do2_outs_pc=(np.array(do2_outs)/1.3313e-5)*100 # percent
#            ax.plot(plotvals, k_37s, marker='o',clip_on=False)
        
#        ax.legend()

#        fig1.tight_layout()
#        plt.show()

