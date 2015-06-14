import json, sys
import matplotlib.pyplot as plt
import numpy as np

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file) as f:
    hops = json.loads(f.read())
    
rtt_acumulado = [(np.average([int(med["rtt"][:-3]) if med["rtt"]!='*' else np.nan
                          for med in hop]))
                 for hop in hops]
print rtt_acumulado

# rtt = []
# for i in range(len(rtt_acumulado)):
#     if i == 0:
#         hop_rtt = rtt_acumulado[0]
#     else:
#         hop_rtt = rtt_acumulado[i] - rtt_acumulado[i-1]
#     rtt.append(hop_rtt)
# print rtt

hop_number = range(1, len(rtt_acumulado) + 1)
plt.bar(hop_number, rtt_acumulado)
plt.savefig(output_file)
