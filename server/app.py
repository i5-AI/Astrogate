import os
import json
import requests
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174"])

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-api-key-here')
OPENAI_API_BASE = "https://api.openai.com/v1"

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}

# Global variables
vector_store_id = None
is_initialized = False

def upload_document(file_path, file_name):
    """Upload a document to OpenAI"""
    try:
        with open(file_path, 'rb') as file:
            files = {'file': (file_name, file, 'application/pdf')}
            data = {'purpose': 'user_data'}
            
            response = requests.post(
                f"{OPENAI_API_BASE}/files",
                headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                files=files,
                data=data
            )
            
            if response.status_code == 200:
                file_id = response.json()["id"]
                logger.info(f"✅ Uploaded {file_name} -> {file_id}")
                return file_id
            else:
                logger.error(f"Failed to upload {file_name}: {response.status_code} - {response.text}")
                return None
                
    except Exception as e:
        logger.error(f"Error uploading {file_name}: {e}")
        return None

def send_message(message):
    """Send a message using the Responses API with vector store search"""
    global vector_store_id
    
    if not vector_store_id:
        logger.error("No vector store available")
        return None
    
    try:
        # Call the Responses API with file search tool
        # Create a prompt that allows both document-based and general responses
        enhanced_message = f"{message}\n\nIMPORTANT: If you find this information in one of the documents, please end your response with 'Section X.X.X' where X.X.X is the specific section number. If the information is not in one of the documents, provide a helpful response based on your general knowledge but do not include any section information."
        
        payload = {
            "model": "gpt-4o",
            "input": enhanced_message,
            "tools": [{
                "type": "file_search",
                "vector_store_ids": [vector_store_id]
            }],
            "include": ["file_search_call.results"]
        }
        
        response = requests.post(
            f"{OPENAI_API_BASE}/responses",
            headers=HEADERS,
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            
            if "output" in result and len(result["output"]) > 0:
                # Find the message output
                for output in result["output"]:
                    if output["type"] == "message":
                        content_obj = output["content"][0]
                        text = content_obj["text"]
                        
                        # Extract citations if they exist (avoid duplicates)
                        citations = set()
                        if "annotations" in content_obj:
                            for annotation in content_obj["annotations"]:
                                if annotation["type"] == "file_citation":
                                    filename = annotation.get('filename', 'Unknown file')
                                    citations.add(f"Source: {filename}")
                        
                        # Add source information right after the section citation
                        if citations:
                            # Get the first citation (filename)
                            source_file = next(iter(citations)).replace("Source: ", "")
                            # Add source info right after the section
                            if "Section" in text:
                                # Find where the section ends and add source
                                lines = text.split('\n')
                                new_lines = []
                                for line in lines:
                                    new_lines.append(line)
                                    if line.strip().startswith("Section"):
                                        new_lines.append(f"Source: {source_file}")
                                        break
                                full_response = '\n'.join(new_lines)
                            else:
                                full_response = text
                        else:
                            # No citations found - just return the AI response without any section/source
                            full_response = text
                        
                        logger.info(f"✅ Response generated successfully")
                        return full_response
                
                logger.error("No message content found in response")
                return None
            else:
                logger.error("No response content found")
                return None
        else:
            logger.error(f"Failed to get response: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return None

def create_vector_store():
    """Create a vector store for document search"""
    try:
        response = requests.post(
            f"{OPENAI_API_BASE}/vector_stores",
            headers=HEADERS,
            json={"name": "Astrogate Air Force Documents"}
        )
        
        if response.status_code == 200:
            vector_store_id = response.json()["id"]
            logger.info(f"✅ Created vector store: {vector_store_id}")
            return vector_store_id
        else:
            logger.error(f"Failed to create vector store: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"Error creating vector store: {e}")
        return None

def upload_to_vector_store(file_id, vector_store_id):
    """Upload a file to the vector store"""
    try:
        response = requests.post(
            f"{OPENAI_API_BASE}/vector_stores/{vector_store_id}/files",
            headers=HEADERS,
            json={"file_id": file_id}
        )
        
        if response.status_code == 200:
            logger.info(f"✅ Uploaded file {file_id} to vector store")
            return True
        else:
            logger.error(f"Failed to upload file to vector store: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error uploading to vector store: {e}")
        return False

def auto_initialize():
    """Auto-initialize the chatbot with documents"""
    global vector_store_id, is_initialized
    
    logger.info("🚀 Auto-initializing Astrogate with documents...")
    
    # Create vector store
    vector_store_id = create_vector_store()
    if not vector_store_id:
        logger.error("❌ Failed to create vector store")
        return False
    
    # List of all Air Force documents
    essential_files = [
        ("documents/FTM_2022_Final.pdf", "FTM_2022_Final.pdf"),
        ("documents/dafpam34-1203.pdf", "dafpam34-1203.pdf"),
        ("documents/dafi36_2903.pdf", "dafi36_2903.pdf"),
        ("documents/DAFI_36_2903_AFROTCSup.pdf", "DAFI_36_2903_AFROTCSup.pdf"),
        ("documents/dafh33_337.pdf", "dafh33_337.pdf"),
        ("documents/_i5SOP.pdf", "_i5SOP.pdf")
    ]
    
    uploaded_files = []
    
    # Upload documents to OpenAI
    for file_path, file_name in essential_files:
        if os.path.exists(file_path):
            file_id = upload_document(file_path, file_name)
            if file_id:
                # Upload to vector store
                if upload_to_vector_store(file_id, vector_store_id):
                    uploaded_files.append(file_id)
        else:
            logger.warning(f"File not found: {file_path}")
    
    if uploaded_files:
        is_initialized = True
        logger.info(f"✅ Astrogate initialized successfully! Documents: {len(uploaded_files)}")
        logger.info("✅ Ready to serve requests!")
        return True
    else:
        logger.error("❌ Failed to upload any documents")
        return False

@app.route("/")
def index():
    return jsonify({"message": "Astrogate Air Force Chatbot API"})

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "initialized": is_initialized,
        "vector_store_id": vector_store_id,
        "timestamp": datetime.now().isoformat()
    })

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "")
        
        if not message:
            return jsonify({"error": "No message provided"}), 400
        
        if not is_initialized:
            return jsonify({"error": "Chatbot not initialized"}), 500
        
        response = send_message(message)
        
        if response:
            return jsonify({"response": response})
        else:
            return jsonify({"error": "Failed to generate response"}), 500
            
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "initialized": is_initialized,
        "vector_store_id": vector_store_id,
        "status": "ready" if is_initialized else "initializing"
    })

# Initialize on startup
if __name__ == "__main__":
    # Auto-initialize on startup
    if auto_initialize():
        logger.info("🚀 Starting Astrogate Air Force Chatbot with Responses API...")
        logger.info("✅ Backend ready! Frontend can now connect.")
        logger.info("🌐 Access the chatbot at: http://localhost:5173")
        app.run(host="0.0.0.0", port=8000, debug=False)
    else:
        logger.error("❌ Failed to initialize. Exiting.")
        exit(1)