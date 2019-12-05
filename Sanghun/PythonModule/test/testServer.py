import flask
import requests
import json

URL = "http://127.0.0.1:4321/thermoReport"
response=requests.post(URL)
data = {"temper":"36", "humid":"70"}
data=json.dumps(data,ensure_ascii=False)
print(data)
print(type(data))
r=requests.post(URL,data=data)

print(r.status_code)
print(r.text)

