"""Learn to estimate functions  from examples. (Chapters 18-20)"""

from utils import *
import agents, random, operator
from copy import deepcopy

#______________________________________________________________________________

class DataSet:
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

    def __init__(self, examples=None, attrs=None, target=-1, values=None,
                 attrnames=None, name='', source='',
                 inputs=None, exclude=(), doc=''):
        """Accepts any of DataSet's fields.  Examples can
        also be a string or file from which to parse examples using parse_csv.
        >>> DataSet(examples='1, 2, 3')
        <DataSet(): 1 examples, 3 attributes>
        """
        update(self, name=name, source=source, values=values)
        # Initialize .examples from string or list or data directory
        if isinstance(examples, str):
            self.examples = parse_csv(examples)
        elif examples is None:
            self.examples = parse_csv(DataFile(name+'.csv').read())
        else:
            self.examples = examples
        map(self.check_example, self.examples)
        # Attrs are the indicies of examples, unless otherwise stated.
        if not attrs and self.examples:
            attrs = range(len(self.examples[0]))
        self.attrs = attrs
        # Initialize .attrnames from string, list, or by default
        if isinstance(attrnames, str): 
            self.attrnames = attrnames.split()
        else:
            self.attrnames = attrnames or attrs
        self.setproblem(target, inputs=inputs, exclude=exclude)

    def setproblem(self, target, inputs=None, exclude=()):
        """Set (or change) the target and/or inputs.
        This way, one DataSet can be used multiple ways. inputs, if specified,
        is a list of attributes, or specify exclude as a list of attributes
        to not put use in inputs. Attributes can be -n .. n, or an attrname.
        Also computes the list of possible values, if that wasn't done yet."""
        self.target = self.attrnum(target)
        exclude = map(self.attrnum, exclude)
        if inputs:
            self.inputs = removeall(self.target, inputs)
        else:
            self.inputs = [a for a in self.attrs
                           if a is not self.target and a not in exclude]
        if not self.values:
            self.values = map(unique, zip(*self.examples))

    def add_example(self, example):
        """Add an example to the list of examples, checking it first."""
        self.check_example(example)
        self.examples.append(example)

    def check_example(self, example):
        """Raise ValueError if example has any invalid values."""
        if self.values:
            for a in self.attrs:
                if example[a] not in self.values[a]:
                    raise ValueError('Bad value %s for attribute %s in %s' %
                                     (example[a], self.attrnames[a], example))

    def attrnum(self, attr):
        "Returns the number used for attr, which can be a name, or -n .. n."
        if attr < 0:
            return len(self.attrs) + attr
        elif isinstance(attr, str): 
            return self.attrnames.index(attr)
        else:
            return attr

    def sanitize(self, example):
       "Return a copy of example, with non-input attributes replaced by 0."
       return [i in self.inputs and example[i] for i in range(len(example))] 

    def __repr__(self):
        return '<DataSet(%s): %d examples, %d attributes>' % (
            self.name, len(self.examples), len(self.attrs))

#______________________________________________________________________________

def parse_csv(input, delim=','):
    r"""Input is a string consisting of lines, each line has comma-delimited 
    fields.  Convert this into a list of lists.  Blank lines are skipped.
    Fields that look like numbers are converted to numbers.
    The delim defaults to ',' but '\t' and None are also reasonable values.
    >>> parse_csv('1, 2, 3 \n 0, 2, na')
    [[1, 2, 3], [0, 2, 'na']]
    """
    lines = [line for line in input.splitlines() if line.strip() is not '']
    return [map(num_or_str, line.split(delim)) for line in lines]

def rms_error(predictions, targets):
    return math.sqrt(ms_error(predictions, targets))

def ms_error(predictions, targets):
    return mean([(p - t)**2 for p, t in zip(predictions, targets)])

def mean_error(predictions, targets):
    return mean([abs(p - t) for p, t in zip(predictions, targets)])

def mean_boolean_error(predictions, targets):
    return mean([(p != t)   for p, t in zip(predictions, targets)])


#______________________________________________________________________________

class Learner:
    """A Learner, or Learning Algorithm, can be trained with a dataset,
    and then asked to predict the target attribute of an example."""

    def train(self, dataset): 
        self.dataset = dataset

    def predict(self, example): 
        abstract


#______________________________________________________________________________

