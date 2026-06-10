from ..tokens.tokens import *



SPECIAL_TABLE: list[tuple[str, type[Token]]] = [

    ("\n",  Newline),
    (":",   Colon),
    (",",   Comma),
    (".",   Point),
    ("->",  Arrow),
    ("(",   LeftRoundBrace),
    (")",   RightRoundBrace),
    ("[",   LeftSquareBrace),
    ("]",   RightSquareBrace)

]

KEYWORD_TABLE: list[tuple[str, type[Token]]] = [

    ("if",      KeywordIf),
    ("elif",    KeywordElif),
    ("else",    KeywordElse),

    ("match",   KeywordMatch),
    ("case",    KeywordCase),

    ("for",     KeywordFor),
    ("while",   KeywordWhile),
    ("skip",    KeywordSkip),
    ("break",   KeywordBreak),

    ("call",    KeywordCall),
    ("class",   KeywordClass),
    ("enum",    KeywordEnum),


    ("abs",     FunctionAbs),
    ("ceil",    FunctionCeil),
    ("floor",   FunctionFloor),
    ("round",   FunctionRound),
    ("sqrt",    FunctionSqrt),

    ("input",   FunctionInput),
    ("print",   FunctionPrint),


    ("real",    TypeReal),
    ("bool",    TypeBool),
    ("str",     TypeStr),
    ("seg",     TypeSeg),
    ("vec",     TypeVec),

    ("return",  KeywordReturn),
    ("yield",   KeywordYield),
    ("int",     TypeInt),
    ("in",      In)

    ("not",     OperationNOT),
    ("or",      OperationOR),
    ("nor",     OperationNOR),
    ("and",     OperationAND),
    ("nand",    OperationNAND),
    ("xor",     OperationXOR),
    ("xnor",    OperationXNOR),
    ("imply",   OperationIMPLY),
    ("nimply",  OperationNIMPLY)

]

OPERATOR_TABLE: list[tuple[str, type[Token]]] = [

    ("+",   OperationPlus),
    ("-",   OperationMinus),
    ("*",   OperationStar),
    ("/",   OperationSlash),
    ("%",   OperationPercent),
    ("^",   OperationCaret),

    ("==",  CompareEqual),
    ("!=",  CompareNotEqual),
    ("<=",  CompareNotMore),
    (">=",  CompareNotLess),
    (">",   CompareMore),
    ("<",   CompareLess)

]



