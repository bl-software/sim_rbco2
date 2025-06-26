# This is a UTF-8 file
from Params.Sim_3__RBCO2.Param_Defaults_RBCO2 import *
from Params.Params import *
import math

#gt='DF016-m'; PMO2LIST= list(np.linspace(0.04,0.07,7))
#gt='DF017-m'; PMO2LIST= list(np.linspace(0.05,0.08,7))
#gt='DF019-f'; PMO2LIST= list(np.linspace(0.03,0.05,7))
#gt='DF020-m'; PMO2LIST= list(np.linspace(0.05,0.08,7))
#gt='DF023-f'; PMO2LIST= list(np.linspace(0.03,0.06,7))
#gt='DF026-f'; PMO2LIST= list(np.linspace(0.03,0.07,7))
#gt='DF028-m'; PMO2LIST= list(np.linspace(0.05,0.08,7))
#gt='DF031-m'; PMO2LIST= list(np.linspace(0.03,0.07,7))
#gt='DF032-m'; PMO2LIST= list(np.linspace(0.03,0.08,7))
#gt='DF033-m'; PMO2LIST= list(np.linspace(0.04,0.08,7))
#gt='DF035-m'; PMO2LIST= list(np.linspace(0.04,0.08,7))
#gt='DF036-m'; PMO2LIST= list(np.linspace(0.04,0.08,7))
#gt='DF038-m'; PMO2LIST= list(np.linspace(0.04,0.08,7))
#gt='DF039-m'; PMO2LIST= list(np.linspace(0.04,0.08,7))
#PMO2LIST= list(np.linspace(0.16164,0.16165,7) )
#PMO2LIST= list(np.linspace(0.1666,0.1668,21                ))
## k=4.156
#PMO2LIST= list(np.linspace(0.1666704,0.166710,21           ))
#                                                   
## k=4.0377
#PMO2LIST= list(np.linspace(0.153155,0.153157,7             ))
#PMO2LIST= list(np.linspace(0.153150055520,0.153150055521,11))
#PMO2LIST= list(np.linspace(0.15,0.16,7                     ))
#PMO2LIST= list(np.logspace(-3,1.5,21                       ))
#PMO2LIST= list(np.linspace(0.1531500550,0.1531500560,11    ))
#PMO2LIST= list(np.linspace(0.153150,0.153155,11            ))
#PMO2LIST= list(np.linspace(0.153150,0.153160,11            ))
#PMO2LIST= list(np.linspace(0.25,0.30,7))
#PMO2LIST= list(np.linspace(0.161,0.163,5) )

#list(np.logspace(-3,1.5,41))
#list(np.logspace(-3,1.5,41))
#list(np.logspace(-3,1.5,41))
#list(np.linspace(0.1666,0.1668,21)                )
#list(np.linspace(0.1666704,0.166710,21)           )
#list(np.linspace(0.153155,0.153157,7)             )
#list(np.linspace(0.153150055520,0.153150055521,11))
#list(np.linspace(0.1531500550,0.1531500560,11)    )
#list(np.linspace(0.153150,0.153155,11)            )
#list(np.linspace(0.153150,0.153160,11)            )
#    'C57BL/6Case_Ctrl_BalbC_Pan': list(np.linspace(0.16164,0.16165,7) ),
#    'BalbC/J_Pan'               : list(np.linspace(0.10,0.12,5)),
#    'C57BL/6Case_Ctrl_6J_Pan'   : list(np.linspace(0.15,0.20,7)),
#    'C57BL/6J_Pan'              : list(np.linspace(0.25,0.30,7))

extras=[\
    'PLOCATOR',
]
### Computer runs out of memory so have to break ( as of 2025 in to 2 parts )
#nbreaks=3
#maxperbreak=27 # total of 81 runs for a nice sigmoid
nbreaks=2
maxperbreak=41 # total of 81 runs for a nice sigmoid
totalruns= nbreaks * maxperbreak
#fulllogspace=list(np.logspace(-2.5,1.5,totalruns))

