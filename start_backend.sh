#!/bin/bash

# Navigate to the server directory
cd "$(dirname "$0")/server"

# Activate virtual environment
source chatbot/bin/activate

# Kill any existing processes on port 8000
lsof -ti:8000 | xargs kill -9 2>/dev/null || true

# Start the backend server
echo "🚀 Starting Astrogate Backend..."
nohup python3 app.py > app.log 2>&1 &

# Wait a moment for startup
sleep 5

# Check if it's running
if curl -s http://localhost:8000/status > /dev/null; then
    echo "✅ Backend is running on http://localhost:8000"
else
    echo "❌ Backend failed to start. Check app.log for details."
fi 