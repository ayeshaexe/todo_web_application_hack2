#!/usr/bin/env python3
"""
Script to start the Todo API server
"""
import uvicorn
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("Starting Todo API server...")
    print("Server will be available at: http://0.0.0.0:8000")
    print("Health check: http://0.0.0.0:8000/health")
    print("API docs: http://0.0.0.0:8000/docs")
    print("Press Ctrl+C to stop the server")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()