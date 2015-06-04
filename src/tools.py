#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Global parameters, is this ok?
DEBUG = False
#DEBUG = True
VERBOSE = False
hops_max = 10
dns_server = "8.8.8.8"
dns_recursive = True

# Constants, is this ok?
DNS_RCODE_OK = 0L
DNS_RCODE_NAME_ERROR = 3L
DNS_TYPE_A = 1

"""
Devuelve True si la ip parámetro es válida
"""
def is_valid_ipv4_address(address):
    import socket
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False
    return True

"""
Esta funcion recibe un hostname
y realiza un traceroute a la
dirección IP correspondiente

(explicar diferencia con traceroute2)
"""
def traceroute(host):
    hosts = []
    for ttl in range(1, 20):
        packet = IP(dst=url, ttl=ttl) / ICMP()
        ans = sr1(packet, verbose=0)
        host = ans[ICMP].underlayer.src
        print host
        hosts.append(host)
        if ans.type == 3:
            return hosts

"""
Esta función recibe un hostname
y lo traduce a una dirección IP.
Es un request DNS, pero hecho a mano.

Más info:
http://itgeekchronicles.co.uk/2014/05/12/scapy-iterating-over-dns-responses/
"""
def dns_resolve(host):
    from scapy.all import sr1, IP, UDP, DNS, DNSQR
    rd = 1 if dns_recursive else 0
    res = sr1(IP(dst=dns_server)/UDP()/DNS(rd=1,qd=DNSQR(qname=host)), timeout=5, verbose=VERBOSE)
    if res[DNS].rcode != DNS_RCODE_OK:
        raise Exception('''\n\nLa query DNS para el host "%s" devolvio un código de error\nEs posible que el dominio no exista.'''%host)
    answers = res[DNS].an
    count = res[DNS].ancount
    while count > 0:
        count -= 1
        if answers[count].type == DNS_TYPE_A:
            return answers[count].rdata
    raise Exception('\n\nLa query DNS para el host "%s" no devolvió ningún registro de clase A.\nNo es posible continuar.'%host)

"""
Esta función recibe un parámetro,
y devuelve una IP válida a partir del mismo
(o levanta una excepción)
"""
def get_ip_from_parameter(host):
    dst_ip = host if is_valid_ipv4_address(host) else dns_resolve(host)
    if not is_valid_ipv4_address(dst_ip): raise Exception("\n\nLa IP %s correspondiente al parametro %s no parece ser válida."%(dst_ip,host))
    return dst_ip     


"""
Esta funcion recibe un hostname
y realiza un traceroute a la
dirección IP correspondiente

(explicar diferencia con traceroute)
"""
def traceroute2(parameter):
    from scapy.all import sr1, IP, TCP, RandShort
    dst_ip = get_ip_from_parameter(parameter)
    rcv,snd,ttl_seq = None,None,1
    print "traceroute to %s (%s), hops max %s"%(url,dst_ip,hops_max)
    while (not rcv or rcv.src!=dst_ip) and ttl_seq<=hops_max:
        print ttl_seq,
        #for snd,rcv in ans:
        #    print "#%d\t %s"%(snd.ttl,rcv.src)
        #    if DEBUG: print rcv.show()
        ans = {}
        host = "?"
        for i in range(0,3):
            ans[i] = {}
            ans[i]['sr1'] = sr1(IP(dst=dst_ip, ttl=ttl_seq, id=RandShort()) / TCP(flags=0x2), timeout=2, retry=0, verbose=VERBOSE)
            if ans[i]['sr1'] != None:
                rcv = ans[i]['sr1']
                ans[i]['time'] = "?"
                host = rcv.src
            else:
                ans[i]['time'] = "*"
        print "%s %s %s %s"%(host, ans[0]['time'], ans[1]['time'], ans[2]['time'])
        ttl_seq += 1


if __name__ == "__main__":
    from functions import *
    check_sudo()
    import sys
    url = sys.argv[1] if len(sys.argv)>1 else 'news.ycombinator.com'
    traceroute2(url)
