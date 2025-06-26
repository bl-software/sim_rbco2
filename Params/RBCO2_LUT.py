''' regex to go from fraser/pan spreadsheet to dict
:s/\(.\{-}\),\(.\{-}\),\(.\{-}\),\(.\{-}\),\(.\{-}\),\(.\{-}\)$/'\1' :{ 'Dµm':\2, 'MCH':\3, 'MCV':\4 }, # 'rbc_kHbO2':\5, 'lys_kHbO2':\6 \6 \6},/10
'''
import pprint
import csv

RBCO2_LUT={}
print('\nParams:RBC_LUT.py: Loading RBC02_LUT from RBC_LUT_Inputs.csv')
with open('RBC_LUT_Inputs.csv') as csvfile:
    line=csvfile.readline()
    while line[0:5] != 'START':
        line=csvfile.readline()
    reader=csv.DictReader(csvfile)
    for i,row in enumerate(reader):
        #print(i,'row=',row)
        try:
            row['Species']
        except KeyError:
            #    print('--- Skipping')
            continue

        s=row['Species']
        g=row['GeneticBackground']
        t=row['GenotypeAndName']
        v=row['MCV (fl)']
        c=row['MCHC (g/dl)']
        h=row['MCH (pg)']
        k=row['Intact-rbc-kHbO2 (s-1)']
        l=row['100%-lysate-kHbO2 (s-1)']
        d=row['Major Diameter (µm)']
        p=row['PmO2']

        if s not in RBCO2_LUT:
            RBCO2_LUT[s]={}
        if g not in RBCO2_LUT[s]:
            RBCO2_LUT[s][g]={}
        RBCO2_LUT[s][g][t]={ 'Dµm':d, 'MCH':h, 'MCV':v, 'kHbO2_lysate':l, 'kHbO2_RBC_target':k, 'PmO2':p }

#pprint.pp(RBCO2_LUT)
#print('\n\n\n\n\n')


