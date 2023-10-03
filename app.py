import numpy as np
from flask import Flask, request, jsonify
from sklearn.neighbors import NearestNeighbors
import pandas as pd

app = Flask(__name__)

# Load the restaurant data from your CSV file
data = pd.read_csv('restaurants.csv')

# Dictionary to map categorical values to numerical labels
category_mapping = {
    'Cheap': 0,
    'Medium': 1,
    'Expensive': 2,
    'Aesthetic': 0,
    'Good': 1,
    'Normal': 2,
    'Non-vegetarian': 1,  # Updated mapping for 'Non-vegetarian' to 1
    'Vegetarian': 2,
    'Fast Food': 0,
    'Healthy': 1,
    'Moderate': 2
}

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    try:
        mood = int(request.args.get('mood'))
        budget = int(request.args.get('budget'))
        aesthetics = int(request.args.get('aesthetics'))
        type = int(request.args.get('type'))
        diet = int(request.args.get('diet'))

        # Added a dietary_preference parameter to specify 'Nonveg' or 'Veg'
        dietary_preference = request.args.get('dietary_preference')  # 'Nonveg' or 'Veg'

        user_profile = np.array([budget, aesthetics, type, diet])

        # Map categorical values to numerical labels
        user_profile = np.array([category_mapping.get(category, 0) for category in user_profile])

        # Filter the dataset based on dietary preference and dietary restrictions
        if dietary_preference == 'Nonveg':
            # Include restaurants that are 'Non-vegetarian' or 'Both'
            filtered_data = data[(data['Diet'] == 'Non-vegetarian') | (data['Diet'] == 'Both')]
        elif dietary_preference == 'Veg':
            filtered_data = data[data['Diet'] == 'Vegetarian']
        else:
            return jsonify({"error": "Invalid dietary_preference. Use 'Nonveg' or 'Veg'."})

        # Create a KNN model
        knn_model = NearestNeighbors(n_neighbors=3, metric='cosine')
        knn_model.fit(filtered_data[['Budget', 'Aesthetics', 'Type', 'Diet']])

        # Calculate cosine similarity
        user_profile = user_profile.reshape(1, -1)  # Reshape for compatibility
        content_similarities, top_recommend_indices = knn_model.kneighbors(user_profile)

        # Get top recommended restaurants based on similarity
        recommended_restaurants = [filtered_data.iloc[idx]['Restaurant'] for idx in top_recommend_indices[0]]

        # Return recommendations
        return jsonify({"recommendations": recommended_restaurants})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
