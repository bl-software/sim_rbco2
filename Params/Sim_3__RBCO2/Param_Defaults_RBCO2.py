# This is a UTF-8 file
# Insert unicode chars in VIM with: insert mode, hit Ctrl-V and type hex unicode "U0001D458"
'''
 NOTE: Unicode: U+2082 ₂ - these print at baseline not decended
 U+2103  ℃ degree C - broken ???
 U+1D443 𝑃 f0 9d 91 83  MATHEMATICAL ITALIC CAPITAL P
 U+1D458 𝑘 (capital U for 5 digit) MATHEMATICAL ITALIC SMALL K 
 U+B5    µ 
'''

'''
 key = Matlab Var Name
   Human Readable Name
   Matlab Var Name
   Validator function
   Format String
   Display Column - dynamic column creation based on what is found here
   Display Group  - dynamic group  creation based on what is found here
   Display Type   - used to create widget and set some attributes
   Value - if applicablen - default in this file - can be a callable function to return the value.
   Callback when value is set - example to show equation on the screen
   List of Dependents - other vals that need to change when this changes

'''

from Params.Param_Validators import *
from Params.RBCO2_LUT import RBCO2_LUT

ls_Hbtot_in='[mono Hb<sub>Total</sub>]<sub>i</sub> (mM)'
ls_r_sphere='r<sub>Sphere</sub> =r<sub>Torus</sub> (µm)'
ls_ph20='𝑃<sub>H<sub>2</sub>O</sub> (mmHg)'
ls_po2='𝑃<sub>O<sub>2</sub></sub> (mmHg)'   
ls_so2='s<sub>O<sub>2</sub></sub> (mM/mmHg)'
ls_o2='[O<sub>2</sub>]<sub>i</sub> (mM)'    
ls_pmo2='𝑃<sub>M,O<sub>2</sub></sub> (cm/s)'
ls_r_torus_u='r<sub>Torus</sub> (µm)'
ls_r_torus_c='r<sub>Torus</sub> (cm)'
ls_pprops='Physiological Properties'

species_choices =list(RBCO2_LUT.keys())
thisS=  species_choices[0] 

genebkg_choices =list(RBCO2_LUT[thisS].keys())
thisGB= genebkg_choices[0] 

mutation_choices=list(RBCO2_LUT[thisS][thisGB].keys())
thisGT= mutation_choices[0]

