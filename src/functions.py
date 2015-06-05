import json, os, pygmaps

from collections import defaultdict


def check_sudo():
    'checks sudo'
    from sys import platform as _platform
    if _platform == "linux" or _platform == "linux2":
        # Linux
        if os.getuid() != 0:
            raise RuntimeError("\n\nYou need to run this script with sudo!")
    #elif _platform == "darwin":
        # MAC OS X
    #elif _platform == "win32":
        # Windows


BASE_WEIGHT = 20.0
        
def plot_routes(input_file, output_file):
    'plots routes with different weights on a google map'
    route_map = pygmaps.maps(37.428, -122.145, 16)

    with open(input_file) as f:
        data = json.reads(f.read())

    previous_node = (-34.5450875, -58.4395502)
        
    for hop in data:
        n = len(hop)
        freqs = defaultdict(int)
        for med in hop:
            ip = med['ip']
            hostname = med['hostname']
            freqs[ip] += 1
        for ip, freq in freqs.items():
            path = (previous_node, get_coords(ip))
            weight = BASE_WEIGHT * float(freq) / n
            route_map.addpath(path, "#FF0000", weight)

        previous_node = get_coords(freqs.items().sort(lambda x: x[1])[0]['ip'])
        
    route_map.draw(output_file)
