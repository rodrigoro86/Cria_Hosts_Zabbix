"""
#####################################################################################################
#
#                                       estrutura_API_ZABBIX.py
#
#####################################################################################################
#
#   Descrição: Para facilitar com o desenvolvimento do código, criei esses dict para servirem como
#                  estruturas para montar a requisição JSON utilizada pela API do ZABBIX
#   Para mais informações sobre API do Zabbix: https://www.zabbix.com/documentation/current/manual/api
#
#   Versão: 16/06/2021 - V1.0
#
#   Desenvolvido por: Rodrigo Broslavschi de Oliveira
#   email: rodrigoliveira132@gmail.com
#
#####################################################################################################
"""

autenticacao = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": "teste",
            "password": "teste"
        },
        'auth': None,
        "id": 1
}
consultas = {
    "hostgroup": {
        "jsonrpc": "2.0",
        "method": "hostgroup.get",
        "params": {
            "output": "groupid",
            "filter": {
                "name": ["teste"]
            }
        },
        "auth": "'$TOKEN'",
        "id": 1
    },
    "hostname": {
 	    "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": ["host"],
            "filter": {
                "name": ["'$NOME_HOST'"]
            }
        },
        "auth": "'$TOKEN'",
        "id": 1
    },
    "hostinterface": {
        "jsonrpc": "2.0",
        "method": "hostinterface.get",
        "params": {
            "output": ["ip"],
            "hostids": "'$ID_HOST'"
        },
        "auth": "'$TOKEN'",
        "id": 1
    },
    "hostid": {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": ["hostid"],
            "filter": {
                "name": ["'$NOME_HOST'"]
            }
        },
        "auth": "'$TOKEN'",
        "id": 1
    },
    'hosts': {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": ["name"]
        },
        "auth": "'$TOKEN'",
        "id": 1
    },
    'template_id': {
        "jsonrpc": "2.0",
        "method": "template.get",
        "params": {
            "output": "templateid",
            "filter": {
                "host": []
            }
        },
        "auth": "038e1d7b1735c6a5436ee9eae095879e",
        "id": 1
    },
}
criacao={
    "hostgroup": {
        "jsonrpc": "2.0",
        "method": "hostgroup.create",
        "params": {
            "name": "'$NOMEGRUPOHOST'"
        },
        "auth": "'$TOKEN'",
        "id": 1
    },
    "host": {
        "jsonrpc": "2.0",
        "method": "host.create",
        "params": {
            "host": "'$HOSTNAME'",
            "name": "'$VISIBLENAME'",
            "interfaces": [],
            "groups": "",
            'templates': [],
            'description': ""
        },
        "auth": "'$TOKEN'",
        "id": 1
    }
}
interface_dict = {
    "type": 1,
    "main": 1,
    "useip": 1,
    "ip": "'$IPHOST'",
    "dns": "",
    "port": "10050"
}