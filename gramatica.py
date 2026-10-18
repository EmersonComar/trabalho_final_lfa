import sys

class Gramatica:
    def __init__(self):
        self.palavras_reservadas = []
        self.gramaticas = []

    def ler_arquivo(self, caminho_arquivo):
        try:
            with open(caminho_arquivo, "r", encoding="UTF-8") as arquivo:
                todas_linhas = arquivo.readlines()

            gramatica_atual = {"regras": {}, "finais": set()}

            for linha in todas_linhas:
                linha = linha.strip()
                if not linha:
                    continue

                if "::=" in linha:
                    linha_limpa = linha.replace("<", "").replace(">", "")
                    esquerda, direita = linha_limpa.split("::=", 1)
                    esquerda_nt = esquerda.strip()

                    if esquerda_nt == "S" and "S" in gramatica_atual["regras"]:
                        self.gramaticas.append(gramatica_atual)
                        gramatica_atual = {"regras": {}, "finais": set()}

                    for prod in direita.split("|"):
                        prod = prod.strip()
                        if not prod:
                            continue

                        if prod in ("ε"):
                            gramatica_atual["finais"].add(esquerda_nt)
                        elif prod[-1].isupper():
                            terminal = prod[:-1].strip()
                            alvo = prod[-1]
                            gramatica_atual["regras"].setdefault(esquerda_nt, []).append((terminal, alvo))
                        else:
                            gramatica_atual["regras"].setdefault(esquerda_nt, []).append((prod, None))
                else:
                    if linha not in self.palavras_reservadas:
                        self.palavras_reservadas.append(linha)

            if gramatica_atual["regras"]:
                self.gramaticas.append(gramatica_atual)

        except FileNotFoundError as e:
            print(f"Erro: o arquivo {caminho_arquivo} não encontrado")
            sys.exit(e.errno)
        except UnicodeError as e:
            print(f"Erro: o arquivo {caminho_arquivo} precisa ser no formato texto")
            sys.exit(e.errno)
        except PermissionError as e:
            print(f"Erro: usuário sem permissão para ler o arquivo {caminho_arquivo}")
            sys.exit(e.errno)

