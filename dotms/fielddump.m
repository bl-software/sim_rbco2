fns = fieldnames(S);
fd= fopen(ofname, 'wt');
for k=1:numel(fns)
    %disp(sprintf('k= %d ',k))
    n= fns{k};
    v= S.(n);
    disp(n)
    if isnumeric(v)
    if length(v) < 5
        disp(v)
        if isinteger(v)
            strtyp= ',%d';
        elseif isfloat(v)
            strtyp= ',%f';
        end
        fstr='%s';
        for i = 1:length(v)
            fstr=strcat(fstr,strtyp);
        end
        fstr=strcat(fstr,'\n');
        disp(fstr);
        fprintf(fd,fstr,n,v);
    end
    end
end
fclose(fd)
