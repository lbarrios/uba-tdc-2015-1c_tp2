#!/usr/bin/env python
# -*- coding: utf-8 -*-                                                                                                      │

import json,os,numpy as np


def calculate_zrtt(filename):
    """ 
    Calcula el zrtt de cada hop y lo imprime por pantalla
    """
    
    with open(filename) as f:
        data = json.loads(f.read())

    avg_rtt = []
    # Calculo el rtt de cada hop
    for hop in data:
        avg = np.average([int(med["rtt"][:-3]) for med in hop if med["rtt"]!='*'])
        if not np.isnan(avg): 
            avg_rtt.append(avg)
            print avg
    #calculo el rtt promedio total
    avg_rtt_total = np.average(avg_rtt)
    rtt_std = np.std(avg_rtt)

    zrtt_list = []
    for rtt in avg_rtt:
        zrtt_list.append( (rtt - avg_rtt_total) / rtt_std )

    return zrtt_list

if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    res = calculate_zrtt(filename)
    print res
