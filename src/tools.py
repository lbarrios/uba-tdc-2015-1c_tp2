from scapy.all import *

def traceroute(url):
    hosts = []
    for ttl in range(1, 20):
        packet = IP(dst=url, ttl=ttl) / ICMP()
        ans = sr1(packet, verbose=0)
        host = ans[ICMP].underlayer.src
        print host
        hosts.append(host)
        if ans.type == 3:
            return hosts

def traceroute2(url):
    ans, unans = sr(IP(dst=url, ttl=(4,25), id=RandShort()) / TCP(flags=0x2))
    for snd,rcv in ans:
        print snd.ttl, rcv.src#, isinstance(rcv.payload, TCP)
        
print traceroute2('news.ycombinator.com')
