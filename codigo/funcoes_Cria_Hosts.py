"""
#####################################################################################################
#
#                                       cria_hosts_Tabela_para_ZABBIX.py
#
#####################################################################################################
#
#   Descrição: Esse código contém todas as funções responsáveis para a leitura da tabela
#               e a criação dos hosts no Zabbix
#
#   Versão: 16/06/2021 - V1.0
#
#   Desenvolvido por: Rodrigo Broslavschi de Oliveira
#   email: rodrigoliveira132@gmail.com
#
#####################################################################################################
"""
from estrutura_API_ZABBIX import * #Nesse código tem vários dicionários que são utilizados como estrutura para o código
import json, openpyxl, requests, re
import pandas as pd


class Le_Tabela():
    # Inicia abrindo a tabela dos hosts
    def __init__(self, tabela):
        doc_planilha = openpyxl.load_workbook(tabela)
        self.planilha = doc_planilha['Hosts']
        self.hosts = []
        self.le_tabela()

    # Faz a leitura da tabela e monta um DataFrame para depois criar os hosts no zabbix
    # Basicamente é transformar um arquivo de tabela numa """"""variável Tabela""""", ajuda muito com o tratamento
    #   das informações
    def le_tabela(self):
        index = ['Host', 'Visible_Name', 'Grupos', 'Interfaces_Tipo', 'Interfaces_IP', 'Interfaces_Porta',
                 'Descricao', 'Templates']
        dados_hosts =[]
        #Faz a leitura de todas as linhas da tabela a partir da linha 4
        for num_linha in range(4, self.planilha.max_row + 1):
            validacao_linha = True
            for celula in range(2, self.planilha.max_column + 1):
                verificacao_celula = self.verifica_celula(num_linha, celula)
                if not verificacao_celula:
                    validacao_linha = False
                    break
                else:
                    validacao_linha = True
            if validacao_linha == True:
                dados_hosts.append(self.le_linha(num_linha))
                self.hosts = pd.DataFrame(data=dados_hosts, columns=index) # Cria o DataFrame

    #Separa todas as informações da linha específica
    def le_linha(self, num_linha):
        host = self.planilha.cell(num_linha, 2).value
        visible_name = self.planilha.cell(num_linha, 3).value
        grupos = (self.planilha.cell(num_linha, 4).value).split(',')
        interfaces_tipo = (self.planilha.cell(num_linha, 5).value).split(',')
        interfaces_ip = (self.planilha.cell(num_linha, 6).value).split(',')
        interfaces_porta = str((self.planilha.cell(num_linha, 7).value)).split(',')
        descricao = self.planilha.cell(num_linha, 8).value
        templates = (self.planilha.cell(num_linha, 9).value).split(',')
        dados_host = [host, visible_name, grupos, interfaces_tipo, interfaces_ip, interfaces_porta, descricao, templates]
        return dados_host

    # Verifica se a célula está vazia, se estiver o código alerta
    def verifica_celula(self, numero_linha, numero_coluna):
        valor_celula = self.planilha.cell(numero_linha, numero_coluna).value
        if not valor_celula:
            print('Verifique a linha {} célula {}'.format(numero_linha, numero_coluna))
            return None
        else:
            return valor_celula

