#!/usr/bin/env python 
# encoding: utf-8
#
#  scriptLattes
#
#  Este programa é um software livre; você pode redistribui-lo e/ou 
#  modifica-lo dentro dos termos da Licença Pública Geral GNU como 
#  publicada pela Fundação do Software Livre (FSF); na versão 2 da 
#  Licença, ou (na sua opinião) qualquer versão.
#
#  Este programa é distribuído na esperança que possa ser util, 
#  mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a qualquer
#  MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
#  Licença Pública Geral GNU para maiores detalhes.
#
#  Você deve ter recebido uma cópia da Licença Pública Geral GNU
#  junto com este programa, se não, escreva para a Fundação do Software
#  Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
import sys
import argparse
import datetime
from scriptLattes.grupo import *
from scriptLattes.util import *

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='scriptLattes runner')
    parser.add_argument('config', help='Configuration file')
    parser.add_argument('--somente-json', action='store_true', help='Generate JSON files only')
    args = parser.parse_args()

    executar_scriptLattes(args.config, somente_json=args.somente_json)
