from enum import StrEnum
from copy import deepcopy



class TokenType(StrEnum):

    # ==============
    # Block Keywords
    # ==============

    IF = "token_type.block.if"                              # if
    ELIF = "token_type.block.elif"                          # elif
    ELSE = "token_type.block.else"                          # else

    MATCH = "token_type.block.match"                        # match
    CASE = "token_type.block.case"                          # case

    FOR = "token_type.block.for"                            # for
    WHILE = "token_type.block.while"                        # while
    SKIP = "token_type.block.skip"                          # Python "continue"
    BREAK = "token_type.block.break"                        # break

    CALL = "token_type.block.call"                          # call ("callable" / function)
    CLASS = "token_type.block.class"                        # class
    ENUM = "token_type.block.enum"                          # enum

    # =================
    # Function Keywords
    # =================

    ABS = "token_type.function.abs"                         # abs()
    CEIL = "token_type.function.ceil"                       # ceil()
    FLOOR = "token_type.function.floor"                     # floor()
    ROUND = "token_type.function.round"                     # round()
    SQRT = "token_type.function.sqrt"                       # sqrt()

    INPUT = "token_type.function.input"                     # input()
    PRINT = "token_type.function.print"                     # print()

    # =============
    # Type Keywords
    # =============

    REAL = "token_type.type.real"                           # real
    BOOL = "token_type.type.bool"                           # bool
    STR = "token_type.type.str"                             # str
    SEG = "token_type.type.seg"                             # seg
    VEC = "token_type.type.vec"                             # vec

    # ==============
    # Other Keywords
    # ==============

    RETURN = "token_type.block.return"                      # return
    YIELD = "token_type.block.yield"                        # yield

    INT = "token_type.type.int"                             # int

    IN = "token_type.in"                                    # in

    # ==========
    # Operations
    # ==========

    OP_PLUS = "token_type.operation.plus"                   # +
    OP_MINUS = "token_type.operation.minus"                 # -
    OP_STAR = "token_type.operation.star"                   # *
    OP_SLASH = "token_type.operation.slash"                 # /
    OP_PERCENT = "token_type.operation.percent"             # %
    OP_CARET = "token_type.operation.caret"                 # ^

    OP_NOT = "token_type.operation.not"                     # not
    OP_OR = "token_type.operation.or"                       # or
    OP_NOR = "token_type.operation.nor"                     # nor
    OP_AND = "token_type.operation.and"                     # and
    OP_NAND = "token_type.operation.nand"                   # nand
    OP_XOR = "token_type.operation.xor"                     # xor
    OP_XNOR = "token_type.operation.xnor"                   # xnor
    OP_IMPLY = "token_type.operation.imply"                 # imply
    OP_NIMPLY = "token_type.operation.nimply"               # nimply

    # ===========
    # Comparisons
    # ===========

    IS_EQUAL = "token_type.comparison.is_equal"             # ==
    IS_NOT_EQUAL = "token_type.comparison.is_not_equal"     # !=
    IS_LESS = "token_type.comparison.is_less"               # <
    IS_NOT_LESS = "token_type.comparison.is_not_less"       # >=
    IS_MORE = "token_type.comparison.is_more"               # >
    IS_NOT_MORE = "token_type.comparison.is_not_more"       # <=

    # ========
    # Literals
    # ========

    LITERAL_REAL = "token_type.literal.real"                # i.e. 2.5, -0.1, 0.(3)
    LITERAL_BOOL = "token_type.literal.bool"                # true or false
    LITERAL_STR = "token_type.literal.str"                  # "Hello, World!"
    LITERAL_SEG = "token_type.literal.seg"                  # [-inf,+inf]
    LITERAL_VEC = "token_type.literal.vec"                  # [1, 1, 2, 3, 5]

    # =======
    # Special
    # =======

    IDENTIFIER = "token_type.identifier"                    # i.e. foo, bar
    INDENT = "token_type.indent"                            # tabs or 4 spaces
    NEWLINE = "token_type.newline"                          # \n
    COMMENT = "token_type.comment"                          # single or multi-line comments
    COLON = "token_type.colon"                              # :
    COMMA = "token_type.comma"                              # ,
    POINT = "token_type.point"                              # .
    ASSIGN = "token_type.assign"                            # =
    ARROW = "token_type.arrow"                              # ->
    WHITESPACE = "token_type.whitespace"                    # 1 space

    LEFT_ROUND_BRACE = "token_type.brace.round.left"        # (
    RIGHT_ROUND_BRACE = "token_type.brace.round.right"      # )
    LEFT_SQUARE_BRACE = "token_type.brace.square.left"      # [
    RIGHT_SQUARE_BRACE = "token_type.brace.square.right"    # ]

    INVALID = "token_type.invalid"



class TokenState:
    def __init__(self):
        pass

class Position:
    def __init__(self, index: int, row: int, col: int):
        self.index = index
        self.pos = [row, col]

    def advance(self, token):
        shift_amount = len(token.token_string)
        if type(token) == LiteralStr:
            shift_amount += 2
        self.index += shift_amount
        self.pos[0] += token.token_string.count("\n")
        self.pos[1] += len(token.token_string.split("\n")[-1])
        return shift_amount
    
    def __repr__(self):
        return f"Position({self.index}, {self.pos})"
    
    def __str__(self):
        return f"Line {self.pos[0]:,} Col {self.pos[1]:,} (Index {self.index:,})"

