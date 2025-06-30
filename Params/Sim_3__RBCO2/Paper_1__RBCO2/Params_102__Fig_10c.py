# This is a UTF-8 file
# Insert unicode chars in VIM with: insert mode, hit Ctrl-V and type hex unicode "U0001D458"
from Params.Sim_3__RBCO2.Param_Defaults_RBCO2 import *
from Params.Params import *
''' Fig 10c - sensitivity khbo2 vs DHbO2o '''

thisS='Mouse' 
thisGB='C57BL/6Case_11dot6_Fig5A'
thisGT='WT'

species_choices =list(RBCO2_LUT.keys())
si= species_choices.index(thisS)

genebkg_choices =list(RBCO2_LUT[species_choices[si]].keys())
gbi= genebkg_choices.index(thisGB)

genotype_choices=list(RBCO2_LUT[species_choices[si]][genebkg_choices[gbi]].keys())

# Human Readable  Matlab       Valid    Format Col  Group                      Type    Value                            OVCCallback   Dependents                  Dropdown Choices
fig_params= {\
    'Species': (( 'Species'    ,     'Species',  a_string, '{}', 1, 'Experiment', 'ch', (thisS,  ), 'sel_newspecies' , GDEPS), {'choices':species_choices } ),
'Genetic_Bkg': (( 'Genetic Bkg', 'Genetic_Bkg',  a_string, '{}', 1, 'Experiment', 'ch', (thisGB, ), 'sel_newgenbkg'  , GDEPS), {'choices':genebkg_choices } ),
   'Genotype': (( 'Genotype'   ,    'Genotype',  a_string, '{}', 1, 'Experiment', 'ch', (thisGT, ), 'sel_newgenotype', GDEPS), {'choices':genotype_choices} ),
#      'tmax': (( 'Max Time (s)'        ,       'tmax' , pos_float, '{}', 1, 'Experiment', 'tb', [15.0                                  ], None, ()), {}),
#   'D_O2out': (( 'D_O<sub>2</sub>out'  , 'D_O2out'    , pos_float, '{}', 2, ls_pprops   , 'tb', list(1.3313e-5*np.linspace(0.01,1.0,10)), None, ()), {}),
# 'D_HbO2out': (( 'D_HbO<sub>2</sub>out', 'D_HbO2out'  , pos_float, '{}', 2, ls_pprops   , 'tb', [0.0                                   ], None, ()), {}),
#   'D_Hbout': (( 'D_Hbout'             , 'D_Hbout'    , pos_float, '{}', 2, ls_pprops   , 'tb', [0.0                                   ], None, ()), {}),
#    'D_O2in': (( 'D_O<sub>2</sub>in'   , 'D_O2in'     , pos_float, '{}', 2, ls_pprops   , 'tb', list(2.7745e-6*np.linspace(0.01,1.0,10)), None, ()), {}),
   'D_HbO2in': (( 'D_HbO<sub>2</sub>in' , 'D_HbO2in'   , pos_float, '{}', 2, ls_pprops   , 'tb', list(6.07e-8  *np.linspace(0.01,1.0,10)), None, ()), {}),
#    'D_Hbin': (( 'D_Hbin'              , 'D_Hbin'     , pos_float, '{}', 2, ls_pprops   , 'tb', list(6.07e-8  *np.linspace(0.01,1.0,10)), None, ()), {}),
}

fig_param_list= build_param_list(param_list_RBCO2,fig_params)
#params= create_params( fig_param_list )
fParams= {\
    'params':create_params( fig_param_list ),
    'valid_figs': ['Fig 10c'],
    'fname':__file__,
}