tmin ={ 0.002   : 30,
        0.02    : 15,
        math.inf:  1.5,
       }
def testtime(v):
    for tmk,tmv in tmin.items():
        if v < tmk:
            return tmv

if 'PLOCATOR' in extras:
    fulllogspace= list(np.logspace(-1,-.5,8))
    fulllogspace= pts41_sig=    list(np.logspace(-3,1.5,41))
    tmaxs=[ testtime(v) for v in fulllogspace ]

run=1
#run=2
#run=3
start= (run-1) * maxperbreak
end  = run     * maxperbreak
pmo2s=fulllogspace[start:end]


thisS='Mouse' 
#thisS='Bovine' 
#thisS='Human' 

#thisGB='Human'
#thisGB='C57BL/6Case_RXO_116'
#thisGB='C57BL/6Case_Ctrl_6J_Pan'
#thisGB='C57BL/6J_Pan'

#thisGB='Sphere'
#thisGB='Sphere2'
thisGB='SphereCTRL'
#thisGB='Sphere647'

#thisGB='C57BL/6Case_Ctrl_BalbC_Pan'
#thisGB='BalbC/J_Pan'
#thisGB='C57BL/6Case_RXO'
#thisGB='AE1'
#thisGB='CAST/EIJ'
#thisGB='Human'                  ############ 3.235   8.2023   

#thisGB='Bovine'
thisGBf=thisGB.replace('/','_').replace('-','_') # Freindly Version

thisGT='WT'
#thisGT='Het'
#thisGT='DF016-m'
#thisGT='DF017-m'
#thisGT='DF019-f'
#thisGT='DF020-m'
#thisGT='DF023-f'
#thisGT='DF026-f'
#thisGT='DF028-m'
#thisGT='DF031-m'
#thisGT='DF032-m'
#thisGT='DF033-m'
#thisGT='DF035-m'
#thisGT='DF036-m'
#thisGT='DF038-m'
#thisGT='DF039-m'
#thisGT='DF040-f'
#thisGT='WT-m'
#thisGT='WT-f'
#thisGT='Human_MaleN11'
#thisGT='Human_FemaleN4'
#thisGT='Human_AvgN15'
#thisGT='Bovine'
#thisGT='C57BL/6J_HumanCtrl'
thisGTf=thisGT.replace('/','_').replace('-','_') # Freindly Version

species_choices =list(RBCO2_LUT.keys())
si= species_choices.index(thisS)

genebkg_choices =list(RBCO2_LUT[species_choices[si]].keys())
gbi= genebkg_choices.index(thisGB)

genotype_choices=list(RBCO2_LUT[species_choices[si]][genebkg_choices[gbi]].keys())
gti= genotype_choices.index(thisGT) # This is only an error check on above

plottitle=f'{thisGB}-{thisGT}-run{run}'                
outfile  =f'{thisS}{thisGBf}{thisGTf}_r{run}_{nbreaks}'
outcol   =f'{thisS}{thisGBf}{thisGTf}'                 


extra=','.join(extras) # need to pass in singe item so no trigger of batching or wrong num params

### TODO WARNING 
### TODO WARNING 
### TODO WARNING 
### TODO WARNING 
### TODO WARNING 
### TODO WARNING 
#pmo2s=[0.1546,]

#pmo2s=[0.15460,]
if len(pmo2s) == 1:
    outfile  =f'{thisS}{thisGBf}{thisGTf}_PmO2_{pmo2s[0]}'
    tmaxs=[1.5,]

