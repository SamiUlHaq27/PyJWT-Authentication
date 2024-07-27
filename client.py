import requests


endpoint = "http://127.0.0.1:8000/"

user3 = {
    'username':'Sami',
    'password':'sami@api4312',
    'first_name':'Sami',
    'last_name':'Ul Haq',
    'email':'123@mail.com'
    }

# res = requests.post("http://127.0.0.1:8000/", data=user3)

res = requests.post(endpoint+"auth/", data=user3)
data = res.json()
print(data)

res2 = requests.get(endpoint+"data/", params={'token':data['token']})

print(res2.json())