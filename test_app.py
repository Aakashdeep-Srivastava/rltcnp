#!/usr/bin/env python3
"""
Script to test the Flask application locally before deploying to Vercel.
"""

import os
import sys
import requests
import time
import subprocess
import webbrowser
from threading import Timer

def open_browser():
    """Open the browser after a short delay."""
    webbrowser.open('http://localhost:5000')

def main():
    """Main function to test the Flask application."""
    print("Testing the Flask application locally...")
    
    # Start the Flask application in a subprocess
    process = subprocess.Popen([sys.executable, 'app.py'])
    
    # Open the browser after a short delay
    Timer(2, open_browser).start()
    
    try:
        # Wait for user to press Ctrl+C
        print("Press Ctrl+C to stop the application...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Stop the Flask application
        process.terminate()
        print("\nApplication stopped.")

if __name__ == "__main__":
    main() 