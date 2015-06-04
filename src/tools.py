#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Global parameters, is this ok?
DEBUG = False
#DEBUG = True
VERBOSE = False
hops_max = 20
dns_server = "8.8.8.8"
dns_recursive = True

# Constants, is this ok?
DNS_RCODE_OK = 0L
DNS_RCODE_NAME_ERROR = 3L
DNS_TYPE_A = 1
DNS_TYPE_PTR = 12

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

def reverse_dns_resolve(ip):
    from scapy.all import sr1, IP, UDP, DNS, DNSQR
    if DEBUG: print "Resolviendo el DNS inverso de %s"%ip
    reversed_ip = ".".join([o for o in reversed(ip.split("."))])
    res = sr1(IP(dst=dns_server)/UDP()/DNS(rd=1,qd=DNSQR(qname='%s.in-addr.arpa'%reversed_ip, qtype='PTR')), timeout=5, verbose=VERBOSE)
    #if res[DNS].rcode != DNS_RCODE_OK:
    #    raise Exception('''\n\nLa query DNS para el host "%s" devolvio un código de error\nEs posible que el dominio no exista.'''%host)
    answers = res[DNS].an
    count = res[DNS].ancount
    while count > 0:
        count -= 1
        if answers[count].type == DNS_TYPE_PTR:
            return answers[count].rdata[:-1]
    #raise Exception('\n\nLa query reverse-DNS para la IP "%s" no devolvió ningún registro de clase PTR.\n'%host)
    return "???"

"""
Esta función recibe un parámetro,
y devuelve una IP válida a partir del mismo
(o levanta una excepción)
"""
def get_ip_from_parameter(host):
    dst_ip = host if is_valid_ipv4_address(host) else dns_resolve(host)
    if not is_valid_ipv4_address(dst_ip): raise Exception("\n\nLa IP %s correspondiente al parametro %s no parece ser válida."%(dst_ip,host))
    return dst_ip     

def traceroute_sr1_to_ans_i(dst_ip,ttl_seq,timeout):
    from scapy.all import sr1, ICMP, TCP, IP, RandShort
    r = {}
    #r['sr1'] = sr1(IP(dst=dst_ip, ttl=ttl_seq, id=RandShort()) / TCP(flags=0x2), timeout=2, retry=0, verbose=VERBOSE)
    r['sr1'] = sr1(IP(dst=dst_ip, ttl=ttl_seq, id=RandShort()) / ICMP(), timeout=2, retry=0, verbose=VERBOSE)
    if r['sr1'] != None:
        r['time'] = "?"
        r['host'] = r['sr1'][IP].src
        r['hostname'] = reverse_dns_resolve(r['host'])
    else:
        r['time'] = "*"
        r['host'] = "*"
        r['hostname'] = "*"
    return r

"""
Esta funcion recibe un hostname
y realiza un traceroute a la
dirección IP correspondiente

(explicar diferencia con traceroute)
"""
def traceroute2(parameter):
    import datetime
    dst_ip = get_ip_from_parameter(parameter)
    rcv,snd,ttl_seq = None,None,1
    print "traceroute to %s (%s), hops max %s"%(url,dst_ip,hops_max)
    while (not rcv or host!=dst_ip) and ttl_seq<=hops_max:
        print "  %s"%ttl_seq,
        ans = {}
        host = "?"
        for i in range(0,3):
            start = datetime.datetime.now()
            ans[i] = rcv = traceroute_sr1_to_ans_i(dst_ip, ttl_seq, 2)
            host = ans[i]['host']
            end = datetime.datetime.now()
            delta = end-start
            ans[i]['time'] = "%s ms"%int(round( delta.total_seconds() * 1000 ))
        print "\t{:15s} {:40s}\t{:6s}\t{:6s}\t{:6s}".format(ans[0]['host'], "(%s)"%ans[0]['hostname'], ans[0]['time'], ans[1]['time'], ans[2]['time'])
        ttl_seq += 1


if __name__ == "__main__":
    from functions import *
    check_sudo()
    import sys
    url = sys.argv[1] if len(sys.argv)>1 else 'news.ycombinator.com'
    traceroute2(url)
