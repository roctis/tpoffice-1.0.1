#!/usr/bin/python     
#Declaring object

class TCP_connection_SERVER:
    'class for connection oriented connected for file transfer'
    tcp_conn_count=0
    clients_addrs=[]
    def __init__(self, (host_port), buffer_size, backlog):
        self.host_port=host_port
        self.buffer_size=buffer_size
        self.backlog=backlog
        #create tcp socket and binding
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(host_port)
        self.s.listen(backlog)
        
    
    def connection_establish(self):
        self.s.setblocking(0)
        try:
            client, addr =self.s.accept()
            clients_addrs=(client, addr)
            #print addr
            if clients_addrs not in TCP_connection_SERVER.clients_addrs:
               TCP_connection_SERVER.clients_addrs.append(clients_addrs)
               
            TCP_connection_SERVER.tcp_conn_count+=1
        except:
            pass
            
        return True
     
     
    def receive_send_file(self, filename, address=False,dest_address=False,only_to_server=False):
        present_client, present_addr=self.get_req_socket(address)
        present_client.settimeout(2.0)
        f=file(filename,'wb')
        try:
            data = present_client.recv(self.buffer_size)
            while data:
                f.write(data)
                data = present_client.recv(self.buffer_size)
        except socket.timeout:
            f.close()
            print "Received File: %s" % (filename)
        if len(TCP_connection_SERVER.clients_addrs)>1 and not only_to_server:
            self.send_file(filename, present_client)
        if len(TCP_connection_SERVER.clients_addrs)>1 and dest_address:
            self.send_file(filename, present_client,dest_address)

        
                
    def send_file(self,filename, present_client, addr=False):
        print "Sending file"
        if not addr:
            for available_client , available_addr in TCP_connection_SERVER.clients_addrs:
                if(present_client!=available_client):
                    f=open(filename, 'rb')
                    data=f.read(1024)
                    try:
                        while data:
                            available_client.send(data)
                            data=f.read(1024)
                        f.close()
                        available_client.send("@!&^")
                    except socket.error:
                        print "Removing Client"
                        rm_dead_socket(available_addr)
                        pass
        
        else:
            dest_client, dest_addr=self.get_req_socket(addr)
            f=open(filename, 'rb')
            data=f.read(1024)
            while data:
                dest_client.send(data)
                data=f.read(1024)
            f.close()

        if rm_server_temp_files:
            os.remove(filename)

            
        
            
                
    def get_req_socket(self, addr):
        
        i=-1
        flag=False
        if len(TCP_connection_SERVER.clients_addrs)>1:
            for sending_client, sending_addr in TCP_connection_SERVER.clients_addrs:
                i+=1
                #print sending_addr[0]
                #print addr[0]
                if sending_addr[0]==addr[0]:
                    flag=True
                    break
            return TCP_connection_SERVER.clients_addrs[i]
            
        else:
            return TCP_connection_SERVER.clients_addrs[0]

    def rm_dead_socket(self, addr):

        i=-1
        flag=False
        if len(TCP_connection_SERVER.clients_addrs)>1:
            for listed_client, listed_addr in TCP_connection_SERVER.clients_addrs:
                i+=1
                #print sending_addr[0]
                #print addr[0]
                if listed_addr[0]==addr[0]:
                    flag=True
                    break
            del TCP_connection_SERVER.clients_addrs[i]

        else:
            del TCP_connection_SERVER.clients_addrs[0]
            
        
                
    def add_clients(self, client):
        if client not in TCP_connection_SERVER.clients:
            TCP_connection_SERVER.clients.append(client)    
        #return TCP_connection_SERVER.clients
        
    def close_socket(self):
        self.s.close()
    
    


class UDP_connection_SERVER:
    'Class for connection less connection for message transfer'
    udp_conn_count=0
    clients=[]
    def __init__(self, (host_port), buffer_size):
        self.host_port=host_port
        self.buffer_size=buffer_size
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(host_port)
        UDP_connection_SERVER.udp_conn_count+=1
        
    def receive_message(self):
        'receive udp message'
        self.data,self.addr = self.s.recvfrom(self.buffer_size)
        self.data=str(self.data)
        return (self.data, self.addr)
               
    def add_client_address(self):
        if self.addr not in UDP_connection_SERVER.clients:
            UDP_connection_SERVER.clients.append(self.addr)    
        return UDP_connection_SERVER.clients
        
    def display_message(self):
        print "["+time.ctime(time.time())+str(self.addr)+"]"+self.data
        
    def send_to_clients(self, msg=False):
        if msg:
            self.data=msg
        for client in UDP_connection_SERVER.clients:
            if client !=self.addr:
                try:
                    self.s.sendto(self.data,  client)
                    return True 
                except:
                    return False        
    
    def close_socket(self):
        self.s.close()
            


#Functions

#def tcp_send_file(self,data):
        
        
def get_server_temp_path(fname, dir):
    if not os.path.isdir(dir): os.makedirs(dir)
    fname=dir+fname
    return fname

def get_filename(data):
    fname=data.split('#')
    return fname[1]

def get_address(data):
    fname=data.split('#')
    return fname[2]

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])
    


if __name__ == '__main__':
    import sys
    import getopt
    import os
    import time
    import socket
    import fcntl
    import struct
    import select

    
    print
    #args, sources = getopt.getopt(sys.argv[1:])
    

#FLAGS
    rm_server_temp_files=True
    server_shutdown=False
    
#global variables
    HOST =get_ip_address('wlan0')
    PORT = 5000
    host_port=(HOST, PORT)
    buffer_size=8000
    backlog=5
    
 #program
    print "SERVER started with ip="+HOST
    text=UDP_connection_SERVER(host_port, buffer_size)
    doc=TCP_connection_SERVER(host_port, buffer_size, backlog)
    
 
    while not server_shutdown:
        doc.connection_establish()
        msg=text.receive_message()
        if msg[0].find('@!file@!')!=-1:
            file_name=get_filename(msg[0])
            text.send_to_clients("@!file@!#"+file_name)
            file_name=get_server_temp_path(file_name, 'server-dl/')
            doc.receive_send_file(file_name, msg[1],False,only_to_server=False)
        elif msg[0].find('@!fileto@!')!=-1:
            file_name=get_filename(msg[0])
            text.send_to_clients("@!file@!#"+file_name)
            file_name=get_server_temp_path(file_name, 'server-dl/')
            doc.receive_send_file(file_name, msg[1], msg[2],only_to_server=False)
        elif msg[0].find('@!filetos@!')!=-1:
            file_name=get_filename(msg[0])
            file_name=get_server_temp_path(file_name, 'server-dl/')
            doc.receive_send_file(file_name, msg[1],False,only_to_server=True )
        
        elif msg[0].find('>xtheserver<')!=-1:
            server_shutdown=True
            
        else:
            add_client=text.add_client_address()
            text.display_message()
            send_all=text.send_to_clients()
        time.sleep(0.2)
        
    text.close_socket()
    doc.close_socket()