# Classe utilizada para fazer a comunicação com a API do zabbix, incrível essa API ajuda bastante !!!!!
class Zabbix():
    header = {'content-type': 'application/json'}

    # Inicia com as informações básicas para estabelecer uma comunicação com o ZABBIX

    def __init__(self, usuario, senha, endereco_url):
        self.url = endereco_url
        autenticacao["params"]["user"] = usuario
        autenticacao["params"]["password"] = senha

        resposta_zbx = self.envia_comando_json(autenticacao)

        # Nessa parte se os dados estiverem certos o zabbix responderá com um token
        if "error" in resposta_zbx:
            result = resposta_zbx["error"]["data"]
            print(result)
            print("Verifique url, header, user ou password !!!")
            print("Código sendo finalizado")
            exit()
        else:
            self.token = resposta_zbx["result"]
            # result = "Token gerado com sucesso"

    # Função utilizada para envia e receber os dados do ZABBIX
    def envia_comando_json(self, comando):
        res = requests.post(self.url, data=json.dumps(comando), headers=self.header)
        resposta = json.dumps(res.json(), indent=4, sort_keys=True)
        resultado = json.loads(resposta)
        return resultado

    # Função utilizada para consultar o id do Grupo
    def consulta_id_grupo_hosts(self, nome_Grupo):
        consultas["hostgroup"]["params"]["filter"]["name"] = nome_Grupo
        consultas["hostgroup"]["auth"] = self.token
        resposta_zbx = self.envia_comando_json(consultas["hostgroup"])
        if not resposta_zbx['result']:
            result = None
        else:
            result = resposta_zbx['result'][0]['groupid']
        return result

    # Essa função primeiro verefica se o grupo existe, se não existir ele cria o grupo
    def cria_grupo(self, nome_grupo):
        nome_grupo = re.sub('^\s*', '', nome_grupo)
        nome_grupo = re.sub('\s*$', '', nome_grupo)
        id_grupo = self.consulta_id_grupo_hosts(nome_grupo) # Verifica se o grupo existe
        if id_grupo == None:
            criacao["hostgroup"]["params"]["name"] = nome_grupo
            criacao["hostgroup"]["auth"] = self.token
            resposta_zbx = self.envia_comando_json(criacao["hostgroup"])
            if "error" in resposta_zbx:
                print('Erro cria Host Group', nome_grupo)
                result = resposta_zbx['error']['data']
            else:
                result = resposta_zbx['result']['groupids'][0]
            return result
        return id_grupo

    # Função utilizada para consultar o ID do Host
    def consulta_id_hosts(self, host_name):
        consultas['hostname']['params']['filter']['name'] = host_name
        consultas["hostname"]["auth"] = self.token
        resposta_zbx = self.envia_comando_json(consultas['hostname'])
        if not resposta_zbx['result']:
            result = None
        else:
            result = resposta_zbx['result'][0]['hostid']
        return result

    # Função utilizada para consultar o ID do Template
    def consulta_id_template(self, template_name):
        nome_template = re.sub('^\s*', '', template_name)
        nome_template = re.sub('\s*$', '', nome_template)
        consultas['template_id']['params']['filter']['host'] = nome_template
        consultas['template_id']["auth"] = self.token
        resposta_zbx = self.envia_comando_json(consultas['template_id'])
        if not resposta_zbx['result']:
            print('ERRO Template [{}] não encontrado, verifique o nome!!!!'.format(nome_template))
            result = None
        else:
            result = resposta_zbx['result'][0]['templateid']
        return result

    # Função utilizada para criar todos os Hosts da tabela
    # Tem como parâmetro o DataFrame "variável tabela"
    def cria_hosts(self, hosts_DataFrame):
        for index, linha in hosts_DataFrame.hosts.iterrows(): #Faz a leitura de cada linha da "Variável Tabela"
            print(linha)   # ----------- Descomente essa linha para ver a estrutura do seu DataFrame ---------- #
            interfaces = []
            grupos = []
            templates = []
            id_grupo = {'groupid': None}
            id_template = {"templateid": None}
            agente_interface = 0
            snmp_interface = 0
            # Essa parte faz a leitura de todas as interfaces cadastradas numa célula separadas por , "vírgula"
            for numero_interface in range(0, len(linha['Interfaces_Tipo'])):
                tipo = linha['Interfaces_Tipo'][numero_interface].replace(' ', '') #tem que usar o replace para remover o espaço que pode ser deixado no início da str
                ip = linha['Interfaces_IP'][numero_interface].replace(' ', '')
                porta = linha['Interfaces_Porta'][numero_interface].replace(' ', '')

                interface_dict['ip'] = ip
                interface_dict['port'] = porta

                if tipo == 'Agente':
                    interface_dict['type'] = 1
                    # toda interface precisa de um default essa parte faz que o primeiro Agent seja default
                    if agente_interface == 0:
                        interface_dict['main'] = 1
                    else:
                        interface_dict['main'] = 0
                    try:
                        del interface_dict['details']
                    except:
                        pass
                    agente_interface += 1
                elif tipo == 'SNMP':
                    interface_dict['type'] = 2
                    interface_dict['details'] = {
                        'version': 2,
                        'bulk': 1,
                        'community': '{$SNMP_COMMUNITY}'}
                    # toda interface precisa de um default essa parte faz que o primeiro SNMP seja default
                    if snmp_interface == 0:
                        interface_dict['main'] = 1
                    else:
                        interface_dict['main'] = 0
                    snmp_interface += 1

                interfaces.append(interface_dict.copy())

            # Faz a consulta de todos os grupos da célula separados por , "Vírgula"
            for grupo in linha['Grupos']:
                id_grupo['groupid'] = self.cria_grupo(grupo)
                grupos.append(id_grupo.copy())

            # Faz a consulta de todos os grupos da célula separados por , "Vírgula"
            for template in linha['Templates']:
                id_template['templateid'] = self.consulta_id_template(template)
                templates.append(id_template.copy())

            # Monta a estrutura do Json que será enviada para o Zabbix
            #   no site do ZABBIX tem todas as informações dessa estrutura
            criacao['host']['params']['host'] = linha['Host']
            criacao['host']['params']['name'] = linha['Visible_Name']
            criacao['host']['params']['interfaces'] = interfaces
            criacao['host']['params']['groups'] = grupos
            criacao['host']['params']['templates'] = templates
            criacao['host']['params']['description'] = linha['Descricao']
            criacao['host']['auth'] = self.token
            resposta_zbx = self.envia_comando_json(criacao['host'])

            if "error" in resposta_zbx:
                print('Erro ao criar o Host ', linha['Host'])
                print(resposta_zbx['error']['data'])

            else:
                print('Host {} criado com sucesso!!!!'.format(linha['Host']))
