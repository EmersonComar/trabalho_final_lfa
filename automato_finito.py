import copy

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

    def processar_gramatica(self, gramaticas):
        if isinstance(gramaticas, dict):
            gramaticas = [gramaticas]

        for gramatica in gramaticas:
            regras = gramatica.get("regras", {})
            finais = gramatica.get("finais", set())

            todos_nt = []
            for nt, producoes in regras.items():
                if nt not in todos_nt:
                    todos_nt.append(nt)
                for terminal, alvo in producoes:
                    if alvo is not None and alvo not in todos_nt:
                        todos_nt.append(alvo)

            mapa = {}
            chaves = {}

            for nt in todos_nt:
                if nt == "S":
                    mapa["S"] = "S"
                    if "S" in finais:
                        chaves["S"] = "*S"
                        if "S" in self.estados:
                            self.estados["*S"] = self.estados.pop("S")
                        else:
                            self.estados.setdefault("*S", {})
                    else:
                        chaves["S"] = "*S" if "*S" in self.estados else "S"
                        self.estados.setdefault(chaves["S"], {})
                else:
                    nome = self.nao_terminal
                    self._incrementar_chave()
                    self.nao_terminal = self.prox_nao_terminal

                    mapa[nt] = nome
                    if nt in finais:
                        chave = f"*{nome}"
                        chaves[nt] = chave
                        self.estados[chave] = {}
                    else:
                        chaves[nt] = nome
                        self.estados[nome] = {}

            for nt, producoes in regras.items():
                origem_chave = chaves[nt]

                for terminal, alvo in producoes:
                    if alvo is not None:
                        destino = mapa[alvo]
                    else:
                        destino = self.nao_terminal
                        self.estados[f"*{destino}"] = {}
                        self._incrementar_chave()
                        self.nao_terminal = self.prox_nao_terminal

                    if terminal not in self.estados[origem_chave]:
                        self.estados[origem_chave][terminal] = []
                    self.estados[origem_chave][terminal].append(destino)

                    if terminal not in self.lista_letras:
                        self.lista_letras.append(terminal)

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

    def _obter_chave_real(self, estados, nome):
        nome_limpo = str(nome).lstrip("*")
        if nome_limpo in estados:
            return nome_limpo
        if f"*{nome_limpo}" in estados:
            return f"*{nome_limpo}"
        return None

    def remover_inalcancaveis(self, estados, apontar_erros=True):
        if not estados:
            return {}

        estado_inicial = self._obter_chave_real(estados, "S")
        if estado_inicial is None:
            estado_inicial = next(iter(estados))

        alcancaveis = {estado_inicial}
        fila = [estado_inicial]

        while fila:
            atual = fila.pop(0)
            transicoes = estados.get(atual, {})
            for destinos in transicoes.values():
                itens = destinos if isinstance(destinos, (list, tuple, set, frozenset)) else [destinos]
                for d in itens:
                    chave_d = self._obter_chave_real(estados, d)
                    if chave_d and chave_d not in alcancaveis:
                        alcancaveis.add(chave_d)
                        fila.append(chave_d)

        inalcancaveis = set(estados.keys()) - alcancaveis
        if inalcancaveis and apontar_erros:
            print(f"\n[Aviso] Estados inalcançáveis detectados: {', '.join(sorted(inalcancaveis))}")

        for est in inalcancaveis:
            del estados[est]

        return estados

    def remover_mortos(self, estados, apontar_erros=True):
        if not estados:
            return {}

        finais = {est for est in estados if est.startswith("*")}

        grafo_reverso = {est: set() for est in estados}
        for origem, transicoes in estados.items():
            for destinos in transicoes.values():
                itens = destinos if isinstance(destinos, (list, tuple, set, frozenset)) else [destinos]
                for d in itens:
                    chave_d = self._obter_chave_real(estados, d)
                    if chave_d:
                        grafo_reverso[chave_d].add(origem)

        vivos = set(finais)
        fila = list(finais)

        while fila:
            atual = fila.pop(0)
            for anterior in grafo_reverso.get(atual, set()):
                if anterior not in vivos:
                    vivos.add(anterior)
                    fila.append(anterior)

        mortos = set(estados.keys()) - vivos
        if mortos and apontar_erros:
            print(f"\n[Aviso] Estados mortos detectados: {', '.join(mortos)}")

        mortos_nomes = {est.lstrip("*") for est in mortos}

        for est in mortos:
            del estados[est]

        for origem, transicoes in estados.items():
            for simbolo in list(transicoes.keys()):
                itens = transicoes[simbolo]
                if isinstance(itens, list):
                    transicoes[simbolo] = [d for d in itens if d.lstrip("*") not in mortos_nomes]
                    if not transicoes[simbolo]:
                        del transicoes[simbolo]
                else:
                    if str(itens).lstrip("*") in mortos_nomes:
                        del transicoes[simbolo]

        return estados

    def minimizacao(self, estados=None, apontar_erros=True):
        if estados is None:
            estados = self.determinizar()

        estados_min = copy.deepcopy(estados)
        estados_min = self.remover_inalcancaveis(estados_min, apontar_erros=apontar_erros)
        estados_min = self.remover_mortos(estados_min, apontar_erros=apontar_erros)
        estados_min = self.remover_inalcancaveis(estados_min, apontar_erros=False)

        return estados_min

