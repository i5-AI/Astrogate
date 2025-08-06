# Astrogate - Fresh Setup Guide

This is a clean, working implementation of the Air Force/Space Force chatbot using OpenAI's Responses API.

## What This Does

- **Backend**: Flask server that properly uses OpenAI's Responses API to manage documents and conversations
- **Frontend**: Modern React chat interface with real-time messaging
- **Documents**: Uploads Air Force PDFs and makes them searchable via natural language
- **Citations**: Every response includes proper document citations

## Quick Setup

### 1. Prepare Your Documents

Create a `documents` folder in the server directory and add your Air Force PDF files:

```bash
mkdir server/documents
# Add your PDF files:
# - FTM_2022_Final.pdf
# - dafi36_2903.pdf  
# - dafpam34_1203.pdf
# - dafh33_337.pdf
# - DAFI_36_2903_AFROTCSup.pdf
# - _i5SOP.pdf
```

### 2. Set Up Backend

```bash
cd server
pip install -r requirements.txt
python app.py
```

**Expected Output:**
```
🚀 Starting Astrogate Air Force Chatbot...
 * Running on http://0.0.0.0:8000
```

### 3. Set Up Frontend

In a new terminal:
```bash
cd client
npm install
npm run dev
```

**Expected Output:**
```
  VITE v5.x.x  ready in xxx ms
  ➜  Local:   http://localhost:5173/
```

### 4. Test the Chatbot

1. Open `http://localhost:5173/` in your browser
2. The chatbot will automatically initialize with your documents
3. Ask questions like:
   - "What are the Air Force uniform standards?"
   - "How do I format a military memorandum?"
   - "What are the basic drill commands?"

## API Endpoints

- `POST /initialize` - Initialize assistant with documents
- `POST /chat` - Send a message and get response
- `GET /health` - Check server status

## Key Features

✅ **Proper Responses API Integration** - Uses OpenAI's latest API correctly
✅ **Document Upload & Management** - Automatically uploads and indexes PDFs
✅ **Citation System** - Every response includes document citations
✅ **Modern UI** - Clean, responsive chat interface
✅ **Error Handling** - Graceful error handling and user feedback
✅ **Real-time Messaging** - Live chat with typing indicators

## Troubleshooting

### Backend Issues
- **"Documents directory not found"**: Make sure you created `server/documents/` and added PDF files
- **"API key error"**: Check your OpenAI API key in the code or set as environment variable
- **"Assistant creation failed"**: Check your OpenAI account has access to the Responses API

### Frontend Issues
- **"Cannot connect to backend"**: Make sure the Flask server is running on port 8000
- **"CORS errors"**: Backend has CORS enabled, restart both servers if needed

### Chatbot Issues
- **"No response"**: Check backend logs for initialization errors
- **"No citations"**: Assistant is configured to always include citations

## Next Steps

Once this is working locally:
1. Deploy backend to production server (AWS EC2, etc.)
2. Update frontend API endpoints to production URLs
3. Deploy frontend to hosting service (Vercel, Netlify, etc.)
4. Add authentication if needed for public deployment

## Architecture

```
Frontend (React) ←→ Backend (Flask) ←→ OpenAI Responses API
                                      ↓
                                   Document Storage
                                   (PDFs uploaded to OpenAI)
```

This implementation is much cleaner and more reliable than the previous version! 