# -*- coding: utf-8 -*-
import enum
import sys

#----------------------------------------------
# Este é o primeiro módulo do meu compilador, o lexer. 
# Dada uma string de código, ele irá iterar caractere por
# caractere para fazer duas coisas: decidir onde cada token
# começa/termina e qual o tipo do token.
# Quando o lexer não puder fazer isso ele retornará um erro
# para token inválido.
#----------------------------------------------


#---------------------CLASS LEXER----------------------------
# A função getToken será a principal do lexer, ela será chamada
# toda vez que o compilador estiver pronto para ler o próximo
# token e fará o classificação deles.
# As funções nextChar e peek são auxiliares para ver o próximo
# caracter; as funções skipWhiteSpace e skipComment consomem os
# espaços e comentários respectivamente; a função
# abort é a que será usada para relatar um token inválido.
#----------------------------------------------------------------
class Lexer :
    #Construtor 
    def __init__ (self, input): 
        self.source = input + '\n' #Acrescenta uma nova linha para simplificar o lexing/parsing do último token/instrução.
        self.curChar = '' #Caracter atual na string. É o que será verificado constantemente para decidir que tipo de token é.
        self.curPos = -1 #Posição atual na string
        self.nextChar()

    #Processa o próximo caracter
    def nextChar(self):
        self.curPos += 1 
        if self.curPos >= len(self.source): #Incrementa a posição atual do lexer e atualiza o caracter atual
            self.curChar = '\0' 
        else:
            self.curChar = self.source[self.curPos] 

    #Retorna o caractere à frente
    def peek(self): #necessário para quando for preciso antecipar o próximo caracter sem atualizar a posição.
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos+1]

    #Token inválido encontrado, imprime uma mensagem de erro e sai
    def abort (self, message):
        sys.exit("Lexing error: " + message)

    #Ignora espaços em branco, exceto em novas linhas, que usaremos para indicar o final de uma instrução
    def skipWhiteSpace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()

    #Ignora comentários no código
    def skipComment (self): 
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()

    #Retorna o próximo token
    def getToken (self):
        self.skipWhiteSpace()
        self.skipComment()
        token = None

        #Verifica o primeiro caracter desse token para saber o que é. 
        #Se for um operador de vários caracteres (ex: !=), número, identificador ou palavra-chave, o resto será processado, caso contrário o compilador irá parar e acusar um erro.

        # VERIFICAÇÃO PARA OPERADORES
        if self.curChar == '+': 
            token = Token(self.curChar, TokenType.PLUS)

        elif self.curChar == '-':
            token = Token(self.curChar, TokenType.MINUS)

        elif self.curChar == '*':
            token = Token(self.curChar, TokenType.ASTERISK)

        elif self.curChar == '/':
            token = Token(self.curChar, TokenType.SLASH)

        elif self.curChar == '=':
            # Verifica se o token é do tipo '=' ou '=='
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)

        elif self.curChar == '>':
            # Verifica se o token é tipo '>' ou '>='
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)

        elif self.curChar == '<':
                # Verifica se o token é tipo '<' ou '<='
                if self.peek() == '=':
                    lastChar = self.curChar
                    self.nextChar()
                    token = Token(lastChar + self.curChar, TokenType.LTEQ)
                else:
                    token = Token(self.curChar, TokenType.LT)

        elif self.curChar == '!':
            # Verifica se o token é tipo '!='
            if self.peek() == '=':
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort("Esperava por '!=', mas recebeu '!'" + self.peek())

        # VERIFICAÇÃO PARA STRINGS
        elif self.curChar == '\"':
            # Lê os caracteres entre aspas
            self.nextChar()
            startPos = self.curPos

            while self.curChar != '\"':
                # Não aceita caracteres especiais na string. Nada novas linhas, tabs ou %.
                # Será usado o printf do C nessa string
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                    self.abort("A string contém caracteres inválidos")

                self.nextChar()
                tokText = self.source[startPos : self.curPos] #Pega a string
                token = Token(tokText, TokenType.STRING)

        # VERIFICAÇÃO PARA NÚMEROS
        elif self.curChar.isdigit():
            # Lê o caracter para saber se é um dígito, ou seja, precisa ser um número.
            # Pega todos os dígitos e decimais consecutivos se houver um.
            startPos = self.curPos

            while self.peek().isdigit():
                self.nextChar()
            
            if self.peek() == '.': # Decimal!
                self.nextChar()

                #É preciso ter pelo menos um dígito após o decimal
                if not self.peek().isdigit():
                    self.abort("Caracter inválido para número.")
                
                while self.peek().isdigit():
                    self.nextChar()

            tokText = self.source[startPos : self.curPos + 1] # Pega o número
            token = Token(tokText, TokenType.NUMBER)

        # VERIFICAÇÃO PARA IDENTIFICADORES E PALAVRAS-CHAVE
        elif self.curChar.isalpha():
            #Se o caractere inicial é uma letra, então deve ser um identificador ou uma palavra chave.
            # Obtém todos os caracteres alfanuméricos consecutivos.
            startPos = self.curPos

            while self.peek().isalnum():
                self.nextChar()

            # Verifica se o token está na lista de palavras-chave
            tokText = self.source[startPos : self.curPos +1] #Pega a palavra
            keyword = Token.checkIfKeyword(tokText)

            if keyword == None: # Identificador
                token = Token(tokText, TokenType.IDENT)
            else: # Palavra-chave
                token = Token(tokText, keyword)         

        elif self.curChar == '\n':
            token = Token(self.curChar, TokenType.NEWLINE)

        elif self.curChar == '\0':
            token = Token(self.curChar, TokenType.EOF)

        else:
            self.abort("Token Desconhecido " + self.curChar) #token DESCONHECIDO!

        self.nextChar()
        return token


#-------------CLASS TOKEN----------------------
# Aqui iremos acompanhar o tipo de token que é
# e o texto exato do código.
#----------------------------------------------

class Token:
    # contém o texto original e o tipo de token
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText # O texto do token atual. Usado por indentificadores, strings e números.
        self.kind = tokenKind # O tipo de token que está classificado.
    
    @staticmethod
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            # Depende de todos os valores de enum de palavra-chave sendo 1XX
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind
        return None


#------------CLASS TOKEN TYPE------------------
# Aqui está definida a classificação de todos os tokens possíveis
# permitidos pela linguagem FoliPop.
#----------------------------------------------

class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3

    # Palavras-Chave
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111

    # Operadores
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211 
