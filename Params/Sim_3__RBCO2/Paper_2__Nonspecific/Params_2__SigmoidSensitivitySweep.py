# This is a UTF-8 file
# Insert unicode chars in VIM with: insert mode, hit Ctrl-V and type hex unicode "U0001D458"
from Params.Sim_3__RBCO2.Param_Defaults_RBCO2 import *
from Params.Params import *

#NOTE Doing this way so LUT file doesnt matter as it changes
Ss = ['Mouse', 'Bovine', 'Human']
GBs= ['C57BL/6Case_Ctrl_6J_Pan', 'C57BL/6J_Pan', 'C57BL/6Case_Ctrl_BalbC_Pan', 'BalbC/J_Pan', 'C57BL/6Case_RXO', 'Human', 'Bovine']
GTs= ['WT', 'WT-m', 'WT-f', 'Bovine_RXOTests', 'Human_FemaleN4', 'Human_MaleN11', 'Human_AvgN15','C57BL/6J_HumanCtrl']

thisS='Mouse' 
#thisS='Bovine' 
#thisS='Human' 

#thisGB='C57BL/6Case_Ctrl_6J_Pan'
thisGB='C57BL/6J_Pan'
#thisGB='C57BL/6Case_Ctrl_BalbC_Pan'
#thisGB='BalbC/J_Pan'
#thisGB='C57BL/6Case_RXO'
#thisGB='Human'
#thisGB='Bovine'

thisGT='WT'
#thisGT='WT-m'
#thisGT='WT-f'
#thisGT='Human_MaleN11'
#thisGT='Human_FemaleN4'
#thisGT='Human_AvgN15'
#thisGT='Bovine_RXOTests'
#thisGT='C57BL/6J_HumanCtrl'


sweeptype='MCH'
#sweeptype='MCV'
#sweeptype='D'
#sweeptype='P50'

note=''

mch_list=['LUT']
mcv_list=['LUT']
d_list=['LUT']
p50_list=[9.35]

titlepart= f'{sweeptype} Sweep'

if sweeptype=='P50':
    batchp_list= ['PO2_50'] # needs to be single item so it doesn trigger a second batch
    p50_list=[3,5,7,9.35,12,15,20]

if sweeptype=='MCH':
    batchp_list= ['MCH,Hbtot_in'] # needs to be single item so it doesn trigger a second batch
    if thisGB=='Human':
        mch_list= [27.0, 28.0, 29.0, 30.0 ,31.0]
    else:
        mch_list= [13.0, 14.0 ,15.0 ,16.0 ,17.0]
elif sweeptype=='MCV':
    batchp_list= ['MCV,Hbtot_in']
    if thisGB=='Human':
        mcv_list= [70.0, 80.0, 90.0, 100.0]
        note='10pts'
        if thisGT in ['Human_AvgN15','Human_FemaleN4','Human_MaleN11']:
            mcv_list= [84.0, 85.0, 86.0, 87.0, 88.0, 89.0, 90.0, 91.0, 92.0, 93.0]
    else:
        mcv_list= [30.0, 40.0, 50.0, 60.0, 70.0]

        note='10pts'
        if thisGB=='C57BL/6Case_Ctrl_6J_Pan':
            mcv_list= [44.0, 45.0, 46.0, 47.0, 48.0, 49.0, 50.0, 51.0, 52.0, 53.0]
        if thisGB=='C57BL/6J_Pan':
            mcv_list= [40.0, 41.0, 42.0, 43.0, 44.0, 45.0, 46.0, 47.0, 48.0, 49.0]
        if thisGB=='C57BL/6Case_Ctrl_BalbC_Pan':
            mcv_list= [45.0, 46.0, 47.0, 48.0, 49.0, 50.0, 51.0, 52.0, 53.0, 54.0]
        if thisGB=='BalbC/J_Pan':
            mcv_list= [47.0, 48.0, 49.0, 50.0, 51.0, 52.0, 53.0, 54.0, 55.0, 56.0]
        if thisGB=='Bovine':
            mcv_list= [44.0, 45.0, 46.0, 47.0, 48.0, 49.0, 50.0, 51.0, 52.0, 53.0]
elif sweeptype=='D':
    batchp_list= ['Dµm']
    if thisS=='Human':
        d_list  = [6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]
    elif thisS=='Mouse':
        d_list  = [5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0]
    elif thisS=='Bovine':
        d_list  = [6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]

if thisGB=='Human':
    plottitle=f'{titlepart}-{thisGT}'
    outfile=f'{sweeptype}Sweep_{thisGT}{note}'
    outcol=f'{thisGT} K_HbO_2'
