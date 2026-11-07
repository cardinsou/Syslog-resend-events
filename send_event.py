#!/usr/bin/python3

import sys
import time
import socket
import argparse
import datetime
from scapy.all import *
from zoneinfo import ZoneInfo

def prepareRFC3164Packet(message,hostname,priority):
    timestamp = datetime.now().strftime("%b %e %H:%M:%S")
    syslogPayload = f"<{priority}>{timestamp} {hostname} {message}"
    return syslogPayload

def prepareRFC5424Packet(message,hostname,appName,procID,messageID,priority):
    timestamp = datetime.now(ZoneInfo("Europe/Rome")).strftime("%Y-%m-%dT%H:%M:%S%:z")
    syslogPayload = f"<{priority}>1 {timestamp} {hostname} {appName} {procID} {messageID} - {message}"
    return syslogPayload

def sendUDP(sourceIP,destinationIP,destinationPort,syslogPayload):
    ip = IP(src=sourceIP, dst=destinationIP)
    udp = UDP(sport=34567,dport=destinationPort)
    pkt = ip/udp/syslogPayload
    send(pkt,verbose=0)
    print("[+] Packet sent: ", syslogPayload, "\n")

def sendTCP(destinationIP,destinationPort,syslogPayload,octetFraming):
    if octetFraming:
        syslogPayload = f"{len(syslogPayload.encode('utf-8'))} {syslogPayload}"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.settimeout(5.0)
        client_socket.connect((destinationIP, destinationPort))
        client_socket.sendall(syslogPayload.encode('utf-8'))
    print("[+] Packet sent: ", syslogPayload, "\n")

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-i',metavar='',type=str,help='Raw events file path',required=True)
    argparser.add_argument('-d',metavar='',default='127.0.0.1',type=str,help='Destination IP, default is 127.0.0.1',required=False)
    argparser.add_argument('-s',metavar='',default='127.0.0.1',type=str,help='Source IP, default is 127.0.0.1',required=False)
    argparser.add_argument('-p',metavar='',default='514',type=str,help='Destination port, default is 514',required=False)
    argparser.add_argument('-o',action="store_true",help='Use old Syslog RFC3164, deafult is RFC5424',required=False)
    argparser.add_argument('-m',metavar='',default=str(socket.gethostname()),type=str,help='Specify Hostname in syslog header, default is "' + str(socket.gethostname()) + '"',required=False)
    argparser.add_argument('-a',metavar='',default='syslog_test',type=str,help='App name used in RFC5424, default is "syslog_test"',required=False)
    argparser.add_argument('-y',metavar='',default='-',type=str,help='Process ID used in RFC5424, default is -',required=False)
    argparser.add_argument('-u',metavar='',default='-',type=str,help='Message ID used in RFC5424, default is -',required=False)
    argparser.add_argument('-r',metavar='',default='42',type=str,help='Priority, default is 42',required=False)
    argparser.add_argument('-t',action="store_true",help='Use TCP, default is UDP',required=False)
    argparser.add_argument('-f',action="store_true",help='Use octet framing with tcp, like syslog()',required=False)
    inputArgs = argparser.parse_args()
    if inputArgs.t:
        print("[+] Sending events from 127.0.0.1 to " + inputArgs.d.strip() + " on TCP port " + inputArgs.p.strip() + " ...\n")
    else:
        print("[+] Sending events from " + inputArgs.s.strip() + " to " + inputArgs.d.strip() + " on UDP port " + inputArgs.p.strip() + " ...\n")
    try:
	    rawEvents = open(inputArgs.i.strip(),"r")
	    for event in rawEvents.readlines():
	        if event.strip(): 
	            if inputArgs.o:
	                syslogPayload = prepareRFC3164Packet(event.strip(),inputArgs.m.strip(),inputArgs.r.strip())
	            else:
	                syslogPayload = prepareRFC5424Packet(event.strip(),inputArgs.m.strip(),inputArgs.a.strip(),inputArgs.y.strip(),inputArgs.u.strip(),inputArgs.r.strip())
	            if inputArgs.t:
	                sendTCP(inputArgs.d.strip(),int(inputArgs.p.strip()),syslogPayload,inputArgs.f)        
	            else:
	                sendUDP(inputArgs.s.strip(),inputArgs.d.strip(),int(inputArgs.p.strip()),syslogPayload)
	            time.sleep(1)
	    rawEvents.close()
    except:
        print("[-] Error - ", sys.exc_info())
        print("[-] Exiting ...")
        exit(1)
    print("[+] Sending complete\n")
            
if __name__ == "__main__":
    main()
    exit(0)
