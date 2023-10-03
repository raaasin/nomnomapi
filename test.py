import requests
url = 'https://nomnomapi.onrender.com/api/recommendations'
params = {
    'dietary_preference': 'Veg', # 'Nonveg' or 'Veg'
    'mood': 'Unsure',  # 'Happy', 'Sad', or 'Unsure'
    'budget': 'Medium', # 'Cheap', 'Medium', or 'Expensive'
    'aesthetics': 'Good', # 'Normal', 'Good', or 'Aesthetic'
    'diet': 'Moderate'  # 'Moderate', 'Fast Food', or 'Healthy'
}
response = requests.get(url, params=params)

if response.status_code == 200:
    recommendations = response.json()
else:
    print('Error:', response.status_code, response.text)
