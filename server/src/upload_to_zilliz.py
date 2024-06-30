# Uploads embeddings to Zilliz Milvus using the Zilliz API.

import requests
import json
import sys
import argparse

# Add the parent directory to the Python path to access config.py
sys.path.append("..")
from config import PUBLIC_ENDPOINT, ZILLIZ_API_KEY

# Set up argument parsing
parser = argparse.ArgumentParser(description="Upload embeddings to Zilliz.")
parser.add_argument(
    "collection_name", type=str, help="Name of the collection to upload to."
)
parser.add_argument(
    "json_file", type=str, help="Path to the JSON file with embeddings."
)
args = parser.parse_args()

# Load the JSON data from file
with open(args.json_file, "r", encoding="utf-8") as file:
    json_data = json.load(file)

# Set up the headers for the API request
headers = {
    "Authorization": f"Bearer {ZILLIZ_API_KEY}",
    "Content-Type": "application/json",
}

# Split the data into chunks with a maximum of 90 vectors per call
chunk_size = 90
vector_chunks = [
    json_data["data"][i : i + chunk_size]
    for i in range(0, len(json_data["data"]), chunk_size)
]

# Iterate over vector chunks and send requests
print(f"Total chunks to upload: {len(vector_chunks)}")
key = 0
for chunk in vector_chunks:
    # Prepare the data to send with unique IDs
    data = []
    for row in chunk:
        data.append(
            {"primary_key": str(key), "vector": row["vector"], "text": row["text"]}
        )
        key += 1
    data_to_send = {"collectionName": args.collection_name, "data": data}
    # Post the data to the API endpoint
    response = requests.post(
        f"{PUBLIC_ENDPOINT}/v1/vector/insert",
        json=data_to_send,
        headers=headers,
    )
    # Print the response text to see if it was successful
    print(response.text)
