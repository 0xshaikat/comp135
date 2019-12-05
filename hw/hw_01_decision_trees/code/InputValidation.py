#Shaikat Islam
class InputValidation:
    def __init__(self, training_set_size, training_increment, heuristic):
        self.training_set_size = training_set_size
        self.training_increment = training_increment
        self.heuristic = heuristic

    '''
    validate_set_size: validates the training set size input
    inputs: input_string_1 -> Part one of string to be presented to user
    input_string_2 -> Part two of string to be presented to user
    output: stdout
    '''
    def validate_set_size(self, input_string_1, input_string_2):
        s_invalid_1 = "Please input a number n, such that n is divisible by 250, "
        s_invalid_2 = "greater than 0, and less than or equal to 1000: "
        while True:
            try:
                self.training_set_size = int(input(input_string_1 + input_string_2))
            except ValueError:
                print("Training set size must be an integer.")
                continue
            cond_1 = not type(self.training_set_size) == int
            cond_2 = self.training_set_size < 250
            cond_3 = self.training_set_size > 1000
            cond_4 = not (self.training_set_size % 250 == 0)
            if cond_1 or cond_2 or cond_3 or cond_4:
                print(s_invalid_1 + s_invalid_2)
                continue
            else:
                break

    '''
    validate_training_increment: validates the training increment input
    inputs: input_string_1 -> Part one of string to be presented to user
    input_string_2 -> Part two of string to be presented to user
    output: stdout
    '''
    def validate_training_increment(self, input_string_1, input_string_2):
        s_invalid_1 = "Please input 10, 25, or 50: "
        while True:
            try:
                self.training_increment = int(input(input_string_1 + input_string_2))
            except ValueError:
                print("Training increment must be an integer.")
                continue
            cond_1 = not (self.training_increment == 10 or self.training_increment == 25 or self.training_increment == 50)
            if cond_1:
                print(s_invalid_1)
                continue
            else:
                break

    '''
    validate_heuristic: validates the heuristic input
    inputs: input_string_1 -> Part one of string to be presented to user
    input_string_2 -> Part two of string to be presented to user
    output: stdout
    '''
    def validate_heuristic(self, input_string_1, input_string_2):
        s_invalid_1 = "Please input 'c' for a counting-based heuristic or "
        s_invalid_2 = "'i' for an information theoretic heuristic: "
        while True:
            try:
                self.heuristic = str(input(input_string_1 + input_string_2))
            except ValueError:
                print("You must input either 'c' or 'i'.")
                continue
            cond_1 = not (self.heuristic.lower() == 'c' or self.heuristic.lower() == 'i' )
            if cond_1:
                print(s_invalid_1 + s_invalid_2)
                continue
            else:
                break

    '''
    validate_training_increment: Runs input validation process
    inputs: None
    output: stdout
    '''
    def input(self):
        s_set_size_1 = "Please enter a training set size "
        s_set_size_2 = "(a positive multiple of 250 that is <= 1000): "
        s_training_increment_1 = "Please enter a training increment "
        s_training_increment_2 = "(either 10, 25, or 50): "
        s_heuristic_1 = "Please enter a heuristic to use "
        s_heuristic_2 = "(either [C]ounting-based or [I]nformation theoretic): "
        self.validate_set_size(s_set_size_1, s_set_size_2)
        self.validate_training_increment(s_training_increment_1, s_training_increment_2)
        self.validate_heuristic(s_heuristic_1, s_heuristic_2)
        print()
