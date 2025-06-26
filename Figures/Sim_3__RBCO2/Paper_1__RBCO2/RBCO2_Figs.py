import matplotlib.pyplot as plt
#from matplotlib.ticker import ScalarFormatter, FormatStrFormatter, FuncFormatter, MaxNLocator
#import matplotlib as mpl
#import matplotlib.artist as mpla
#import matplotlib.patches as mpatch
#from mpl_toolkits.axes_grid1 import make_axes_locatable
#from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg    as FigureCanvas
#from matplotlib.figure import Figure
##from cycler import cycler
##from adjustText import adjust_text
import numpy as np
#import pandas as pd

from Figures.SimFigure import SimFigure
class RBCO2_Fig(SimFigure):
    class FancyText:
        math_khbo2   = r'$k_{HbO_2}$'
        title_kvperms= r'$k_{HbO_2} vs. Pm_{O_2}$'
        title_hbsat  = r'$Hb_{Sat} vs. Time$'
        yaxis_khbo2  = r'$1/t_{37} = k_{HbO_2}$'
        xaxis_perms  = r'$Pm_{O_2}$'
    shades_rbc_o = plt.cm.YlOrRd(np.linspace(0.9 , 0.5, 10))
    shades_rbc_b = plt.cm.BuPu(  np.linspace(0.8 , 0.4, 10))
    
    def __init__(self,sim_results,*args,**kwargs):
        super().__init__()

#    def __init__(self,run_time,run_data,run_params):
#        super().__init__()#'figidDale','sim_resDale','figpropsDale')
    
