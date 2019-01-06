# DegreeDropper
Degree Dropper Algorithm

This is a python module implementing the degree dropper algorithm based on 
page 197, Algebraic Cryptanlysis, G. V. Bard.

This module is used to transform a system of arbitrary high degree equations
over `GF(2)`, into an equivalent quadratic system. This is done by introducing
new variables to encode high degree monomials and new equations relating them. 

## Python Example
```
import DegreeDropper
sys = ["x1*x3 + x2", "x2*x1*x4 + x1*x3 + x1 + 1", "x1*x2*x3*x4 + x1*x3*x2 + x2*x3 + x1"]
all_eqs, all_vars = DegreeDropper.simple_degree_dropper(sys)
print(all_eqs)
print(all_vars)
```
## SageMath Example
```
import DegreeDropper
sys = ["x1*x3 + x2", "x2*x1*x4 + x1*x3 + x1 + 1", "x1*x2*x3*x4 + x1*x3*x2 + x2*x3 + x1 + 1"]
monomials = DegreeDropper.get_monomials_from_list_of_polys(sys)     
vars = DegreeDropper.get_variables_from_list_of_monomials(monomials)
B = BooleanPolynomialRing(len(vars), vars)
ps = map(B, sys)
I = Ideal(ps)
sys1, vars1 = DegreeDropper.simple_degree_dropper(sys)
B1 = BooleanPolynomialRing(len(vars1), vars1)
ps1 = map(B1, sys1)
I1 = Ideal(ps1)
%time I.variety()
%time I1.variety()
```
