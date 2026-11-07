# Syslog-resend-events

This script aims to resend syslog events during SIEM or Syslog server ingestion configuration.

Usage:

```
user$ python3 send_event.py -h
usage: send_event.py [-h] -i  [-d ] [-s ] [-p ] [-o] [-m ] [-a ] [-y ] [-u ] [-r ] [-t] [-f]

options:
  -h, --help  show this help message and exit
  -i          Raw events file path
  -d          Destination IP, default is 127.0.0.1
  -s          Source IP, default is 127.0.0.1
  -p          Destination port, default is 514
  -o          Use old Syslog RFC3164, deafult is RFC5424
  -m          Specify Hostname in syslog header, default is "hostname"
  -a          App name used in RFC5424, default is "syslog_test"
  -y          Process ID used in RFC5424, default is -
  -u          Message ID used in RFC5424, default is -
  -r          Priority, default is 42
  -t          Use TCP, default is UDP
  -f          Use octet framing with tcp, like syslog()

```

Example, send via UDP and RFC3164 (with UDP you can spoof source IP address, so you need sudo):

```
user$ sudo python3 send_event.py -i input.txt -o -s 10.10.10.10
[+] Sending events from 10.10.10.10 to 127.0.0.1 on UDP port 514 ...
[+] Packet sent:  <42>Nov  7 13:31:48 hostname sudo[4146]: pam_unix(sudo-i:session): session closed for user root 
[+] Packet sent:  <42>Nov  7 13:31:49 hostname sudo[4146]:     user : TTY=pts/2 ; PWD=/root ; USER=root ; COMMAND=/bin/bash 
[+] Packet sent:  <42>Nov  7 13:31:50 hostname sudo[4146]: pam_unix(sudo-i:session): session opened for user root(uid=0) by user(uid=1000) 
[+] Sending complete
user$
```

Example, send via TCP and RFC3164:

```
user$ python3 send_event.py -i input.txt -o -t
[+] Sending events from 127.0.0.1 to 127.0.0.1 on TCP port 514 ...
[+] Packet sent:  <42>Nov  7 13:35:02 hostname sudo[4146]: pam_unix(sudo-i:session): session closed for user root 
[+] Packet sent:  <42>Nov  7 13:35:03 hostname sudo[4146]:     user : TTY=pts/2 ; PWD=/root ; USER=root ; COMMAND=/bin/bash 
[+] Packet sent:  <42>Nov  7 13:35:04 hostname sudo[4146]: pam_unix(sudo-i:session): session opened for user root(uid=0) by user(uid=1000) 
[+] Sending complete
user$ 
```

Example, send via TCP and RFC5424:

```
user$ python3 send_event.py -i input.txt -t 
[+] Sending events from 127.0.0.1 to 127.0.0.1 on TCP port 514 ...
[+] Packet sent:  <42>1 2026-11-07T13:36:36+05:00 hostname syslog_test - - - sudo[4146]: pam_unix(sudo-i:session): session closed for user root 
[+] Packet sent:  <42>1 2026-11-07T13:36:37+05:00 hostname syslog_test - - - sudo[4146]:     user : TTY=pts/2 ; PWD=/root ; USER=root ; COMMAND=/bin/bash 
[+] Packet sent:  <42>1 2026-11-07T13:36:38+05:00 hostname syslog_test - - - sudo[4146]: pam_unix(sudo-i:session): session opened for user root(uid=0) by user(uid=1000) 
[+] Sending complete
user$ 
```

Example, send via TCP and RFC5424 + Octet Framing:

```
user$ python3 send_event.py -i input.txt -t -f
[+] Sending events from 127.0.0.1 to 127.0.0.1 on TCP port 514 ...
[+] Packet sent:  127 <42>1 2026-11-07T13:37:52+05:00 hostname syslog_test - - - sudo[4146]: pam_unix(sudo-i:session): session closed for user root 
[+] Packet sent:  137 <42>1 2026-11-07T13:37:53+05:00 hostname syslog_test - - - sudo[4146]:     user : TTY=pts/2 ; PWD=/root ; USER=root ; COMMAND=/bin/bash 
[+] Packet sent:  152 <42>1 2026-11-07T13:37:54+05:00 hostname syslog_test - - - sudo[4146]: pam_unix(sudo-i:session): session opened for user root(uid=0) by user(uid=1000) 
[+] Sending complete
user$ 
```

