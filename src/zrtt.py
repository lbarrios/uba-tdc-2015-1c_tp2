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
    # Calculo el rtt de cada hop haciendo el promedio entre todos los paquetes
    # enviados
    for hop in data:
     #    avg = np.average([int(med["rtt"][:-3]) for med in hop if med["rtt"]!='*'])
     #   if not np.isnan(avg): 
     #       avg_rtt.append(avg)
           # print avg
    
        mierda = [int(medicion['rtt'][:-3]) for medicion in hop if medicion['rtt'] != '*']
        avg_rtt.append ( np.average( mierda ) if len(mierda) >0 else 0  )
   
    #calculo de rtt haciendo la diferencia entre saltos
    avg_rtt = [avg_rtt[i] - avg_rtt[i-1] for i in range(len(avg_rtt)) if i!=0]
   
   #calculo el rtt promedio total y el desvio estandar 
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
