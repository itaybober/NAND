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
        self.output.write("<tokens>")

    def compile_class(self) -> None:
        """Compiles a complete class."""
        self.output.write("<class>")
        self.eat("class")
        self.write_out()
        self.eat("{")
        # TODO this could cause endless loop
        while(self.tokenizer.cur_token in ["static", "field"]):
            self.compile_class_var_dec()
        while (self.tokenizer.cur_token in ["constructor", "function", "method"]):
            self.compile_subroutine()
        self.eat("}")
        self.output.write("</class>")


    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        pass

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
        # Your code goes here!
        pass

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        pass

    def compile_let(self) -> None:
        """Compiles a let statement."""

        self.eat("let")
        self.output.write("<letStatement>\n<keyword>" + self.tokenizer.cur_token + "</keyword>\n")
        self.output.write("<identifier>" + self.tokenizer.cur_token + "</identifier>\n")
        self.eat("=")
        self.output.write("<symbol>" + self.tokenizer.cur_token + "</symbol>\n")
        self.compile_expression()
        self.eat(";")
        self.output.write("<symbol>" + self.tokenizer.cur_token + "</symbol>\n")
        self.output.write("</letStatement>\n")



    def compile_while(self) -> None:
        """Compiles a while statement."""

        self.eat("while")
        output = "<whileStatement>\n" \
                 "<keyword>" + self.tokenizer.cur_token + "</keyword>\n"
        self.eat("(")
        output += "<symbol>" + self.tokenizer.cur_token + "</symbol>\n"
        self.output.write(output)
        output = ""
        self.compile_expression()
        self.eat(")")
        output += "<symbol>" + self.tokenizer.cur_token + "</symbol>\n"
        self.eat("{")
        output += "<symbol>" + self.tokenizer.cur_token + "</symbol>\n"
        self.output.write(output)
        output = ""
        self.compile_statements()
        self.eat("}")
        output += "<symbol>" + self.tokenizer.cur_token + "</symbol>\n"
        self.output.write(output)
        self.output.write("</whileStatement>\n")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self.output.write("<returnStatement>\n")
        self.eat("return")
        if (self.tokenizer.cur_token != ";"):
            self.compile_expression()
        self.eat(";")
        self.output.write("<returnStatement>\n")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        self.eat("if")
        self.output.write("<ifStatement>\n<keyword>if</keyword>\n")
        self.eat("(")
        self.output.write("<symbol>(</symbol>\n")
        self.compile_expression()
        self.eat(")")
        self.output.write("<symbol>" + self.tokenizer.cur_token + "</symbol>\n")
        self.eat("{")
        self.output.write("<symbol>" + self.tokenizer.cur_token + "</symbol>\n")
        self.compile_statements()
        self.eat("}")
        self.output.write("<symbol>" + self.tokenizer.cur_token + "</symbol>\n")
        self.output.write("</ifStatement>\n")



    def compile_expression(self) -> None:
        """Compiles an expression."""


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
        # Your code goes here!


    def eat(self, string):
        if self.tokenizer.cur_token != string:
            raise Exception("Expected different string")
        else:
            self.write_out()
            self.tokenizer.advance()

    def write_out(self):
        type = self.tokenizer.token_type()
        self.output.write("<" + self.dict[type] + ">" + self.tokenizer.cur_token +"</" + self.dict[type] + ">\n")
        self.tokenizer.advance()



#TODO subrutine
#TODO param list
#TODO var dec
#TODO statements
#TODO expration
#TODO expration list

