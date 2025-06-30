# This is a UTF-8 file
# Insert unicode chars in VIM with: insert mode, hit Ctrl-V and type hex unicode "U0001D458"
from Params.Sim_3__RBCO2.Param_Defaults_RBCO2 import *
from Params.Params import *

''' Fig 6 - bar graph of 4 types '''

sp= 'Mouse'

#bk= 'C57BL/6Case_RXO_116'
bk= 'C57BL/6Case_DEH_goodklys'

#gt=( 'WT',)
#gt= ('AQP1-KO',)
#gt=( 'RhAG-KO',)
gt=( 'dKO',)

#gt=( 'WT','AQP1-KO','RhAG-KO','dKO')
#species_choices =list(RBCO2_LUT.keys())
#genebkg_choices =list(RBCO2_LUT[sp].keys())
#mutation_choices=list(RBCO2_LUT[sp][bk].keys())
hbtotin,r={
        'WT'     :(18.73, 1.01e-4),
        'AQP1-KO':(17.71, 1.04e-4),
        'RhAG-KO':(17.87, 1.09e-4),
        'dKO'    :(18.16, 1.07e-4),
    }[gt[0]]
#                   Human Readable  Matlab       Valid    Format Col  Group                      Type    Value                            OVCCallback   Dependents                  Dropdown Choices
fig_params= {\
         'Species': ((     'Species',     'Species',  a_string, '{}', 1, 'Experiment', 'ch', (sp,)  , 'sel_newspecies' , GDEPS), {'choices':species_choices }),
     'Genetic_Bkg': (( 'Genetic Bkg', 'Genetic_Bkg',  a_string, '{}', 1, 'Experiment', 'ch', (bk,)  , 'sel_newgenbkg'  , GDEPS), {'choices':genebkg_choices }),
        'Genotype': ((    'Genotype',    'Genotype',  a_string, '{}', 1, 'Experiment', 'ch', gt     , 'sel_newgenotype', GDEPS), {'choices':mutation_choices}),
            'tmax': (('Max Time (s)',        'tmax', pos_float, '{}', 1, 'Experiment', 'tb', [1.50 ],              None, (   )), {}),
           'Pm_O2': ((       ls_pmo2,       'Pm_O2', pos_float, '{}', 2,    ls_pprops, 'tb', ['LUT'],              None, (   )), {}),

'kHbO2_RBC_target': (('kHbO2_RBC_target', 'kHbO2_RBC_target', pos_float, '{}', None, None        ,    '', ['LUT'  ], None, ()), {}),
       'PlotTitle': ((       'PlotTitle',        'PlotTitle',  a_string, '{}',    2, 'Extra'     ,  'tb', [''     ], None, ()), {}),
        'Hbtot_in': ((       ls_Hbtot_in,         'Hbtot_in', pos_float, '{}',    1, 'Experiment', 'otb', [hbtotin], None, ()), {}),
               'R': ((      ls_r_torus_u,      'nomat_R_TOR', pos_float, '{}',    1, 'Experiment', 'otb', [1.01e-4], None, ()), {}),
}

fig_param_list= build_param_list(param_list_RBCO2,fig_params)
#params= create_params( fig_param_list )

fParams= {\
    'params':create_params( fig_param_list ),
    'valid_figs': ['Fig 6 Bar'],
    'fname':__file__,
}

