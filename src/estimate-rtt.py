import csv, subprocess, sys

host = sys.argv[1]  # host al que hace el ping
n = int(sys.argv[2])  # cantidad de pings
alpha = float(sys.argv[3])  # parametro de resistencia a outliers

cmd = 'ping -c %d %s' % (n, host)
output = subprocess.check_output(cmd, shell=True, executable="/bin/bash",
                                 stderr=subprocess.STDOUT)

csvreader = csv.reader(output.splitlines(), delimiter=' ')
i = -1

estimated_rtt = None
for row in csvreader:
    i += 1
    if i == 0:
        continue
    if i > n:
        break
    
    sample_rtt = float(row[-2][5:])
    if i == 1:
        estimated_rtt = sample_rtt
    estimated_rtt = alpha * estimated_rtt + (1 - alpha) * sample_rtt

print estimated_rtt  # una estimacion mejor que el promedio, ya que tiene en cuenta los outliers
