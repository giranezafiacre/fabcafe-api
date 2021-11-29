import requests,math,random
from decouple import config

def process_payment(amount,phone,fullname):
     auth_token= config('FLUTTERWAVE_KEY')
     print(auth_token)
     hed = {'Authorization': f'{auth_token}'}
     data = {
                "tx_ref":str(math.floor(1000000 + random.random()*9000000)),
                "amount":str(amount),
                "currency":"RWF",
                "network":"MTN",
                "email":"user@gmail.com",
                "phone_number":str(phone),
                "fullname":fullname,
                }
     url = 'https://api.flutterwave.com/v3/charges?type=mobile_money_rwanda'
     response = requests.post(url, json=data, headers=hed)
     response=response.json()
     data={}
     if(response['status']):
        data=response
     else:
         data['status']='failed'
     return data

def verify_payment(flwref):
     auth_token= config('FLUTTERWAVE_KEY')
     # print(auth_token)
     hed = {'Authorization': f'{auth_token}'}
     data = {
                "flwref": flwref,
                "SECKEY":auth_token
                }
     url = "https://api.ravepay.co/flwv3-pug/getpaidx/api/v2/verify"
     response = requests.post(url, json=data, headers=hed)
     response=response.json()
     print(response)
     return response