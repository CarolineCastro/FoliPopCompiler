import sys
from lex import *
from emit import *

#------------------------------------------------
# Aqui está o segundo módulo do meu compilador, o parser.
# É o componente que garantirá que o código siga a sintaxe correta,
# analisando os tokens, um por um, e decidindo se a ordenação será 
# aceita, conforme definido pela minha linguagem.
#--------------------------------------------------

#------------------CLASS PARSER--------------------
# O objeto Parser acompanha o token atual e verifica se o código corresponde à gramática.
# A função checkToken e checkPeek permitão que o parser decida qual regra gramatical aplicar em seguida, dado o token atual ou o próximo.
# A função match é para os casos em que o parser já sabe qual regra gramatical aplicar.
#--------------------------------------------------

class Parser:
    #construtor
    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.symbols = set() # Variáveis declaradas até agora
        self.labelsDeclared = set() # rótulos declarados até agora
        self.labelsGotoed = set () # rótulos goto adicionados até agora

        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken() # Chamado duas vezes para inicializar o atual e o peek

    #Retorna verdadeiro se o token atual for correspondente
    def checkToken(self, kind):
        return kind == self.curToken.kind

    #Retorna verdadeiro se o próximo token também for correspondente 
    def checkPeek(self, kind):
        return kind == self.peekToken.kind

    #Tenta corresponder ao token atual. Se falso dá um erro, retorna um erro
    def match (self, kind):
        if not self.checkToken(kind):
            self.abort("Esperava " + kind.name + ", mas recebeu " + self.curToken.kind.name)
        self.nextToken()

    #Passa para o próximo token
    def nextToken(self): 
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()

    #Retorna verdadeiro se o token atual é um operador de comparação
    def isComparisonOperator(self):
        return self.checkToken(TokenType.GT) or self.checkToken(TokenType.GTEQ) or self.checkToken(TokenType.LT) or self.checkToken(TokenType.LTEQ) or self.checkToken(TokenType.EQEQ) or self.checkToken(TokenType.NOTEQ)


    #Para a excução em caso de erro
    def abort(self, message):
        sys.exit("Erro: " + message)

    
    # REGRAS DE PRODUÇÃO
    
    # programa ::= { declaração }
    def program(self):
        self.emitter.headerLine("#include <stdio.h>")
        self.emitter.headerLine("int main (void){")

        #Algumas novas linhas são necessárias na gramática do FoliPop, então é preciso pular o excesso
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

        #Analisa todas as declações no programa
        while not self.checkToken(TokenType.EOF):
            self.statement()
        
        # Encerrar o código
        self.emitter.emitLine("return 0;")
        self.emitter.emitLine("}")

        #Verifica se cada rótulo referenciado em um GOTO está declarado
        for label in self.labelsGotoed:
            if label not in self.labelsDeclared:
                self.abort("Tentando GOTO para um rótulo não declado: " + label )

    
    # REGRAS DE DECLARAÇÃO
    def statement(self):
        # Verifica o primeiro token para ver o tipo de declaração que é

        # "PRINT" (expressão | string)
        if self.checkToken(TokenType.PRINT):
            self.nextToken()

            if self.checkToken(TokenType.STRING):
                # String simples, então imprima
                self.emitter.emitLine("printf(\"" + self.curToken.text + "\\n\");")
                self.nextToken()
            
            else: 
                # Espera uma expressão e imprime o resultado como float
                self.emitter.emit("printf (\"%" + ".2f\\n\", (float)(")
                self.expression()
                self.emitter.emitLine("));")

         #"IF" comparação "THEN" nl { declaração } "ENDIF"
        elif self.checkToken(TokenType.IF):
            self.nextToken()
            self.emitter.emit("if(")
            self.comparison()

            self.match(TokenType.THEN)
            self.nl()
            self.emitter.emitLine("){")

            #Zero ou mais declarações no escopo
            while not self.checkToken(TokenType.ENDIF):
                self.statement()
            
            self.match(TokenType.ENDIF)
            self.emitter.emitLine("}")
        
        #"WHILE" comparação "REPEAT" { declaração } "ENDWHILE"
        elif self.checkToken(TokenType.WHILE):
            self.nextToken()
            self.emitter.emit("while(")
            self.comparison()

            self.match(TokenType.REPEAT)
            self.nl()
            self.emitter.emitLine("){")

            #Zero ou mais declarações no escopo do loop
            while not self.checkToken(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)
            self.emitter.emitLine("}")
        
        #"LABEL" identificador
        elif self.checkToken(TokenType.LABEL):
            self.nextToken()

            #Tenha certeza que esse rótulo já não existe
            if self.curToken.text in self.labelsDeclared:
                self.abort("Label já existe: " + self.curToken.text)
            
            self.labelsDeclared.add(self.curToken.text)

            self.emitter.emitLine(self.curToken.text + ":")
            self.match(TokenType.IDENT)
        
        #"GOTO" identificador
        elif self.checkToken(TokenType.GOTO):
            self.nextToken()
            self.labelsGotoed.add(self.curToken.text)
            self.emitter.emitLine("goto " + self.curToken.text + ";")
            self.match(TokenType.IDENT)
        
        #"LET" identificador "=" expressão 
        elif self.checkToken(TokenType.LET):
            self.nextToken()

            #Verifica se o identificador já existe na tabela de símbolos. Se não, declare-o
            if self.curToken.text not in self.symbols:
                self.symbols.add(self.curToken.text)
                self.emitter.headerLine("float " + self.curToken.text + ";")

            self.emitter.emit(self.curToken.text + " = ")
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)

            self.expression()
            self.emitter.emitLine(";")
        
        #"INPUT" identificador
        elif self.checkToken(TokenType.INPUT):
            self.nextToken()

            #Se a variável não existe, declare-a
            if self.curToken.text not in self.symbols:
                self.symbols.add(self.curToken.text)
                self.emitter.headerLine("float " + self.curToken.text + ";")

            #Emite o scanf mas também vai validar a entrada. Se inválida, define a variável como 0 e limpa a entrada
            self.emitter.emitLine("if(0 == scanf(\"%" + "f\", &" + self.curToken.text + ")) {")
            self.emitter.emitLine(self.curToken.text + " = 0;")
            self.emitter.emit("scanf(\"%")
            self.emitter.emitLine("*s\");")
            self.emitter.emitLine("}")

            self.match(TokenType.IDENT)
        
        #Não é uma declaração válida!
        else:
            self.abort("Declaração inválida em " + self.curToken.text + " (" + self.curToken.kind.name + ") ")

        #Nova Linha
        self.nl()


    #REGRAS DE EXPRESSÃO
    
    # comparação ::= expressão (("==" | "!=" | ">" | ">=" | "<" | "<=") expressão) +
    def comparison(self):
        self.expression()

        # É preciso ter um operador de comparação e outra expressão
        if self.isComparisonOperator():
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.expression()
        else: 
            self.abort("Expected comparison operator at: " + self.curToken.text)

        #Pode ter zero ou mais operadores de comparação e expressões.
        while self.isComparisonOperator():
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.expression()

    #expressão ::= termo {( "-" | "+" ) termo}
    def expression(self):
        self.term()
        
        #Pode haver zero ou mais +/- e expressões
        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.term()
    
    #termo ::= unário {( "/" | "*" ) unário}
    def term(self):
        self.unary()

        #Pode haver zero ou mais *// e expressões
        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
            self.unary()
    
    #unário ::= ["+" | "-"] primário
    def unary(self):

        #Unário opcional +/-
        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
        
        self.primary()

    #primário ::= número | identificador
    def primary(self):
        
        if self.checkToken(TokenType.NUMBER):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
        
        elif self.checkToken(TokenType.IDENT):

            #Verifica se a variável já existe
            if self.curToken.text not in self.symbols:
                self.abort("Variável referenciada antes da atribuição: " + self.curToken.text)

            self.emitter.emit(self.curToken.text)
            self.nextToken()
        else:
            # Erro!
            self.abort("Token inesperado em " + self.curToken.text)


    #nl ::= '\n' +
    def nl(self):

        # Requer pelo menos uma nova linha
        self.match(TokenType.NEWLINE)

        # Mas também serão permitidas novas linhas extras
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()
    
   
