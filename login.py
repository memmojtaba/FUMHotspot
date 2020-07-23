#!/usr/bin/python3

# Author: Mojtaba Miraghajanian
# Email: mem.mojtaba@gmail.com

import hashlib, requests, json, sched, time, sys, logging

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a', format='%(asctime)s :: %(levelname)s: %(name)s --> %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-8s: %(levelname)-8s: %(message)s')
console.setFormatter(formatter)
loginLogger = logging.getLogger('Login')
loginLogger.addHandler(console)
s = sched.scheduler(time.time, time.sleep)
if(len(sys.argv) > 1 and sys.argv[1]):
  interval = float(sys.argv[1])
else:
  interval = 300.0

def doLogin(username, password):
  md5 = hashlib.md5()
  md5.update(password.encode('utf8'))
  authData = {
    'id': 'sign_in',
    'username': username,
    'password': md5.hexdigest()
  }
  check = checkLogin()
  if(check):
    loginLogger.info(check + ' => Login successful.\n' + remaining(check))
    return True

  else:
    requests.post('https://hotspot.um.ac.ir/login', data = authData)
    check = checkLogin()
    if(check):
      loginLogger.info(check + ' => Login successful.\n' + remaining(check))
      return True
    else:
      loginLogger.warning(username + ' => Login failed.')
      return False

def checkLogin():
  # utf-8 byteCode of نام کاربری:
  usernameinBin = b'\xc3\x99\xc2\x86\xc3\x98\xc2\xa7\xc3\x99\xc2\x85 \xc3\x9a\xc2\xa9\xc3\x98\xc2\xa7\xc3\x98\xc2\xb1\xc3\x98\xc2\xa8\xc3\x98\xc2\xb1\xc3\x9b\xc2\x8c:'
  checkResponse = requests.get('http://hotspot.um.ac.ir/status')
  # print(checkResponse.text.encode('utf8'))
  if (checkResponse.url.split('/')[-1] == 'login'):
    return 0
  else:
    ID = str(checkResponse.text.encode('utf8').split(usernameinBin)[1].split(b'\x3e')[1].split(b'\x3c')[0])
    return ID[2:len(ID)-1]

def remaining(id):
    usageData = {"username" : id}
    usageResponse = requests.post('https://hs.um.ac.ir/usage.php', data = usageData)
    res = json.loads(usageResponse.text)
    monthly = (float(res['month']) * 1024)
    consumed = (monthly - float(res['usage']))
    remaining = (round((consumed / 1024), 1))
    # return ("{:<24}Total: " + res['month'] + "\n{:<24}Used: " + 
    #   str(round((float(res['usage']) / 1024), 1)) + "\n{:<24}Remainig: " + str(remaining)).format(' ', ' ', ' ')
    return ("==========================\n" + "‖{:<4}Total:{:<5}" + res['month'] + "GB\t ‖" + 
      "\n‖{:<4}Used:{:<6}" + str(round((float(res['usage']) / 1024), 1)) + "GB\t ‖" + 
      "\n‖{:<4}Remainig:{:<2}" + str(remaining) + "GB\t ‖" + "\n==========================").format(' ',' ',' ',' ',' ',' ')


def login():
  with open("auth.json", "r") as f:
    auths = json.load(f)

  for auth in auths:
    result = doLogin(auth['username'], auth['password'])
    if(result):
      break

  s.enter(interval, 1, login)

s.enter(0, 1, login)
s.run()