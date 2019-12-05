'''
@author: Shaikat Islam
@title: hw01_01
@professor: Martin Allen
@date: 25-09-2019
'''
from InputValidation import InputValidation
from Node import Node
from ProcessData import ProcessData
from DecisionTree import DecisionTree
import sys

if __name__ == "__main__":
    sys.setrecursionlimit(1500)
    inputs = InputValidation(0,0,"i")
    inputs.input()
    s_stats = ""
    interval = inputs.training_increment
    data = ProcessData([], [])
    data.process_file()
    data.get_n_random(data.raw_data, inputs.training_set_size)
    print()
    while(interval <= inputs.training_set_size):
        try:
            randomized_training_set = data.training_set[0:interval - 1]
            all_data = data.get_examples_without_training_set(data.training_set, data.raw_data)
            dtree = DecisionTree(None)
            entropy = dtree.calculate_total_entropy(all_data)
            tree = dtree.train(inputs.heuristic, entropy, randomized_training_set, randomized_training_set)
            stat_arr = []
            for entry in all_data:
                dtree.test(tree, entry, stat_arr)
            corr = 0
            wrong = 0
            for entry in stat_arr:
                if (entry == "c"):
                    corr+=1
                else:
                    wrong+=1
            stat = (corr/(corr+wrong))*100
            print()
            print("Given current tree, there are " + str(corr) + " correct classifications out of " + str(len(all_data)) + " possible (a success rate of " + "%.4f" % stat + " percent).")
            s_stats += "Training set size: " + str(interval) + ". " + "Success: " + "%.4f" % stat + " percent.\n"
            interval += inputs.training_increment
            if interval > inputs.training_set_size:
                pass
            else:
                print("Running with " + str(interval) + " examples in training set.")
        except RecursionError as re:
            pass
    print("\n-------------------\nFinal Decision Tree\n-------------------")
    print(tree)
    print("\n----------\nStatistics\n----------")
    print(s_stats)
