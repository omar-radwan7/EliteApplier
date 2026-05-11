#!/bin/bash
# Script to launch the EliteApplier AI Dashboard as a small menu bar app (Chrome App mode)

# Ensure the Flask app is running in the background if it isn't already
if ! curl -s http://127.0.0.1:5000 > /dev/null; then
    echo "Starting Dashboard Backend..."
    source venv/bin/activate
    python3 app.py &
    sleep 2
fi

# Try to open it using google-chrome in app mode with a specific window size
if command -v google-chrome &> /dev/null; then
    google-chrome --app="http://127.0.0.1:5000" --window-size=450,800
elif command -v google-chrome-stable &> /dev/null; then
    google-chrome-stable --app="http://127.0.0.1:5000" --window-size=450,800
elif command -v chromium &> /dev/null; then
    chromium --app="http://127.0.0.1:5000" --window-size=450,800
else
    # Fallback if Chrome isn't found
    xdg-open "http://127.0.0.1:5000"
fi
