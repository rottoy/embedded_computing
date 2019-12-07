import flask
import requests
import json

URL = "http://172.30.1.55:4321/thermoReport"
data = {"temper":"36", "humid":"70"}
data=json.dumps(data,ensure_ascii=False)
print(data)
print(type(data))
r=requests.post(URL,data=data)
print(type(r))
print(r.json()['light'])
print(r.status_code)
print(r.text)

