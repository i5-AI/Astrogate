#!/bin/bash

# Navigate to the client directory
cd "$(dirname "$0")/client"

# Kill any existing processes on port 5173
lsof -ti:5173 | xargs kill -9 2>/dev/null || true

# Start the frontend server
echo "🚀 Starting Astrogate Frontend..."
npm run dev 