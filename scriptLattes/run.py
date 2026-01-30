# encoding: utf-8
import sys
import argparse
import datetime
import os
from scriptLattes.grupo import Grupo
from scriptLattes.util import criarDiretorio, copiarArquivos

def formatar_tempo_decorrido(tempo_decorrido):
    segundos = int(tempo_decorrido.total_seconds())

    if segundos < 60:
        return f"{segundos} segundos"
    elif segundos < 3600:
        minutos, segundos = divmod(segundos, 60)
        return f"{minutos} minutos e {segundos} segundos"
    else:
        horas, segundos = divmod(segundos, 3600)
        minutos, segundos = divmod(segundos, 60)
        return f"{horas} horas, {minutos} minutos e {segundos} segundos"

def executar_scriptLattes(arquivoConfiguracao, somente_json=False):
    print("[SCRIPTLATTES INICIADO]\n")
    # os.chdir( os.path.abspath(os.path.join(arquivoConfiguracao, os.pardir)))
    tempo_inicial = datetime.datetime.now()
    novoGrupo = Grupo(arquivoConfiguracao)
    novoGrupo.imprimirListaDeTermos()
    novoGrupo.imprimirListaDeRotulos()

    if criarDiretorio(novoGrupo.obterParametro('global-diretorio_de_saida')):
        novoGrupo.carregarDadosCVLattes() #obrigatorio
        novoGrupo.compilarListasDeItems() # obrigatorio
        
        if not somente_json:
            novoGrupo.gerarGrafosDeColaboracoes() # obrigatorio
            novoGrupo.gerarPaginasWeb() # obrigatorio
            novoGrupo.gerarArquivosTemporarios() # obrigatorio
        
        novoGrupo.gerarArquivosJSONIndividuais() # gerar JSON individual por pesquisador

        if not somente_json:
            # copiar css
            copiarArquivos(novoGrupo.obterParametro('global-diretorio_de_saida'))

        # finalizando o processo
        print ('\n[PARA REFERENCIAR/CITAR ESTE SOFTWARE USE] \n\
    Jesus P. Mena-Chalco & Roberto M. Cesar-Jr.\n\
    scriptLattes: An open-source knowledge extraction system from the Lattes Platform.\n\
    Journal of the Brazilian Computer Society, vol.15, n.4, páginas 31-39, 2009.\n\
    http://dx.doi.org/10.1007/BF03194511\n')

    tempo_final = datetime.datetime.now()
    tempo_decorrido = formatar_tempo_decorrido(tempo_final - tempo_inicial)
    print(f"scriptLattes executado em: {tempo_decorrido}.\n")

def main():
    parser = argparse.ArgumentParser(description='scriptLattes runner')
    parser.add_argument('config', help='Configuration file')
    parser.add_argument('--somente-json', action='store_true', help='Generate JSON files only')
    args = parser.parse_args()

    executar_scriptLattes(args.config, somente_json=args.somente_json)

if __name__ == "__main__":
    main()
