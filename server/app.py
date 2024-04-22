from flask import Flask, request, jsonify, render_template, make_response
import requests
import json
import sys
import os
from flask_cors import CORS

sys.path.append("..")
from server.config import OPENAI_API_KEY, ZILLIZ_API_KEY, PUBLIC_ENDPOINT

# flask_app = Flask(__name__)
# app = Flask(__name__, template_folder='client')

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})  # Allows all domains

# app = Flask(__name__)
# CORS(app, support_credentials=True)

@app.route("/login")
def login():
  return jsonify({'success': 'ok'})

@app.route("/")
def helloWorld():
  return "Hello, cross-origin-world!"

@app.route("/api/data", methods=["GET", "POST"])
def get_data():
    if request.method == 'POST':
        data = request.get_json()
        return jsonify({"message": "Data received", "received_data": data}), 200
    elif request.method == 'GET':
        sample_data = {"key6": "value1", "key3": "value5"}
        return jsonify(sample_data), 200
    else:
        sample_data = {"key1": "value1", "key2": "value2"}
        return jsonify(sample_data), 200

# @app.route('/')
# def home():
#     return render_template('index.html')

@app.route('/create-embedding', methods=['POST'])
def create_embedding():
    text = request.json['query']
    
    # Generate the embedding using OpenAI API
    embedding = generate_embedding(text)
    
    # Find the closest matching texts using Zilliz vector search
    closest_texts = find_closest_matches(embedding)

    print("USER QUESTION:", text)
    answer = ask_gpt(text, closest_texts)
    
    # this function is now useless because closest texts already cuts off the text to the threshold we need it to be
    # combined_text = combine_texts(closest_texts, threshold=0.71)
    
    return jsonify({"answer": answer})

@app.route('/ask-question', methods=['POST'])
def ask_question():
    data = request.json
    question = data['question']
    document_text = data['documentText'][:28000]  # Ensure text is no longer than 30,000 characters

    answer = ask_gpt(question, document_text)
    
    return jsonify({"answer": answer})

def generate_embedding(text):
    url = "https://api.openai.com/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "input": text,
        "model": "text-embedding-ada-002"
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        embedding = response.json()['data'][0]['embedding']
        print(f"Embedding generated successfully!!! {embedding}")
        return embedding
    else:
        raise Exception(f"Failed to generate embedding: {response.status_code} {response.text}")


def find_closest_matches(embedding):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ZILLIZ_API_KEY}"
    }
    
    payload = {
        "collectionName": "thunderstorm_vectors",
        "filter": "",
        "limit": 10,
        "outputFields": ["id", "text"],
        "vector": embedding
    }

    response = requests.post(f"{PUBLIC_ENDPOINT}/v1/vector/search", headers=headers, json=payload)
    
    response_json = response.json()
    print("Response JSON:", response_json)

    print("OUTPUT TEXT SAVED")

    if response.status_code == 200:
        # Extract the 'data' list from the response
        data_list = response.json()['data']

        chat_gpt_text = extract_text({'data': data_list})
        
        # Retrieve both text and distance for each result
        closest_texts_with_distances = [
            (item['text'], item['distance']) for item in data_list
        ]
        
        # If you only want the texts without the distances, uncomment the following line
        # closest_texts = [item['text'] for item in data_list]

        # Return the list of tuples with text and distance\
        print('CLOSEST TEXTS', closest_texts_with_distances, "distances", closest_texts_with_distances[0][1])
        return chat_gpt_text 
    # Or just return 'closest_texts' if you don't need the distances
    else:
        raise Exception(f"Failed to find closest matches: {response.status_code} {response.text}")

def save_response_to_file(data, filename):
    # Ensure the 'outputs' directory exists
    if not os.path.exists('outputs'):
        os.makedirs('outputs')

    data_list = data.get('data', [])
    
    # Retrieve both text and distance for each result
    closest_texts_with_distances = [
        (item['text'], item['distance']) for item in data_list
    ]
    print("CLOSEST TEXTS", closest_texts_with_distances, "distances")

    # Define the path for the output file
    output_file_path = os.path.join('outputs', filename)

    # Write the data to the file in JSON format
    with open(output_file_path, 'w', encoding='utf-8') as file:
        # Saving original response JSON
        json.dump(data, file, indent=4)
        file.write("\n\nClosest Texts with Distances:\n")
        file.write(str(closest_texts_with_distances[0][1]))
    
    print(f"Response JSON saved to {output_file_path}")

# Function to extract text up to a maximum of 120,000 characters
def extract_text(data, max_chars=40000):
    # Initialize variables
    extracted_text = ''
    current_length = 0

    # Iterate through the text blocks and concatenate until the limit is reached
    for item in data["data"]:
        # Check if adding the next block of text exceeds the maximum character limit
        if current_length + len(item["text"]) > max_chars:
            # Calculate how many characters can still be added
            remaining_chars = max_chars - current_length
            extracted_text += item["text"][:remaining_chars]
            break
        else:
            extracted_text += item["text"]
            current_length += len(item["text"])

    print("EXTRCTED TEXT SAVED")

    return extracted_text

# def combine_texts(data, threshold=0.765):
#     combined_texts = []
#     print("MATCHES", data, "END!!!!")

#     for match in data: 
#         text = match.get("text", "")
#         distance = match.get("distance", 0)
#         print(f"Distance: {distance}")
        
#         if distance > threshold:
#             print(f"Distance value above threshold: {distance}")
#             combined_texts.append(text)

#     combined_text = " ".join(combined_texts)

#     return combined_text

def ask_gpt(question, document_text):
    print("Asking GPT...")

    # Estimated average token size is 4 characters per token, so 8192 tokens * 4 characters/token
    safe_character_limit = 8000 * 4
    if len(document_text) > safe_character_limit:
        document_text = document_text[safe_character_limit:]
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are being given an air force document with very specific numbering and section breakdown. Respond to the user's query with only text from the document, and cite where you found the text."},
            {"role": "user", "content": "My query is: " + question},
            {"role": "assistant", "content": "Use this as your only source: " + document_text}
        ]
    }
    print("DATA", data);
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("GPT response received successfully.", response.json())
        return response.json()['choices'][0]['message']['content']
    else:
        error_message = f"Failed to ask GPT: {response.status_code} {response.text}"
        print(error_message)
        raise Exception(error_message)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
