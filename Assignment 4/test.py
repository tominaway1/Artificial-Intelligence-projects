"""A data set for a machine learning problem.  It has the following fields:

    [['T', 'T', 'Lost'], ['T', 'T', 'Lost'], ['T', 'F', 'Lost'], ['T', 'F', 'Lost'], ['F', 'T', 'NotLost'], ['F', 'T', 'NotLost'], ['F', 'T', 'NotLost'], ['F', 'T', 'NotLost'], ['F', 'T', 'NotLost'], ['F', 'F', 'Lost']]
    d.examples    A list of examples.  Each one is a list of attribute values.
    
    [0, 1, 2]
    d.attrs       A list of integers to index into an example, so example[attr]
                  gives a value. Normally the same as range(len(d.examples)). 
    
    
    ['X1', 'X2', 'Y']
    d.attrnames   Optional list of mnemonic names for corresponding attrs.
    
    2
    d.target      The attribute that a learning algorithm will try to predict.
                  By default the final attribute.
    
    [0, 1]
    d.inputs      The list of attrs without the target.
    

    [['T', 'F'], ['T', 'F'], ['NotLost', 'Lost']]
    d.values      A list of lists, each sublist is the set of possible
                  values for the corresponding attribute. If None, it
                  is computed from the known examples by self.setproblem.
                  If not None, an erroneous value raises ValueError.
    d.name  (dc)      Name of the data set (for output display only).
    d.source (dc)     URL or other source where the data came from.

    Normally, you call the constructor and you're done; then you just
    access fields like d.examples and d.target and d.inputs."""