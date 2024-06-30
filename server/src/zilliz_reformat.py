# Reformat the JSON structure created by running tokenize_text.py into a format that can be uploaded to Zilliz Milvus using the Zilliz API.

import json
import sys


def reformat_embeddings(input_file, output_file, collection_name):
    # Load the JSON data from file
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            json_data = json.load(file)
    except Exception as e:
        print(f"Error loading JSON data: {e}")
        sys.exit(1)

    # Check and print the structure of JSON data to understand it
    if isinstance(json_data, dict):
        print("JSON data is a dictionary. Keys:", list(json_data.keys()))
        # Assume embeddings are under the 'embeddings' key
        if "embeddings" in json_data and isinstance(json_data["embeddings"], list):
            json_data = json_data["embeddings"]
            print("First few items of 'embeddings':", json_data[:3])
        else:
            print("Dictionary does not contain a list under 'embeddings' key.")
            sys.exit(1)
    else:
        print(f"Unexpected JSON structure: {type(json_data)}")
        sys.exit(1)

    # Prepare the data in the new format
    data = []
    for i, item in enumerate(json_data):
        try:
            if isinstance(item, dict) and "embedding" in item and "text" in item:
                data.append(
                    {
                        "vector": item["embedding"],
                        "primary_key": i + 1,
                        "text": item["text"],
                    }
                )
            else:
                print(f"Skipping unexpected item structure at index {i}: {item}")
        except Exception as e:
            print(f"Error processing item at index {i}: {e}")

    new_data = {"collectionName": collection_name, "data": data}

    # Save the new JSON data to file
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(new_data, file, indent=2)
        print(f"Reformatted data saved to {output_file}")
    except Exception as e:
        print(f"Error saving reformatted data: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Usage: python zilliz_reformat.py <input_file> <output_file> <collection_name>"
        )
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    collection_name = sys.argv[3]

    reformat_embeddings(input_file, output_file, collection_name)
