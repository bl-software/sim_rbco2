The computationa model of the spherical RBC includes the following 10 .m files:

(1) SingleSpeciesDiffMatDistr.m        
(2) DiffusionMatrixInsideDistr.m       
(3) DiffusionMatrixOutsideDistr.m
(4) DiffusionMatrixDistr_RBC.m
(5) ReactionDiffusionDistrRHS_RBC.m

(6) ModelParameters_RBC_ok_PmO2_Params_ok_JP.m
(7) ModelParameters_RBC_ok_PmO2_Params_ok_klysate_JP.m (this file is needed only for the sims in Fig 5B)

(8) Simulate_O2_Efflux.m
(9) Calculate_t37_JP.m

(10) Fig_4_7_JP.m  (plots the six panels of Fig 4 (WT only) and of Fig 7 (WT and dKO + pCMBS)

The folder "Sims_ArithMean" includes all the simulations (Matlab data files .mat) presented in the ms and that are needed to run, for example, Fig_4_7_JP.m. Note that all figs in the ms that present sims (with the exception of Figs 4 & 7) were generated in Excel 

----------------------------

Files:
	(1)-(5) Set up the model engine (should not be modified); 
	(6)-(7) Set up the model params  
		Note that currently (6) has the params values to reproduce the data of the bar graph in Figure 5A; #7 has the params values for the bar graph data in Figure 5B in the manuscript)
		If users would like to run all other simulations included in the ms, user needs to choose the option 'WT' for "Mouse_type" and then change the appropriate input value for the param of interest. For example, the 				simulations of Fig 6 are obtained by setting param values in file (6) to 'WT" and then manually change the value of Pm_O2
	(8)     Main file to run the simulations. It calls either (6) or (7), (4) and then (5) in the ode solver. Note that in turn (4) calls all the other files (1) - (3), which build the model 
	(9)     Postprocessing file to calculate the t37 and MMM-KHbO2 (called k37 in the code)


In order to run the model, the user needs to  

	(a) Choose param values in ModelParameters_RBC_ok_PmO2_Params_ok_JP.m 

	(b) Run the Simulate_O2_Efflux.m ...main file to run the simulations 

	(c) Run Calculate_t37_JP.m to calculate t37 and MMM-KHbO2 (called k37 in the code)

