import numpy as np
from Figures.Sim_1__JTB.Paper_1__JTB2012.JTB2012_Figs import JTB2012_Fig

class Fig(JTB2012_Fig):
    def __init__(self,sim_results,*args,**kwargs):
        super().__init__(sim_results,args,kwargs)

        sr=sim_results

        self.fp= self.FigProps(
            nrows = 2,
            ncols = 2,
            title = 'JTB 2012 Fig 7: Effect of CO_2 membrane permeability',
            plot_d= { 'colors'   : (self.shades_7,) * 4,
                        #'remborder': ['top','right'],
                         'tickspos' : 'both', }
        )
        self.make_fig()
        axs={'pHs'   : self.axs[0,0],
             'pHi'   : self.axs[0,1],
             'delpHs': self.axs[1,0],
             'dpHidt': self.axs[1,1],
        } 

        paneltext= [      'A',       'C',     'B',     'D']
        xlabels  = ['Time(s)', 'Time(s)', '$P_{M,CO_{2}}(cm/s)$', '$P_{M,CO_{2}}(cm/s)$']
        ylabels  = [r'$pH_s$', r'$pH_i$', r'$(\Delta pH_s)_{max}$', r'$-(dpH_i/dt)_{max}$' ]

        pmcl='$P_{M,CO_{2}}$'
        labels= [\
            f'{pmcl}$ = 34.2\ cm/s$',
            f'{pmcl}$/10^1$',
            f'{pmcl}$/10^2$',
            f'{pmcl}$/10^3$',
            f'{pmcl}$/10^4$',
            f'{pmcl}$/25x10^4$',
            f'{pmcl}$/50x10^4$',
            f'{pmcl}$/75x10^4$',
            f'{pmcl}$/10^5$',]

        #if self.TESTING:
        #    exp_results,exp_testkeys = self.jtb2012_fig7_expected()
        #test_res= {}
        fpp=self.FigPanelProps() # 1 FPP is sufficient here to reuse for all 6 panels
        for i,(axn,ax) in enumerate(axs.items()):
            fpp.paneltate = paneltext[i]
            fpp.ylabel    = ylabels[i]
            fpp.xlabel    = xlabels[i]
            fpp.logx= 'linear'
            if axn in ['delpHs','dpHidt']:
                fpp.logx= 'log'
            self.setup_axes( ax, fpp )

        plotkwargs={\
                'pHi': {'linestyle':'-', 'linewidth':3.0, 'marker':''},
                'pHs': {'linestyle':'-', 'linewidth':3.0, 'marker':''},
                'dpHidt': {'linestyle':'' , 'markersize':10.0, 'marker':'o'},
                'delpHs': {'linestyle':'' , 'markersize':10.0, 'marker':'o'},
            }
        pmco2s= [ v for v in sr.cp['Pm_CO2_input']()] # mm -> um

        sr.extract( [ sr.get_substance, ], [('pH',),], [{},] )
        
        for ri,(pmco2,lab) in enumerate(zip(pmco2s,labels)):
            ed= sr.eds[ri]
            pHi= sr.get_pHi(ri,ed,depth_um=50)
            pHs= sr.get_pHs(ri,ed,depth_um=0 )

            fpp.xvar= np.array(sr.t[ri])[:,0]

            fpp.plotkwargs=plotkwargs['pHi']
            fpp.plotkwargs.update({'label':lab})
            fpp.yvar= pHi
            self.plot_pH(axs['pHi'], fpp)

            fpp.plotkwargs=plotkwargs['pHs']
            fpp.plotkwargs.update({'label':lab})
            fpp.yvar= pHs
            self.plot_pH(axs['pHs'], fpp)

            fpp.xvar= pmco2

            sr.get_dpHi_dt(ri,ed,pHi)
            sr.get_delpHs(ri,ed,pHs)

            fpp.yvar= ed.del_pHs_I
            fpp.plotkwargs=plotkwargs['delpHs']
            self.plot_delpHs(axs['delpHs'], fpp)

            fpp.yvar= -ed.max_dpHi_dt_I
            fpp.plotkwargs=plotkwargs['dpHidt']
            self.plot_delpHs(axs['dpHidt'], fpp)

        self.set_legend(axs['pHi'])
        self.set_legend(axs['pHs'])

        self.show_fig()

        #test_res[run_var_s]={}

#            if self.TESTING:
#                axs2[0,0].plot(pHi, label=f'pHi {run_var_s}')
#                axs2[0,0].legend()
#
#                dpHi = np.ediff1d( pHi ) #The differences between consecutive elements of an array.
#                axs2[1,0].plot(dpHi, label=f'dpHi {run_var_s}')
#                axs2[1,0].legend()
#
#                dt = np.ediff1d( np_time )
#                axs2[2,0].semilogy(dt, label=f'dt {run_var_s}')
#                axs2[2,0].legend()
#                # axs2[2].set_ylim(0.0,0.5)
#                # axs2[3].plot(dpHi_dt[2500:], label='dpHi_dt')
#                axs2[3,0].plot(dpHi_dt, label=f'dpHi_dt {run_var_s}')
#                #axs2[3,0].plot(range(1500,2500),dpHi_dt[1500:2500], label=f'dpHi_dt {run_var_s}')
#                axs2[3,0].plot(max_dpHi_dt_idx, max_dpHi_dt, 'kx')
#                #axs2[3,0].plot(dpHi_dt[:100], label='dpHi_dt')
#                axs2[3,0].legend()
#                axs2[3,0].set_ylim(-0.01,0.005)
#
#            test_res[run_var_s]['max_dpHi_dt'  ]= max_dpHi_dt,None
#            test_res[run_var_s]['index_dpHi_dt']= max_dpHi_dt_idx,None
#            test_res[run_var_s]['delta_pHs'    ]= delta_pHs,None
#            #print(test_res)
#
#        if self.TESTING:
#            self.test_mfiles()
#            self.test_results(exp_results,test_res)
 