#RBCO2_LUT={
#    'Mouse':{
#        'C57BL/6Case_rxoData':{# D - µm      MCH pg         MCV fL         => MCHC in mM
#            'WT'     :{ 'Dµm':6.80 , 'MCH':14.425, 'MCV':47.9  , 'kHbO2_lysate': 11.60 , 'kHbO2_rbc_target':0.00 },
#            'AQP1-KO':{ 'Dµm':6.69 , 'MCH':14.1  , 'MCV':49.525, 'kHbO2_lysate': 11.60 , 'kHbO2_rbc_target':0.00 },
#            'RhAG-KO':{ 'Dµm':6.53 , 'MCH':14.65 , 'MCV':51.0  , 'kHbO2_lysate': 11.60 , 'kHbO2_rbc_target':0.00 },
#            'dKO'    :{ 'Dµm':6.55 , 'MCH':14.525, 'MCV':49.75 , 'kHbO2_lysate': 11.60 , 'kHbO2_rbc_target':0.00 },
#        },
#        'C57BL/6Case_vs6J_Pan':{# D - µm      MCH pg         MCV fL         => MCHC in mM
#            'WT'     :{ 'Dµm':6.956, 'MCH':14.64 , 'MCV':48.49 , 'kHbO2_lysate': 12.167, 'kHbO2_rbc_target':0.00 },
#            'WT-m'   :{ 'Dµm':7.128, 'MCH':14.62 , 'MCV':00.00 , 'kHbO2_lysate':  0.000, 'kHbO2_rbc_target':0.00 },
#            'WT-f'   :{ 'Dµm':6.785, 'MCH':00.00 , 'MCV':00.00 , 'kHbO2_lysate':  0.000, 'kHbO2_rbc_target':0.00 },
#        },
#        'C57BL/6J_Pan':{
#            'WT'     :{ 'Dµm':7.600, 'MCH':14.64 , 'MCV':44.20 , 'kHbO2_lysate': 11.305, 'kHbO2_rbc_target':0.00 },
#            'WT-m'   :{ 'Dµm':7.768, 'MCH':00.00 , 'MCV':00.00 , 'kHbO2_lysate':  0.000, 'kHbO2_rbc_target':0.00 },
#            'WT-f'   :{ 'Dµm':7.433, 'MCH':00.00 , 'MCV':00.00 , 'kHbO2_lysate':  0.000, 'kHbO2_rbc_target':0.00 },
#        },
#        'C57BL/6Case_vsBalbC_Pan':{# D - µm      MCH pg         MCV fL         => MCHC in mM
#            'WT'     :{ 'Dµm':6.956, 'MCH':14.61 , 'MCV':49.40 , 'kHbO2_lysate': 12.092, 'kHbO2_rbc_target':0.00 },
#            'WT-m'   :{ 'Dµm':7.128, 'MCH':00.00 , 'MCV':00.00 , 'kHbO2_lysate':  0.000, 'kHbO2_rbc_target':0.00 },
#            'WT-f'   :{ 'Dµm':6.785, 'MCH':00.00 , 'MCV':00.00 , 'kHbO2_lysate':  0.000, 'kHbO2_rbc_target':0.00 },
#        },
#        'BalbC/J_Pan':{
#            'WT'     :{ 'Dµm':7.414, 'MCH':14.81 , 'MCV':51.66 , 'kHbO2_lysate': 13.350, 'kHbO2_rbc_target':0.00 },
#            'WT-m'   :{ 'Dµm':7.323, 'MCH':00.00 , 'MCV':00.00 , 'kHbO2_lysate':  0.000, 'kHbO2_rbc_target':0.00 },
#            'WT-f'   :{ 'Dµm':7.480, 'MCH':00.00 , 'MCV':00.00 , 'kHbO2_lysate':  0.000, 'kHbO2_rbc_target':0.00 },
#        },
#    },
#    'Human':{
#        'Human': {
#            'Human_AVG15' :{ 'Dµm':9.0377, 'MCH':29.32, 'MCV':88.12 , 'kHbO2_lysate': 0.00, 'kHbO2_rbc_target':0.00 },
#            'Males_AVG11' :{ 'Dµm':8.9567, 'MCH':29.28, 'MCV':87.68 , 'kHbO2_lysate': 0.00, 'kHbO2_rbc_target':0.00 },
#            'Females_AVG4':{ 'Dµm':9.2606, 'MCH':29.43, 'MCV':89.33 , 'kHbO2_lysate': 0.00, 'kHbO2_rbc_target':0.00 },
#            'DF017'       :{ 'Dµm':8.2573, 'MCH':28.9 , 'MCV':88.4  , 'kHbO2_lysate': 0.00, 'kHbO2_rbc_target':0.00 },
#            'DF016'       :{ 'Dµm':8.818 , 'MCH':30.4 , 'MCV':89.4  , 'kHbO2_lysate': 0.00, 'kHbO2_rbc_target':0.00 },
#            'DF020'       :{ 'Dµm':8.608 , 'MCH':29.5 , 'MCV':89.5  , 'kHbO2_lysate': 0.00, 'kHbO2_rbc_target':0.00 },
#            'DF023'       :{ 'Dµm':9.5434, 'MCH':29.8 , 'MCV':88.8  , 'kHbO2_lysate': 0.00, 'kHbO2_rbc_target':0.00 },
#            'DF019'       :{ 'Dµm':9.169 , 'MCH':29.1 , 'MCV':90    , 'kHbO2_lysate': 0.00, 'kHbO2_rbc_target':0.00 },
#            'DF031'       :{ 'Dµm':8.803 , 'MCH':27.7 , 'MCV':84.7  , 'kHbO2_lysate': 0.00, 'kHbO2_rbc_target':0.00 },
#            'DF028'       :{ 'Dµm':9.1228, 'MCH':30.7 , 'MCV':87.9  , 'kHbO2_lysate': 0.00, 'kHbO2_rbc_target':0.00 },
#            'DF035'       :{ 'Dµm':9.3435, 'MCH':28.1 , 'MCV':84.1  , 'kHbO2_lysate': 0.00, 'kHbO2_rbc_target':0.00 },
#            'DF040'       :{ 'Dµm':9.2124, 'MCH':28.3 , 'MCV':86.6  , 'kHbO2_lysate': 0.00, 'kHbO2_rbc_target':0.00 },
#            'DF033'       :{ 'Dµm':9.0662, 'MCH':29.8 , 'MCV':89    , 'kHbO2_lysate': 0.00, 'kHbO2_rbc_target':0.00 },
#            'DF038'       :{ 'Dµm':9.1314, 'MCH':28.5 , 'MCV':87    , 'kHbO2_lysate': 0.00, 'kHbO2_rbc_target':0.00 },
#            'DF026'       :{ 'Dµm':9.1178, 'MCH':30.5 , 'MCV':91.9  , 'kHbO2_lysate': 0.00, 'kHbO2_rbc_target':0.00 },
#            'DF032'       :{ 'Dµm':9.1402, 'MCH':28.9 , 'MCV':84.4  , 'kHbO2_lysate': 0.00, 'kHbO2_rbc_target':0.00 },
#            'DF039'       :{ 'Dµm':9.6248, 'MCH':29.5 , 'MCV':88.8  , 'kHbO2_lysate': 0.00, 'kHbO2_rbc_target':0.00 },
#            'DF036'       :{ 'Dµm':8.6083, 'MCH':30.1 , 'MCV':91.3  , 'kHbO2_lysate': 0.00, 'kHbO2_rbc_target':0.00 },
#        },
#    },
#    'Bovine':{
#        'Bovine': {
#            'RXO Test Bovine' :{ 'Dµm'   :8.653500191890201, 'MCH':15.3140656935  , 'MCV':47.55 , 'kHbO2_lysate': 0.00, 'kHbO2_rbc_target':0.00 },
#            #'Bovine' :{ 'Dµm':1.01e-4, 'MCH':14.425, 'MCV':47.9  }, #'Hbtot_in':111118.73 },
#        },
#    },
#    'RXOTest':{
#        'RXOTest': {
#            'Rtor_1.01' :{ 'Dµm':6.777655814594635, 'MCH': 14.425548193, 'MCV':47.9 , 'kHbO2_lysate': 0.00, 'kHbO2_rbc_target':0.00  },
#            'Rtor_0.81' :{ 'Dµm':9.017172224459667, 'MCH':14.425548193, 'MCV':47.9  , 'kHbO2_lysate': 0.00, 'kHbO2_rbc_target':0.00  },
#        },
#    },
#
#}

#pprint.pp(RBCO2_LUT)
