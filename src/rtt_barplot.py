import json, sys
import matplotlib.pyplot as plt
import numpy as np

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file) as f:
    hops = json.loads(f.read())

rtt_acumulado = []

for hop in hops:
	mierda = [int(medicion['rtt'][:-3]) for medicion in hop if medicion['rtt'] != '*']
	rtt_acumulado.append ( np.average( mierda ) if len(mierda) >0 else 0  )
    
# rtt_acumulado = [(np.average([int(med["rtt"][:-3])
#                               if med["rtt"]!='*' else np.nan
#                           for med in hop]))
#                  for hop in hops]

hop_number = range(1, len(rtt_acumulado) + 1)
ind = np.arange(len(hop_number))
width = 1.0

plt.bar(ind, rtt_acumulado, width)
plt.xticks(ind + width / 2.0, hop_number)
plt.xlabel('Hop number')
plt.ylabel('Round trip time(ms)')
plt.savefig(output_file)
