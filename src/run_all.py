import json, os, sys
import functions

url = sys.argv[1]

os.system('python traceroute.py ' + url)
functions.plot_routes(url + '.json', url + '.html')

cmd = 'xdg-open %s.html' % url
if sys.platform == 'darwin':
    cmd = 'open %s.html' % url
os.system(cmd)
