# Author: Mojtaba Miraghajanian
# Email: mem.mojtaba@gmail.com

import requests, time, logging

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w', format='%(asctime)s :: %(levelname)s: %(name)s --> %(message)s')

response = requests.get('http://hotspot.um.ac.ir/logout')
checkResponse = requests.get('http://hotspot.um.ac.ir/status')
if (checkResponse.url.split('/')[-1] == 'login'):
    logging.info('Logout successful.')
else:
    logging.warning('Logout failed.')
