import re  # regex lib
from token import *


class Tokenizer:

    def __init__(self, input):
        # private attributes

        self.__input = input
        self.__digit_regex = "[0-9]+"  # to do signed
        self.__identif_regex = "[a-zA-Z]+([a-zA-Z]|[0-9])*|([a-zA-Z]|[0-9])*"
        # self.__exp_regex = self.__identif_regex ------>> not working
        self.__symbols_list = ['+', '-', '*', '/', '=', '<', '>', '(', ')', ';', ':=']
        self.__keywords_list = []
        self.__tokens_list = []
        #self.__identif_list = []
        #self.digit_list = []

    def split_to_lines(self, input):
        lines = input.split("\n")
        return lines

    def split_on_spaces(self, lines):  # lines is a list
        words = lines.split(" ")
        return words

    def is_id(self, word):
        match_object = re.match(self.__identif_regex, word)
        start, length = match_object.span()
        if start == 0 and length == len(word):
            return True
        else:
            return False

    def is_digit(self, word):
        match_object = re.match(self.__digit_regex, word)
        begin ,  length = match_object.span()
        if begin == 0 and length == len(word):
            return True
        else:
            return False

#  WRITE READ IF ELSE RETURN BEGIN END MAIN STRING INT REAL
    def is_keyword(self, word):
        if word == "write" or word == "read" or word == "if" or word == "else" or word == "return" or word == "begin" or word == "end" or word == "main" or word == "string" or word == "int":
            return True
        else:
            return False

    def is_exp(self, word):  # to be postponed (state machine, regex is not working)
        pass

    def check_word(self, word):
        if (not(self.is_keyword())) and (not(self.is_digit())) and (not(self.is_id())) and \
                (not(word in self.__symbols_list)):
            return False

    def tokenize_exp(self, exp):  # to be postponed
        pass

    def classify(self, token):
        if not(self.check_word(token)):
            return "error" # will be modified to generate error message
        elif self.is_keyword(token):
            token_obj = Token(token, 'keyword')
            self.__tokens_list.append(token_obj)
        elif self.is_id(token):
            token_obj = Token(token, 'identifier')
            self.__tokens_list.append(token_obj)
        elif self.is_digit(token):
            token_obj = Token(token, 'digit')
            self.__tokens_list.append(token_obj)

        
   



'''
+ 
then - 
else *
end /
repeat = identifier
until < (1 or more letters)
read (
write )
;
:=


'''






## reg1 = '(\+)|(-)|(\*)|(/)|(=)|(<)|(>)|(\()|(;)|(:=)|(\))'
