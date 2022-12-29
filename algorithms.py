# coding: utf-8


# This file was *autogenerated* from the file algorithms.sage
from sage.all_cmdline import *   # import sage library

_sage_const_0 = Integer(0); _sage_const_1 = Integer(1); _sage_const_2 = Integer(2); _sage_const_3 = Integer(3); _sage_const_4 = Integer(4)#!/usr/bin/env python

# In[ ]:


import algorithm_states, common


# In[3]:


def lemma_2_6(m, k = QQ.algebraic_closure()):
    state = algorithm_states.SL2SL2State(m0, output = False)
    
    if state.m[_sage_const_0 , _sage_const_0 ] == _sage_const_0  and state.m[_sage_const_0 , _sage_const_1 ] == _sage_const_0 :
        state.add_row(_sage_const_2 , _sage_const_0 )
        
    if state.m[_sage_const_1 , _sage_const_0 ] == _sage_const_0 :
        state.add_row(_sage_const_0 , _sage_const_1 )
        
    state.add_row(_sage_const_1 , _sage_const_0 , scale = (_sage_const_1  - state.m[_sage_const_0 , _sage_const_0 ]) / state.m[_sage_const_1 , _sage_const_0 ])
    
    state.add_row(_sage_const_0 , _sage_const_1 , scale = -state.m[_sage_const_1 , _sage_const_0 ])
    
    state.add_row(_sage_const_0 , _sage_const_2 , scale = -state.m[_sage_const_2 , _sage_const_0 ])
    
    state.add_row(_sage_const_3 , _sage_const_2 , scale = -state.m[_sage_const_2 , _sage_const_3 ])
    
    state.add_row(_sage_const_3 , _sage_const_1 , scale = -state.m[_sage_const_1 , _sage_const_3 ])
    
    mu = k(sqrt(state.m[_sage_const_1 , _sage_const_1 ]))
    state.step((diagonal_matrix([_sage_const_1 /mu, mu]), diagonal_matrix([mu, _sage_const_1 /mu])))
    
    (lift1, lift2) = state.t
    
    return lift1.inverse(), lift2.inverse()


# In[ ]:


def lemma_3_1(m):
    state = algorithm_states.SLnState(m, output = False)
    
    for j in range(_sage_const_0 , state.dim - _sage_const_1 ):
        while len([i for i in range(state.dim) if state.m[j, i] != _sage_const_0 ]) > _sage_const_1 :
            columns = sorted([(ZZ(state.m[j, i]), i) for i in range(state.dim)], reverse = True)
            source = columns[_sage_const_1 ][_sage_const_1 ]
            target = columns[_sage_const_0 ][_sage_const_1 ]
            factor = columns[_sage_const_0 ][_sage_const_0 ] // columns[_sage_const_1 ][_sage_const_0 ]
            state.add_column(source, target, scale = -factor, description = f"Subtract {factor} times column {source} from {target}")

        if state.m[j, state.dim - _sage_const_1 ] == _sage_const_0 :
            i = [i for i in range(state.dim) if state.m[j, i] != _sage_const_0 ][_sage_const_0 ]
            state.switch_columns(i, state.dim - _sage_const_1 , description = f"Switch columns {i} and {state.dim - 1}")

        state.add_column(state.dim - _sage_const_1 , j, scale = ZZ(_sage_const_1  / state.m[j, state.dim - _sage_const_1 ]), description = f"Make entry ({j}, {j}) equal to 1")

        state.add_column(j, state.dim - _sage_const_1 , scale = -state.m[j, state.dim - _sage_const_1 ], description = f"Make entry ({j}, {state.dim - 1}) equal to 0")

        for i in range(j + _sage_const_1 , state.dim):
            state.add_row(j, i, scale = -state.m[i, j], description = f"Make entry ({i}, {j}) equal to zero")
            
    left_lift, right_lift = state.t
    return left_lift.inverse() * right_lift.inverse()


# In[2]:


