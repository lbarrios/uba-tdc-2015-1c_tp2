import csv, datetime, math, subprocess, sys
from scapy.all import sr, sr1, ICMP, TCP, IP, RandShort

host = sys.argv[1]  # host al que hace el ping
n = int(sys.argv[2])  # cantidad de pings
alpha = float(sys.argv[3])  # parametro de resistencia a outliers

sample_rtts = []

for i in range(n):
    packet = IP(dst=host) / ICMP(type="echo-request")
    start = datetime.datetime.now()
    ans, unans = sr(packet, timeout=0.5, retry=0, verbose=False)
    end = datetime.datetime.now()
    sample_rtt = (end - start).microseconds / 1000
    if len(ans) == 1 and len(unans) == 0:
        sample_rtts.append(sample_rtt)

p = 1.0 - (float(len(sample_rtts)) / float(n))
print p
if p == 0.0:
    raise Exception('mathis undefinido pues p == 0. pruebe un n mas grande')

if len(sample_rtts) == 0:
    raise Exception('no answered packets')

estimated_rtt = sample_rtts[0]
for i in range(1, len(sample_rtts)):
    estimated_rtt = alpha * estimated_rtt + (1 - alpha) * sample_rtts[i]

MSS = 1460
mathis_throughput = MSS / (estimated_rtt * math.sqrt(p))

print 'estimated rtt: ', estimated_rtt  # una estimacion mejor que el promedio, ya que tiene en cuenta los outliers
print 'mathis throughput: ', mathis_throughput
