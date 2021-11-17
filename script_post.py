from datetime import datetime
import requests
import pandas as pd
import json

import random
import time

url1 = 'http://64.227.30.92/gets/'
url2 = 'http://127.0.0.1:8000/gets/'
url3 = 'https://www.agrower.xyz/gets/'

auth = ' username="joda" password="199519polofo"'
token1 = 'token 4089697204ef95c3dd2e76a3eb7ec33074322e5b'
token2 = 'token df767297ec8cea089c22d07cec40a02890247410'
token3 = 'token d28bf835b030ec9afb23093ad6fc801c6fcabb65'


def introducir_sensor(ruta, token):

    dic_data = {'humedad_aire': random.randint(0,100),
                'temperatura_aire':random.randint(18,34),
                'humedad_suelo_1':random.randint(1400,2500),
                'humedad_suelo_2':random.randint(1400,2500),
                'humedad_suelo_3':random.randint(1400,2500),
                'humedad_suelo_4':random.randint(1400,2500),
                'luz':random.randint(200,3000),
                'Estado_riego':1,
                'Estado_luz':0,
                'modo_riego':2,
                'modo_luz':2}
    print(dic_data)
    response = requests.post(ruta, data=json.dumps(dic_data),
                               headers = {'Authorization': token,
                                'Content-Type': 'application/json'} )
    problema = response.text
    print(problema[5000:6000])
    print(response)
    print(problema)


while True:
    
    introducir_sensor(url2, token2)
    time.sleep(3)
