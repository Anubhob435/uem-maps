from flask import Flask, request, jsonify
import requests
import googlemaps
import json

app = Flask(__name__)

# Existing routing code integrated into Flask
@app.route('/get-route', methods=['POST'])
def get_route():
    # Extract origin and destination from the request
    origin = request.json.get('origin', '22.459057, 88.379041')
    destination = request.json.get('destination', '22.560322, 88.490434')
    
    # Define the API endpoint and parameters
    url = "https://api.olamaps.io/routing/v1/directions"
    api_key = "rxS3WOVB7zNbC0kvfLtpljJVa6lAqoIZpoqsytwU"  # Replace with your actual API key
    x_request_id = "your_request_id_here"  # Replace with your actual request ID

    # Parameters without waypoints
    params = {
        'origin': origin,
        'destination': destination,
        'api_key': api_key
    }
    # Headers
    headers = {
        'X-Request-Id': x_request_id
    }

    # Make the POST request
    response = requests.post(url, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        overview_polyline = data['routes'][0]['overview_polyline']
        
        # Decode the polyline
        decoded_points = googlemaps.convert.decode_polyline(overview_polyline)
        
        # Convert decoded points to a list of (longitude, latitude) tuples
        points_list = [[point['lng'], point['lat']] for point in decoded_points]

        with open('data.json', 'w') as json_file:
            # Step 3: Convert the Python array to JSON and write it to the file
            json.dump(points_list, json_file)

        return jsonify({
            'message': "Array has been written to data.json",
            'points': points_list
        })
    else:
        return jsonify({
            'error': f"Request failed with status code: {response.status_code}",
            'details': response.text
        }), response.status_code

@app.route('/save-coordinates', methods=['POST'])
def save_coordinates():
    data = request.json
    # Save coordinates or perform any action needed
    return jsonify({"status": "Coordinates saved"}), 200

@app.route('/calculate-route', methods=['POST'])
def calculate_route():
    data = request.json
    origin = data['origin']
    destination = data['destination']

    # Call the Ola Maps Routing API
    response = requests.get(f"https://api.olamaps.io/routing/v1/directions?origin={origin}&destination={destination}&api_key={rxS3WOVB7zNbC0kvfLtpljJVa6lAqoIZpoqsytwU}")
    if response.status_code == 200:
        route_data = response.json()
        # Extract relevant information and return it
        return jsonify({
            'distance': route_data['routes'][0]['distance'],
            'duration': route_data['routes'][0]['duration'],
            'geometry': route_data['routes'][0]['geometry'],
        })
    else:
        return jsonify({"error": "Route calculation failed"}), 400


if __name__ == '__main__':
    app.run(debug=True)
