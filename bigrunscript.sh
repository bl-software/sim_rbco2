STORAGEFOLDER=lglogsweep_0068
PARAMFILE=Params/Sim_2__AJP/Paper_3__Nonspecific/Params_4__Fig_GenSweeps.py

# first 3 are gam sweeps
sed --debug --in-place -e 's/^sweepvar=/#sweepvar=/' $PARAMFILE
sed --in-place -e 's/#sweepvar=\["tort_gamma"]/sweepvar=["tort_gamma"]/' $PARAMFILE

sed --in-place -e 's/^Ai=\[/#Ai=[/' $PARAMFILE
sed --in-place -e 's/^As=\[/#As=[/' $PARAMFILE
sed --in-place -e 's/#Ai=\[     5.0 ]/Ai=[     5.0 ]/' $PARAMFILE
sed --in-place -e 's/#As=\[   150.0 ]/As=[   150.0 ]/' $PARAMFILE

#read -p 5_150
for i in {0..20}
do
    sed --in-place -e 's/lamsel=[0-9]*$/lamsel='$i'/' $PARAMFILE
    #PYOPENGL_PLATFORM=egl python mgui.py --simtype=1 --paper=1 --figure=Fig_LamGamSweeps --sdp=$STORAGEFOLDER/ajpswp_5_150_gams_l$i --dosim --dofig='Fig GenSweeps' --doexit
done

sed --in-place -e 's/^Ai=\[/#Ai=[/' $PARAMFILE
sed --in-place -e 's/^As=\[/#As=[/' $PARAMFILE
sed --in-place -e 's/#Ai=\[  1000.0 ]/Ai=[  1000.0 ]/' $PARAMFILE
sed --in-place -e 's/#As=\[   150.0 ]/As=[   150.0 ]/' $PARAMFILE
#read -p 1000_150
for i in {0..20}
do
    sed --in-place -e 's/lamsel=[0-9]*$/lamsel='$i'/' $PARAMFILE
    #PYOPENGL_PLATFORM=egl python mgui.py --simtype=1 --figure=Fig_GenSweeps --sdp=$STORAGEFOLDER/ajpswp_1000_150_gams_l$i --dosim --dofig='Fig GenSweeps' --doexit
done

sed --in-place -e 's/^Ai=\[/#Ai=[/' $PARAMFILE
sed --in-place -e 's/^As=\[/#As=[/' $PARAMFILE
sed --in-place -e 's/#Ai=\[    40.0 ]/Ai=[    40.0 ]/' $PARAMFILE
sed --in-place -e 's/#As=\[ 10000.0 ]/As=[ 10000.0 ]/' $PARAMFILE

#read -p 40_1000
for i in {0..20}
do
    sed --in-place -e 's/lamsel=[0-9]*$/lamsel='$i'/' $PARAMFILE
    #PYOPENGL_PLATFORM=egl python mgui.py --simtype=1 --figure=Fig_GenSweeps --sdp=$STORAGEFOLDER/ajpswp_40_10000_gams_l$i --dosim --dofig='Fig GenSweeps' --doexit
done
    

# next 3 are lam sweeps
sed --debug --in-place -e 's/^sweepvar=/#sweepvar=/' $PARAMFILE
sed --debug --in-place -e 's/#sweepvar=\["oos_tort_lambda"]$/sweepvar=["oos_tort_lambda"]/' $PARAMFILE

#read -p 'should be oos_tort_lam'
sed --in-place -e 's/^Ai=\[/#Ai=[/' $PARAMFILE
sed --in-place -e 's/^As=\[/#As=[/' $PARAMFILE
sed --in-place -e 's/#Ai=\[     5.0 ]/Ai=[     5.0 ]/' $PARAMFILE
sed --in-place -e 's/#As=\[   150.0 ]/As=[   150.0 ]/' $PARAMFILE
#read -p 5_150
for i in {0..20}
do
    sed --in-place -e 's/gamsel=[0-9]*$/gamsel='$i'/' $PARAMFILE
    #PYOPENGL_PLATFORM=egl python mgui.py --simtype=1 --figure=Fig_GenSweeps --sdp=$STORAGEFOLDER/ajpswp_5_150_g${i}_lams --dosim --dofig='Fig GenSweeps' --doexit
done

sed --in-place -e 's/^Ai=\[/#Ai=[/' $PARAMFILE
sed --in-place -e 's/^As=\[/#As=[/' $PARAMFILE
sed --in-place -e 's/#Ai=\[  1000.0 ]/Ai=[  1000.0 ]/' $PARAMFILE
sed --in-place -e 's/#As=\[   150.0 ]/As=[   150.0 ]/' $PARAMFILE
#read -p 'shoud be 1000_150'
for i in {0..20}
do
    sed --in-place -e 's/gamsel=[0-9]*$/gamsel='$i'/' $PARAMFILE
    #PYOPENGL_PLATFORM=egl python mgui.py --simtype=1 --figure=Fig_GenSweeps --sdp=$STORAGEFOLDER/ajpswp_1000_150_g${i}_lams --dosim --dofig='Fig GenSweeps' --doexit
done

sed --in-place -e 's/^Ai=\[/#Ai=[/' $PARAMFILE
sed --in-place -e 's/^As=\[/#As=[/' $PARAMFILE
sed --in-place -e 's/#Ai=\[    40.0 ]/Ai=[    40.0 ]/' $PARAMFILE
sed --in-place -e 's/#As=\[ 10000.0 ]/As=[ 10000.0 ]/' $PARAMFILE
#read -p 'should be 40_1000'
for i in {0..20}
do
    sed --in-place -e 's/gamsel=[0-9]*$/gamsel='$i'/' $PARAMFILE
    #PYOPENGL_PLATFORM=egl python mgui.py --simtype=1 --figure=Fig_GenSweeps --sdp=$STORAGEFOLDER/ajpswp_40_10000_g${i}_lams --dosim --dofig='Fig GenSweeps' --doexit
done
 
