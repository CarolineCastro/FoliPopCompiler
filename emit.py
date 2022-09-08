#---------------------------------------------
# Aqui está o terceiro módulo do meu compilador, o emissor.
# O emissor é aquele que irá produzir o código em C. 
# O emissor está efitivamente apenas anexando um monte de
# strings enquanto segue ao longo da árvore de análise.
#-----------------------------------------------

#----------------CLASS EMITTER------------------
# O objeto Emitter acompanha o código gerado e
# o gera. É apenas uma classe auxiliar para anexar
# strings. A função emit é usada para adicionar um 
# fragmento de código C e emitLine para adicionar 
# um fragmento que termina em uma linha. A função 
# headerLine é para adicionar uma linha de código 
# C ao topo do arquivo, como incluir um cabeçalho 
# de biblioteca. Por fim, a função writeFile grava
# o código C em um arquivo.  
#------------------------------------------------

class Emitter:
    
    def __init__(self, fullPath):
        self.fullPath = fullPath
        self.header = ""
        self.code = ""

    
    def emit(self, code):
        self.code += code
    
    def emitLine(self, code):
        self.code += code + '\n'
    
    def headerLine(self, code):
        self.header += code + '\n'
    
    def writeFile(self):
        with open(self.fullPath, 'w') as outputFile:
            outputFile.write(self.header + self.code)