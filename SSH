import paramiko
import getpass
import time
import sys
import netmiko
def SshCiscoHP(ip,user,senha):
  #Para SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip,username=user,password=senha)
    tn = ssh.invoke_shell()
    return tn 

def SwiCisco(ip,user,password,vlans,nome,vlDados):

    tn=SshCiscoHP(ip,user,password)
    print("\nComandos efetuados SWI: ",ip)
    #comandos de configuracao
    tn.send("ena\n")
    tn.send("configure terminal\n")
    tn.send("hostname SWI"+ str(nome) + "\n")
    
    for vl in range (2,vlans+1):
        tn.send('vlan ' + str(vl) + '\n')
        tn.send('name VLAN' + str(vl) + '\n')
    
    for iface in range (5,10):
            tn.send('int fa1/' + str(iface) + '\n')
            tn.send('switchport mode access\n')
            tn.send('switchport access vlan ' + str(vlDados) + '\n')
   
    tn.send("end\n")
    time.sleep(1)
    output = tn.recv(65535)
    print (output)
    tn.close

def RoteadorCisco(ip,user,password,nome,nunInt):
    tn=SshCiscoHP(ip,user,password)
    print("\nComandos efetuados Roteador: ",ip)
    #comandos de configuracao
    tn.send("configure terminal\n")
    tn.send("hostname SWI"+ str(nome) + "\n")
    
    tn.send('int g2/0\n')
    tn.send('ip add 10.0.' + str(nunInt) + '.254 255.255.255.0\n')
    tn.send('no shutdown\n')
    tn.send('exit\n')
    tn.send('router ospf 1\n')
    tn.send('passive-interface g2/0\n')
    tn.send('network 10.0.' + str(nunInt) + '.0 0.0.0.255 area 0\n')
    tn.send('network 192.168.0.0  0.0.0.255 area 0\n')
    
    tn.send('end\n')
    time.sleep(1)
    output = tn.recv(65535)
    print (output)
    tn.close

def RoteadorHP(ip,user,password,nome,nunInt):
    tn=SshCiscoHP(ip,user,password)
    print("\nComandos efetuados Roteador: ",ip)
    #comandos de configuracao
    tn.send('system-view\n')
    tn.send('hostname R' + str(nome) + '\n')
    
    tn.send('interface g2/0\n')
    tn.send('ip add 10.0.' + str(nunInt) + '.254 255.255.255.0\n')
    tn.send('ospf 1\n')
    tn.send('silent-interface g2/0\n')
    tn.send('area 0\n')
    tn.send('network 10.0.' + str(nunInt) + '.0 0.0.0.255\n')
    tn.send('network 192.168.0.0  0.0.0.255\n')
    
    tn.send('end\n')
    time.sleep(1)
    output = tn.recv(65535)
    print (output)
    tn.close

def SwiHP(ip,user,password,vlans,nome,vlDados):
   
    tn=SshCiscoHP(ip,user,password)
    print("\nComandos efetuados SWI HP: ",ip)
    #comandos de configuracao
    tn.send('system-view\n')
    tn.send('hostname R' + str(nome) + '\n')
    
    for vl in range (2,vlans+1):
        tn.send('vlan ' + str(vl) + '\r')
        tn.send('name VLAN' + str(vl) + '\r')
        tn.send('exit\r')
    
    for iface in range (5,10):
        tn.send('inter g' + str(iface) + '/0\r')
        tn.send('port access vlan ' + str(vl_dados) + '\r')     

    tn.send("end\n")
    time.sleep(1)
    output = tn.recv(65535)
    print (output)
    tn.close

def SwiMikrotik(ip,user,password,nome,vlans):
  
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=ip,username=user,password=password)
    except Exception:
        print("conexao nao estabelecida..",ip)
        return
    
    print("\nConfiguracao efetuada: "+str (ip))
    print('< system identity set name=S + str(%s) +  >\r'%(nome))
    #comandos de configuracao
    ssh.exec_command('system identity set name=S' + str(nome) + '\r')
    
    for vl in range (2,vlans +1):
            print("< vlan + str(%s) + >\r" %(vl))
            ssh.exec_command('vlan ' + str(vl) + '\r')
            print("< interface vlan add name=VLAN + str(%s) + vlan-id= + str(%s) + interface=ether1\rs >"%(vl,vl))
            ssh.exec_command('interface vlan add name=VLAN' + str(vl) + ' vlan-id=' + str(vl) + ' interface=ether1\rs')   
    print("< quit >\r")
    ssh.exec_command('quit\r')
    
    ssh.close()

