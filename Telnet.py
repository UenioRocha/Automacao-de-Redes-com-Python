import pexpect

vl_dados = raw_input('Entre com a VLAN de Dados (ex: 10): ')
no_sw_rot = input('Entre com o numero de switches e roteadores a serem configurados: ')
user = raw_input('Entre com o usuario Telnet: ')
senha = raw_input('Entre com a senha para Telnet: ')

#Define as Funcoes  
def sw1 (): # CISCO    
    if user and senha:
        tn.expect('Username: ')
        tn.sendline(user)
        tn.expect('Password:')
        tn.sendline(senha)

        tn.sendline('conf t\n')
        tn.sendline('hostname S' + str(c1) + '\n') 

        for vl in range (2,21):
            tn.sendline('vlan ' + str(vl) + '\n')
            tn.sendline('name VLAN' + str(vl) + '\n')

        for iface in range (5,10):
            tn.sendline('int fa1/' + str(iface) + '\n')
            tn.sendline('switchport mode access\n')
            tn.sendline('switchport access vlan ' + str(vl_dados) + '\n')
   
def sw2 (): # HP
    if user and senha:
        tn.expect('login: ')
        tn.sendline(user)
        tn.expect('Password: ')
        tn.sendline(senha)

        tn.sendline('\r\n')
        tn.sendline('system-view')
        tn.sendline('hostname S' + str(c1) + '\r')

        for vl in range (2,21):
            tn.sendline('vlan ' + str(vl) + '\r')
            tn.sendline('name VLAN' + str(vl) + '\r')
            tn.sendline('exit')

        for iface in range (5,10):
            tn.sendline('inter g' + str(iface) + '/0\r')
            tn.sendline('port access vlan ' + str(vl_dados) + '\r')

def sw3 (): # MIKROTIK
    if user and senha:
        tn.sendline(user)
        tn.expect('Password:')
        tn.sendline(senha)   

        tn.sendline('\r\n') 
        tn.expect('>')
        tn.sendline('system identity set name=S' + str(c1) + '\r')

        for vl in range (2,21):
            tn.sendline('vlan ' + str(vl) + '\r')
            tn.sendline('interface vlan add name=VLAN' + str(vl) + ' vlan-id=' + str(vl) + ' interface=ether1\r')

def sw4 (): # CISCO     
    if user and senha:
        tn.expect('Username:')
        tn.sendline(user)
        tn.expect('Password:')
        tn.sendline(senha)

        tn.sendline('conf t\n')
        tn.sendline('hostname S' + str(c1) + '\n') 

        for vl in range (2,21):
            tn.sendline('vlan ' + str(vl) + '\n')
            tn.sendline('name VLAN' + str(vl) + '\n')
            tn.sendline('exit\n')

        for iface in range (5,10):
            tn.sendline('inter fa1/' + str(iface) + '\n')
            tn.sendline('switchport mode access\n')
            tn.sendline('switchport access vlan ' + str(vl_dados) + '\n')

def R1 (): # CISCO
    if user and senha:
        tn.expect('Username:')
        tn.sendline(user)
        tn.expect('Password:')
        tn.sendline(senha)

        tn.sendline('conf t\n')
        tn.sendline('hostname R' + str(c2) + '\n') 
        tn.sendline('int g2/0\n')
        tn.sendline('ip add 10.0.' + str(c2) + '.254 255.255.255.0\n')
        tn.sendline('no shutdown\n')
        tn.sendline('router ospf 1\n')
        tn.sendline('passive-interface g2/0\n')
        tn.sendline('network 10.0.' + str(c2) + '.0 0.0.0.255 area 0\n')
        tn.sendline('network 192.168.0.0  0.0.0.255 area 0\n')
        tn.sendline('end\n')

def R2 (): # HP
    if user and senha:
        tn.expect('login:')
        tn.sendline(user)
        tn.expect('Password:')
        tn.sendline(senha)

        tn.sendline('\r\n')
        tn.sendline('system-view')
        tn.sendline('hostname R' + str(c2) + '\r')
        tn.sendline('int g2/0\r')
        tn.sendline('ip add 10.0.' + str(c2) + '.254 255.255.255.0\r')
        tn.sendline('ospf \r')
        tn.sendline('silent-interface g2/0\r')
        tn.sendline('area 0\r')
        tn.sendline('network 10.0.' + str(c2) + '.0 0.0.0.255 \r')
        tn.sendline('network 192.168.0.0  0.0.0.255\n')
        tn.sendline('\r\n')

def R3 (): # MIKROTIK
    if user and senha:
        tn.sendline(user)
        tn.expect('Password:')
        tn.sendline(senha)   

        tn.sendline('\r\n') 
        tn.expect('>')
        tn.sendline('system identity set name=R' + str(c2) + '\r')
        tn.expect('>')
        tn.sendline('ip address add address=10.0.' + str(c2) + '.254/24 interface=ether2\r')
        tn.sendline('routing ospf instance add name=default\r')
        tn.sendline('routing ospf network add network=10.0' + str(c2) + '.0/24 area=backbone\r')
        tn.sendline('routing ospf network add network=192.168.0.0/24 area=backbone\r')
        tn.sendline('\r\n')
        tn.sendline('quit\r')

def R4 (): # JUNIPER
    if user and senha:
        tn.expect('login:')
        tn.sendline(user)
        tn.expect('Password:')
        tn.sendline(senha)   

        tn.sendline('\r\n')
        tn.sendline('configure\r')
        tn.expect('#')
        tn.sendline('set system host-name R' + str(c2) + '\r')
        tn.sendline('commit\r')
        tn.sendline('set interfaces em1 unit 0 family inet address 10.0.' + str(c2) + '.254/24\r')
        tn.sendline('commit\r')
        tn.sendline('set protocols ospf area 0.0.0.0 interface em0\r')
        tn.sendline('commit\r')
        tn.sendline('set protocols ospf area 0.0.0.0 interface em1 passive\r')
        tn.sendline('commit\r')
#Cria o Dicionario que Relaciona as Funcoes 
switch = { 1: sw1, 2: sw2, 3: sw3, 4: sw4, 21: R1, 22: R2, 23: R3, 24: R4,}

for c1 in range (1,no_sw_rot + 1):
    tn = pexpect.spawn('telnet 192.168.0.' + str(c1))
    switch.get(c1)() #Retorna o Dicionario 
    c2 = c1 + 20
    tn = pexpect.spawn('telnet 192.168.0.' + str(c2))
    switch.get(c2)()
