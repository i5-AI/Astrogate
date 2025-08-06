# 🚀 Astrogate Quick Start Guide

## **Automated Startup Options:**

### **Option 1: Start Everything at Once**
```bash
./start_all.sh
```
This will start both backend and frontend automatically.

### **Option 2: Start Backend Only**
```bash
./start_backend.sh
```
This starts just the backend server.

### **Option 3: Start Frontend Only**
```bash
./start_frontend.sh
```
This starts just the frontend (requires backend to be running).

## **Manual Commands (if needed):**

### **Backend:**
```bash
cd server
source chatbot/bin/activate
python3 app.py
```

### **Frontend:**
```bash
cd client
npm run dev
```

## **Access Points:**
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000

## **Troubleshooting:**
- If ports are in use, the scripts will automatically kill existing processes
- Check `server/app.log` for backend errors
- Backend status: `curl http://localhost:8000/status`

## **Stop All Services:**
```bash
lsof -ti:8000 | xargs kill -9  # Stop backend
lsof -ti:5173 | xargs kill -9  # Stop frontend
``` 