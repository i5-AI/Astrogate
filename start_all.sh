#!/bin/bash

echo "🚀 Starting Astrogate Air Force Chatbot..."

# Start backend in background
./start_backend.sh &
BACKEND_PID=$!

# Wait for backend to initialize
echo "⏳ Waiting for backend to initialize..."
sleep 10

# Check if backend is ready
if curl -s http://localhost:8000/status > /dev/null; then
    echo "✅ Backend is ready!"
    
    # Start frontend
    echo "🚀 Starting frontend..."
    ./start_frontend.sh
else
    echo "❌ Backend failed to start. Please check the logs."
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi 