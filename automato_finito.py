class Automato_finito:
    def __init__(self):
        self.estados = {"S": {}}
        self.nao_terminal = "A"
        self.prox_nao_terminal = "A"
        self.lista_letras = []

    def _incrementar_chave(self):
        lista = list(self.prox_nao_terminal)
        i = len(lista) - 1

        while i >= 0:
            if lista[i] == "Z":
                lista[i] = "A"
                i -= 1
            else:
                lista[i] = chr(ord(lista[i]) + 1)
                if lista[i] == "S":
                    lista[i] = chr(ord(lista[i]) + 1)
                self.prox_nao_terminal = "".join(lista)
                return
        
        self.prox_nao_terminal = "A" + "".join(lista)

    def _transformar_estado_final(self):
        if self.nao_terminal in self.estados:
            nova_chave = f"*{self.nao_terminal}"
            self.estados[nova_chave] = self.estados[self.nao_terminal]
            del self.estados[self.nao_terminal]
        else:
            print("Chave não encontrada")

    def processar_palavras(self, palavras_reservadas):
        for palavra in palavras_reservadas:
            inicio_palavra = 1
            for letra in palavra:

                if inicio_palavra:
                    if not letra in self.estados["S"]:
                        self.estados["S"][letra] = []
                    self.estados["S"][letra].append(self.nao_terminal)
                    if not letra in self.lista_letras:
                        self.lista_letras.append(letra)
                    inicio_palavra = 0
                    continue

                self._incrementar_chave()
                if not self.nao_terminal in self.estados:
                    self.estados[self.nao_terminal] = {letra: []}

                self.estados[self.nao_terminal][letra].append(self.prox_nao_terminal)
                self.nao_terminal = self.prox_nao_terminal 

                if not letra in self.lista_letras:
                    self.lista_letras.append(letra)

            self.estados.update({self.nao_terminal: {}})
            self._transformar_estado_final()
            self._incrementar_chave()
            self.nao_terminal = self.prox_nao_terminal

    def imprimir_tabela(self):
        print("δ", end="\t")
        for letra in self.lista_letras:
            print(letra, end="\t")
        print()

        for chave, transicoes in self.estados.items():
            print(chave, end="\t")

            for letra in self.lista_letras:
                if letra in transicoes:
                    destinos = ",".join(transicoes[letra])
                    print(destinos, end="\t")
                else:
                    print("", end="\t")
            print()
