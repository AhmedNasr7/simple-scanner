import re # regex lib




class Tokenizer():


    def __init__(self, input):
        ## private attributes
        self.__input = input
        self.__digit_regex = "[0-9]+" # to do signed 
        self.__identif_regex = "[a-zA-Z]+([a-zA-Z]|[0-9])*|([a-zA-Z]|[0-9])*"
        self.__exp_regex = "" # to do 
        self.__symbols_list = [] # to do 


    def split_to_lines(self, input):
        pass

    def split_on_spaces(self, lines): #lines is a list
        pass

    def is_id(self, word):
        match_object = re.match(self.__identif_regex)
        start, length = match_object.span()
        if start == 0 and length == len(word):
            return True
        else:
            return False

    def is_digit(self, word):
        pass

    def is_keyword(self, word):
        pass

    def is_exp(self, word):
        pass

    def check_word(self, word):
        pass

    def tokenize_exp(self, exp):
        pass

    def classify(self, token):
        pass

   

