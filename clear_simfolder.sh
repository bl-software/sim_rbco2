for var in "$@"
do
    echo Doing "$var"
    if [ -d "$var" ];  then
        ls $var;
        rm -v $var/run_*
        rm -v $var/$var_*
    fi;
done
