import sys
import csv

fn1=sys.argv[1]
fn2=sys.argv[2]

def makedict(fn):
    with open(fn) as csv_file:
        d={}
        reader = csv.DictReader(csv_file,fieldnames=['varn',])
        for row in reader:
            items=row.items()
            for i,(k,varval) in enumerate(items):
                #print(f'k:{k}, vv:{varval}   {len(varval)}')
                if i == 0:
                    var=varval
                    if var=='alpha':
                        var='perm_alpha'
            if len(varval)==1:
                d[var]=varval[0]
            else:
                d[var]=varval
    return d

d1=makedict(fn1)
d2=makedict(fn2)
print(f'{fn1} {d1}')
print(f'{fn2} {d2}')

d1ks= list(d1.keys())
print(type(d1ks), d1ks)

eqs=[]
neqs=[]
for k in d1ks:
    v1=d1.pop(k)
    try:
        v2=d2.pop(k)
    except KeyError:
        print(f'No {k} in d2')
        continue

    if v1 == v2:
        eqs.append(f'{k} equal {v1} == {v2}')
    else:
        neqs.append(f'\n!!!!!\n{k} NOT equal {v1} != {v2}')

print('\nEQUAL:\n','\n'.join(eqs))
print('\nNOT EQUAL:\n','\n'.join(neqs))
print(f'\n{fn1} {d1}')
print(f'\n{fn2} {d2}')
#breakpoint()
