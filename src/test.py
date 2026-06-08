from interpreter.tokens.tokens import *
from interpreter.first_pass.lexing import Lexer
from interpreter.second_pass.parsing import Parser

lexer = Lexer()
tokens = lexer.tokenize_file("test/test_program.prtn")

identifiers = set()

for token in tokens:
    #print(repr(token.token_string))
    token_type = str(type(token)).split(".")[-1][:-2]
    token_string = repr(token.token_string)

    print(f"{token_type:>24} | {token_string} ({token.position})")
    
    if type(token) == Identifier:
        identifiers.add(token.token_string)

print(f"{len(tokens):,} Tokens")

for identifier in sorted(identifiers):
    print(identifier)

print(sorted(identifiers))