def RoteadorMikrotik(ip,user,password,nome,nunInt):
  
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=ip,username=user,password=password)
    except Exception:
        print("conexao nao estabelecida..",ip)
        return
    #comandos de configuracaos
    print("\nConfiguracao efetuada: "+str (ip))
    print("<system identity set name=R' + str(%s) + '\r' >"%(nome))
    ssh.exec_command('system identity set name=R' + str(nome) + '\r')
    print("< ip address add address=10.0.' + str(%s) + '.254/24 interface=ether2\r >"%(nunInt))
    ssh.exec_command('ip address add address=10.0.' + str(nunInt) + '.254/24 interface=ether2\r')
    print("< routing ospf instance add name=default\r >")
    ssh.exec_command('routing ospf instance add name=default\r')
    print("< routing ospf network add network=10.0' + str(%s) + '.0/24 area=backbone\r >"%(nome))
    ssh.exec_command('routing ospf network add network=10.0' + str(nome) + '.0/24 area=backbone\r')
    print("< routing ospf network add network=192.168.0.0/24 area=backbone\r >")
    ssh.exec_command('routing ospf network add network=192.168.0.0/24 area=backbone\r')
    print("< quit\r> ")    
    ssh.exec_command('quit\r')

    ssh.close()
    
def RoteadorJunipe(Ip,user,password,nome,nunInt):
    iosv_l2 = {
    'device_type': 'juniper',
    'ip': Ip,
    'username': user,
    'password': password,
    }
    tn = netmiko.ConnectHandler(**iosv_l2)
    
    print("\nConfigurando Roteador Juniper "+str(Ip))
    tn.config_mode()
    tn.send_command('set system host-name R-'+str(nome)+'\r')
    tn.send_command('set interfaces em1 unit 0 family inet address 10.0.' + str(nunInt) + '.254/24\r')
    tn.send_command('set protocols ospf area 0.0.0.0 interface em0\r')
    tn.send_command('set protocols ospf area 0.0.0.0 interface em1 passive\r')
    
    protocolos=tn.send_command("show protocols\r")
    tn.commit()
    tn.disconnect()
    print(protocolos)

user = raw_input('Entre com o usuario SSH: ')
senha = getpass.getpass('Senha: ')
no_sw_rot= int(input('Entre com o numero de switches e roteadores a serem configurados: '))
vl_dados = raw_input('Entre com a VLAN de Dados (ex: 10): ')
vlans=int(input("Informe a quantidade de VLANS para configurar: "))
cont=1
for cl in range(1,(1+no_sw_rot)):
    
    if(cl % 2 == 0):#Rotedor
        if(cont == 2):
            RoteadorHP("192.168.0."+str(cl),user,senha,cl,cl)
        elif( cont == 4):
            RoteadorCisco("192.168.0."+str(cl),user,senha,cl,cl)            
        elif(cont == 6):
            RoteadorMikrotik("192.168.0."+str(cl),user,senha,cl,cl)
        elif(cont==8):
            RoteadorJunipe("192.168.0."+str(cl),user,"a123456",cl,cl)

    if(cl % 2 ==1 ):#switches
        if(cont == 1):
            SwiHP("192.168.0."+str(cl),user,senha,vlans,cl,vl_dados)
        elif(cont == 3):
            SwiCisco("192.168.0."+str(cl),user,senha,vlans,cl,vl_dados)            
        elif(cont == 5):
            SwiMikrotik("192.168.0."+str(cl),user,senha,cl,vlans)
        elif(cont==7):
            SwiCisco("192.168.0."+str(cl),user,senha,vlans,cl,vl_dados)

    cont=cont+1
