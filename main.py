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
    parser.add_argument(
        "--afnd", action="store_true", help="Exibir apenas automato finito não deterministico"
    )
    parser.add_argument(
        "--afd", action="store_true", help="Exibir apenas automato finito deterministico"
    )
    parser.add_argument(
        "--min", action="store_true", help="Exibir apenas automato finito deterministico minimizado"
    )
    parser.add_argument(
        "--erro", action="store_true", help="Preencher células do AFD não mapeados com estado ERRO"
    )
    args = parser.parse_args()
    return args


def main():
    args = entrada_dados()
    g = Gramatica()
    afnd = Automato_finito()
    g.ler_arquivo(args.arquivo)

    afnd.processar_palavras(g.palavras_reservadas)
    afnd.processar_gramatica(g.gramaticas)

    if args.afnd:
        afnd.imprimir_tabela(estados=afnd.estados, alfabeto=afnd.lista_letras, titulo="Automato finito não deterministico")
    elif args.afd:
        afnd.imprimir_tabela(estados=afnd.determinizar(), titulo="Automato finito deterministico")
    elif args.min:
        afd = afnd.determinizar()
        afd_min = afnd.minimizacao(estados=afd, incluir_erro=args.erro)
        afnd.imprimir_tabela(estados=afd_min, titulo="Automato finito deterministico minimizado")
    else:
        afnd.imprimir_tabela(estados=afnd.estados, alfabeto=afnd.lista_letras, titulo="Automato finito não deterministico")
        afd = afnd.determinizar()
        afnd.imprimir_tabela(estados=afd, titulo="Automato finito deterministico")
        afd_min = afnd.minimizacao(estados=afd)
        afnd.imprimir_tabela(estados=afd_min, titulo="Automato finito deterministico minimizado")
if __name__ == "__main__":
    main()
