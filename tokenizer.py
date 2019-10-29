import re  # regex lib
from PyQt5.QtCore import QThread, QObject, pyqtSlot, pyqtSignal
from token_module import *



class Tokenizer(QObject):

    pass_data_signal = pyqtSignal(list)

    def __init__(self, input):


        super().__init__()
        # private attributes

        self.__input = input
        self.__digit_regex = "[0-9]+"  # to do signed

        self.__identif_regex = r"^[^\d\W]\w*\Z"
        # self.__exp_regex = self.__identif_regex ------>> not working
        self.__symbols_list = ['+', '-', '*', '/', '=', '<', '>', '(', ')', ';', ':=']
        self.__keywords_list = []
        self.__tokens_list = []
   

        

    def split_to_lines(self, input):
        lines = input.split("\n")
        return lines

    def split_on_spaces(self, lines):  # lines is a list
        lines_list = []
        for line in lines:
            line_words = line.split(' ') # list
            lines_list.append(line_words) # append to list of lists
        
        return lines_list # list of lists

    def is_id(self, word):
        try:
            match_object = re.match(self.__identif_regex, word)
            start, length = match_object.span()
        except:
            if match_object == None:
                return False
        if start == 0 and length == len(word):
            return True
        else:
            return False

    def is_digit(self, word):
        try:
            match_object = re.match(self.__digit_regex, word)
            begin, length = match_object.span()
        except:
            if match_object == None:
                return False     
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
        if (not(self.is_keyword(word))) and (not(self.is_digit(word))) and (not(self.is_id(word))) and \
                (not(word in self.__symbols_list)):
                if len(word) > 1:
                    return True
                else:
                    return False


    def check_word(self, word): 
        return self.is_exp(word)
        

    def tokenize_exp(self, exp):  # to be postponed
        s = exp
        symb_found = False
        while(len(s) > 1):
            for i in range(len(s)):
                if s[i] == ":" and i != (len(s) - 1):      
                    if s[i+1] == '=':
                        symb_found = True
                        symbol = ":="
                        sub = s[0:i - 1]
                        self.classify(sub)
                        token_obj = Token_(symbol, 'special symbol')
                        self.__tokens_list.append(token_obj)
                        i += 2
                    else:
                        self.generate_erorr() 
                        # break        
                elif s[i] in self.__symbols_list:
                    symb_found = True
                    sub = s[0:i-1]
                    self.classify(sub) # classify not symbol   
                    symbol = s[i]
                    token_obj = Token_(symbol, 'special symbol')
                    self.__tokens_list.append(token_obj)
                else:
                    pass
            
                if symb_found:
                    s = s[i:]
                    break
                
                
    

        
        

    def classify(self, token):
        if not(self.check_word(token)):
            #print('error----->', token) # will be modified to generate error message
            token_obj = Token_(token, 'wrong-token')
            self.__tokens_list.append(token_obj)

        elif self.is_keyword(token):
            token_obj = Token_(token, 'keyword')
            self.__tokens_list.append(token_obj)
        elif self.is_id(token):
            token_obj = Token_(token, 'identifier')
            self.__tokens_list.append(token_obj)
        elif self.is_digit(token):
            token_obj = Token_(token, 'number')
            self.__tokens_list.append(token_obj)
        elif token in self.__symbols_list:
            token_obj = Token_(token, 'special symbol')
            self.__tokens_list.append(token_obj)
        else:
            if (self.is_exp(token)):
                self.tokenize_exp(token)

            elif token == "\t" or token == "\n" or token == "\r" or token == " ":
                pass
            else:
                token_obj = Token_(token, 'unknown-token')
                self.__tokens_list.append(token_obj)



    def tokenize(self):
        lines = self.split_to_lines(self.__input) # list of lines
        lines_list = self.split_on_spaces(lines) # list of lists of words

        for line_words in lines_list: # a line_words is a list of words
            for word in line_words:
                self.classify(word)

           
        #printing tokens values and types --> will be replaced by generating it in GUI 
        #for token in self.__tokens_list:
            #print(token.value(), token.type())

        self.send_data()

        

    def send_data(self):
        self.pass_data_signal.emit(self.__tokens_list)

    
    def generate_erorr(self):
        pass 


        
   







## reg1 = '(\+)|(-)|(\*)|(/)|(=)|(<)|(>)|(\()|(;)|(:=)|(\))'