def lemma_4_3(m, p):
    state = algorithm_states.ModelState(m, output = False)
    a = _sage_const_1 
    
    for i in range(_sage_const_0 , state.dim - _sage_const_1 ):
        (o, j) = min((common.ord_vector(p, state.m, j), j) for j in range(i, state.dim))
        if o < common.ord_vector(p, state.m, i):
            state.switch_columns(j, i, description = f"Make sure that the order of column {i} is minimal")

        (o, j) = min((common.ord(p, state.m[j, i]), j) for j in range(i, state.dim))
        for k in range(_sage_const_2 ):
            if o < common.ord(p, state.m[i, i]):
                state.add_row(j, i, description = f"Make sure that the order of entry ({i}, {i}) is minimal")

        a = lcm(a, (state.m[i, i] * p**(-common.ord(p, state.m[i, i]))).numerator())

        for j in range(i + _sage_const_1 , state.dim):
            state.add_row(i, j, -state.m[i, j] / state.m[i, i], f"Make entry ({i}, {j}) equal to 0")
        
    return state.m, state.t, a


# In[ ]:


def lemma_4_5(m, t, p):
    state = algorithm_states.ModelImprovementState(m, t, output = False)
    s = []
    
    for i in range(_sage_const_0 , state.dim):
        (o, j) = min((common.ord_vector(p, state.improvement, j), j) for j in range(i, state.dim))
        if o < common.ord_vector(p, state.improvement, i):
            state.switch_columns(j, i, description = f"Make the order of column {i} minimal")

        s.append(common.ord_vector(p, state.improvement, i))

        (o, j) = min((common.ord(p, state.improvement[j, i]), j) for j in range(i, state.dim))
        if o < common.ord(p, state.improvement[i, i]):
            state.switch_rows(j, i, description = f"Make the order of entry ({i}, {i}) minimal")

        state.step((identity_matrix(state.dim), elementary_matrix(QQ, state.dim, row1=i, scale=p**s[i] / state.improvement[i, i])), description = f"Convert entry ({i}, {i}) to the form p^s")

        for j in range(i + _sage_const_1 , state.dim):
            state.add_column(i, j, -state.improvement[i, j] / state.improvement[i, i], f"Make entry ({i}, {j}) equal to 0")
            
    s_matrix = diagonal_matrix(QQ, [p**n for n in s])
    r = (state.improvement * s_matrix.inverse()).apply_map(lambda x: ZZ(Integers(p**(-_sage_const_2  * s[_sage_const_0 ]))(x)))
    return state.t[_sage_const_0 ].inverse() * r, s_matrix


# In[ ]:


