"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import JackTokenizer
from NAND11.SymbolTable import SymbolTable

NON_VALID_TYPE = ['class', 'constructor', 'function', 'method', 'field',
           'static', 'var','true',
           'false', 'null', 'this', 'let', 'do', 'if', 'else',
           'while', 'return','{', '}', '(', ')', '[', ']', '.', ',', ';', '+',
           '-', '*', '/', '&', ',', '<', '>', '=', '~', '^', '#','0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

NON_VALID_NAME = ['class', 'constructor', 'function', 'method', 'field',
           'static', 'var', 'int', 'char', 'boolean', 'void', 'true',
           'false', 'null', 'this', 'let', 'do', 'if', 'else',
           'while', 'return','{', '}', '(', ')', '[', ']', '.', ',', ';', '+',
           '-', '*', '/', '&', ',', '<', '>', '=', '~', '^', '#', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

KEYORDS = ['class', 'constructor', 'function', 'method', 'field',
           'static', 'var', 'int', 'char', 'boolean', 'void', 'true',
           'false', 'null', 'this', 'let', 'do', 'if', 'else',
           'while', 'return']
SYMBOLS = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+',
           '-', '*', '/', '&', ',', '<', '>', '=', '~', '^', '#']
INTEGERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """
    dict = {"KEYWORD": "keyword", "SYMBOL": "symbol", "INT_CONST": "integerConstant",
            "STRING_CONST": "stringConstant", "IDENTIFIER": "identifier"}

    tabs = 0

    def __init__(self, input_stream: "JackTokenizer", output_stream) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.symtable = None
        self.tokenizer = input_stream
        self.output = output_stream
        self.compile_class()

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.write_tabs("open", "class")
        self.symtable = SymbolTable()
        self.eat("class")
        self.is_valid_type()
        self.eat("{")
        while self.tokenizer.cur_token in ["static", "field"]:
            self.compile_class_var_dec()
        while self.tokenizer.cur_token in ["constructor", "function", "method"]:
            self.compile_subroutine()
        self.eat("}")
        self.write_tabs("close", "class")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        self.write_tabs("open", "classVarDec")
        if self.tokenizer.cur_token == "static":
            self.eat("static")
            kind = "STATIC"
        elif self.tokenizer.cur_token == "field":
            self.eat("field")
            kind = "FIELD"
        else:
            self.eat(1)
        var_type = self.tokenizer.cur_token
        self.is_valid_type()
        names = []
        names.append(self.tokenizer.cur_token)
        self.is_valid_name()
        while self.tokenizer.cur_token != ";":
            self.eat(",")
            names.append(self.tokenizer.cur_token)
            self.is_valid_name()
        self.eat(";")
        for name in names:
            self.symtable.define(name, var_type, kind)
        print(self.symtable)
        self.write_tabs("close", "classVarDec")

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        self.symtable.start_subroutine()
        self.write_tabs("open", "subroutineDec")
        if self.tokenizer.cur_token == "constructor":
            self.eat("constructor")
        elif self.tokenizer.cur_token == "function":
            self.eat("function")
        elif self.tokenizer.cur_token == "method":
            self.eat("method")
        else:
            self.eat(1)
        if self.tokenizer.cur_token == "void":
            self.eat("void")
        else:
            self.is_valid_type()
        self.is_valid_name()
        self.eat("(")
        self.compile_parameter_list()
        self.eat(")")
        self.compile_subroutine_body()
        print(self.symtable)
        self.write_tabs("close", "subroutineDec")




    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """

        self.write_tabs("open", "parameterList")
        if self.tokenizer.cur_token != ")":
            kind = "ARG"
            name_type_list = []
            var_type1 = self.tokenizer.cur_token
            self.is_valid_type()
            name1 = self.tokenizer.cur_token
            self.is_valid_name()
            name_type_list.append((name1, var_type1))

            while self.tokenizer.cur_token == ",":
                self.eat(",")
                var_type = self.tokenizer.cur_token
                self.is_valid_type()
                name = self.tokenizer.cur_token
                self.is_valid_name()
                name_type_list.append((name, var_type))

            for (name, var_type) in name_type_list:
                self.symtable.define(name, var_type, kind)

        self.write_tabs("close", "parameterList")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.write_tabs("open", "varDec")
        kind = "VAR"
        self.eat("var")
        var_type = self.tokenizer.cur_token
        self.is_valid_type()
        names = []
        names.append(self.tokenizer.cur_token)
        self.is_valid_name()
        while self.tokenizer.cur_token == ",":
            self.eat(",")
            names.append(self.tokenizer.cur_token)
            self.is_valid_name()
        self.eat(";")
        for name in names:
            self.symtable.define(name, var_type, kind)
        self.write_tabs("close", "varDec")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        self.write_tabs("open", "statements")
        while self.tokenizer.cur_token in ["if", "while", "let", "do", "return"]:
            if self.tokenizer.cur_token == "if":
                self.compile_if()
            elif self.tokenizer.cur_token == "let":
                self.compile_let()
            elif self.tokenizer.cur_token == "while":
                self.compile_while()
            elif self.tokenizer.cur_token == "do":
                self.compile_do()
            elif self.tokenizer.cur_token == "return":
                self.compile_return()
        self.write_tabs("close", "statements")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.write_tabs("open", "doStatement")
        self.eat("do")
        self.compile_subroutine_call()
        self.eat(";")
        self.write_tabs("close", "doStatement")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.write_tabs("open", "letStatement")
        self.eat("let")
        self.is_valid_name()
        if self.tokenizer.cur_token == "[":
            self.eat("[")
            self.compile_expression()
            self.eat("]")
        self.eat("=")
        self.compile_expression()
        self.eat(";")
        self.write_tabs("close", "letStatement")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self.write_tabs("open","whileStatement")
        self.eat('while')
        self.eat("(")
        self.compile_expression()
        self.eat(")")
        self.eat("{")
        self.compile_statements()
        self.eat("}")
        self.write_tabs("close","whileStatement")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.write_tabs("open","returnStatement")
        self.eat("return")
        if self.tokenizer.cur_token != ";":
            self.compile_expression()
        self.eat(";")
        self.write_tabs("close","returnStatement")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        self.write_tabs("open","ifStatement")
        self.eat("if")
        self.eat("(")
        self.compile_expression()
        self.eat(")")
        self.eat("{")
        self.compile_statements()
        self.eat("}")
        if self.tokenizer.cur_token == "else":
            self.eat("else")
            self.eat("{")
            self.compile_statements()
            self.eat("}")
        self.write_tabs("close","ifStatement")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        self.write_tabs("open", "expression")
        self.compile_term()
        while self.tokenizer.cur_token in ['+', '-', '*', "/", "&", "|", "<", ">", "="]:
            self.write_out()
            self.compile_term()
        self.write_tabs("close", "expression")

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        # Your code goes here!
        self.write_tabs("open", "term")
        if self.tokenizer.token_type() == "IDENTIFIER":
            self.is_valid_name()
            if self.tokenizer.cur_token == "[":
                self.eat("[")
                self.compile_expression()
                self.eat("]")
            elif self.tokenizer.cur_token == "(":
                self.eat("(")
                self.compile_expression_list()
                self.eat(")")
            elif self.tokenizer.cur_token == ".":
                self.eat(".")
                self.is_valid_name()
                self.eat("(")
                self.compile_expression_list()
                self.eat(")")
        elif self.tokenizer.cur_token == "(":
            self.eat("(")
            self.compile_expression()
            self.eat(")")
        elif self.tokenizer.cur_token in ["-","~"]:
            self.write_out()
            self.compile_term()
        else:
            self.write_out()
        self.write_tabs("close", "term")

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self.write_tabs("open","expressionList")
        while self.tokenizer.cur_token != ")":
            self.compile_expression()
            if self.tokenizer.cur_token == ",":
                self.eat(",")
        self.write_tabs("close","expressionList")

    def eat(self, string):
        if self.tokenizer.cur_token != string:
            raise Exception("\n     Expected: " + string+"\n     Recieved: "+ self.tokenizer.cur_token + "\nfileName: " + self.output.name)
        else:
            self.write_out()

    def write_out(self):
        self.write_tabs()
        value = "ERROR"
        type = self.tokenizer.token_type()
        if type == "IDENTIFIER":
            value = self.tokenizer.identifier()

        if type == "INT_CONST":
            value = self.tokenizer.int_val()
        if type == "STRING_CONST":
            value = self.tokenizer.string_val()
        if type == "SYMBOL":
            value = self.tokenizer.symbol()
        if type == "KEYWORD":
            value = self.tokenizer.keyword()

        self.output.write("<" + self.dict[type] + "> " + str(value) + " </" + self.dict[type] + ">\n")
        self.tokenizer.advance()

    def write_tabs(self, state=None, token=None):
        if state == "open":
            self.output.write("  " * self.tabs + "<" + token + ">\n")
            self.tabs += 1
        elif state == "close":
            self.tabs -= 1
            self.output.write("  " * self.tabs + "</" + token + ">\n")
        else:
            self.output.write("  " * self.tabs)

    def compile_subroutine_body(self):
        self.write_tabs("open", "subroutineBody")
        self.eat("{")
        while self.tokenizer.cur_token == "var":
            self.compile_var_dec()
        self.compile_statements()
        self.eat("}")
        self.write_tabs("close", "subroutineBody")

    def is_valid_type(self):
        if self.tokenizer.cur_token in NON_VALID_TYPE:
            self.eat(1)
        self.write_out()

    def is_valid_name(self):
        if self.tokenizer.cur_token in NON_VALID_NAME:
            self.eat(1)
        if self.tokenizer.cur_token[0] in INTEGERS:
            self.eat(1)
        self.write_out()

    def compile_subroutine_call(self):
        self.is_valid_name()
        if self.tokenizer.cur_token == ".":
            self.eat(".")
            self.is_valid_name()
        self.eat("(")
        self.compile_expression_list()
        self.eat(")")
