from Figures.Sim_3__RBCO2.Paper_1__RBCO2.Figure6 import Fig6
class Fig(Fig6):
    def __init__(self,run_time,run_data,run_params,*args,**kwargs):
        super().__init__(run_time,run_data,run_params,'6PERMSSweep',args,kwargs)
    def post_plot(self,ax):
        pass

