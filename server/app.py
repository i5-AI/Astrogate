from flask import Flask, request, jsonify, render_template, make_response
import requests
import sys
from flask_cors import CORS
import logging

sys.path.append("..")
from server.config import OPENAI_API_KEY, ZILLIZ_API_KEY, PUBLIC_ENDPOINT

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def index():
    return "Testing 1-2-3!"


@app.route("/create-embedding", methods=["POST"])
def create_embedding():
    print("Creating embedding...", request.json)

    text = request.json["query"]
    print("User query received:", text)

    # Generate the embedding using OpenAI API
    embedding = generate_embedding(text)

    # Find the closest matching texts using Zilliz vector search
    closest_texts = find_closest_matches(embedding)

    answer = ask_gpt(text, closest_texts)

    return jsonify({"answer": answer})


@app.route("/ask-question", methods=["POST"])
def ask_question():
    data = request.json
    question = data["question"]
    document_text = data["documentText"][
        :28000
    ]  # Ensure text is no longer than 30,000 characters

    answer = ask_gpt(question, document_text)

    return jsonify({"answer": answer})


def generate_embedding(text):
    url = "https://api.openai.com/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {"input": text, "model": "text-embedding-ada-002"}

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        embedding = response.json()["data"][0]["embedding"]
        return embedding
    else:
        raise Exception(
            f"Failed to generate embedding: {response.status_code} {response.text}"
        )


def find_closest_matches(embedding):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ZILLIZ_API_KEY}",
    }

    collections = [
        "FTM_2022_Final",
        "dafi36_2903",
        "dafpam34_1203",
        "dafh33_337",
        "DAFI_36_2903_AFROTCSup",
        "_i5SOP",
    ]

    all_results = []

    for collection in collections:
        payload = {
            "collectionName": collection,
            "filter": "",
            "limit": 10,
            "outputFields": ["id", "text"],
            "vector": embedding,
        }

        response = requests.post(
            f"{PUBLIC_ENDPOINT}/v1/vector/search", headers=headers, json=payload
        )

        if response.status_code == 200:
            data_list = response.json()["data"]
            logging.debug(f"Data list from collection {collection}: {data_list}")
            all_results.extend(data_list)
        else:
            logging.warning(
                f"Failed to find closest matches in {collection}: {response.status_code} {response.text}"
            )

    # Check the structure of the results and handle accordingly
    if all_results and "distance" not in all_results[0]:
        logging.error(f"Unexpected result structure: {all_results[0]}")
        raise KeyError("'distance' key not found in results")

    # Sort all results by their distance and take the top 10 (smaller distance is better)
    all_results = sorted(all_results, key=lambda x: x["distance"])[:10]

    chat_gpt_text = extract_text({"data": all_results})
    return chat_gpt_text


def extract_text(data, max_chars=40000):
    extracted_text = ""
    current_length = 0

    for item in data["data"]:
        if current_length + len(item["text"]) > max_chars:
            remaining_chars = max_chars - current_length
            extracted_text += item["text"][:remaining_chars]
            break
        else:
            extracted_text += item["text"]
            current_length += len(item["text"])

    return extracted_text


def ask_gpt(question, document_text):
    # Estimated average token size is 4 characters per token, so 8192 tokens * 4 characters/token
    safe_character_limit = 8000 * 4
    if len(document_text) > safe_character_limit:
        document_text = document_text[safe_character_limit:]
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-4",
        "messages": [
            {
                "role": "system",
                "content": "You are being given an air force document with very specific numbering and section breakdown. Respond to the user's query with only text from the document, and cite where you found the text.",
            },
            {"role": "user", "content": "My query is: " + question},
            {
                "role": "assistant",
                "content": "Use this as your only source: " + document_text,
            },
        ],
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        error_message = f"Failed to ask GPT: {response.status_code} {response.text}"
        raise Exception(error_message)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
