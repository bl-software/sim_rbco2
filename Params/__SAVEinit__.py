import glob,os
import importlib
print(f'\n{__name__}:__path__=',__path__)
print(f'{__name__}:__name__=',__name__) # "Params"
print(f'{__name__}:__file__=',__file__) # "Params"

def importer(indent,modprefix,name):
    #indent=f'imp{indent}'
    _namepath= name.replace('.','/')
    _moddirs=glob.glob(f'{_namepath}/{modprefix}*')
    #print('np=',_namepath)
    #print('mp=',modprefix)
    print(f'{indent}{_namepath}: {modprefix}:_moddirs=',_moddirs)

    _modnames=[ os.path.basename(os.path.normpath(f)).removesuffix('.py') for f in _moddirs ]
    print(f'{indent}{_namepath}: {modprefix}:_modnames=',_modnames)

    for modname in _modnames:
        print(f'{indent}{_namepath}: doing modname:',modname)
        shortmodname= modname.strip(modprefix)
        print(f'{indent}shortmodname=',shortmodname)
        module = importlib.import_module('.'+modname, package=name)
        try:
            if modprefix == 'Figure__':
                Modules[shortmodname]=module.Fig
            else:
                Modules[shortmodname]=module.Modules
        except AttributeError:
            print(f'{indent}Need to Define "Modules" in  {module}')

    print(f'{indent}{_namepath}: Modules=',Modules)


#Want name "Params" in mgui.py
Params=Modules={}

_modprefix='Sim__'
_namepath= __name__.replace('.','/')
_moddirs=glob.glob(f'{_namepath}/{_modprefix}*')
print(f'Params: {_modprefix}:_moddirs=',_moddirs)

_modnames=[ os.path.basename(os.path.normpath(f)) for f in _moddirs ]
print(f'Params: {_modprefix}:_modnames=',_modnames)

for modname in _modnames:
    print(f'{__name__}: doing modname:',modname)
    shortmodname= modname.strip(_modprefix)
    module = importlib.import_module('.'+modname, package=__name__)
    try:
        Modules[shortmodname]=module.Modules
    except AttributeError:
        print(f'Need to Define "Modules" in  {module}')

print('Params: Modules=',Modules)



#OLD #OLD
#OLD #print( 'globs=',glob.glob('Params__*'))
#OLD #print( 'globs=',glob.glob('Params/Params__*'))
#OLD #print( 'globs=',[ os.path.basename(fn) for fn in glob.glob('Params/Params__*.py')])
#OLD pfigs=  [ os.path.basename(fn).split('.py')[0] for fn in glob.glob('Params/Params__JTB_2012*.py')]
#OLD pfigs+= [ os.path.basename(fn).split('.py')[0] for fn in glob.glob('Params/Params__AJP_2014*.py')]
#OLD pfigs+= [ os.path.basename(fn).split('.py')[0] for fn in glob.glob('Params/Params__RBCO2*.py')]
#OLD pdefs= [ os.path.basename(fn).split('.py')[0] for fn in glob.glob('Params/Param_Defaults_*.py')]
#OLD sep='\n    '
#OLD print(f'\nFound Param Modules:{sep}{sep.join(pfigs)}')
#OLD __all__= [
#OLD  'Param_Funcs',
#OLD  'Param_Validators',
#OLD # 'Param_Defaults_JTB2012',
#OLD # 'Param_Defaults_AJP2014',
#OLD # 'Param_Defaults_RBCO2',
#OLD  'RBCO2_LUT'] \
#OLD  + pdefs \
#OLD  + pfigs
#OLD 
#OLD 
#OLD #__all__= [
#OLD # 'Param_Funcs',
#OLD # 'Param_Validators',
#OLD # 'Param_Defaults_JTB2012',
#OLD # 'Param_Defaults_AJP2014',
#OLD # 'Params__JTB_2012__fig_3_4_5',
#OLD # 'Params__JTB_2012__fig_6',
#OLD # 'Params__JTB_2012__fig_7_8',
#OLD # 'Params__JTB_2012__fig_9',
#OLD # 'Params__JTB_2012__fig_10',
#OLD # 'Params__JTB_2012__fig_11_12',
#OLD # 'Params__AJP_2014__fig_4',
#OLD # 'Params__AJP_2014__fig_5',
#OLD # 'Params__AJP_2014__fig_6',
#OLD # 'Params__AJP_2014__fig_8',
#OLD ## 'Params__AJP_2014__custom',
#OLD #]
