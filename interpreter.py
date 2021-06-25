import sys
 
LOAD = ";"
PRINT = "."
BEGIN_LOOP = "{"
END_LOOP = "}"
BEGIN_IF = "["
BEGIN_VAR = "<"
END_VAR = ">"
END_IF = "]"
TOP = "^"
INFINITE="~"
EQUAL = "="
ADD = "+"
SUB = "-"
MUL = "*"
DIV = "/"
INT_INP = "#"
INP = ":"
REM = ","
LOAD_VAR = "("

# String manipulation functions

def number_from_index(i,string):
    number = ""
    j = i+1
    try:
        while string[j].isdigit():
            number += string[j]
            j+=1
    except:
        pass

    return number

def extract_until_char(j,char,string):
    res = ""
    while string[j] != char:
        res += string[j]
        j+=1
    return res

# Tokens to represent operations and functions

class Token:
    def __init__(self,op):
        self.op = op

    def print_token(self):
        print(self.op)


class OpToken:
    def __init__(self,number,op):
        self.number = number
        self.op = op

    def print_token(self):
        print(self.op, self.number)


class VarToken:
    def __init__(self, name,op):
        self.op = op
        self.name = name

    def print_token(self):
        print(self.op)


class EqualToken:
    def __init__(self,before,after):
        self.before = before
        self.after = after
        self.op = "EQUAL"

    def print_token(self):
        print(self.before[0].op,self.op,self.after[0].op)


class ControlFlowToken:
    def __init__(self,parameters,code,op):
        self.parameters = parameters
        self.code = code
        self.op = op

    def print_token(self):
        print("Repeat",self.code,self.parameters,"times")


class InpToken():
    def __init__(self,op):
        self.op = op

    def int_inp(self):
        str_inp = ""
        while True:
            try:
                str_inp = input(":")
                inp = int(str_inp)
                break
            except:
                inp = ord(str_inp)
                break
                
        return inp
        


