'''
@author: Shaikat Islam
@title: hw01_01
@professor: Martin Allen
@date: 25-09-2019
'''
import re
import math
from Node import Node

class DecisionTree:
    def __init__(self, decision_tree):
        self.decision_tree = decision_tree

    '''
    find_guess: returns the most frequent label within the training set
    inputs: training_set -> an array of arrays describing mushroom data
    output: 'Poisonous' or 'edible'
    '''
    def find_guess(self, training_set):
        dict = {}
        for entries in training_set:
            key = entries[22]
            if key in dict:
                dict[key] += 1
            else:
                dict[key] = 1
        p_count = 0
        e_count = 0
        if 'p' in dict:
            p_count = dict['p']
        if 'e' in dict:
            e_count = dict['e']
        if (p_count > e_count):
            return 'Poisonous'
        else:
            return 'Edible'

    '''
    most_important_feature_counting: returns an array containing a split point,
    the most important feature, the index of the most important feature, and
    two arrays: one containing the feature, and one without it (based on Daume's
    counting based algorithm)
    inputs: arr -> an array describing the training set
    output: ret -> an array containing a split point,
    the most important feature, the index of the most important feature, and
    two arrays: one containing the feature, and one without it
    '''
    def most_important_feature_counting(self, arr):
        # process data to figure feature with most extreme label percentages
        master_dict = {}
        for entries in arr:
            for i in range(len(entries) - 1):
                if i in master_dict:
                    if entries[i] in master_dict[i]:
                        if (entries[22] == 'p'):
                            master_dict[i][entries[i]][0]+=1
                            poisonous = master_dict[i][entries[i]][0]
                            edible = master_dict[i][entries[i]][1]
                            percent_edible = (edible/(edible + poisonous)) * 100
                            master_dict[i][entries[i]][2] = percent_edible
                        elif (entries[22] == 'e'):
                            master_dict[i][entries[i]][1]+=1
                            poisonous = master_dict[i][entries[i]][0]
                            edible = master_dict[i][entries[i]][1]
                            percent_edible = (edible/(edible + poisonous)) * 100
                            master_dict[i][entries[i]][2] = percent_edible
                    else:
                        master_dict[i][entries[i]] = [0,0,0.0]
                else:
                    master_dict[i] = {}
        # find split point
        max_percent_edible = float('-inf')
        feature_index = 0
        feature = ''
        new_training_set = []
        old_training_set = []
        ret = []
        for key in master_dict:
            for feature_label in master_dict[key]:
                if (master_dict[key][feature_label][2] > max_percent_edible):
                    max_percent_edible = master_dict[key][feature_label][2]
                    feature = feature_label
                    feature_index = key
        for j in range(len(arr)):
            if (arr[j][feature_index] == feature):
                new_training_set.append(arr[j])
            else:
                old_training_set.append(arr[j])
        # return split point
        ret.append(feature)
        ret.append(new_training_set)
        ret.append(old_training_set)
        ret.append(feature_index)
        return ret

    '''
    calculate_total_entropy: calculates total entropy of a dataset using the
    formula (P(Pos)*logbase2ofP(Pos) + P(Neg)*logbase2ofP(Neg))
    inputs: arr -> an array describing the training set
    output: entropy -> a float describing the entropy of the data set
    '''
    def calculate_total_entropy(self, arr):
        num_yes = 0
        num_no = 0
        num_total = 0
        for entries in arr:
            num_total += 1
            if entries[22] == 'p':
                num_no += 1
            else:
                num_yes += 1
        p_pos = num_yes/(num_no + num_yes)
        p_neg = num_no/(num_no + num_yes)
        entropy = 0
        if p_pos == 0 and p_neg == 0:
            entropy = 0
        elif p_pos == 0:
            entropy = -(0 + (p_neg * math.log(p_neg, 2)))
        elif p_neg == 0:
            entropy = -((p_pos * math.log(p_pos, 2)) + 0)
        else:
            entropy = -((p_pos * math.log(p_pos, 2)) + (p_neg * math.log(p_neg, 2)))
        return entropy

    '''
    most_important_feature_information: returns an array containing a split point,
    the most important feature, the index of the most important feature, and
    two arrays: one containing the feature, and one without it (based on an
    information theoretic based approach described in Lecture 3 of Prof. Marty
    Allen's
    inputs: arr -> an array describing the training set,
    entropy -> a float describing the entropy of the training set
    output: ret -> an array containing a split point,
    the most important feature, the index of the most important feature, and
    two arrays: one containing the feature, and one without it
    '''
    def most_important_feature_information(self, entropy, arr):
        # Process data to figure out raw components of Gain(x) - Remainder(x)
        m_dict = {}
        for entries in arr:
            for i in range(len(entries) - 1):
                if i in m_dict:
                    if entries[i] in m_dict[i]:
                        if (entries[22] == 'e'):
                            m_dict[i][entries[i]][0]+=1
                            m_dict[i][entries[i]][2]+=1
                            m_dict[i][entries[i]][3] = len(arr) + 1
                        elif (entries[22] == 'p'):
                            m_dict[i][entries[i]][1]+=1
                            m_dict[i][entries[i]][2]+=1
                            m_dict[i][entries[i]][3] = len(arr) + 1
                    else:
                        m_dict[i][entries[i]] = [0,0,0,0,0.0,0.0,0.0,0.0]
                else:
                    m_dict[i] = {}
        # Calculate Information Gain for Every Feature
        for key in m_dict:
            for feature_label in m_dict[key]:
                a_p = m_dict[key][feature_label][0]
                a_n = m_dict[key][feature_label][1]
                if (a_p == 0 and a_n == 0):
                    m_dict[key][feature_label][7] = 0
                    break
                a_pos = a_p/(a_p + a_n)
                a_neg = a_n/(a_p + a_n)
                m_dict[key][feature_label][4] = m_dict[key][feature_label][2]/m_dict[key][feature_label][3]
                if a_p == 0 and a_n == 0:
                    m_dict[key][feature_label][5] = 0
                elif a_p == 0:
                    m_dict[key][feature_label][5] = -(0 + (a_neg * math.log(a_neg, 2)))
                elif a_n == 0:
                    m_dict[key][feature_label][5] = -((a_pos * math.log(a_pos, 2)) + 0)
                else:
                    m_dict[key][feature_label][5] = -((a_pos * math.log(a_pos, 2)) + (a_neg * math.log(a_neg, 2)))
                m_dict[key][feature_label][6] = m_dict[key][feature_label][4] * m_dict[key][feature_label][5]
                m_dict[key][feature_label][7] = entropy - m_dict[key][feature_label][6]
        # Find Feature with Most Information Gain
        max_information_gain = float('-inf')
        feature = ""
        feature_index = 0
        new_training_set = []
        old_training_set = []
        ret = []
        for key in m_dict:
            for feature_label in m_dict[key]:
                if m_dict[key][feature_label][7] > max_information_gain:
                    max_information_gain = m_dict[key][feature_label][7]
                    feature = feature_label
                    feature_index = key
        for j in range(len(arr)):
            if (arr[j][feature_index] == feature):
                new_training_set.append(arr[j])
            else:
                old_training_set.append(arr[j])
        #Return Split Point
        ret.append(feature)
        ret.append(new_training_set)
        ret.append(old_training_set)
        ret.append(feature_index)
        return ret

    '''
    all_label_same: returns True if all the labels of a training set are the
    same; false otherwise
    inputs: arr -> an array describing the training set
    output: True or False
    '''
    def all_labels_same(self, arr):
        label_set = set()
        for entries in arr:
            label_set.add(entries[22])
        if len(label_set) > 1:
            return False
        else:
            return True

    '''
    remove_feature_from_remaining: removes all instances of the most important
    feature from a training set
    inputs: feature -> a string describing the feature,
    index -> the position of the feature in an instance of a feature set
    remaining -> array describing the training set
    output: remaining -> the array without the feature
    '''
    def remove_feature_from_remaining(self, feature, index, remaining):
        remaining_set = []
        old_set = []
        for entries in remaining:
            if (entries[index] == feature):
                old_set.append(entries)
            else:
                remaining_set.append(entries)
        return remaining_set

    '''
    feature_at_index: returns True if feature exists at index; false otherwise
    inputs: feature -> a string describing the feature,
    index -> the position of the feature in an instance of a feature set
    test_point -> the array describing the feature set
    output: True or False
    '''
    def feature_at_index(self, feature, index, test_point):
        s_feature = "''" + feature + "''"
        if(test_point[index] == feature):
            return True
        else:
            return False

    '''
    train: Trains the decision tree based on an information theoretic or
    counting based heuristic
    inputs: heuristic -> a string describing the heuristic to be used
    entropy_input -> a float describing the entropy of the training set
    data -> all of the training data
    remaining_features -> the set of feature_sets that remain
    output: Node -> a decision tree containing the split points and attributes
    describing the training set
    '''
    def train(self, heuristic, entropy_input, data, remaining_features):
        guess = self.find_guess(data)
        # base case 1 and 2
        if self.all_labels_same(data) or len(remaining_features) == 0:
            leaf = Node()
            leaf.data = guess
            return leaf
        else:
            # heuristic choice
            if (heuristic == "c"):
                MIF_result = self.most_important_feature_counting(remaining_features)
            elif (heuristic == "i"):
                entropy = entropy_input
                MIF_result = self.most_important_feature_information(entropy, remaining_features)
            # split point arrays
            MIF_feature = MIF_result[0]
            MIF_yes = MIF_result[2]
            MIF_no = MIF_result[1]
            MIF_index = MIF_result[3]
            # remove split point feature from remaining features
            remaining_features_without_f = self.remove_feature_from_remaining(MIF_feature, MIF_index, remaining_features)
            # recurse on left subtree
            subtree_left = self.train(heuristic, entropy_input, MIF_no, remaining_features_without_f)
            # recurse on right subtree
            subtree_right = self.train(heuristic, entropy_input, MIF_yes, remaining_features_without_f)
            node = Node()
            node.data = ("Attrib #" + str(MIF_index + 1) + ": " + MIF_feature)
            node.feature_index = MIF_index
            node.feature_name = MIF_feature
            # create tree
            node.left = subtree_left
            node.right = subtree_right
            return node

    '''
    test: Tests the decision tree on a test point
    inputs: tree -> a Node object (the decision tree)
    test_point -> the feature set to be tested
    arr -> a result array to be written to in case of correctness or invalidity
    output: None
    '''
    def test(self, tree, test_point, arr):
        # check if its a leaf
        if tree.is_leaf():
            # append to statistic array if right, else wrong
            if (tree.data[:1].lower() == test_point[22]):
                arr.append("c")
            else:
                arr.append("w")
        else:
            # traverse parent nodes
            if self.feature_at_index(tree.feature_name, tree.feature_index, test_point):
                self.test(tree.left, test_point, arr)
            else:
                self.test(tree.right, test_point, arr)
