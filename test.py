import requests

# Define the API URL and query parameters
url = 'http://localhost:5000/api/recommendations'
params = {
    'dietary_preference': 'Veg', # 'Nonveg' or 'Veg'
    'mood': 'Unsure',  # 'Happy', 'Sad', or 'Unsure'
    'budget': 'Medium', # 'Cheap', 'Medium', or 'Expensive'
    'aesthetics': 'Good', # 'Normal', 'Good', or 'Aesthetic'
    'diet': 'Moderate'  # 'Moderate', 'Fast Food', or 'Healthy'
}
response = requests.get(url, params=params)

# Check the response status code
if response.status_code == 200:
    recommendations = response.json()
    if recommendations:
        print(recommendations)
    else:
        print("No recommendations available.")
else:
    print('Error:', response.status_code, response.text)
