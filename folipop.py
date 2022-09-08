from lex import *
from parse import *
from emit import *
import sys

def main():
    print("FoliPop Compiler")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], 'r') as inputFile:
        input = inputFile.read()

    
    # Inicializa o lexer, o emitter e o parser
    lexer = Lexer(input)
    emitter = Emitter("out.c")
    parser = Parser(lexer, emitter)

    parser.program() #Inicia o parser
    emitter.writeFile() #Escreve o arquivo de saída
    print("Código compilado com sucesso")

main() 