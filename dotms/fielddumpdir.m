%dirlist= dir('*.mat')
dirlist= dir('rbc2024Rp8/rbc2024Rp8.mat')
%disp(dirlist)
for k = 1:length(dirlist)
    fname=dirlist(k).name;
    disp(fname);
    ofname=replace(fname, '.mat', '.csv');
    S=load(fname);
    fielddump
end
