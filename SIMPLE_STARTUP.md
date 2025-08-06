# 🚀 Simple Astrogate Startup

## **Backend (Terminal 1):**
```bash
cd server
source chatbot/bin/activate
python3 app.py
```

## **Frontend (Terminal 2):**
```bash
cd client
npm run dev
```

## **Access:**
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000

## **What happens automatically:**
- ✅ Backend auto-initializes with documents
- ✅ Vector store creation
- ✅ File uploads to OpenAI
- ✅ Server starts on port 8000
- ✅ Frontend connects to backend

## **Stop Services:**
- Backend: `Ctrl+C` in Terminal 1
- Frontend: `Ctrl+C` in Terminal 2

## **Troubleshooting:**
- If port 8000 is in use: `lsof -ti:8000 | xargs kill -9`
- If port 5173 is in use: `lsof -ti:5173 | xargs kill -9`
- Check backend status: `curl http://localhost:8000/status` 