# Turn PDF document into JSON embeddings

import requests
import json
import sys
import argparse
from pdfminer.high_level import extract_text
import os

sys.path.append("..")
from config import OPENAI_API_KEY


def create_embeddings(text):
    url = "https://api.openai.com/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {"input": text, "model": "text-embedding-ada-002"}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()


def chunk_text_by_characters(text, max_chars=400):
    chunks = []
    current_chunk = ""
    for char in text:
        current_chunk += char
        if len(current_chunk) >= max_chars:
            chunks.append(current_chunk)
            current_chunk = ""
    if current_chunk:
        chunks.append(current_chunk)
    return chunks


def extract_text_from_pdf(file_path):
    return extract_text(file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate embeddings from a PDF file.")
    parser.add_argument("file_path", type=str, help="Path to the PDF file")
    args = parser.parse_args()

    text = extract_text_from_pdf(args.file_path)

    chunks = chunk_text_by_characters(text)
    all_embeddings = []

    for index, chunk in enumerate(chunks):
        print(f"Processing chunk {index + 1} with {len(chunk.split())} words:")
        print(
            chunk.split("\n")[0][:100] + "..."
        )  # print the first 100 characters of the first line for context
        embeddings_response = create_embeddings(chunk)

        if "data" in embeddings_response and len(embeddings_response["data"]) > 0:
            embedding_value = embeddings_response["data"][0].get("embedding", [])
        else:
            embedding_value = []

        embedding_data = {"index": index, "text": chunk, "embedding": embedding_value}

        all_embeddings.append(embedding_data)

        if "error" in embeddings_response:
            print(
                f"Error in chunk {index+1}: {embeddings_response['error']['message']}"
            )

    # Set the output directory to af-embeddings
    output_directory = "../public/af-embeddings"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    output_file_name = (
        output_directory
        + "/"
        + args.file_path.split("/")[-1].split(".")[0]
        + "_embeddings.json"
    )
    print(output_file_name, "OUTPUT FILE NAME")
    with open(output_file_name, "w", encoding="utf-8") as file:
        json.dump(all_embeddings, file, indent=4)
