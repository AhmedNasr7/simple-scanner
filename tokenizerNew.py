import re  # regex lib
from PyQt5.QtCore import QThread, QObject, pyqtSlot, pyqtSignal
from token_module import *



class Tokenizer(QObject):

    pass_data_signal = pyqtSignal(list)
    error_signal = pyqtSignal(str)


    def __init__(self, input):


        super().__init__()
        # private attributes

        self.__input = input
        self.__digit_regex = "[0-9]+"  # to do signed

        #self.__identif_regex = r"^[^\d\W]\w*\Z"
        self.__identif_regex = "[a-zA-Z]+"
        # self.__exp_regex = self.__identif_regex ------>> not working
        self.__symbols_list = ['+', '-', '*', '/', '=', '<', '>', '(', ')', ';', ':=']
        #self.__keywords_list = []
        self.__tokens_list = []

        self.__comment_flag = False

   


    def filter_comments(self, input):
        start = -1
        end = -1
        for i in range(len(input)):

            if input[i] == '{':
                start = i
            if start > -1 and input[i] == '}':
                end = i
            if start > -1 and end > -1:
                new_input = input[0:start] + input[end + 1:]
                return new_input
            
        return input
                
                
            
                
        

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
        if word == "write" or word == "read" or word == "if" or word == "else" or word == "return" or word == "repeat" or word == "begin" or word == "end" or word == "main" or word == "string" or word == "then" or word == "int" or word == "until":
            return True
        else:
            return False

    def is_exp(self, word):  # to be postponed (state machine, regex is not working)
        if (not(self.is_keyword(word))) and (not(self.is_digit(word))) and (not(self.is_id(word))) and \
                (not(word in self.__symbols_list)):
                if len(word) > 1:
                    count = 0
                    for s in self.__symbols_list:
                        if word.count(s) > 0:
                            count += 1
                    
                    if count > 0:
                        return True
                    else:
                        return False
                else:
                    return False


    def check_word(self, word):
        if (not(self.is_keyword(word))) and (not(self.is_digit(word))) and (not(self.is_id(word))) and \
                (not(word in self.__symbols_list)) and not (self.is_exp(word)):
            return False
        else:
            return True
        

    def tokenize_exp(self, exp):  # to be postponed
        s = exp
        done = False
        try:
            while(len(s) > 0 and not done): # suspected
                for i in range(len(s)):
                    if s[i] == ":" and i != (len(s) - 1) and not self.__comment_flag:
                        if s[i+1] == '=':
                            symb_found = True
                            symbol = ":="
                            sub = s[0:i]
                            self.classify(sub)
                            token_obj = Token_(symbol, 'special symbol')
                            self.__tokens_list.append(token_obj)
                            #i += 2
                            s = s[i + 2:]
                            break

                        else:
                            if exp.count('{') > 0 or exp.count('}') > 0:
                                pass
                            else:
                                self.generate_erorr('Error! illegal identifier') 
                            # break        
                    elif s[i] in self.__symbols_list and not self.__comment_flag:
                        sub = s[0:i]
                        self.classify(sub) # classify not symbol  
                        symbol = s[i]
                        token_obj = Token_(symbol, 'special symbol')
                        self.__tokens_list.append(token_obj)
                        s = s[i + 1:]
                        break
                    elif s[i] == "{":
                        self.__comment_flag = True
                        continue
                    elif s[i] == "}" and self.__comment_flag:
                        self.__comment_flag = False
                        continue
                    else:
                        continue
                else:
                    for symb in self.__symbols_list:
                        if symb in s:
                            print("error")
                        else:
                            self.classify(s)
                            s = ""
                            done = True
                            
                
                   
        except Exception as e:
            print(e.__str__)
                    

    def classify(self, token):
        if not(self.check_word(token)):
            #print('error----->', token) # will be modified to generate error message
            if token == "":
                return
            if token.count('{') > 0 or token.count('}') > 0:
                pass
            else:
                self.generate_erorr("Error! '" + token + "' is a wrong token!")
            #token_obj = Token_(token, 'wrong-token')
            #self.__tokens_list.append(token_obj)

        elif self.is_keyword(token):
            if token == 'if' or token == 'IF':
                token_obj = Token_(token, 'IF Token')
                self.__tokens_list.append(token_obj)
            elif token == 'else' or token == "ELSE":
                token_obj = Token_(token, 'ELSE Token')
                self.__tokens_list.append(token_obj)
            else:
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
                self.generate_erorr('Error: the token is unkown')
                #token_obj = Token_(token, 'unknown-token')
                #self.__tokens_list.append(token_obj)



    def tokenize(self):
        filterd_input = self.filter_comments(self.__input)
        lines = self.split_to_lines(filterd_input) # list of lines
        lines_list = self.split_on_spaces(lines) # list of lists of words

        for line_words in lines_list: # a line_words is a list of words
            for word in line_words:
                if word == "{":
                    self.__comment_flag = True
                    continue
                elif word == "}" and self.__comment_flag:
                    self.__comment_flag = False
                    continue
                elif self.__comment_flag:
                    continue
                else:
                    self.classify(word)

           
        #printing tokens values and types --> will be replaced by generating it in GUI 
        #for token in self.__tokens_list:
            #print(token.value(), token.type())

        self.send_data()

        

    def send_data(self):

        try:
            self.pass_data_signal.emit(self.__tokens_list)
        except Exception as e:
            pass

    
    def generate_erorr(self, error_msg):
        self.error_signal.emit(error_msg)
        self.pass_data_signal = None


        
   







## reg1 = '(\+)|(-)|(\*)|(/)|(=)|(<)|(>)|(\()|(;)|(:=)|(\))'
