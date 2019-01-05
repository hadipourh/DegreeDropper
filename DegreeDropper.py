"""
@H. Hadipour
SAT, JAN 5, 2019
SAT, DEY 15, 1398

This is a python module implementing the degree dropper algorithm based on 
page 197, Algebraic Cryptanlysis, G. V. Bard.

This module is used to transform a system of arbitrary high degree equations
over GF(2), into an equivalaent quadratic system. This is done by introducing
new variables to encode high degree monomials and new equations relating them. 
"""



#A global variable which contains all of the original variables in it. 
reference_variables = list()


def get_variables_from_monomial(monomial):
    """
    it gets a non-constant monomial like x*y*z and 
    rturns a list consisting of given monomial's
    variables. which in this case are: ['x', 'y', 'z']
    """
    assert(not monomial.isdigit())
    temp = monomial.split('*')
    temp.sort()
    return temp

def get_variables_from_list_of_monomials(list_of_monomials):
    """
    it gets a list of monomials and rturns the variables 
    which are used in the given monomials
    """
    vars = set()
    for monomial in list_of_monomials:
        vars = vars.union(get_variables_from_monomial(monomial))
    temp = list(vars)
    temp.sort()
    return temp

def get_monomials_from_polynomial(polynomial):
    """
    it gets a polynomial, and returns its monomials
    """
    monomials = polynomial.split(' + ')
    if '1' in monomials:
        monomials.remove('1')
    return list(set(monomials))

def get_monomials_from_list_of_polys(polys):
    """
    it gets a list of polynomials and returns
    all of the monomials which are used in the given 
    polynomials
    """
    monomials = set()
    for poly in polys:
        monos = set(get_monomials_from_polynomial(poly))
        monomials = monomials.union(monos)
    return list(monomials)

def update_reference_variable(variables):
    """
    updates reference variables, whenever a degree dropper
    function is called
    """
    global reference_variables
    ref_var_set = set(reference_variables)
    vars_set = set(variables)
    new_vars = vars_set.difference(ref_var_set)    
    new_vars = list(new_vars)
    reference_variables.extend(new_vars)

def clear_reference_variables():
    """
    it is used to clear the list of reference variables
    """
    global reference_variables
    reference_variables.clear()

def degree_of_monomial(monomial):
    """
    it returns degree of the given monomial
    """
    vars = get_variables_from_monomial(monomial)
    return len(vars)    

def __monomial_degree_dropper(monomial, extra_var_name = 't'):
    """
    it gets a monomial and returns three outputs:
    1 - Extra quadratic equations needed to decrease the monomial's 
    degree to two
    2 - Extra variables which are created to get an equavalent
    quadratic system of equations
    3 - A quadratic term according to new variables 
    which can be replaced with the given monomial
    
    for example let 'x1*x2*x3' be the input, then the outputs are:
    1 - ['t01 + x1*x2']
    2 - ['t01']
    3 - 't01*x3'
    """
    global reference_variables
    variables = get_variables_from_monomial(monomial)
    ##update_reference_variable(variables)
    degree = degree_of_monomial(monomial)
    extra_equations = list()
    extra_variables = list()
    assert(degree > 2)
    # variable indices with respect to reference variable
    var_indices = [reference_variables.index(x) for x in variables]
    ext_var = extra_var_name + str(var_indices[0]) + str(var_indices[1])
    temp = ext_var + ' + ' + variables[0] + '*' + variables[1]
    extra_equations.append(temp)
    extra_variables.append(ext_var)
    for i in range(2, degree - 1):
        indices = range(0, i)
        new_var1 = extra_var_name + "".join([str(var_indices[j]) for j in indices])
        new_var2 = new_var1 + str(var_indices[i])
        extra_variables.append(new_var2)
        extra_equations.append(new_var2 + ' + ' + new_var1 + "*" + variables[i])
    new_term = extra_var_name + "".join([str(var_indices[i]) for i in range(0, degree - 1)]) \
    + "*" + variables[degree - 1]
    return (extra_equations, extra_variables, new_term)

def polynomial_degree_dropper(polynomial):
    """
    it gets a boolean polynomial and returns two outputs:
    1 - a system of equations of degree at most two which is equivalanet 
    to the main equation
    2 - all extra variables generated to obtain the equivalent system of 
    quadratic equations
    """
    global reference_variables
    monomials = get_monomials_from_polynomial(polynomial)
    main_variables = get_variables_from_list_of_monomials(monomials)
    update_reference_variable(main_variables)
    reference_variables.sort()

    all_equations = list()
    extra_equations = list()
    extra_variables = list()
    new_terms_dict = dict()

    for m in monomials:
        if degree_of_monomial(m) > 2:
            extra_eq, extra_var, new_term = __monomial_degree_dropper(m)
            extra_equations.extend(extra_eq)
            extra_variables.extend(extra_var)
            new_terms_dict[m] = new_term
    new_equation = polynomial
    for key in new_terms_dict.keys():
        new_equation = new_equation.replace(key, new_terms_dict[key])
    all_equations.append(new_equation)
    all_equations.extend(extra_equations)
    return (all_equations, extra_variables)

def simple_degree_dropper(poly_sys):
    """
    it gets a system of polynomial equations and returns two outputs:
    1 - A system of polynomial equations of degree at most two, whih is equivalent with 
    the given system

    2 - List of all variables used in the equivalent system of quadratic equations, in sahpe of
    [main_variables] + [extra_variables]    
    """
    global reference_variables
    all_equations = list()
    extra_variables = list()
    new_terms_dict = dict()
    all_monomials = get_monomials_from_list_of_polys(poly_sys)

    main_variables = get_variables_from_list_of_monomials(all_monomials)
    update_reference_variable(main_variables)
    reference_variables.sort()
    for m in all_monomials:
        monomial_degree = degree_of_monomial(m)
        if monomial_degree > 2:
            extra_eq, extra_var, new_term = __monomial_degree_dropper(m)            
            all_equations.extend(extra_eq)
            extra_variables.extend(extra_var)
            new_terms_dict[m] = new_term
    for p in poly_sys:
        new_equation = p
        for key in new_terms_dict.keys():
            new_equation = new_equation.replace(key, new_terms_dict[key])
        all_equations.append(new_equation)
    extra_variables = list(set(extra_variables))
    extra_variables.sort()
    all_equations = list(set(all_equations))
    return (all_equations, main_variables + extra_variables)

"""
Python example:
import DegreeDropper
sys = ["x1*x3 + x2", "x2*x1*x4 + x1*x3 + x1 + 1", "x1*x2*x3*x4 + x1*x3*x2 + x2*x3 + x1"]
all_eqs, all_vars = DegreeDropper.simple_degree_dropper(sys)
print(all_eqs)
print(all_vars)

"""

"""
SageMath example:

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

"""
