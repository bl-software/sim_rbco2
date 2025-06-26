import subprocess
import glob
import os
import sys

current_env = os.environ.copy()
#print(current_env)
current_env.update({"PYOPENGL_PLATFORM":"egl"})

#ds= glob.glob('ajpswp_5_150_*')#gams_lam1*')
#ds= glob.glob('ajpswp_40_10000_*')#gams_lam1*')
#ds= glob.glob('lamgamsweepsims/ajpswp_1000_150_*')#gams_lam1*')
ds= glob.glob('lamgamsweepsims/ajpswp_*')#gams_lam1*')
print(f'ds={ds}')
#sys.exit()

lruns= len(ds)
for i,directory in enumerate(ds):
    l= [
         "python",
         "mgui.py",
         "--simtype=1",
         "--paper=AJP_2014",
         "--figure=Fig_GenSweeps",
         "--dofig=Fig GenSweeps",
         f"--sdp={directory}/",
         "--exitaf",
         "."
    ]
    print('\n'*4,f'Run {i} of {lruns}')
    print(l)

    subprocess.run(l, env=current_env)


