#! /usr/bin/env python
#-*- coding:utf-8 -*-
# version : Python 2.7.13

import time
import socket

def doConnect(host,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try :         
        sock.connect((host,port))
    except :
        pass 
    return sock
        
def main():   
    host,port = "101.132.163.200",8888
    print host,port    
    sockLocal = doConnect(host,port)   
    
    while True :
        try :
            msg = str(time.time())
            sockLocal.send(msg) 
            print "send msg ok : ",msg                
            print "recv data :",sockLocal.recv(1024)
        except socket.error :
            print "\r\nsocket error,do reconnect "
            time.sleep(3)
            sockLocal = doConnect(host,port)   
        except :
            print '\r\nother error occur '            
            time.sleep(3) 
        time.sleep(1)
    
if __name__ == "__main__" :
    main()
    