class Lexer:
    def __init__(self):
        """

        """

        pass

    def get_next_token(self) -> None | Token:
        """

        """

        # EOF - The program is empty
        if self.program_string == "":
            return None
    
        
        char = self.program_string[0]

        if self.program_string.startswith(" " * 4):
            return Indent(self.position, " " * 4)
        elif self.program_string[0] == "\t":
            return Indent(self.position, "\t")

        # Whitespace Removal Service
        #     Whitespace removed in 10ms or your removal is free!
        #     Additional terms may apply
        #     Not all locations may participate
        #     Check out example.com for details
        elif char == " ":
            return Whitespace(self.position)


        # ========
        # Comments
        # ========
        #     Single-line comments are allowed to extend to EOF
        #     Multi-line comments are not, since it's best to ensure the comment wasn't unintentionally left open into actual code
        elif self.program_string.startswith("//"):
            token_string = self.program_string.split("\n", 1)[0]
            return Comment(self.position, token_string)

        elif self.program_string[:2] == "/*":
            if "*/" not in self.program_string[2:]:
                raise Exception("Multi-line comment was not closed with \"*/\"before EOF")
            index = self.program_string.index("*/") + 2
            token_string = self.program_string[:index]
            return Comment(self.position, token_string)


        # Special Tokens
        for special, token_class in SPECIAL_TABLE:
            if self.program_string.startswith(special):
                return token_class(self.position)


        # =====================
        # Keyword or Identifier
        # =====================
        #     I'm not entirely sure what I want to allow for identifiers
        #     Part of me wants to enforce a particular type of variable, maybe even depending on the type or use of the variable
        #         * i.e. how often constants are written in all caps
        #     Currently keywords are context-sensitive similar to Python's "match" and "case"
        #         * Keywords are valid as identifiers if they're used in contexts which aren't valid for those keywords, but are valid for identifiers
        if char.isalpha() or char == "_":

            token_string = char
            for char in self.program_string[1:]:
                if char.isalnum() or char == "_":
                    token_string += char
                    continue
                break
                
            for keyword, token_class in KEYWORD_TABLE:
                if token_string == keyword:
                    return token_class(self.position)
            
            if token_string == "inf":
                return LiteralReal(self.position, "inf")
            elif token_string == "true" or token_string == "false":
                return LiteralBool(self.position, token_string == "true")
            
            return Identifier(self.position, token_string)
        
        
        # ============
        # Real Literal
        # ============
        #     I'm still working out what rules I want to enforce on real literals
        #     I've got some ideas I like, but that also seem potentially annoying if you're fighting against a specific required format
        #         * Essentially a minimal float, but digits must exist to justify decimal points and the parenthesis for repeating decimals
        #         * Something like .5 wouldn't be allowed in favor of 0.5
        #         * 1/3 could be written as 0.(3) where the parenthesis indicate the repeating digits
        elif char.isnumeric():

            real_state = "INTEGER"
            
            token_string = char
            index = 1

            while index < len(self.program_string):
                
                char = self.program_string[index]

                if char.isnumeric():
                    token_string += char
                    index += 1
                
                elif real_state == "INTEGER" and char == ".":
                    real_state = "DECIMAL"
                    token_string += char
                    index += 1

                elif real_state == "DECIMAL" and char == "(":
                    real_state = "REPEATING"
                    token_string += char
                    index += 1
                
                elif real_state == "REPEATING" and char == ")":
                    token_string += char
                    return LiteralReal(self.position, token_string)
            
                elif real_state != "REPEATING":
                    return LiteralReal(self.position, token_string)
                
                else:
                    raise Exception("Invalid real literal")
            
            if real_state == "REPEATING":
                raise Exception("Invalid real literal")
            
            return LiteralReal(self.position, token_string)

        
        # ==============
        # String Literal
        # ==============
        elif char == "\"":

            token_string = char
            index = 1

            while index < len(self.program_string):

                char = self.program_string[index]

                # Currently only tabs, newlines, and backslashes are included as escape characters
                # Later on I'll look into unicode and any other characters I've neglected
                if char == "\\":

                    if index + 1 == len(self.program_string):
                        raise Exception("String literal not terminated before EOF")
                    
                    index += 1
                    char = self.program_string[index]

                    if char not in ["t", "n", "\\"]:
                        raise Exception("Unrecognized escape character (currently only \"\\t\", \"\\n\", and \"\\\" are recognized)")
                    
                    index += 1

                elif char == "\"":
                    return LiteralStr(self.position, self.program_string[1:index])
                
                elif char == "\n":
                    raise Exception("String literal not terminated before newline")
                
                else:
                    index += 1
            
            raise Exception("Stiring literal not terminated before EOF")
        
        # ====================
        # Comparison Operators
        # ====================
        for operator, token_class in OPERATOR_TABLE:
            if self.program_string.startswith(operator):
                return token_class(self.position)
        
        # Assignment
        if char == "=":
            return Assign(self.position)

        # Catch

        raise Exception("Invalid token")


    def tokenize(self, program_string: str) -> list[Token]:
        """

        """

        self.program_string = program_string
        self.position = Position(0, 1, 0) # Line numbers start from 1, index and column start from 0
        self.tokens = []

        self.context_reserved = False

        while (token := self.get_next_token()) is not None:

            self.tokens.append(token)
            shift_amount = self.position.advance(token)
            self.program_string = self.program_string[shift_amount:]

        return self.tokens
    
    def tokenize_file(self, path: str) -> list[Token]:
        with open(path) as f:
            return self.tokenize(f.read())