class Token:
    def __init__(
        self,
        position: Position,
        token_type: TokenType,
        token_string: str
    ):
        self.position = deepcopy(position)
        self.token_type = token_type
        self.token_string = token_string
    
    def __repr__(self):
        return f"{str(type(self)).split(".")[-1][:-2]}({repr(self.position)}, {self.token_type}, {repr(self.token_string)})"
    
    def __str__(self):
        return f"\"{self.token_string}\" @ {self.position}"



class KeywordIf(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.IF, "if")

class KeywordElif(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.ELIF, "elif")

class KeywordElse(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.ELSE, "else")

class KeywordFor(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.FOR, "for")

class KeywordWhile(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.WHILE, "while")

class KeywordSkip(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.SKIP, "skip")

class KeywordBreak(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.BREAK, "break")

class KeywordMatch(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.MATCH, "match")

class KeywordCase(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.CASE, "case")

class KeywordCall(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.CALL, "call")

class KeywordClass(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.CLASS, "class")

class KeywordEnum(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.ENUM, "enum")



class FunctionAbs(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.ABS, "abs")

class FunctionCeil(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.CEIL, "ceil")

class FunctionFloor(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.FLOOR, "floor")

class FunctionRound(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.ROUND, "round")

class FunctionSqrt(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.SQRT, "sqrt")

class FunctionInput(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.INPUT, "input")

class FunctionPrint(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.PRINT, "print")



class TypeReal(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.REAL, "real")

class TypeBool(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.BOOL, "bool")

class TypeStr(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.STR, "str")

class TypeSeg(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.SEG, "seg")

class TypeVec(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.VEC, "vec")



class KeywordReturn(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.RETURN, "return")

class KeywordYield(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.YIELD, "yield")

class TypeInt(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.INT, "int")

class In(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.IN, "in")



class OperationPlus(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.OP_PLUS, "+")

class OperationMinus(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.OP_MINUS, "-")

class OperationStar(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.OP_STAR, "*")

class OperationSlash(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.OP_SLASH, "/")

class OperationPercent(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.OP_PERCENT, "%")

class OperationCaret(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.OP_CARET, "^")

class OperationNOT(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.OP_NOT, "not")

class OperationOR(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.OP_OR, "or")

class OperationNOR(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.OP_NOR, "nor")

class OperationAND(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.OP_AND, "and")

class OperationNAND(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.OP_NAND, "nand")

class OperationXOR(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.OP_XOR, "xor")

class OperationXNOR(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.OP_XNOR, "xnor")

class OperationIMPLY(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.OP_IMPLY, "imply")

class OperationNIMPLY(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.OP_NIMPLY, "nimply")



class CompareEqual(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.IS_EQUAL, "==")

class CompareNotEqual(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.IS_NOT_EQUAL, "!=")

class CompareLess(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.IS_LESS, "<")

class CompareNotLess(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.IS_NOT_LESS, ">=")

class CompareMore(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.IS_MORE, ">")

class CompareNotMore(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.IS_NOT_MORE, "<=")



class LiteralReal(Token):
    def __init__(
        self,
        position: Position,
        literal: str
    ):
        super().__init__(position, TokenType.LITERAL_REAL, literal)
        self.literal = literal

class LiteralBool(Token):
    def __init__(
        self,
        position: Position,
        literal: bool
    ):
        super().__init__(position, TokenType.LITERAL_BOOL, "true" if literal else "false")
        self.literal = literal

class LiteralStr(Token):
    def __init__(
        self,
        position: Position,
        literal: str
    ):
        super().__init__(position, TokenType.LITERAL_STR, literal)
        self.literal = literal



class Identifier(Token):
    def __init__(
        self,
        position: Position,
        identifier: str
    ):
        super().__init__(position, TokenType.IDENTIFIER, identifier)
        self.identifier = identifier

class Indent(Token):
    def __init__(
        self,
        position: Position,
        token_string: str
    ):
        super().__init__(position, TokenType.INDENT, token_string)

class Newline(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.NEWLINE, "\n")

class Comment(Token):
    def __init__(
        self,
        position: Position,
        comment: str
    ):
        super().__init__(position, TokenType.COMMENT, comment)
        self.comment = comment

class Colon(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.COLON, ":")

class Comma(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.COMMA, ",")

class Point(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.POINT, ".")

class Assign(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.ASSIGN, "=")

class Arrow(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.ARROW, "->")

class Whitespace(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.WHITESPACE, " ")

class LeftRoundBrace(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.LEFT_ROUND_BRACE, "(")

class RightRoundBrace(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.RIGHT_ROUND_BRACE, ")")

class LeftSquareBrace(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.LEFT_SQUARE_BRACE, "[")

class RightSquareBrace(Token):
    def __init__(
        self,
        position: Position
    ):
        super().__init__(position, TokenType.RIGHT_SQUARE_BRACE, "]")

class Invalid(Token):
    def __init__(
        self,
        position: Position,
        token_string: str
    ):
        super().__init__(position, TokenType.INVALID, token_string)
        self.token_string = token_string