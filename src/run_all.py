import json, os, sys
import functions

url = sys.argv[1]

os.system('python traceroute.py ' + url)
functions.plot_routes(url + '.json', url + '.html')
os.system('open %s.html' % url)
