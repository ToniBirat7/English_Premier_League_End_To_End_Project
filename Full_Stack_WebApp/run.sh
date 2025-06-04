#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Python is installed
if ! command_exists python3; then
    echo "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if Node.js is installed
if ! command_exists node; then
    echo "Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is installed
if ! command_exists npm; then
    echo "npm is not installed. Please install npm first."
    exit 1
fi

# Start Backend
echo "Starting Backend..."
cd Backend_WebApp

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing backend requirements..."
pip install -r requirements.txt

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Start Django server
echo "Starting Django server..."
python manage.py runserver 8000 &
DJANGO_PID=$!

# Start Frontend
echo "Starting Frontend..."
cd ../Frontend_WebApp

# Install dependencies
echo "Installing frontend dependencies..."
npm install

# Start Next.js development server
echo "Starting Next.js server..."
npm run dev &
NEXT_PID=$!

# Function to handle script termination
cleanup() {
    echo "Shutting down servers..."
    kill $DJANGO_PID
    kill $NEXT_PID
    exit 0
}

# Set up trap for cleanup
trap cleanup SIGINT SIGTERM

# Wait for both processes
wait $DJANGO_PID $NEXT_PID 