class DecisionTree:
    """A DecisionTree holds an attribute that is being tested, and a
    dict of {attrval: Tree} entries.  If Tree here is not a DecisionTree
    then it is the final classification of the example."""

    def __init__(self, attr, attrname=None, branches=None):
        "Initialize by saying what attribute this node tests."
        update(self, attr=attr, attrname=attrname or attr,
               branches=branches or {})

    def predict(self, example):
        "Given an example, use the tree to classify the example."
        child = self.branches[example[self.attr]]
        if isinstance(child, DecisionTree):
            return child.predict(example)
        else:
            return child  

    def add(self, val, subtree):
        "Add a branch.  If self.attr = val, go to the given subtree."
        self.branches[val] = subtree
        return self

    def outputDecisionTree(self, path):
        # implement this function
        with open(path, 'w') as f:
            print >>f, " "      

    def count_nodes(self):
        return 0

    def display(self, indent=0):
        name = self.attrname
        print 'Test', name
        for (val, subtree) in self.branches.items():
            print ' '*4*indent, name, '=', val, '==>',
            if isinstance(subtree, DecisionTree):
                subtree.display(indent+1)
            else:
                print 'RESULT = ', subtree

    def __repr__(self):
        return 'DecisionTree(%r, %r, %r)' % (
            self.attr, self.attrname, self.branches)

Yes, No = True, False
        
#______________________________________________________________________________

class DecisionTreeLearner(Learner):

    def predict(self, example):
        if isinstance(self.dt, DecisionTree):
            return self.dt.predict(example)
        else:
            return self.dt

    def train(self, dataset):
        self.dataset = dataset
        self.attrnames = dataset.attrnames
        self.dt = self.decision_tree_learning(dataset.examples, dataset.inputs)
    
    def prune(self, dataset, maxDeviation):
        dt = self.dt
        #check if already a leaf node
        tree = dt.branches
        v = dt.attr
        # print tree
        # if not isinstance(tree['T'],DecisionTree) and not isinstance(tree['F'],DecisionTree):
        #     return 

        for item in dataset.values[v]:
            if isinstance(tree[item],DecisionTree):
                new_dataset = deepcopy(dataset)
                new_examples = self.make_array(new_dataset.examples,item,v)
                new_dataset.examples = new_examples
                self.dt.branches[item] = self.prune_helper(tree[item],new_dataset,maxDeviation)

        # #evaluate subtrees
        # if isinstance(tree['F'],DecisionTree):
        #     new_dataset = deepcopy(dataset)
        #     new_examples = self.make_array(new_dataset.examples,'F',v)
        #     new_dataset.examples = new_examples
        #     self.dt.branches['F'] = self.prune_helper(tree['F'],new_dataset,maxDeviation)
        dt.display()
        return

    def make_array(self, examples, compare,v):
        new_examples = []
        for item in examples:
            if item[v] == compare:
                new_examples.append(item)
        return new_examples

    def prune_helper(self,dt,current_dataset,maxDeviation):
        tree = dt.branches
        v = dt.attr
        #check left and right subtrees
        print tree
        for item in current_dataset.values[v]:
            if isinstance(tree[item],DecisionTree):
                new_dataset = deepcopy(current_dataset)
                new_examples = self.make_array(new_dataset.examples,item,v)
                new_dataset.examples = new_examples
                dt.branches[item] = self.prune_helper(tree[item],new_dataset,maxDeviation)
        # if isinstance(tree['F'],DecisionTree):
        #     new_dataset = deepcopy(dataset)
        #     new_examples = self.make_array(new_dataset.examples,'F',v)
        #     new_dataset.examples = new_examples
        #     dt.branches['F'] = self.prune_helper(tree['F'],new_dataset,maxDeviation)

        #check if you can prune
        if not isinstance(tree['T'],DecisionTree) and not isinstance(tree['F'],DecisionTree):
            #make copy of left subtree
            left_dataset = deepcopy(current_dataset)
            new_examples = self.make_array(left_dataset.examples,'F',v)
            left_dataset.examples = new_examples
            #make copy of right subtree
            right_dataset = deepcopy(current_dataset)
            new_examples = self.make_array(right_dataset.examples,'T',v)
            right_dataset.examples = new_examples

            estimated_values = self.find_percentages(current_dataset)
            #left tree and right tree
            left_values = self.find_percentages(left_dataset)
            right_values = self.find_percentages(right_dataset)

            #find deviations
            dev = self.find_deviation(estimated_values,left_values,right_values)
            if dev < maxDeviation:
                return self.find_max(estimated_values)
            else:
                return tree
        else:
            return tree
    
    def find_max(self,d):
        maximum = 0
        ans = None
        for key in d:
            if d[key] >= maximum:
                maximum = d[key]
                ans = key
        return ans



    def find_deviation(self, estimated_values, left_values, right_values):
        dev = 0
        total = self.find_total(estimated_values)
        left_total = self.find_total(left_values)
        right_total = self.find_total(right_values)
        for key in estimated_values:
            expected_left = (estimated_values[key] * left_total * 1.0) / (total * 1.0)
            expected_right = (estimated_values[key] * right_total * 1.0) / (total * 1.0)
            dev += (expected_left-left_values[key])**2 / expected_left + (expected_right - right_values[key])**2 / expected_right
        print dev
        return dev
    
    def find_total(self,d):
        total = 0
        for key in d:
            total += d[key]
        return total

    def find_percentages(self,dataset):
        inputs = dataset.inputs
        vals = dataset.values
        target = dataset.target
        ans = {}
        for item in vals[target]:
            ans[item] = 0
        for item in dataset.examples:
            temp = ans[item[target]]
            ans[item[target]] = temp + 1
        return ans

    def decision_tree_learning(self, examples, attrs, default=None):
        if len(examples) == 0:
            return default
        elif self.all_same_class(examples):
            return examples[0][self.dataset.target]
        elif  len(attrs) == 0:
            return self.majority_value(examples)
        else:
            best = self.choose_attribute(attrs, examples)
            tree = DecisionTree(best, self.attrnames[best])
            for (v, examples_i) in self.split_by(best, examples):
                subtree = self.decision_tree_learning(examples_i,
                  removeall(best, attrs), self.majority_value(examples))
                tree.add(v, subtree)
            return tree

    def choose_attribute(self, attrs, examples):
        "Choose the attribute with the highest information gain."
        return argmax(attrs, lambda a: self.information_gain(a, examples))

    def all_same_class(self, examples):
        "Are all these examples in the same target class?"
        target = self.dataset.target
        class0 = examples[0][target]
        for e in examples:
           if e[target] != class0: return False
        return True

    def majority_value(self, examples):
        """Return the most popular target value for this set of examples.
        (If target is binary, this is the majority; otherwise plurality.)"""
        g = self.dataset.target
        return argmax(self.dataset.values[g],
                      lambda v: self.count(g, v, examples))

    def count(self, attr, val, examples):
        return count_if(lambda e: e[attr] == val, examples)
    
    def information_gain(self, attr, examples):
        def I(examples):
            target = self.dataset.target
            return information_content([self.count(target, v, examples)
                                        for v in self.dataset.values[target]])
        N = float(len(examples))
        remainder = 0
        for (v, examples_i) in self.split_by(attr, examples):
            remainder += (len(examples_i) / N) * I(examples_i)
        return I(examples) - remainder

    def split_by(self, attr, examples=None):
        "Return a list of (val, examples) pairs for each val of attr."
        if examples == None:
            examples = self.dataset.examples
        return [(v, [e for e in examples if e[attr] == v])
                for v in self.dataset.values[attr]]
    