fig_params= {\
    'Species': (( 'Species'    ,     'Species',  a_string, '{}', 1, 'Experiment', 'ch', (thisS,   ), 'sel_newspecies' , GDEPS), {'choices':species_choices } ),
'Genetic_Bkg': (( 'Genetic Bkg', 'Genetic_Bkg',  a_string, '{}', 1, 'Experiment', 'ch', (thisGB,  ), 'sel_newgenbkg'  , GDEPS), {'choices':genebkg_choices } ),
   'Genotype': (( 'Genotype'   ,    'Genotype',  a_string, '{}', 1, 'Experiment', 'ch', (thisGT,  ), 'sel_newgenotype', GDEPS), {'choices':genotype_choices} ),

       'tmax': (('Max Time (s)',        'tmax', pos_float, '{}', 1, 'Experiment', 'tb', tmaxs      ,              None, (   )), {}),
      'Pm_O2': ((       ls_pmo2,       'Pm_O2', pos_float, '{}', 2,    ls_pprops, 'tb', pmo2s      ,              None, (   )), {}),

  'PlotTitle': (( 'PlotTitle'  ,   'PlotTitle',  a_string, '{}', 2,      'Extra', 'tb', [plottitle],              None, (   )), {}),
    'OutFile': (( 'OutFile'    ,     'OutFile',  a_string, '{}', 2,      'Extra', 'tb', [outfile  ],              None, (   )), {}),
     'OutCol': (( 'OutCol'     ,      'OutCol',  a_string, '{}', 2,      'Extra', 'tb', [outcol   ],              None, (   )), {}),
      'Extra': (( 'Extra'      ,       'Extra',  a_string, '{}', 2,      'Extra', 'tb', [extra    ],              None, (   )), {}),
}
if thisGB=='Sphere647':
#SPHEROCYTE
    fig_params.update({\
    'Hbtot_in': (( ls_Hbtot_in       , 'Hbtot_in'       , pos_float, '{}',   1, 'Experiment', 'otb',[9.5,      ], None , ( )), {} ),
             'rµm': (( ls_r_torus_u      , 'R_um'           , pos_float, '{}',   1, 'Experiment', 'otb',[3.23,   ], None , ('R_infµm','n_in','r_sphere','rcm',)), {} ),
             'rcm': (( ls_r_torus_c      , 'R'              , pos_float, '{}',   1, 'Experiment', 'otb',[0.000323, ], None , ( )), {} ),
               'R': (( 'R<sub>Torus</sub> (µm)', 'nomat_R_TOR', pos_float, '{}', 1, 'Experiment', 'otb',[0.0,      ], None , ( )), {} ),
'kHbO2_RBC_target': (( 'kHbO2_RBC_target','kHbO2_RBC_target', pos_float, '{}',None,         None,    '',[1.85189,  ], None , ( )), {} ),
})
elif thisGB=='SphereCTRL':
    fig_params.update({\
    'Hbtot_in': (( ls_Hbtot_in       , 'Hbtot_in'       , pos_float, '{}',   1, 'Experiment', 'otb',[18.73,      ], None , ( )), {} ),
             'rµm': (( ls_r_torus_u      , 'R_um'           , pos_float, '{}',   1, 'Experiment', 'otb',[1.01,   ], None , ('R_infµm','n_in','r_sphere','rcm',)), {} ),
             'rcm': (( ls_r_torus_c      , 'R'              , pos_float, '{}',   1, 'Experiment', 'otb',[0.000101, ], None , ( )), {} ),
               'R': (( 'R<sub>Torus</sub> (µm)', 'nomat_R_TOR', pos_float, '{}', 1, 'Experiment', 'otb',[0.0,      ], None , ( )), {} ),
'kHbO2_RBC_target': (( 'kHbO2_RBC_target','kHbO2_RBC_target', pos_float, '{}',None,         None,    '',[4.03581,  ], None , ( )), {} ),
})
fig_param_list= build_param_list(param_list_RBCO2,fig_params)
#params= create_params( fig_param_list )

fParams= {\
    'params':create_params( fig_param_list ),
    'valid_figs': ['Fig 5', 'Fig SigPLocator'],
    'fname':__file__,
}

