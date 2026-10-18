import sys

class Gramatica:
    def __init__(self):
        self.palavras_reservadas = []
        self.regras_producoes = {}

    def ler_arquivo(self, caminho_arquivo):
        try:
            with open(caminho_arquivo, "r", encoding="UTF-8") as arquivo:
                todas_linhas = arquivo.readlines()

            i=0
            while i < len(todas_linhas):
                linha = todas_linhas[i].strip()

                if "::=" in linha:
                    pass
                else:
                    if linha:
                        if not linha in self.palavras_reservadas:
                            self.palavras_reservadas.append(linha)
                i += 1

        except FileNotFoundError as e:
            print(f"Erro: o arquivo {caminho_arquivo} não encontrado")
            sys.exit(e.errno);
        except UnicodeError as e:
            print(f"Erro: o arquivo {caminho_arquivo} precisa ser no formato texto")
            sys.exit(e.errno)
        except PermissionError as e:
            print(f"Erro: usuário sem permissão para ler o arquivo {caminho_arquivo}")
            sys.exit(e.errno)

