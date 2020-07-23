#!/usr/bin/python3

# Author: Mojtaba Miraghajanian
# Email: mem.mojtaba@gmail.com

import requests, time, logging

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w', format='%(asctime)s :: %(levelname)s: %(name)s --> %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-8s: %(levelname)-8s: %(message)s')
console.setFormatter(formatter)
logout = logging.getLogger('Logout')
logout.addHandler(console)

response = requests.get('http://hotspot.um.ac.ir/logout')
checkResponse = requests.get('http://hotspot.um.ac.ir/status')
if (checkResponse.url.split('/')[-1] == 'login'):
    logout.info('Logout successful.')
else:
    logout.warning('Logout failed.')
