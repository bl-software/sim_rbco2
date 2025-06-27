# sim_rbco2
Red Blood Cell simulations supporting RBCO2 Paper.
This is also all encompassing and will do JTB2012 and AJP2014 simulations, see below.

# Status as of June 2025:
The goal was for this code to be production ready.  However, due to funding cuts (2025) this is mostly a code dump in its current state.  Not a finished product.  There will be bugs.  We were in process of separating into 3 code bases, to simplify usage for users.  That code is in the JTB2012 (working) and AJP2014 (somewhat working) and in the development tree, which I plan on putting into github alongside these in a development repository.  The code you are looking at right now is the combined code for all 3 types of simulations in a state prior to the split.  It runs all 3 simulations, however all of the figures in AJP and RBC have not been created.  See the dropdowns in the app for which figures are implemented.  If someone in the future picks up this project, I recommend starting with the development branch, INSERT GITHUB LINK HERE, as it has been cleaned up a lot, but there are still significant bugs and refactoring to work out.

If you want to run JTB or AJP simulations, I recommend that you run the version from those github repos. These have the most development completed.  That code needs to be merged back into the development version.

# Setup in Ubuntu Linux (24.04):
The command "PYOPENGL_PLATFORM=egl python mgui.py --simtype=2" will make the software run, ready for an RBCO2 simulation, assuming the python (venv) and Linux (apt) environments are properly setup.  A python virtual env should be setup, then use the reqs.txt file to install the reqs.  The code requires MATLAB as of this version.  There is code to make it work with Octave, though it is untested, as Octave had an issue when this part was added, the ode15s equivalent solver was not working.  You must pip install the Matlab engine, see Mathworks for instructions.

The code will run the simulations, but there is no guarantee the figures will match what will be in the RBCO2 Paper.  I know some of the figure numbers have been changed in the final version of the paper and these now differ from the code.

One significant bug is the OpenGL context switch.  You can switch between JTB and AJP, and then to RBC, but once the RBC has been selected, you cannot go back to JTB or AJP.  So simply restart the program.


> PYOPENGL_PLATFORM=egl python mgui.py --help gives all the option
The development version has a bit freindlier command line interface.

# Running in Ubuntu Linux (24.04):
A quick runthrough.
Start the code

> PYOPENGL_PLATFORM=egl python mgui.py --simtype=2

Click "Run Simulation" big red button.
Create a folder to hold the simulation data.
Wait, files will be created, Matlab will launch, the sims will run.
When the sims are complete, you'll see (Run 10/10) on the terminal, hit the "Fig 3a" button and it will create what was at one point figure 3a in the paper.

There are many combinations and batch options.

Last I checked the code will run in python under Anaconda.  Use conda to install the required packages.

# More Examples
To automatically run the sims for 3a 3b 3c 3d -> Renamed in paper to 9a 9b 9c 9d
this creates the data folder, runs the sim, and generates the figure
> PYOPENGL_PLATFORM=egl python mgui.py --simtype=2 --paper=0 --fig=0 --sdp=testf3a/ --dofig='Fig 3a' --dosim

> PYOPENGL_PLATFORM=egl python mgui.py --simtype=2 --paper=0 --fig=1 --sdp=testf3b/ --dofig='Fig 3b' --dosim

> PYOPENGL_PLATFORM=egl python mgui.py --simtype=2 --paper=0 --fig=2 --sdp=testf3c/ --dofig='Fig 3c' --dosim

> PYOPENGL_PLATFORM=egl python mgui.py --simtype=2 --paper=0 --fig=3 --sdp=testf3d/ --dofig='Fig 3d' --dosim

This will regenerate the figure on an existing data folder
> PYOPENGL_PLATFORM=egl python mgui.py --simtype=2 --paper=0 --fig=0 --sdp=testf3a/ --dofig='Fig 3a'

This will remove the data in the data folder and rerun the sim and gen the figure (good for testing)
> rm testf3d/*; PYOPENGL_PLATFORM=egl python mgui.py --simtype=2 --paper=0 --fig=3 --sdp=testf3d/ --dofig='Fig 3d' --dosim
> rm testf3c/*; PYOPENGL_PLATFORM=egl python mgui.py --simtype=2 --paper=0 --fig=2 --sdp=testf3c/ --dofig='Fig 3c' --dosim

This will simply open the app set to do RBC sims related to paper 1
> PYOPENGL_PLATFORM=egl python mgui.py --simtype=2 --paper=0

Create Sigmoid similar to Fig 5 for any strains
requires 2 runs for first half of the point and second half of the points. To much data for the computer to run all at once.
Edit the file Params/Sim_3__RBCO2/Paper_1__RBCO2/Params_8__Fig_5.py
-- in extras comment out FIG5
-- set run=1
save
> PYOPENGL_PLATFORM=egl python mgui.py --simtype=2 --paper=0 --fig=4 --sdp=testSS1/ --dofig='Fig 5' --dosim
edit again
-- set run=2
save
> PYOPENGL_PLATFORM=egl python mgui.py --simtype=2 --paper=0 --fig=4 --sdp=testSS2/ --dofig='Fig 5' --dosim
the result will be 2 files similar to:
    MouseC57BL_6Case_AvgWT_r1_2.csv
    MouseC57BL_6Case_AvgWT_r2_2.csv
then you can use the file df_combine.py to put them together - you'll have to edit df_combine for each experiment to make it work
> python df_combine.py

If you leave FIG5 in extras, the system will create Figure 5 exactly

# Some general notes
The files in Params contain the defaults
Copy and edit them to do your own custom simulations.
Try to follow the file hierarchy
Params_<n>__<name>.py
n= number in the app
name = often the figure number in the paper - but also your custom name if it is not in the paper
> tree output
└── Sim_3__RBCO2
    ├── __init__.py
    ├── Paper_1__RBCO2
    │   ├── __init__.py
    │   ├── Params_1__Fig_3a.py
    │   ├── Params_2__Fig_3b.py
    │   ├── Params_3__Fig_3c.py
    │   ├── Params_4__Fig_3d.py
    │   ├── Params_8__Fig_5.py
    │   ├── Params_9__Fig_6_Bar.py
    ├── Paper_2__Nonspecific
    │   ├── __init__.py
    │   ├── Params_1__BaseSim.py
    │   ├── Params_2__SigmoidSensitivitySweep.py
    │   ├── Params_3__SigPLocator.py
    ├── Param_Defaults_RBCO2.py


