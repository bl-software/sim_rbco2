# sim_rbco2
Red Blood Cell simulations supporting RBCO2 Paper.
This is also all encompassing and will do JTB2012 and AJP2014 simulations, see below.

# Status as of June 2025:
The goal was for this code to be production ready.  However, due to funding cuts (2025) this is mostly a code dump in its current state.  Not a finished product.  There will be bugs.  We were in process of separating into 3 code bases, to simplify usage for users.  That code is in the JTB2012 (working) and AJP2014 (somewhat working) and in the development tree (which is now this repo),
w̶h̶i̶c̶h̶ ̶I̶ ̶p̶l̶a̶n̶ ̶o̶n̶ ̶p̶u̶t̶t̶i̶n̶g̶ ̶i̶n̶t̶o̶ ̶g̶i̶t̶h̶u̶b̶ ̶a̶l̶o̶n̶g̶s̶i̶d̶e̶ ̶t̶h̶e̶s̶e̶ ̶i̶n̶ ̶a̶ ̶d̶e̶v̶e̶l̶o̶p̶m̶e̶n̶t̶ ̶r̶e̶p̶o̶s̶i̶t̶o̶r̶y̶.̶
The code you are looking at right now is the combined code for all 3 types of simulations in a state prior to the split.  It runs all 3 simulations, however all of the figures in AJP and RBC have not been created.  See the dropdowns in the app for which figures are implemented.  If someone in the future picks up this project, I recommend starting with the sim_rbco2 branch, there is code in the sim_jtb and sim_ajp that needs to be pulled into sim_rbco2 after it works. https://github.com/bl-software is the link to all 3.

If you want to run JTB or AJP simulations, I recommend that you run the version from those github repos. These have the most development completed.  That code needs to be merged back into the development version.

# Setup in Ubuntu Linux (24.04):
The command "PYOPENGL_PLATFORM=egl python mgui.py --simtype=2" will make the software run, ready for an RBCO2 simulation, assuming the python (venv) and Linux (apt) environments are properly setup, See INSTALL file.  A python virtual env should be setup, then use the reqs.txt file to install the reqs.  The code requires MATLAB as of this version.  There is code to make it work with Octave, though it is untested, as Octave had an issue when this part was added, the ode15s equivalent solver was not working.  You must pip install the Matlab engine, see Mathworks for instructions.

The code will run the simulations, but there is no guarantee the figures will match what will be in the RBCO2 Paper.  I know some of the figure numbers have been changed in the final version of the paper and these now differ from the code.

One significant bug is the OpenGL context switch.  You can switch between JTB and AJP, and then to RBC, but once the RBC has been selected, you cannot go back to JTB or AJP.  So simply restart the program.


```PYOPENGL_PLATFORM=egl python mgui.py --help```
To see all the options.  
The development version has a bit freindlier command line interface.

# Running in Ubuntu Linux (24.04):
A quick runthrough.
Start the code

```PYOPENGL_PLATFORM=egl python mgui.py --simtype=2```

Click "Run Simulation" big red button.
Create a folder to hold the simulation data.
Wait, files will be created, Matlab will launch, the sims will run.
When the sims are complete, you'll see (Run 10/10) on the terminal, hit the "Fig 10a" button and it will create figure 10a in the paper.

There are many combinations and batch options.

Last I checked the code will run in python under Anaconda.  Use conda to install the required packages.

# More Examples
If you are running a lot of simulations the simplest way is through the command line.  I like to use a line like this:
(These are 3 examples of running the exact same simulation and parameters. Simplest first, most efficient last)
```PYOPENGL_PLATFORM=egl python mgui.py --simtype=RBCO2 --paper=0 --figure=2          --sdp=test_rf10a/  --dofig="Fig 10a"  --dosim```  
```PYOPENGL_PLATFORM=egl python mgui.py --simtype=RBCO2 --paper=0 --figure="Fig_10a"  --sdp=test_rf10a/  --dofig="Fig 10a"  --dosim```  
```export FIG='10a';
PYOPENGL_PLATFORM=egl python mgui.py --simtype=RBCO2 --paper=0 --figure="Fig_$FIG" --sdp=test_rf$FIG/ --dofig="Fig $FIG" --dosim```  
Breakdown:  
```export FIG='10a'  -- Sets the figure you are interested into a shell variable for use later in the command```  
```PYOPENGL_PLATFORM=egl -- is sometimes necessary for OpenGL code to run properly (required in Ubuntu 24.04 with X11 and Wayland)```  
```python mgui.py -- starts the program in default mode  JTB2012, paper 1, first figure you can manually change everything```  

```--simtype=RBCO2 --paper=0 --figure="Fig_10a"```  
equivalent using the exported var   
```--simtype=RBCO2 --paper=0 --figure="Fig_$FIG" --sets the simulation type, paper and the figure<br/>```  
```---sdp=test_rf$FIG/ -- sets the data folder (sdp=set data path) for the outputs of the simulation```  
```--dofig="Fig $FIG" -- tells the system to actually generate the figure after either finding the data in the data directory or after finishing a sim```  
```--dosim -- as long as you set an sdp then automatically start running the sim, this will delete previous code (with dialog boxes to confirm EVERY file```  

