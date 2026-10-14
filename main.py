import json
import argparse
from gramatica import Gramatica
from automato_finito import Automato_finito

def entrada_dados():
    parser = argparse.ArgumentParser(
        description="Gerador de AFD livre de estados inalcançaveis e mortos"
    )
    parser.add_argument(
        "--arquivo", type=str, help="Arquivo contendo a relaçao sentença (tokens e/ou GRs) de uma linguagem", required=True
    )
    args = parser.parse_args()
    return args


def main():
    args = entrada_dados()
    g = Gramatica()
    g.ler_arquivo(args.arquivo)

    
    afnd = Automato_finito()

    print(g.palavras_reservadas)
    afnd.processar_palavras(g.palavras_reservadas)

    afnd.imprimir_tabela()

if __name__ == "__main__":
    main()
