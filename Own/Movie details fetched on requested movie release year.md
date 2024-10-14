```python
import requests
import pandas as pd
from datetime import datetime
import os

# Replace 'YOUR_API_KEY' with your actual OMDb API key.
api_key = '876703b4'

# Load movie names from a CSV file (e.g., 'movies.csv') with a column named 'Movie'
input_file_path = r'D:\Main\My Practice and experiments\My Practice LAB\Python\2023\Movie recommendation project\DATA_IN\movie_titles.csv'  # Specify the path to your input CSV file here
movie_df = pd.read_csv(input_file_path)

# Extract movie names into a list from the 'Movie' column in the CSV
movie_names = movie_df['Movie'].tolist()

# Prompt the user to enter a movie year
movie_year = input("Enter a movie year: ")

# Folder to save the output CSV file
output_folder = r'D:\Main\My Practice and experiments\My Practice LAB\Python\2023\Movie recommendation project\DATA_OUT'  # You can specify the folder path here

# Ensure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Function to get movie details
def get_movie_details(movie_name, year): # 
    try:
        # Construct the API request URL
        url = f"http://www.omdbapi.com/?apikey={api_key}&t={movie_name.replace(' ', '+')}&y={year}"
        
        # Send the GET request to OMDb API
        response = requests.get(url)

        # Parse the JSON response
        data = response.json()

        # Check if the movie was found and contains required details
        if 'Response' in data and data['Response'] == 'True':
            return {
                "Movie": movie_name,
                "Year": year,
                "IMDb ID": data.get('imdbID', "N/A"),
                "IMDb Rating": data.get('imdbRating', "N/A")

            }
        else:
            return None

    except Exception as e:
        return {
            "Movie": movie_name,
            "Year": year,
            "Error": str(e),
            "IMDb Rating": imdb_rating
        }

# Create a list of dictionaries containing movie details
movie_details_list = []

for movie_name in movie_names:
    movie_detail = get_movie_details(movie_name, movie_year)  
    if movie_detail is not None:
        movie_details_list.append(movie_detail)

# Create a DataFrame from the list
movie_details_df = pd.DataFrame(movie_details_list)

# Get the current date-time stamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# Save the DataFrame to a CSV file with date-time stamp in the file name
output_file = os.path.join(output_folder, f'movie_details_{movie_year}_{timestamp}.csv')
movie_details_df.to_csv(output_file, index=False)

print(f"Movie details for the year {movie_year} have been saved to '{output_file}'")
```