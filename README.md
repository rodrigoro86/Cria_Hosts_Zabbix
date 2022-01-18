
# Cria_Hosts_Zabbix

## Descrição  
No zabbix de uma forma manual é necessário clicar em muitos botões e preencher muitos campos para criar <b>UM</b> host, agora imagina o trabalho repetitivo que daria para criar 100 hosts, sendo que esses 100 hosts muda só o nome e o ip ?  
Desenvolvi esse código para facilitar essa criação, só precisa preencher uma planilha com os dados de cada host, configurar o código para encontrar o servidor do zabbix e executar, pronto você acaba de criar e monitor 100 hosts !!!   

## :arrow_forward: Executando
#### 1) Preparar um ambiente virtual, para facilitar a excução do código e não atrapalhar outros projetos: 
$ python -m venv venv

#### 2) Instalar as seguintes bibliotécas: 
1. openpyxl
2. requests
3. pandas

$ pip install <nome_biblioteca> 

#### 3) Preecher a planilha tabelas/Tabela de Hosts.xlsx com os dados dos hosts que serão criados: 
![image](https://user-images.githubusercontent.com/35868287/149992658-d563929b-fcf1-4074-80bb-433f6b82b311.png)  

<b>Host: </b>
- Nome do host.  

<b>Visible_Name:</b> 
- O nome do host que ficara visível no zabbix.  

<b>Grupos:</b> 
- Qual grupo o host vai pertencer, caso o grupo não existe o código vai criar o grupo.  
- Um host pode ter mais de um grupo, nesse caso é só separar os grupos por vírgula ",".  

<b>Interface</b> 
- Nesse campo é possível criar mais de uma interface para o mesmo host, no caso de ter mais de uma interface é só separar por vírgula ","  
- <b>Tipo -></b> é a forma que o servidor zabbix vai acessar o host, esse código aceita apenas dois tipo Agente ou SNMP  
- <b>IP -></b> Ip do host que o servidor zabbix vai fazer a consulta  
- <b>Porta -></b> A porta configurada no host para se comunicar com o servidor  

<b>Descricao </b>
- Descrição do host 

<b>Templates</b> 
- Qual ou quais templates serão utilizados pelo hosts, igual ao grupo se houver mais de um template é só separa-los por vírgula ","  

#### 4) Configurar o arquivo  codigo/run.py   
