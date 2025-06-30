from Figures.Sim_3__RBCO2.Paper_1__RBCO2.RBCO2_Figs import RBCO2_Fig

class Fig(RBCO2_Fig):
    def __init__(self,run_time,run_data,run_params,*args,**kwargs):
        super().__init__(run_time,run_data,run_params,'5',args,kwargs)
#def fig__RBCO2_fig_5bar(self, fignum, rp):
        ''' bar plot with WT, AQP, RhAG, dKO '''
        print('''FIG 5 bar plot with WT, AQP, RhAG, dKO ''')
        plot_rows=1
        plot_cols=1

        try:
            titlepart = self.run_params['PlotTitle'][0]
            titlepart=titlepart.replace('_','\_')
        except KeyError:
            titlepart='def'
        print('tp=',titlepart)


        fig,axs = self.fig_makefig(1, 1, size=None, title=f'BAR{titlepart}')
        ax_hbsat=axs[0,0]
        ax_hbsat.set_ylabel('K37', size=18, style='normal')
        ax_hbsat.set_xlabel('Stuff', size=18, style='normal')

        k_37s=[]
        batchlist=[]
        n_runs = len(self.run_time)
        for i,ri in enumerate(range(n_runs)):
            t     = self.run_time[ri]
            X     = self.run_data[ri]
            R     = self.run_params['rcm'][ri]
            R_inf = self.run_params['R_infcm'][ri]
            n_in  = self.run_params['n_in'][ri]
            n_out = self.run_params['n_out'][ri]
            #print('PR=',self.run_params)
            N= n_in + n_out + 1
            hbtot_in = self.run_params['Hbtot_in'][ri]
            #pm_o2 = self.run_params['Pm_O2'][ri]
            #khbo2_target = self.run_params['kHbO2_RBC_target'][ri]

            #batchparams = self.run_params['BatchParams' ][0]
            #sweeptype = self.run_params['SweepType' ][0]

            Hb_Sat= self.calc_hb_sat(X,N,n_in,n_out,R,R_inf)
            k_37,t_37,y_37,t1,t2,y1,y2= self.calc_37s(t,Hb_Sat)
            #pm_o2s.append(pm_o2)
            k_37s.append(k_37)
        print(f'k37:{k_37s}   rcm:{R}   hbtotin:{hbtot_in}')