GDEPS=('MCH','MCV','Dµm','kHbO2_lysate')
#                      Human Readable              Matlab           Valid     Format Col  Group           Type   Value            OnValChCallback    Dependents
def_param_list_RBCO2= {\
         'Species': (( 'Species'               , 'Species'     ,  a_string,   '{}', 1,   'Experiment',  'ch', (thisS,          ), 'sel_newspecies' , GDEPS)        , {'choices':species_choices } ),
     'Genetic_Bkg': (( 'Genetic Bkg'           , 'Genetic_Bkg' ,  a_string,   '{}', 1,   'Experiment',  'ch', (thisGB,         ), 'sel_newgenbkg'  , GDEPS)        , {'choices':genebkg_choices } ),
        'Genotype': (( 'Genotype'              , 'Genotype'    ,  a_string,   '{}', 1,   'Experiment',  'ch', (thisGT,         ), 'sel_newgenotype', GDEPS)        , {'choices':mutation_choices} ),
             'MCH': (( 'MCH (pg Hb/cell)'      , 'MCH'         , pos_float,   '{}', 1,   'Experiment', 'otb', ['LUT'           ], None             , ('Hbtot_in',)), {} ),
             'MCV': (( 'MCV (fl/cell)'         , 'MCV'         , pos_float,   '{}', 1,   'Experiment', 'otb', ['LUT'           ], None             , ('Hbtot_in',)), {} ),
             'Dµm': (( 'D<sub>RBC</sub> (µm)'  , 'D_um'        ,    Dtorus,   '{}', 1,   'Experiment',  'tb', ['LUT'           ], None             , ('rµm','Dcm'            )), {} ),
             'Dcm': (( 'D<sub>RBC</sub> (cm)'  , 'D'           , pos_float,   '{}', 1,   'Experiment', 'otb', ('f__D_cm',      ), None             , (                       )), {} ),
             'rµm': (( ls_r_torus_u            , 'R_um'        , pos_float,   '{}', 1,   'Experiment', 'otb', ('f__rtorus',    ), None             , ('R_infµm','n_in','r_sphere','rcm',)), {} ),
             'rcm': (( ls_r_torus_c            , 'R'           , pos_float,   '{}', 1,   'Experiment', 'otb', ('f__rtorus_cm', ), None             , (                       )), {} ),
               'R': (( 'R<sub>Torus</sub> (µm)', 'nomat_R_TOR' , pos_float,   '{}', 1,   'Experiment', 'otb', ('f__RfromD',    ), None             , (                       )), {} ),
        'Hbtot_in': (( ls_Hbtot_in             , 'Hbtot_in'    , pos_float,   '{}', 1,   'Experiment', 'otb', ('f__HbTotIn',   ), None             , (                       )), {} ),
            'tmax': (( 'Max Time (s)'          , 'tmax'        , pos_float,   '{}', 1,   'Experiment',  'tb', [1.5             ], None             , (                       )), {} ),

        'r_sphere': (( ls_r_sphere             , 'r_sphere'    , pos_float,   '{}', 1,     'Geometry', 'otb', ('f__rsphere',   ), None             , (                       )), {} ),
         'd_eufµm': (( 'd<sub>EUF</sub> (µm)'  , 'd_euf_um'    , pos_float,   '{}', 1,     'Geometry',  'tb', [1.00,           ], None             , ('R_infµm','d_eufcm',   )), {} ),
         'd_eufcm': (( 'd<sub>EUF</sub> (cm)'  , 'd_euf_cm'    , pos_float,   '{}', 1,     'Geometry', 'otb', ('f__deuf_cm',   ), None             , (                       )), {} ),
         'R_infµm': (( 'Edge Comp Domain (µm)' , 'R_inf_um'    , pos_float,   '{}', 1,     'Geometry', 'otb', ('f__r_inf',     ), None             , ('R_infcm','n_out',     )), {} ),
         'R_infcm': (( 'Edge Comp Domain (cm)' , 'R_inf'       , pos_float,   '{}', 1,     'Geometry', 'otb', ('f__r_inf_cm',  ), None             , (                       )), {} ),
            'n_in': (( '# Shells In'           , 'n_in'        ,   pos_int, '{:d}', 1,     'Geometry', 'otb', ('f__n_in',      ), None             , (                       )), {} ),
           'n_out': (( '# Shells Out'          , 'n_out'       ,   pos_int, '{:d}', 1,     'Geometry', 'otb', ('f__n_out',     ), None             , (                       )), {} ),

               'T': (( 'T (℃ )'                , 'T'           , pos_float,   '{}', 2,  'Environment', 'otb', [10.0            ], None             , (                       )), {} ),
              'PB': (( '𝑃<sub>B</sub> (mmHg)'  , 'PB'          , pos_float,   '{}', 2,  'Environment',  'tb', [760.0           ], None             , ('PO2',                 )), {} ),
            'PH2O': (( ls_ph20                 , 'PH2O'        , pos_float,   '{}', 2,  'Environment', 'otb', [9.2             ], None             , ('PO2',                 )), {} ),
           'O2_pc': (( '%O<sub>2</sub>'        , 'O2_pc'       ,   percent,   '{}', 2,  'Environment',  'tb', [21              ], None             , ('PO2',                 )), {} ),
             'PO2': (( ls_po2                  , 'PO2'         , pos_float,   '{}', 2,  'Environment', 'otb', ('f__pO2',       ), None             , (                       )), {} ),
             'sO2': (( ls_so2                  , 'sO2'         , pos_float,   '{}', 2,  'Environment',  'tb', [2.24e-3         ], None             , (                       )), {} ),
              'O2': (( ls_o2                   , 'O2'          , pos_float,   '{}', 2,  'Environment', 'otb', [152.25*0.00224  ], None             , (                       )), {} ),

          'PO2_50': (( '𝑃<sub>50</sub> (mmHg)' , 'PO2_50'      , pos_float,   '{}', 2,      ls_pprops,  'tb', [9.35            ], None             , (                       )), {} ),
           'Pm_O2': (( ls_pmo2                 , 'Pm_O2'       , pos_float,   '{}', 2,      ls_pprops,  'tb', ['LUT'           ], None             , (                       )), {} ),
     'kHbO2_lysate': (( 'kHbO2_lysate'         , 'k_lysate'    , pos_float,   '{}', 2,      ls_pprops,  'tb', ['LUT'           ], None             , (                       )), {} ),
          'D_O2out': (( 'D_O<sub>2</sub>out'   , 'D_O2out'     , pos_float,   '{}', 2,      ls_pprops,  'tb', [1.3313e-5       ], None             , (                       )), {} ),
        'D_HbO2out': (( 'D_HbO<sub>2</sub>out' , 'D_HbO2out'   , pos_float,   '{}', 2,      ls_pprops,  'tb', [0.0             ], None             , (                       )), {} ),
          'D_Hbout': (( 'D_Hbout'              , 'D_Hbout'     , pos_float,   '{}', 2,      ls_pprops,  'tb', [0.0             ], None             , (                       )), {} ),
           'D_O2in': (( 'D_O<sub>2</sub>in'    , 'D_O2in'      , pos_float,   '{}', 2,      ls_pprops,  'tb', [2.7745e-6       ], None             , (                       )), {} ),
         'D_HbO2in': (( 'D_HbO<sub>2</sub>in'  , 'D_HbO2in'    , pos_float,   '{}', 2,      ls_pprops,  'tb', [6.07e-8         ], None             , (                       )), {} ),
           'D_Hbin': (( 'D_Hbin'               , 'D_Hbin'      , pos_float,   '{}', 2,      ls_pprops,  'tb', [6.07e-8         ], None             , (                       )), {} ),
 'kHbO2_RBC_target': (( 'kHbO2_RBC_target',  'kHbO2_RBC_target', pos_float,   '{}', None,        None,    '', ['LUT'           ], None             , (                       )), {} ),
        'PlotTitle': (( 'PlotTitle'            , 'PlotTitle'   ,  a_string,   '{}', 2,        'Extra',  'tb', [''              ], None             , (                       )), {} ),
          'OutFile': (( 'OutFile'              , 'OutFile'     ,  a_string,   '{}', 2,        'Extra',  'tb', ['DEFFILE'       ], None             , (                       )), {} ),
           'OutCol': (( 'OutCol'               , 'OutCol'      ,  a_string,   '{}', 2,        'Extra',  'tb', ['DEVCOL'        ], None             , (                       )), {} ),
     'BatchParams': (( 'BatchParams'           , 'BatchParams' ,  a_string,   '{}', None,        None,    '', [''              ], None             , (                       )), {} ),
       'SweepType': (( 'SweepType'             , 'SweepType'   ,  a_string,   '{}', None,        None,    '', [''              ], None             , (                       )), {} ),
}

param_list_RBCO2 = def_param_list_RBCO2
