"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

import JackTokenizer




class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """
    dict = {"KEYWORD": "keywords", "SYMBOL": "symbol", "INT_CONST": "integerConstant",
                  "STRING_CONST":"stringConstant", "IDENTIFIER":"identifier"}


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
        self.tokenizer = input_stream
        self.output = output_stream
        self.output.write("<tokens>\n")

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.output.write("<class>\n")
        self.eat("class")
        self.write_out()
        self.eat("{")
        while self.tokenizer.cur_token in ["static", "field"]:
            self.compile_class_var_dec()
        while self.tokenizer.cur_token in ["constructor", "function", "method"]:
            self.compile_subroutine()
        self.eat("}")
        self.output.write("</class>\n")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        self.output.write("<varDec>\n")
        self.eat("var")
        # TODO do i need to parse which type it is specifically
        self.write_out()
        self.write_out()
        while self.tokenizer.cur_token != ";":
            self.eat(",")
            self.write_out()
        self.eat(";")
        self.output.write("</varDec>\n")

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        # Your code goes here!
        pass

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!
        pass

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!
        pass

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        self.output.write("<statements>\n")
        while self.tokenizer.cur_token in ["if", "while", "let", "do", "return"]:
            if self.tokenizer.cur_token == "if":
                self.compile_if()
            elif self.tokenizer.cur_token == "let":
                self.compile_if()
            elif self.tokenizer.cur_token == "while":
                self.compile_while()
            elif self.tokenizer.cur_token == "do":
                self.compile_do()
            elif self.tokenizer.cur_token == "return":
                self.compile_return()
        self.output.write("</statements>\n")


    def compile_do(self) -> None:
        """Compiles a do statement."""
        self.output.write("<doStatement>\n")
        self.eat("do")
        self.write_out()
        if self.tokenizer.cur_token == ".":
            self.eat(".")
            self.write_out()
            self.eat("(")
            self.compile_expression_list()
            self.eat(")")
        else:
            self.write_out()
            self.output.write("</doStatement>\n")




    def compile_let(self) -> None:
        """Compiles a let statement."""

        self.output.write("<letStatement>\n")
        self.eat("let")
        self.write_out()
        self.eat("=")
        self.compile_expression()
        self.eat(";")
        self.output.write("</letStatement>\n")



    def compile_while(self) -> None:
        """Compiles a while statement."""

        self.output.write("<whileStatement>\n")
        self.eat('while')
        self.eat("(")
        self.compile_expression()
        self.eat(")")
        self.eat("{")
        self.compile_statements()
        self.eat("}")
        self.output.write("</whileStatement>\n")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.output.write("<returnStatement>\n")
        self.eat("return")
        if self.tokenizer.cur_token != ";":
            self.compile_expression()
        self.eat(";")
        self.output.write("<returnStatement>\n")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        self.output.write("<ifStatement>\n")
        self.eat("if")
        self.eat("(")
        self.compile_expression()
        self.eat(")")
        self.eat("{")
        self.compile_statements()
        self.eat("}")
        self.output.write("</ifStatement>\n")



    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        self.output.write("<expression>\n")
        self.compile_term()
        self.output.write()
        self.output.write("</expression>\n")

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
        self.output.write("<term>\n")
        prev_token = self.tokenizer.cur_token
        self.write_out()
        if prev_token == "IDENTIFIER":
            if self.tokenizer.cur_token == ".":
                self.eat(".")
                self.compile_subroutine()
            elif self.tokenizer.cur_token == "(":
                self.eat("(")
                # TODO this is definetly wrong
                self.compile_expression()
                self.eat(")")
            elif self.tokenizer.cur_token == "[":
                self.eat("[")
                self.compile_expression()
                self.eat("]")
            elif self.tokenizer.cur_token in ['-','~']:
                self.write_out()
        self.output.write("</term>\n")


    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self.output.write("<expressionList>\n")
        while self.tokenizer.cur_token != ")":
            self.compile_expression()
            if self.tokenizer.cur_token == ",":
                self.eat(",")
        self.output.write("</expressionList>\n")


    def eat(self, string):
        if self.tokenizer.cur_token != string:
            raise Exception("Expected different string")
        else:
            self.write_out()

    def write_out(self):
        type = self.tokenizer.token_type()
        self.output.write("<" + self.dict[type] + ">" + self.tokenizer.cur_token +"</" + self.dict[type] + ">\n")
        self.tokenizer.advance()



#TODO subrutine
#TODO param list
#TODO expration

