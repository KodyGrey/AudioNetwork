import requests

with open('static/audio/mp3/1.mp3', 'rb') as f:
    dtc = {
        'login': 'hello',
        'password': 'asdf',
        'title': 'hi',
        'file': str(f.read())
    }


def load(number):
    json = dtc
    json['title'] += str(number)
    res = requests.post('http://localhost:5000/api/posts', json=json)
    print(res)


for i in range(20):
    load(i)

# print(type(bytes(dtc['file'], 'ascii')))
