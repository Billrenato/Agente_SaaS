import requests

url = "http://localhost:9000/upload/xml"

files = {
    "arquivo": open("C:/xml/35251032034550000118550010000019231180402234-nfe.xml", "rb")
}

data = {
    "cnpj": "32034550000118"
}

headers = {
    "Authorization": "Bearer TOKEN123"
}

r = requests.post(url, files=files, data=data, headers=headers)

print(r.text)