else:
    plottitle=f'{titlepart}-{thisGB}-{thisGT}'
    outfile=f'{sweeptype}Sweep_{thisGB}{note}'
    outcol=f'{thisGB} K_HbO_2'

species_choices =list(RBCO2_LUT.keys())
si= species_choices.index(thisS)

genebkg_choices =list(RBCO2_LUT[species_choices[si]].keys())
gbi= genebkg_choices.index(thisGB)

genotype_choices=list(RBCO2_LUT[species_choices[si]][genebkg_choices[gbi]].keys())

extras=[\
        #    'FULLSIGMOID', # sets axes to full sig, leave off if finding perms and want defaults for smaller run
        #    'DEBUGHBS',    # adds t1,t2, y1,y2 and lines for interpolation in hbsat
        #    'FIG5', # exact from manuscript
]
extra=','.join(extras) # need to pass in singe item so no trigger of batching or wrong num params

#
fig_params= {\
         'Species': (( 'Species'              , 'Species'      ,  a_string, '{}',    1, 'Experiment', 'ch', (thisS,     ), 'sel_newspecies' , GDEPS), {'choices':species_choices } ),
     'Genetic_Bkg': (( 'Genetic Bkg'          , 'Genetic_Bkg'  ,  a_string, '{}',    1, 'Experiment', 'ch', (thisGB,    ), 'sel_newgenbkg'  , GDEPS), {'choices':genebkg_choices } ),
        'Genotype': (( 'Genotype'             , 'Genotype'     ,  a_string, '{}',    1, 'Experiment', 'ch', (thisGT,    ), 'sel_newgenotype', GDEPS), {'choices':genotype_choices} ),

             'MCH': (( 'MCH (pg Hb/cell)'     , 'MCH'          , pos_float, '{}',    1, 'Experiment', 'tb', mch_list     , None             , ('Hbtot_in', )), {}),
             'MCV': (( 'MCV (fl/cell)'        , 'MCV'          , pos_float, '{}',    1, 'Experiment', 'tb', mcv_list     , None             , ('Hbtot_in', )), {}),
             'Dµm': (( 'D<sub>RBC</sub> (µm)' , 'D_um'         ,    Dtorus, '{}',    1, 'Experiment', 'tb', d_list       , None             , ('rµm','Dcm' )), {}),
          'PO2_50': (( '𝑃<sub>50</sub> (mmHg)', 'PO2_50'       , pos_float, '{}',    2,    ls_pprops, 'tb', p50_list     , None             , ()), {}),
           'Pm_O2': (( ls_pmo2                , 'Pm_O2'        , pos_float, '{}',    2,    ls_pprops, 'tb', ['LUT'      ], None             , ()), {}),
'kHbO2_RBC_target': (( 'kHbO2_RBC_target',  'kHbO2_RBC_target' , pos_float, '{}', None,        None ,   '', ['LUT'      ], None             , ()), {}),

       'PlotTitle': (( 'PlotTitle'            , 'PlotTitle'    ,  a_string, '{}',    2,      'Extra', 'tb', [plottitle  ], None             , ()), {}),
         'OutFile': (( 'OutFile'              , 'OutFile'      ,  a_string, '{}',    2,      'Extra', 'tb', [outfile    ], None             , ()), {}),
          'OutCol': (( 'OutCol'               , 'OutCol'       ,  a_string, '{}',    2,      'Extra', 'tb', [outcol     ], None             , ()), {}),
           'Extra': (( 'Extra'                , 'Extra'        ,  a_string, '{}',    2,      'Extra', 'tb', [extra      ], None             , ()), {}),

     'BatchParams': (( 'BatchParams'          , 'BatchParams'  ,  a_string, '{}',    2,      'Extra', 'tb', batchp_list  , None             , ()), {}),
       'SweepType': (( 'SweepType'            , 'SweepType'    ,  a_string, '{}',    2,      'Extra', 'tb', [sweeptype  ], None             , ()), {}),

}

#import pprint
#pp = pprint.PrettyPrinter(indent=3)
#USAGE pp.pprint(FigParams)

fig_param_list= build_param_list(param_list_RBCO2,fig_params)
#print('BuildParamList=')
#pp.pprint(fig_param_list)
#params= create_params( fig_param_list )
#print('CreateParamList=')
#pp.pprint([(v.human_name,v()) for k,v in params.items()])

fParams= {\
    'params':create_params( fig_param_list ),
    'valid_figs': ['Fig SigmoidSensitivitySweep'],
    'fname':__file__,
}
