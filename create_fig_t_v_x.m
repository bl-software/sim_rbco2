function []=create_fig__t_v_x( chart_type, shell_str,time_str,sol_n1,mytitle,xlab,ylab,figfilename )

global gl_time gl_X gl_n1
gl_n1
%class(gl_n1)
gl_n1= sol_n1
%class(gl_n1)

if time_str=="" || time_str==":"
    time_str='[1:end]'
end
x_str= sprintf('gl_time(%s)',time_str)
x= eval(x_str);

%NOTE - require - assume good users - no testing
%if shell_str=="" || shell_str==":"
%    shell_str = '1:end'
%end
cols_str= sprintf('%s+gl_n1',shell_str)
if chart_type=="pH"
    y_str= sprintf('3-log10(gl_X(%s, %s))',time_str,cols_str )
else
    y_str= sprintf('gl_X(%s, %s)',time_str,cols_str )
end
y= eval(y_str);

figure()
plot(x,y,'LineWidth',2)
% GOAL: plot(gl_time([1:end]),3-log10(gl_X([1:end], [631 633:638] )),'LineWidth',2)

shells= eval(shell_str)
legend(eval(sprintf('{%s}',sprintf('"Sh %d",',shells))))
xlim([0 gl_time(end)])
%ylim([-0.1 10.0])
title(mytitle)
xlabel(xlab)
ylabel(ylab)
hold all

savefig( figfilename )

