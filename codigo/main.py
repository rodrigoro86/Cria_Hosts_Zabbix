"""
#####################################################################################################
#
#                                       main.py
#
#####################################################################################################
#
#   Descrição: O main serve para mostrar como utiliza o código cria_hosts_Tabela_para_ZABBIX
#
#   Versão: 16/06/2021 - V1.0
#
#   Desenvolvido por: Rodrigo Broslavschi de Oliveira
#   email: rodrigoliveira132@gmail.com
#
#####################################################################################################
"""

from cria_hosts_Tabela_para_ZABBIX import *

tabela = Le_Tabela('ACCBS-Hosts.xlsx')

# Neste exemplo estou usando o zabbix 5.4, dependendo da versão do zabbix descomente o código abaixo
#zabbix = Zabbix('Admin', 'zabbix', "http://192.168.220.136/zabbix/api_jsonrpc.php")
#zabbix = Zabbix('Admin', 'zabbix', "http://192.168.220.136/api_jsonrpc.php")

zabbix.cria_hosts(tabela)
