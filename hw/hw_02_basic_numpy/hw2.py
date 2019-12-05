'''
hw2.py
Author: Shaikat Islam

Tufts COMP 135 Intro ML

'''

import numpy as np
import math
def split_into_train_and_test(x_all_LF, frac_test=0.5, random_state=None):
    ''' Divide provided array into train and test set along first dimension

    User can provide a random number generator object to ensure reproducibility.

    Args
    ----
    x_all_LF : 2D array, shape = (n_total_examples, n_features) (L, F)
        Each row is a feature vector
    frac_test : float, fraction between 0 and 1
        Indicates fraction of all L examples to allocate to the "test" set
    random_state : np.random.RandomState instance or integer or None
        If int, code will create RandomState instance with provided value as seed
        If None, defaults to the current numpy random number generator np.random

    Returns
    -------
    x_train_MF : 2D array, shape = (n_train_examples, n_features) (M, F)
        Each row is a feature vector
        Should be a separately allocated array, NOT a view of any input array

    x_test_NF : 2D array, shape = (n_test_examples, n_features) (N, F)
        Each row is a feature vector
        Should be a separately allocated array, NOT a view of any input array

    Post Condition
    --------------
    This function should be side-effect free. The provided input array x_all_LF
    should not change at all (not be shuffled, etc.)

    Examples
    --------
    >>> x_LF = np.eye(10)
    >>> xcopy_LF = x_LF.copy() # preserve what input was before the call
    >>> train_MF, test_NF = split_into_train_and_test(
    ...     x_LF, frac_test=0.3, random_state=np.random.RandomState(0))
    >>> train_MF.shape
    (7, 10)
    >>> test_NF.shape
    (3, 10)
    >>> print(train_MF)
    [[0. 0. 1. 0. 0. 0. 0. 0. 0. 0.]
     [0. 0. 0. 0. 0. 0. 0. 0. 1. 0.]
     [0. 0. 0. 0. 1. 0. 0. 0. 0. 0.]
     [0. 0. 0. 0. 0. 0. 0. 0. 0. 1.]
     [0. 1. 0. 0. 0. 0. 0. 0. 0. 0.]
     [0. 0. 0. 0. 0. 0. 1. 0. 0. 0.]
     [0. 0. 0. 0. 0. 0. 0. 1. 0. 0.]]
    >>> print(test_NF)
    [[0. 0. 0. 1. 0. 0. 0. 0. 0. 0.]
     [1. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
     [0. 0. 0. 0. 0. 1. 0. 0. 0. 0.]]

    ## Verify that input array did not change due to function call
    >>> np.allclose(x_LF, xcopy_LF)
    True

    References
    ----------
    For more about RandomState, see:
    https://stackoverflow.com/questions/28064634/random-state-pseudo-random-numberin-scikit-learn
    '''
    if random_state is None:
        random_state = np.random
    # get size of input array
    size = len(x_all_LF)
    # round size of test array up using math.ceil
    test_size = int(math.ceil(size * frac_test))
    # get a copy of the input array to use the shuffle method on
    x_all_LF_copy = x_all_LF.copy()
    # shuffle the array using the random_state class, or np.random based on the input
    random_state.shuffle(x_all_LF_copy)
    # create distinct arrays in memory for the test and training set
    x_test_NF_img = x_all_LF_copy[0:test_size]
    x_train_MF_img = x_all_LF_copy[test_size:]
    x_test_NF = x_test_NF_img.copy()
    x_train_MF = x_train_MF_img.copy()
    return np.array(x_train_MF), np.array(x_test_NF)


def calc_euclidean_distance(vector_1, vector_2):
    ''' Compute and return  Euclidean distance between two vectors

    Args
    ----
    vector_1 : 1D array, shape = (n_features)
    vector_2 : 1D array, shape = (n_features)

    Returns
    -------
    euclid_distance : euclidean distance between vector_1 and vector_2
    '''
    sum = 0
    difference = 0
    difference_squared = 0
    for i in range(len(vector_1)):
        difference = vector_1[i] - vector_2[i]
        difference_squared = difference * difference
        sum += difference_squared
    sum_sqrt = math.sqrt(sum)
    return sum_sqrt

def calc_k_nearest_neighbors(data_NF, query_QF, K=1):
    ''' Compute and return k-nearest neighbors under Euclidean distance

    Any ties in distance may be broken arbitrarily.

    Args
    ----
    data_NF : 2D array, shape = (n_examples, n_features) aka (N, F)
        Each row is a feature vector for one example in dataset
    query_QF : 2D array, shape = (n_queries, n_features) aka (Q, F)
        Each row is a feature vector whose neighbors we want to find
    K : int, positive (must be >= 1)
        Number of neighbors to find per query vector

    Returns
    -------
    neighb_QKF : 3D array, (n_queries, n_neighbors, n_feats) (Q, K, F)
        Entry q,k is feature vector of the k-th neighbor of the q-th query
    '''
    # array to return
    neighb_QKF = []
    # dictionary to store k closest neighbors indexed by query_QF
    dict = {}
    # iterate through query array
    for i in range(len(query_QF)):
        k_closest = []
        # iterate through data array
        for j in range(len(data_NF)):
            # calculcate euclidean distance between two vectors
            # append value to k_closest array along with data_NF[j]
            # into k_closest arr, which is added to the dictionary to be stored
            # by index
            euclid_distance_arr = []
            euclid_distance_arr.append(data_NF[j])
            euclid_distance_arr.append(calc_euclidean_distance(query_QF[i], data_NF[j]))
            k_closest.append(euclid_distance_arr)
        dict[i] = k_closest
    # sort the dictionary entries by euclidean distance
    for i in range(len(dict)):
        dict[i].sort(key = lambda x:x[1])
    # parse dictionary and add entries to neighb_QKF
    for i in range(len(dict)):
        k_closest_neighbors = []
        for element in dict[i]:
            k_closest_neighbors.append(element[0])
        neighb_QKF.append(k_closest_neighbors)
    return numpy.array(neighb_QKF)
