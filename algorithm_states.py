# coding: utf-8


# This file was *autogenerated* from the file algorithm_states.sage
from sage.all_cmdline import *   # import sage library

_sage_const_1 = Integer(1); _sage_const_0 = Integer(0); _sage_const_2 = Integer(2); _sage_const_4 = Integer(4)#!/usr/bin/env python

# In[2]:


class AlgorithmState():
    def __init__(self, m, t, output = True):
        self.m = m
        self.t = t
        self.output = output
        
    def apply_transform(self, transform):
        raise NotImplementedError("The method apply_transform has not been defined on this state type")
        
    def compose_transform(self, t1, t2):
        raise NotImplementedError("The method compose_transform has not been defined on this state type")
        
    def step(self, transform, description = None):
        m_before = self.m
        self.apply_transform(transform)
        if self.m == m_before:
            return
        self.t = self.compose_transform(self.t, transform)
        if self.output:
            if description is not None:
                print(description)
            pretty_print(self.m)
        
    def row_addition_transform(self, source, target, scale = _sage_const_1 ):
        raise NotImplementedError("The method row_addition_transform has not been defined on this state type")
        
    def add_row(self, source, target, scale = _sage_const_1 , description = None):
        self.step(self.row_addition_transform(source, target, scale), description)
        
    def switch_rows(self, source, target, description = None):
        self.step(
            self.compose_transform(
                self.compose_transform(
                    self.row_addition_transform(source, target),
                    self.row_addition_transform(target, source, scale = -_sage_const_1 ),
                ),
                self.row_addition_transform(source, target),
            ), description
        )
    
    def column_addition_transform(self, source, target, scale = _sage_const_1 ):
        raise NotImplementedError("The method column_addition_transform has not been defined on this state type")
    
    def add_column(self, source, target, scale = _sage_const_1 , description = None):
        self.step(self.column_addition_transform(source, target, scale), description)
        
    def switch_columns(self, source, target, description = None):
        self.step(
            self.compose_transform(
                self.compose_transform(
                    self.column_addition_transform(source, target),
                    self.column_addition_transform(target, source, scale = -_sage_const_1 ),
                ),
                self.column_addition_transform(source, target),
            ), description
        )


# In[3]:


class SLnState(AlgorithmState):
    def __init__(self, m, output = True):
        dim = m.nrows()
        super().__init__(m, (identity_matrix(dim), identity_matrix(dim)), output)
        self.dim = dim
        
    def apply_transform(self, transform):
        self.m = transform[_sage_const_0 ] * self.m * transform[_sage_const_1 ]
        
    def compose_transform(self, t1, t2):
        return (t2[_sage_const_0 ] * t1[_sage_const_0 ], t1[_sage_const_1 ] * t2[_sage_const_1 ])
        
    def column_addition_transform(self, source, target, scale = _sage_const_1 ):
        return (identity_matrix(self.dim), elementary_matrix(ZZ, self.dim, row1 = source, row2 = target, scale = scale))

    def row_addition_transform(self, source, target, scale = _sage_const_1 ):
        return (elementary_matrix(ZZ, self.dim, row1 = target, row2 = source, scale = scale), identity_matrix(self.dim))


# In[4]:


class SL2SL2State(AlgorithmState):
    def __init__(self, m, output = True):
        super().__init__(m, (identity_matrix(_sage_const_2 ), identity_matrix(_sage_const_2 )), output)
        
    def project(self, m1, m2):
        return matrix([[m1[y // _sage_const_2 , x // _sage_const_2 ] * m2[y % _sage_const_2 , x % _sage_const_2 ] for x in range(_sage_const_4 )] for y in range(_sage_const_4 )])
    
    def apply_transform(self, transform):
        self.m = self.project(transform[_sage_const_0 ], transform[_sage_const_1 ]) * self.m
    
    def compose_transform(self, t1, t2):
        return (t2[_sage_const_0 ] * t1[_sage_const_0 ], t2[_sage_const_1 ] * t1[_sage_const_1 ])
    
    def row_addition_transform(self, source, target, scale = _sage_const_1 ):
        offset = min(source, target)
        source -= offset
        target -= offset
        if source == _sage_const_0  and target == _sage_const_1 :
            return (identity_matrix(_sage_const_2 ), elementary_matrix(ZZ, _sage_const_2 , row1 = _sage_const_1 , row2 = _sage_const_0 , scale = scale))
        if source == _sage_const_1  and target == _sage_const_0 :
            return (identity_matrix(_sage_const_2 ), elementary_matrix(ZZ, _sage_const_2 , row1 = _sage_const_0 , row2 = _sage_const_1 , scale = scale))
        if source == _sage_const_0  and target == _sage_const_2 :
            return (elementary_matrix(ZZ, _sage_const_2 , row1 = _sage_const_1 , row2 = _sage_const_0 , scale = scale), identity_matrix(_sage_const_2 ))
        if source == _sage_const_2  and target == _sage_const_0 :
            return (elementary_matrix(ZZ, _sage_const_2 , row1 = _sage_const_0 , row2 = _sage_const_1 , scale = scale), identity_matrix(_sage_const_2 ))
    
    def column_addition_transform(self, source, target, scale = _sage_const_1 ):
        raise NotImplementedError("Column manipulation is not implemented")


# In[5]:


class ModelState(AlgorithmState):
    def __init__(self, m, output = True):
        dim = m.nrows()
        super().__init__(m, identity_matrix(dim), output)
        self.dim = dim
    
    def apply_transform(self, transform):
        self.m = transform.transpose() * self.m * transform
        
    def compose_transform(self, t1, t2):
        return t1 * t2
    
    def row_addition_transform(self, source, target, scale = _sage_const_1 ):
        return elementary_matrix(scale.parent(), self.dim, row1 = source, row2 = target, scale = scale)
    
    def column_addition_transform(self, source, target, scale = _sage_const_1 ):
        return self.row_addition_transform(source, target, scale)


# In[ ]:


class ModelImprovementState(AlgorithmState):
    def __init__(self, m, improvement, output = True):
        dim = m.nrows()
        super().__init__((m, improvement), (identity_matrix(dim), identity_matrix(dim)), output)
        self.dim = dim
    
    @property
    def improvement(self):
        return self.m[_sage_const_1 ]
    
    def apply_transform(self, transform):
        (m1, m2) = self.m
        (t1, t2) = transform
        self.m = (t1.inverse().transpose() * m1 * t1.inverse(), t1 * m2 * t2)
        
    def compose_transform(self, t1, t2):
        return (t2[_sage_const_0 ] * t1[_sage_const_0 ], t1[_sage_const_1 ] * t2[_sage_const_1 ])
    
    def column_addition_transform(self, source, target, scale = _sage_const_1 ):
        return (identity_matrix(self.dim), elementary_matrix(scale.parent(), self.dim, row1 = source, row2 = target, scale = scale))

    def row_addition_transform(self, source, target, scale = _sage_const_1 ):
        return (elementary_matrix(scale.parent(), self.dim, row1 = target, row2 = source, scale = scale), identity_matrix(self.dim))

