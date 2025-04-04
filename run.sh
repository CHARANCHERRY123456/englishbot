#!/bin/bash
# Script to run the FastAPI application

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Run the application
echo "Running application..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000