def information_content(values):
    "Number of bits to represent the probability distribution in values."
    # If the values do not sum to 1, normalize them to make them a Prob. Dist.
    values = removeall(0, values)
    s = float(sum(values))
    if s != 1.0: values = [v/s for v in values]
    return sum([- v * log2(v) for v in values])


#_____________________________________________________________________________
# Functions for testing learners on examples

def test(learner, dataset, examples=None, target_classes=None, verbose=0):
    """Return macro F1 score on the dataset. Assumes the learner has already been trained."""
    if examples == None: examples = dataset.examples
    # right = 0.0
    metrics = {}
    if len(examples) == 0: return (0.0, 0.0)
    if target_classes == None: 
        metrics = {example[dataset.target]: {"tn": 0, "fn": 0, "tp": 0, "fp": 0} 
                for example in examples}
    else:
        metrics = {target_class: {"tn": 0, "fn": 0, "tp": 0, "fp": 0} 
                for target_class in target_classes}
    
    for example in examples:
        desired = example[dataset.target]
        output = learner.predict(dataset.sanitize(example))
        update_metrics(metrics, desired, output)
        if output == desired:
            # right += 1
            if verbose >= 2:
               print '   OK: got %s for %s' % (desired, example)
        elif verbose:
            print 'WRONG: got %s, expected %s for %s' % (
               output, desired, example)
    macro_recall = mean([v["tp"]/(v["tp"]+v["fn"]+1e-9) for v in metrics.values()]) 
    macro_precision = mean([v["tp"]/(v["tp"]+v["fp"]+1e-9) for v in metrics.values()])
    f1_score = 2*(macro_recall*macro_precision)/(macro_recall+macro_precision)
    return f1_score

def update_metrics(metrics, desire, output):
    if (desire == output):
        # true positive
        metrics[desire]["tp"] += 1
    else:
        # false positive
        metrics[output]["fp"] += 1
        # false negative
        metrics[desire]["fn"] += 1
    # true negative
    for k in metrics.keys():
        metrics[k]["tn"]=metrics[k]["tn"]+1 if k != desire and k != output else metrics[k]["tn"]

