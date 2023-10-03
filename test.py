import requests

url = 'http://localhost:5000/api/recommendations'
params = {
    'mood': 1,
    'budget': 0,
    'aesthetics': 1,
    'type': 0,
    'diet': 2
}

response = requests.get(url, params=params)

if response.status_code == 200:
    recommendations = response.json()
    print(recommendations)
else:
    print('Error:', response.status_code, response.text)
