# DegreeDropper
Degree Dropper Algorithm

This is a python module implementing the degree dropper algorithm based on 
page 197, Algebraic Cryptanlysis, G. V. Bard.

This module is used to transform a system of arbitrary high degree equations
over `GF(2)`, into an equivalent quadratic system. This is done by introducing
new variables to encode high degree monomials and new equations relating them. 

## Python Example
```
In [1]: import DegreeDropper
In [2]: sys = ["x1*x3 + x2", "x2*x1*x4 + x1*x3 + x1 + 1", "x1*x2*x3*x4 + x1*x3*x2 + x2*x3 + x1"]
In [3]: all_eqs, all_vars = DegreeDropper.simple_degree_dropper(sys)
In [4]: all_eqs                                                                                                                
Out[4]: 
['t01*x4 + x1*x3 + x1 + 1',
 't012*x4 + t01*x3 + x2*x3 + x1',
 't01 + x1*x2',
 'x1*x3 + x2',
 't012 + t01*x3']
In [5]: all_vars                                                                                                               
Out[5]: ['x1', 'x2', 'x3', 'x4', 't01', 't012']
```
## SageMath Example
```
import DegreeDropper
sys = ["x1*x3 + x2", "x2*x1*x4 + x1*x3 + x1 + 1", "x1*x2*x3*x4 + x1*x3*x2 + x2*x3 + x1 + 1"]
monomials = DegreeDropper.get_monomials_from_list_of_polys(sys)     
vars = DegreeDropper.get_variables_from_list_of_monomials(monomials)
B = BooleanPolynomialRing(len(vars), vars)
ps = map(B, sys)
I = Ideal(list(ps))
sys1, vars1 = DegreeDropper.simple_degree_dropper(sys)
B1 = BooleanPolynomialRing(len(vars1), vars1)
ps1 = map(B1, sys1)
I1 = Ideal(list(ps1))
```
Solving the equations using Groebner basis algorithm: 
```
sage: %time I.variety()
CPU times: user 93.4 ms, sys: 22.3 ms, total: 116 ms
Wall time: 197 ms
[{x4: 0, x3: 0, x2: 0, x1: 1}, {x4: 1, x3: 0, x2: 0, x1: 1}]

sage: %time I1.variety()
CPU times: user 41.5 ms, sys: 64.7 ms, total: 106 ms
Wall time: 107 ms
[{t012: 0, t01: 0, x4: 0, x3: 0, x2: 0, x1: 1},
 {t012: 0, t01: 0, x4: 1, x3: 0, x2: 0, x1: 1}]
```