def train_and_test(learner, maxDeviation, train_dataset, cv_dataset, test_dataset):
    """Train the learner on train_dataset and test it on test_dataset.
    If maxDeviation>0, prune the decision tree with cv_dataset
    Return the node count and the f1 score of the decision tree"""
    learner.dataset = train_dataset 
    learner.train(train_dataset)
    if maxDeviation > 0:
        learner.prune(cv_dataset, maxDeviation)
    node_count = learner.dt.count_nodes()
    f1_score = test(learner, test_dataset)
    return (node_count, f1_score) 

def learningcurve(learner, maxDeviation, 
    train_dataset, cv_dataset, test_dataset, 
    step_size=10, trials=1, sizes = None, random_shuffle = False):
    if sizes == None:
        sizes = range(step_size, len(train_dataset.examples), step_size)
        if (sizes[-1] != len(train_dataset.examples)):
            sizes.append(len(train_dataset.examples))
    def score(learner, size):
        examples = train_dataset.examples
        try:
            if random_shuffle:
                random.shuffle(train_dataset.examples)
            train_dataset.examples = train_dataset.examples[0: size]
            return train_and_test(learner, maxDeviation, train_dataset, cv_dataset, test_dataset)
        finally:
            train_dataset.examples = examples
    return [(size, tuple(map(lambda x: mean(x),  \
                zip(*[score(learner, size) for t in range(trials)])))) \
                for size in sizes]


#______________________________________________________________________________
# The rest of this file gives Data sets for machine learning problems.

orings = DataSet(name='orings', target='Distressed',
                 attrnames="Rings Distressed Temp Pressure Flightnum")


zoo = DataSet(name='zoo', target='type', exclude=['name'],
              attrnames="name hair feathers eggs milk airborne aquatic " +
              "predator toothed backbone breathes venomous fins legs tail " +
              "domestic catsize type") 


iris = DataSet(name="iris", target="class",
               attrnames="sepal-len sepal-width petal-len petal-width class")

#______________________________________________________________________________
# The Restaurant example from Fig. 18.2

def RestaurantDataSet(examples=None):
    "Build a DataSet of Restaurant waiting examples."
    return DataSet(name='restaurant', target='Wait', examples=examples,
                  attrnames='Alternate Bar Fri/Sat Hungry Patrons Price '
                   + 'Raining Reservation Type WaitEstimate Wait')

restaurant = RestaurantDataSet()

def T(attrname, branches):
    return DecisionTree(restaurant.attrnum(attrname), attrname, branches)

Fig[18,2] = T('Patrons',
             {'None': 'No', 'Some': 'Yes', 'Full':
              T('WaitEstimate',
                {'>60': 'No', '0-10': 'Yes', 
                 '30-60':
                 T('Alternate', {'No':
                                 T('Reservation', {'Yes': 'Yes', 'No':
                                                   T('Bar', {'No':'No',
                                                             'Yes':'Yes'})}),
                                 'Yes':
                                 T('Fri/Sat', {'No': 'No', 'Yes': 'Yes'})}),
                 '10-30':
                 T('Hungry', {'No': 'Yes', 'Yes':
                           T('Alternate',
                             {'No': 'Yes', 'Yes':
                              T('Raining', {'No': 'No', 'Yes': 'Yes'})})})})})

def SyntheticRestaurant(n=20):
    "Generate a DataSet with n examples."
    def gen():
        example =  map(random.choice, restaurant.values)
        example[restaurant.target] = Fig[18,2].predict(example)
        return example
    return RestaurantDataSet([gen() for i in range(n)])

#______________________________________________________________________________
# Artificial, generated  examples.

def Majority(k, n):
    """Return a DataSet with n k-bit examples of the majority problem:
    k random bits followed by a 1 if more than half the bits are 1, else 0."""
    examples = []
    for i in range(n):
        bits = [random.choice([0, 1]) for i in range(k)]
        bits.append(sum(bits) > k/2)
        examples.append(bits)
    return DataSet(name="majority", examples=examples)

def Parity(k, n, name="parity"):
    """Return a DataSet with n k-bit examples of the parity problem:
    k random bits followed by a 1 if an odd number of bits are 1, else 0."""
    examples = []
    for i in range(n):
        bits = [random.choice([0, 1]) for i in range(k)]
        bits.append(sum(bits) % 2)
        examples.append(bits)
    return DataSet(name=name, examples=examples)

def Xor(n):
    """Return a DataSet with n examples of 2-input xor."""
    return Parity(2, n, name="xor")

def ContinuousXor(n):
    "2 inputs are chosen uniformly form (0.0 .. 2.0]; output is xor of ints."
    examples = []
    for i in range(n):
        x, y = [random.uniform(0.0, 2.0) for i in '12']
        examples.append([x, y, int(x) != int(y)])
    return DataSet(name="continuous xor", examples=examples)

    
