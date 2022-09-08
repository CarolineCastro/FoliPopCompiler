Um compilador escrito em Python para a linguagem FoliPop que compilará em código C.

O compilador funciona em 3 etapas: 

    1. LEXER (Lexing) - quebra o código de entrada em pequenos pedaços chamados de tokens.
    2. ANALISADOR (Parsing) - verifica se os tokens estão na ordem permitida pela linguagem.
    3. EMISSOR (Emitting) - produz o código C apropriado.


REGRAS DO LEXER PARA A LINGUAGEM FOLIPOP:
    
    *OPERADOR: um ou dois caracteres consecutivos que correspondam a: + - * / = == != > < >= <=

    *STRING: aspas duplas seguidas de zero ou mais caracteres e aspas duplas. Tais como: "olá, mundo" e ""

    *NÚMEROS: Um ou mais caracteres númericos seguidos por um ponto decimal opcional e um ou mais caracteres númericos. Tais como: 10 e 1,05

    *IDENTIFICADOR: Um caractere alfabético seguido por zero ou mais caracteres alfanuméricos.

    *PALAVRAS-CHAVE: Palavras reservadas da linguagem que correspondem a exatamente a:  LABEL, GOTO, PRINT, INPUT, LET, IF, THEN, ENDIF, WHILE, REPEAT, ENDWHILE

REGRAS DO ANALISADOR PARA A LINGUAGEM FOLIPOP:

    *REGRAS DE DECLARAÇÃO - programa ::= { declaração }
                            declaração ::= "PRINT" (expressão | string) nl(novalinha)

                            declaração ::= Comparação "IF" "THEN" nl { instrução } "ENDIF" nl

                            declaração ::= Comparação "WHILE" "REPEAT" nl { instrução nl } "ENDWHILE" nl

                            declaração ::= "LABEL" identificador nl

                            declração ::= "GOTO" identificador nl

                            declaração ::= "LET" identificador "=" expressão nl

                            declaração ::= "INPUT" identificador nl
    
    *REGRAS DE EXPRESSÃO - comparação ::= expressão (("==" | "!=" |
                             ">" | ">=" | "<" | "<=") expressão )

                             expressão ::= termo {("/" | "*") termo}

                             termo ::= unário {("/" | "*") unário}

                             unário ::= [ "+" | "-" ] primário
                             
                             primário ::= número | identificador



Para executar o código gerado em out.c, acesse: https://replit.com/languages/c



    


