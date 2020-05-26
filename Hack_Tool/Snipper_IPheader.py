#-*- coding:utf-8 -*-

import os 
import struct 
from socket import *

# 소켓으로부터 수신한 데이터의 20바이트 IP혜더를 튜플 자료형으로 변환함
def parse_ipheader(data):
	# 두번째 인자를 첫번째 인자 포맷 문자열에 맞게 변환해 퓨틀로 리턴
	ipheader = struct.unpack('!BBHHHBBH4s4s', data[:20])
	return ipheader

# ipheader의 2번째 헤더 필드인 Total Length을 리턴
def getDatagramSize(ipheader):
	return ipheader[2]

# 어떠한 프로토콜을 사용했는지 확인
def getProtocol(ipheader):
	protocols = {1:'ICMP', 6:'TCP', 17:'UDP'}
	proto = ipheader[6]
	if proto in protocols:
		return protocols[proto]
	else:
		return 'OTHERS'

def getIP(ipheader):
	src_ip = inet_ntoa(ipheader[8]) #바이트 -> IP 주소형식
	dst_ip = inet_ntoa(ipheader[9])
	return (src_ip, dst_ip)

def recvData(sock):
	data = ''
	try:
		data = sock.recvfrom(65565)
	except timeout:
		data = ''
	return data[0]

def sniffing (host):
	if os.name == 'nt':
		sock_protocol = IPPROTO_IP
	else:
		sock_protocol = IPPROTO_ICMP

	sniffer = socket(AF_INET, SOCK_RAW, sock_protocol)
	sniffer.bind((host,0))
	sniffer.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)

	if os.name == 'nt':
		sniffer.ioctl(SIO_RCVALL, RCVALL_OFF)

	count = 1
	try:
		while True:
			data = recvData(sniffer)
			ipheader = parse_ipheader(data[:20])
			DatagramSize = getDatagramSize(ipheader)
			protocol = getProtocol(ipheader)
			src_ip, dst_ip = getIP(ipheader)
			print "\nSNIFFED [%d] ++++++++" %count
			print "Datagram SIZE:\t%s " % str(DatagramSize)
			print "protocol:\t%s" % protocol
			print "Source IP:\t%s" % src_ip
			print "Destination IP:\t%s" %dst_ip
			count += 1
	except KeyboardInterrupt:
		if os.name == 'nt':
			sniffer.ioctl(SIO_RCVALL, RCVALL_OFF)

def main():
	host = gethostbyname(gethostname())
	print "START Sniffer at [%s]" % host
	sniffing(host)

if __name__ == '__main__':
	main()