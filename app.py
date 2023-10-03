from flask import Flask, request, jsonify
import pandas as pd
import json

app = Flask(__name__)

# Load data from the combined CSV file
df = pd.read_csv('vizag.csv')

# Cuisines known to be spicy
spicy_cuisines = ['Asian', 'Mexican', 'Indian']

# Cuisines known to be sweet
sweet_cuisines = ['Bakery', 'Cafe']

# Function to recommend restaurants based on user input
def recommend_restaurants(dietary_preference, mood, budget, aesthetics, diet):
    # Filter restaurants based on dietary preference
    if dietary_preference == 'Nonveg':
        filtered_df = df[(df['Type'] == 'Both') | (df['Type'] == 'Non-vegetarian')]
    elif dietary_preference == 'Veg':
        filtered_df = df[df['Type'] == 'Vegetarian']
    else:
        return {"error": "Invalid dietary preference. Use 'Nonveg' or 'Veg'."}

    # Filter restaurants based on mood
    if mood == 'Happy':
        mood_cuisines = spicy_cuisines
    elif mood == 'Sad':
        mood_cuisines = sweet_cuisines
    elif mood == 'Unsure':
        # When unsure, recommend both spicy and sweet cuisines
        mood_cuisines = spicy_cuisines + sweet_cuisines
    else:
        return {"error": "Invalid mood. Use 'Happy', 'Sad', or 'Unsure'."}

    filtered_df = filtered_df[filtered_df['Cuisine'].isin(mood_cuisines)]

    # Filter restaurants based on budget
    filtered_df = filtered_df[filtered_df['Budget'] == budget]

    # Filter restaurants based on diet preference
    if diet == 'Moderate':
        filtered_df = filtered_df
    elif diet == 'Fast Food':
        filtered_df = filtered_df[filtered_df['Diet'] == 'Fast Food']
    elif diet == 'Healthy':
        filtered_df = filtered_df[filtered_df['Diet'] == 'Healthy']
    else:
        return {"error": "Invalid diet preference. Use 'Moderate', 'Fast Food', or 'Healthy'."}

    # Filter restaurants based on aesthetics
    if aesthetics == 'Normal':
        filtered_df = filtered_df
    elif aesthetics == 'Good':
        filtered_df = filtered_df[(filtered_df['Aesthetics'] == 'Normal') | (filtered_df['Aesthetics'] == 'Good')]
    elif aesthetics == 'Aesthetic':
        filtered_df = filtered_df[filtered_df['Aesthetics'] == 'Aesthetic']
    else:
        return {"error": "Invalid aesthetics preference. Use 'Normal', 'Good', or 'Aesthetic'."}

    # Sort restaurants by rating in descending order
    sorted_df = filtered_df.sort_values(by='Rating', ascending=False)

    # Extract and return top 3 rated restaurant details
    recommendations = []
    for _, row in sorted_df.iterrows():
        restaurant_data = {
            "Restaurant": row['Restaurant'],
            "Rating": row['Rating'],
            "URL": row['url'],
            "ImageURL": row['pic']
        }
        recommendations.append(restaurant_data)

    if len(recommendations) > 3:
        return recommendations[:3]
    else:
        return recommendations

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    try:
        dietary_preference = request.args.get('dietary_preference')
        mood = request.args.get('mood')
        budget = request.args.get('budget')
        aesthetics = request.args.get('aesthetics')
        diet = request.args.get('diet')

        recommendations = recommend_restaurants(dietary_preference, mood, budget, aesthetics, diet)
        
        if isinstance(recommendations, list):
            if len(recommendations) > 0:
                return jsonify(recommendations)
            else:
                return jsonify({"message": "No recommendations available."})
        else:
            return jsonify(recommendations)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
