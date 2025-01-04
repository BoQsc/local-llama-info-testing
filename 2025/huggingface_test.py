import requests

# Hugging Face API URL for TheBloke
user_url = "https://huggingface.co/api/models"
params = {"author": "TheBloke"}  # Specify the user

# Make a GET request to the API
response = requests.get(user_url, params=params)

if response.status_code == 200:
    repos = response.json()
    for repo in repos:
        print(f"Name: {repo['modelId']}, Downloads: {repo.get('downloads', 'N/A')}")
else:
    print(f"Failed to fetch repositories. Status Code: {response.status_code}")