class Interpreter:
    def __init__(self, file):
        self.file = file
        self.stack = []
        self.variables = {}

    def run(self):
        formatted = self.format_file(self.file)
        tokenised = self.parse(formatted)
        self.interpret(tokenised)
        print(self.stack)


    # format the file 
    # - remove comments
    # - remove spaces
    # - remove new lines

    def format_file(self,file):
        stripped_file = ""
        with open(file,"r") as f: 
            for line in f:
                line = line.replace("\n","")
                for character in line:
                    if character == "@":
                        break
                    elif character != " ":
                        stripped_file += character

        return stripped_file

    # parse single character

    def single_parse(self,code):
        if code == TOP:
            top_token = Token("TOP")
            return top_token
        
        if code.isdigit():
            number = int(code)
            num_token = OpToken(number,"NUM")
            return num_token
            
            

    # parse boolean condition
    def parse_condition(self, condition):
        tokens = []
        for i, char in enumerate(condition):
            if char == EQUAL:
                before = condition[:i]
                after = condition[i+1:]
                before_tok = self.single_parse(before)
                after_tok = self.single_parse(after)
                equal_tok = EqualToken([before_tok],[after_tok])

                return equal_tok

        return tokens


    def parse(self, formatted_file):
        tokens = []
        i = 0
        while i < len(formatted_file):
            character = formatted_file[i]


            if character == BEGIN_VAR:
                name = extract_until_char(i+1,">",formatted_file)
                i += len(name) + 1
                var_token = VarToken(name,"VAR")
                tokens.append(var_token)


            if character == BEGIN_LOOP:
                repeat = extract_until_char(i+1,"\\",formatted_file)
                code = extract_until_char(i+len(repeat)+2,"}",formatted_file)
                code_tokenised = self.parse(code)
                
                if repeat == TOP:
                    token = Token("TOP")
                elif repeat == INFINITE:
                    token = Token("INFINITE")
                else:
                    token = OpToken(int(repeat),"NUM")

                loop_token = ControlFlowToken(token,code_tokenised,"LOOP")
                tokens.append(loop_token)
                i += len(repeat) + 2 + len(code) + 1


            if character == BEGIN_IF:
                condition = extract_until_char(i+1,"\\",formatted_file)
                code = extract_until_char(i+len(condition)+2,"]",formatted_file)
                code_tokenised = self.parse(code)
                condition_tokenised = self.parse_condition(condition) 
                if_tok = ControlFlowToken(condition_tokenised,code_tokenised,"IF")
                tokens.append(if_tok)
                i += len(condition) + 2 + len(code) 


            if character == LOAD:
                number = number_from_index(i,formatted_file)                    
                i += len(number)
                load_token = OpToken(int(number),"LOAD")
                tokens.append(load_token)


            if character in (ADD,SUB,DIV,MUL):
                number = number_from_index(i,formatted_file)
                number = "1" if number == "" else number

                token = OpToken(int(number),"NUM")
                if formatted_file[i+1] == "(":
                    name = extract_until_char(i+2,")",formatted_file) 
                    token = VarToken(name,"LOAD_VAR")
                    i += len(name) + 1
                else:
                    i += len(number)

                if character == ADD: token = OpToken(token,"ADD")
                if character == SUB: token = OpToken(token,"SUB")
                if character == MUL: token = OpToken(token,"MUL")
                if character == DIV: token = OpToken(token,"DIV")
                tokens.append(token)


            if character == PRINT:
                print_token = Token("PRINT")
                tokens.append(print_token)


            if character == INP:
                inp_token = InpToken("INP")
                tokens.append(inp_token)


            if character == INT_INP:
                inp_token = InpToken("INT_INP")
                tokens.append(inp_token)

            
            if character == REM:
                rem_token = Token("REM")
                tokens.append(rem_token)


            if character == LOAD_VAR:
                name = extract_until_char(i+1,")",formatted_file)
                var_token = VarToken(name,"LOAD_VAR")
                tokens.append(var_token)
                i+= len(name) + 1

            i += 1
        return tokens

    # interpret the tokens and return a result
    # used in parsing and interpreting conditions
    def interpret_results(self,tokens):
        result = 0
        stack = []
        for token in tokens:

            if token.op == "LOAD":
                stack.append(token.number)

            if token.op == "ADD":
                result = self.stack[-1] + token.number
                stack.append(result)

            if token.op == "SUB":
                result = self.stack[-1] - token.number
                stack.append(result)

            if token.op == "MUL":
                result = self.stack[-1] * token.number
                stack.append(result)

            if token.op == "DIV":
                result = self.stack[-1] / token.number
                stack.append(result)

            if token.op == "PRINT":
                print(self.stack[-1])

            if token.op == "INP":
                stack.append(input(":"))

            if token.op == "INT_INP":
                stack.append(token.int_inp())

            if token.op == "TOP":
                stack.append(self.stack[-1])

            if token.op == "NUM":
                stack.append(token.number)


        return stack[-1]

        
        

    # parse individual token
    def interpret_token(self,token):

        if token.op == "VAR":
            self.variables[token.name] = self.stack[-1]

        if token.op == "LOAD_VAR":
            self.stack.append(self.variables[token.name])

        if token.op == "LOAD":
            self.stack.append(token.number)


        if token.op == "ADD":
            if token.number.op == "NUM":
                result = self.stack[-1] + token.number.number
            else: 
                result = self.stack[-1] + self.variables[token.number.name]
            self.stack.append(result)


        if token.op == "DIV":
            if token.number.op == "NUM":
                result = self.stack[-1] / token.number.number
            else: 
                result = self.stack[-1] / self.variables[token.number.name]
            self.stack.append(result)


        if token.op == "MUL":
            if token.number.op == "NUM":
                result = self.stack[-1] * token.number.number
            else: 
                result = self.stack[-1] * self.variables[token.number.name]
            self.stack.append(result)


        if token.op == "SUB":
            if token.number.op == "NUM":
                result = self.stack[-1] - token.number.number
            else: 
                result = self.stack[-1] - self.variables[token.number.name]
            self.stack.append(result)


        if token.op == "PRINT":
            print(self.stack[-1])


        if token.op == "INP":
            self.stack.append(input(":"))


        if token.op == "INT_INP":
            self.stack.append(token.int_inp())


        if token.op == "REM":
            self.stack.pop()


        if token.op == "LOOP":
            
            if token.parameters.op == "INFINITE":
                while True:
                    self.interpret(token.code)

                    
            if token.parameters.op == "NUM":
                val = token.parameters.number


            if token.parameters.op == "TOP":
                val = self.stack[-1]


            for i in range(val):
                self.interpret(token.code)


        if token.op == "IF":
            before_res = self.interpret_results(token.parameters.before)
            after_res = self.interpret_results(token.parameters.after)

            if before_res == after_res:
                self.interpret(token.code)


    def interpret(self, tokens):
        for token in tokens:
            self.interpret_token(token)

file_name = sys.argv[1]
interpreter = Interpreter(file_name)
interpreter.run()
