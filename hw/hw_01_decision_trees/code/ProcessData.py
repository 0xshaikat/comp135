'''
@author: Shaikat Islam
@title: hw01_01
@professor: Martin Allen
@date: 25-09-2019
'''
import os.path
import random
from os import path

'''
ProcessData: parses mushroom_data.txt into an array of arrays to be used in
other classes
'''
class ProcessData:
    def __init__(self, raw_data, training_set):
        self.raw_data = raw_data
        self.training_set = training_set

    '''
    process_file: opens mushroom_data.txt for reading and writes data to
    self.raw_data, an array
    inputs: None
    output: stdout
    '''
    def process_file(self):
        print("Loading Property Information from file.")
        print("Loading Data from database.")
        print()
        all_lines = []
        try:
            with open(os.path.dirname(__file__) + "/../input_files/mushroom_data.txt") as textfile: #TODO: put this file in a separate directory
                all_lines = [line.split() for line in textfile]
                self.raw_data = all_lines
        except IOError:
            print("File not found! Try again.")
        self.raw_data = all_lines

    '''
    get_n_random: gets 'size' random training examples from arr
    inputs: arr -> an array describing the training set
    size -> an integer describing the size of the array to be randomized
    output: stdout
    '''
    def get_n_random(self, arr, size):
        random.shuffle(arr)
        print("Collecting set of " + str(size) + " training examples.")
        randomized_training_set = arr[0:size]
        self.training_set = randomized_training_set

    '''
    get_examples_without_training_set: removes training set from all of the data
    inputs: training_set -> array describing the training set
    all_data -> array describing all the data from mushroom_data.txt
    output: all_data -> array describing all the data from mushroom_data.txt
    without the training_set
    '''
    def get_examples_without_training_set(self, training_set, all_data):
        for entry in training_set:
            if entry in all_data:
                all_data.remove(entry)
        return all_data
