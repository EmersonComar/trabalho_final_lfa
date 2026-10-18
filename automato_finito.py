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

    def _procura_n_terminal(self, texto):
        inicio = texto.find('<')
        fim = texto.find('>')

        if inicio != -1 and fim != -1 and fim > inicio:
            return texto[inicio + 1:fim]

        return None


    def _obter_estados_finais(self):
        return {estado.lstrip("*") for estado in self.estados if estado.startswith("*")}

    def _obter_transicoes(self, estado):
        estado_limpo = estado.lstrip("*")
        if estado_limpo in self.estados:
            return self.estados[estado_limpo]
        if f"*{estado_limpo}" in self.estados:
            return self.estados[f"*{estado_limpo}"]
        return {}

    def determinizar(self):
        estados_finais = self._obter_estados_finais()
        estado_inicial = frozenset({"S"})
        afd_raw = {estado_inicial: {}}
        fila = [estado_inicial]

        while fila:
            atual = fila.pop(0)
            for letra in self.lista_letras:
                destinos = set()
                for estado in atual:
                    transicoes = self._obter_transicoes(estado)
                    if letra in transicoes:
                        destinos.update(transicoes[letra])

                if not destinos:
                    continue

                chave = frozenset(destinos)
                if chave not in afd_raw:
                    afd_raw[chave] = {}
                    fila.append(chave)
                afd_raw[atual][letra] = chave

        afd = {}
        for conjunto, transicoes in afd_raw.items():
            nome_estado = ",".join(sorted(e.lstrip("*") for e in conjunto))
            eh_final = any(e.lstrip("*") in estados_finais for e in conjunto)
            chave_estado = f"*{nome_estado}" if eh_final else nome_estado

            afd[chave_estado] = {}
            for letra, prox_conjunto in transicoes.items():
                destino_nome = ",".join(sorted(p.lstrip("*") for p in prox_conjunto))
                afd[chave_estado][letra] = [destino_nome]

        return afd

    def imprimir_tabela(self, estados=None, alfabeto=None, titulo=None):
        if estados is None:
            estados = self.estados
        if alfabeto is None:
            alfabeto = self.lista_letras

        if titulo:
            print(f"\n--- {titulo} ---")

        print("δ", end="\t")
        for letra in alfabeto:
            print(letra, end="\t")
        print()

        estados_finais = self._obter_estados_finais()

        for estado, transicoes in estados.items():
            if isinstance(estado, (set, frozenset)):
                nome_base = ",".join(sorted(str(e).lstrip("*") for e in estado))
                eh_final = any(str(e).lstrip("*") in estados_finais or str(e).startswith("*") for e in estado)
                rotulo_estado = f"*{nome_base}" if eh_final else nome_base
            else:
                rotulo_estado = str(estado)

            print(rotulo_estado, end="\t")
            for letra in alfabeto:
                destinos = transicoes.get(letra)
                if destinos:
                    if isinstance(destinos, str):
                        print(destinos, end="\t")
                    elif isinstance(destinos, (set, frozenset)):
                        print(",".join(sorted(str(d).lstrip("*") for d in destinos)), end="\t")
                    elif isinstance(destinos, (list, tuple)):
                        destinos_formatados = []
                        for d in destinos:
                            if isinstance(d, (set, frozenset)):
                                destinos_formatados.append(",".join(sorted(str(x).lstrip("*") for x in d)))
                            else:
                                destinos_formatados.append(str(d))
                        print(",".join(destinos_formatados), end="\t")
                    else:
                        print(str(destinos), end="\t")
                else:
                    print(end="\t")
            print()