To automatically run the sims for figures 10a-d  
this creates the data folder, runs the sim, and generates the figure  
```PYOPENGL_PLATFORM=egl python mgui.py --simtype=2 --paper=0 --fig=2 --sdp=testf10a/ --dofig='Fig 10a' --dosim```  
```PYOPENGL_PLATFORM=egl python mgui.py --simtype=2 --paper=0 --fig=3 --sdp=testf10b/ --dofig='Fig 10b' --dosim```  
```PYOPENGL_PLATFORM=egl python mgui.py --simtype=2 --paper=0 --fig=4 --sdp=testf10c/ --dofig='Fig 10c' --dosim```  
```PYOPENGL_PLATFORM=egl python mgui.py --simtype=2 --paper=0 --fig=5 --sdp=testf10d/ --dofig='Fig 10d' --dosim```  

This will regenerate the figure on an existing data folder from a previously run simulation  
```PYOPENGL_PLATFORM=egl python mgui.py --simtype=2 --paper=0 --fig=2 --sdp=testf10a/ --dofig='Fig 10a'```  

This will remove the data in the data folder and rerun the sim and gen the figure (good for testing)  

```rm testf3d/*; PYOPENGL_PLATFORM=egl python mgui.py --simtype=2 --paper=0 --fig=5 --sdp=testf10d/ --dofig='Fig 10d' --dosim```  

```rm testf3c/*; PYOPENGL_PLATFORM=egl python mgui.py --simtype=2 --paper=0 --fig=4 --sdp=testf10c/ --dofig='Fig 10c' --dosim```  

This will simply open the app set to do RBC sims related to paper 1  
```PYOPENGL_PLATFORM=egl python mgui.py --simtype=2 --paper=0```  

# Create Sigmoid similar to Fig 6 for any strains  
Requires 2 runs for first half of the point and second half of the points. To much data for the computer to run all at once.  
Edit the file Params/Sim_3__RBCO2/Paper_1__RBCO2/Params_060__Fig_6.py.py  
-- in extras comment out FIG6  (around line 56)  
-- set run=1   (around line 88)  
save  
```PYOPENGL_PLATFORM=egl python mgui.py --simtype=2 --paper=0 --fig=1 --sdp=testSS1/ --dofig='Fig 6' --dosim```  

edit again  
-- set run=2  (around line 88)  
save  
```PYOPENGL_PLATFORM=egl python mgui.py --simtype=2 --paper=0 --fig=1 --sdp=testSS2/ --dofig='Fig 6' --dosim```  
the result will be 2 files similar to:  
    MouseC57BL_6Case_AvgWT_r1_2.csv  
    MouseC57BL_6Case_AvgWT_r2_2.csv  
the important part being the _r1_2 - means run 1 of 2.  
then you can use the file df_combine.py to put them together - you'll have to edit df_combine for each experiment to make it work based on your ouput  
```python df_combine.py```  

Editing the file; If you leave FIG6 in extras, the system will create Figure 6 exactly as in the paper.  

# Some general notes  
The files in Params contain the default parameters to run the figures in the paper.  
Copy and edit them to do your own custom simulations. For some you need to change the dropdown selections or edit the params file data for each run.  Examples are in Figure 6 sigmoid files.  
The Figures files contain code to create the figures.  

Try to follow the file hierarchy  
n= number in the app  
name = often the figure number in the paper - but also your custom name if it is not a paper specific figure.  
```Params_<n>__<name>.py  
└── Sim_3__RBCO2
    ├── __init__.py
    ├── Paper_1__RBCO2
    │   ├── __init__.py
    │   ├── Params_050__Fig_5_Bar.py
    │   ├── Params_060__Fig_6.py
    │   ├── Params_100__Fig_10a.py
    │   ├── Params_101__Fig_10b.py
    │   ├── Params_102__Fig_10c.py
    │   └── Params_103__Fig_10d.py
    ├── Paper_2__Nonspecific
    │   ├── __init__.py
    │   ├── Params_1__BaseSim.py
    │   ├── Params_2__SigmoidSensitivitySweep.py
    │   └── Params_3__SigPLocator.py
    └── Param_Defaults_RBCO2.py```

```Figures_<n>__<name>.py
├── Sim_3__RBCO2
│   ├── __init__.py
│   ├── Paper_1__RBCO2
│   │   ├── Figure_050__5bar.py
│   │   ├── Figure_060__6.py
│   │   ├── Figure_061__6PERMSSweep.py
│   │   ├── Figure_100__10a.py
│   │   ├── Figure_101__10b.py
│   │   ├── Figure_102__10c.py
│   │   ├── Figure_103__10d.py
│   │   ├── Figure10.py
│   │   ├── Figure6.py
│   │   ├── __init__.py
│   │   ├── RBCO2_Figs.py
│   │   └── XFigure_6__5PERMS.py
│   └── Paper_2__Nonspecific
│       ├── Figure_1__SigmoidSensitivitySweep.py
│       ├── Figure_2__SigPLocator.py
│       └── __init__.py
└── SimFigure.py```