def theorem_4_1(m, p):
    state = algorithm_states.ModelState(m, output = False)
    k = common.ord(p, state.m.determinant())
    F = GF(p)

    (_, diagonal_transform, _) = lemma_4_3(state.m, p)
    state.step(diagonal_transform, "Rediagonalize")

    state.step(diagonal_matrix(_sage_const_1  / p**((common.ord(p, state.m[i, i]) // _sage_const_2 )) for i in range(state.dim)), "Remove excess square powers of p")

    while min(i for i in range(state.dim) if state.m[i, i] % p != _sage_const_0 ) < max(i for i in range(state.dim) if state.m[i, i] % p == _sage_const_0 ):
        i = min(i for i in range(state.dim) if state.m[i, i] % p != _sage_const_0 )
        j = max(i for i in range(state.dim) if state.m[i, i] % p == _sage_const_0 )
        state.switch_rows(j, i, "Move entries divisible by p to the front")

    k = common.ord(p, state.m.determinant())
    
    while k >= _sage_const_4 :
        # Find a solution
        solution = None
        if F(-state.m[_sage_const_2 , _sage_const_2 ] / state.m[_sage_const_1 , _sage_const_1 ]).is_square():
            solution = (_sage_const_0 , _sage_const_1 , ZZ(F(-state.m[_sage_const_2 , _sage_const_2 ] / state.m[_sage_const_1 , _sage_const_1 ]).sqrt()))
        else:
            for x2 in range((p + _sage_const_1 ) / _sage_const_2 ):
                if F(-(state.m[_sage_const_0 , _sage_const_0 ] + x2**_sage_const_2  * state.m[_sage_const_1 , _sage_const_1 ]) / state.m[_sage_const_2 , _sage_const_2 ]).is_square():
                    solution = (_sage_const_1 , x2, ZZ(F(-(state.m[_sage_const_0 , _sage_const_0 ] + x2**_sage_const_2  * state.m[_sage_const_1 , _sage_const_1 ]) / state.m[_sage_const_2 , _sage_const_2 ]).sqrt()))
                    break

        if solution[_sage_const_0 ] == _sage_const_0 :
            state.switch_rows(_sage_const_1 , _sage_const_0 , description = "Make the first coefficient of the solution nonzero")
            solution = (solution[_sage_const_1 ], solution[_sage_const_0 ], solution[_sage_const_2 ])

        state.add_row(_sage_const_1 , _sage_const_0 , ZZ(solution[_sage_const_1 ]), "Apply partial improvement")
        state.add_row(_sage_const_2 , _sage_const_0 , ZZ(solution[_sage_const_2 ]), "Apply partial improvement")
        state.step(elementary_matrix(QQ, state.dim, row1 = _sage_const_0 , scale = _sage_const_1  / p))

        (_, diagonal_transform, _) = lemma_4_3(state.m, p)
        state.step(diagonal_transform, "Rediagonalize")

        state.step(diagonal_matrix(_sage_const_1  / p**((common.ord(p, state.m[i, i]) // _sage_const_2 )) for i in range(state.dim)), "Remove excess square powers of p")

        while min(i for i in range(state.dim) if state.m[i, i] % p != _sage_const_0 ) < max(i for i in range(state.dim) if state.m[i, i] % p == _sage_const_0 ):
            i = min(i for i in range(state.dim) if state.m[i, i] % p != _sage_const_0 )
            j = max(i for i in range(state.dim) if state.m[i, i] % p == _sage_const_0 )
            state.switch_rows(j, i, "Move entries divisible by p to the front")

        k = common.ord(p, state.m.determinant())
    
    if k == _sage_const_2 :
        l = ZZ(F(-state.m[_sage_const_0 , _sage_const_0 ] / state.m[_sage_const_1 , _sage_const_1 ]).sqrt())
        state.add_row(_sage_const_1 , _sage_const_0 , l, "Apply partial improvement")
        state.step(elementary_matrix(QQ, state.dim, row1 = _sage_const_0 , scale = _sage_const_1  / p))

        (_, diagonal_transform, _) = lemma_4_3(state.m, p)
        state.step(diagonal_transform, "Rediagonalize")
        k = common.ord(p, state.m.determinant())
    return state.m, state.t


# In[ ]:


def lemma_4_7(m):
    state = algorithm_states.ModelState(m, output = False)
    
    while len([i for i in range(_sage_const_0 , state.dim) if (state.m[i, i] + _sage_const_2  * i) % _sage_const_4  != _sage_const_1 ]) > _sage_const_0 :
        i = [i for i in range(_sage_const_0 , state.dim) if (state.m[i, i] + _sage_const_2  * i) % _sage_const_4  != _sage_const_1 ][_sage_const_0 ]
        j = [j for j in range(i, state.dim) if (state.m[j, j] + _sage_const_2  * i) % _sage_const_4  == _sage_const_1 ][_sage_const_0 ]
        state.switch_rows(j, i, description = f"Make sure that entry ({i}, {i}) has the correct parity")
        
    for i in range(_sage_const_0 , state.dim // _sage_const_2 ):
        state.add_row(_sage_const_2  * i, _sage_const_2  * i + _sage_const_1 , description = f"Add column {2 * i} to {2 * i + 1}")
        state.step(elementary_matrix(QQ, state.dim, row1 = _sage_const_2  * i + _sage_const_1 , scale = _sage_const_1  / _sage_const_2 ), description = f"Divide a factor 2 from column {2 * i + 1}")
    
    return state.m, state.t

