import requests
import googlemaps

# Define the API endpoint and parameters
url = "https://api.olamaps.io/routing/v1/directions"
api_key = "rxS3WOVB7zNbC0kvfLtpljJVa6lAqoIZpoqsytwU"  # Replace with your actual API key
x_request_id = "your_request_id_here"  # Replace with your actual request ID

# Parameters without waypoints
params = {
    'origin': '18.76029027465273,73.3814242364375',
    'destination': '18.73354223011708,73.44587966939002',
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
    
    # Print the list of points
    print(points_list)

else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)  # Display the error message
