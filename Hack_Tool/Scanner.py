#-*- coding:utf-8 -*-

import optparse
from socket import *
from threading import *

#screenLock = print control
screenLock = Semaphore(value=1)

#소켓을 이용해 메세지 응답을 확인하여 연결을 확인한다.
def ConnScan(HostT, PortT):
	try:
		conn = socket(AF_INET, SOCK_STREAM)
		conn.connect((HostT, PortT))
		conn.send('vionlent python\n')
		result = conn.recv(8888)
		screenLock.acquire()
		print "%d TCP OPEN" % PortT
		print "\n" + str(result)
	except:
		screenLock.acquire()
		print "%d TCP CLosed " % PortT

	finally:
		screenLock.release()
		conn.close()

# 스레드를 이용해 포트를 스캔하여 속도를 높인다.
def PortScan(HostT, PortT):
	try:
		Target_IP = gethostbyname(HostT)
	except:
		print "cannot Resolve '%s' : Unknown Host\n" % HostT
		return 

	try:
		Target_Name = gethostbyname(Target_IP)
		print "\nScan Result For : " + Target_Name[0]
	except:
		print "\nScan Result For : " + Target_IP

	setdefaulttimeout(1)
	for port in PortT:
		print "Scanning Port " + port
		t = Thread(target=ConnScan, args=(HostT, int(port)))
		t.start()

def main():
	parser  = optparse.OptionParser(usage='Usage %prog -H <Target Host> -P <Target Port>')
	parser.add_option('-H', dest='HostT', type='string', help='Specity Target IP')
	parser.add_option('-P', dest='PortT', type='string', help='Specity Target Port')
	(options, args) = parser.parse_args()

	HostT = options.HostT
	PortT = str(options.PortT).split(',')

	if(HostT == None) | (PortT == None):
		print parser.usage
		exit(0)
	PortScan(HostT, PortT)

if __name__ == '__main__':
	main()