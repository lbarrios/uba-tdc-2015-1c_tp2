import json, sys
import matplotlib.pyplot as plt
import numpy as np
from zrtt import calculate_zrtt

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file) as f:
    hops = json.loads(f.read())

rtt_acumulado = []

for hop in hops:
    rtts_hop = [int(medicion['rtt'][:-3]) for medicion in hop if medicion['rtt'] != '*']
    rtt_acumulado.append ( np.average( rtts_hop ) if len(rtts_hop) >0 else 0  )

zrtt = calculate_zrtt(input_file)

hop_number = range(1, len(rtt_acumulado) + 1)
ind = np.arange(len(hop_number))
width = 1.0

fig, ax1 = plt.subplots()
ax1.bar(ind, rtt_acumulado, width)

ax1.set_xticks(ind + width / 2.0)
ax1.set_xticklabels(hop_number)

ax1.set_xlabel('Hop_number')
ax1.set_ylabel('Round trip time(ms)')

ax2 = ax1.twinx()
ax2.plot(ind, zrtt, 'r.')

plt.savefig(output_file)
raise Exception('final')



plt.bar(ind, rtt_acumulado, width)
plt.xticks(ind + width / 2.0, hop_number)
plt.xlabel('Hop number')
plt.ylabel('Round trip time(ms)')
plt.savefig(output_file)

fig, ax1 = plt.subplots()
t = np.arange(0.01, 10.0, 0.01)  # hop_number
s1 = np.exp(t)  # rtt_acumulado
ax1.plot(t, s1, 'b-')
ax1.set_xlabel('time (s)')
# Make the y-axis label and tick labels match the line color.
ax1.set_ylabel('exp', color='b')
for tl in ax1.get_yticklabels():
    tl.set_color('b')


ax2 = ax1.twinx()
s2 = np.sin(2*np.pi*t)
ax2.plot(t, s2, 'r.')
ax2.set_ylabel('sin', color='r')
for tl in ax2.get_yticklabels():
    tl.set_color('r')
