from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import csv
from datetime import datetime
import os
import sys
import signal
import subprocess
import time

# Add current directory to path so modules can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from modules import config_manager

app = Flask(__name__)
CORS(app)

# Global variable to track the bot process
bot_process = None

PATH = 'all excels/'
@app.route('/')
def home():
    """Displays the home page of the application."""
    return render_template('index.html')

@app.route('/applied-jobs', methods=['GET'])
def get_applied_jobs():
    '''
    Retrieves a list of applied jobs from the applications history CSV file.
    
    Returns a JSON response containing a list of jobs, each with details such as 
    Job ID, Title, Company, HR Name, HR Link, Job Link, External Job link, and Date Applied.
    
    If the CSV file is not found, returns a 404 error with a relevant message.
    If any other exception occurs, returns a 500 error with the exception message.
    '''

    try:
        jobs = []
        with open(PATH + 'all_applied_applications_history.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                jobs.append({
                    'Job_ID': row['Job ID'],
                    'Title': row['Title'],
                    'Company': row['Company'],
                    'HR_Name': row['HR Name'],
                    'HR_Link': row['HR Link'],
                    'Job_Link': row['Job Link'],
                    'External_Job_link': row['External Job link'],
                    'Date_Applied': row['Date Applied']
                })
        return jsonify(jobs)
    except FileNotFoundError:
        return jsonify({"error": "No applications history found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/applied-jobs/<job_id>', methods=['PUT'])
def update_applied_date(job_id):
    """
    Updates the 'Date Applied' field of a job in the applications history CSV file.

    Args:
        job_id (str): The Job ID of the job to be updated.

    Returns:
        A JSON response with a message indicating success or failure of the update
        operation. If the job is not found, returns a 404 error with a relevant
        message. If any other exception occurs, returns a 500 error with the
        exception message.
    """
    try:
        data = []
        csvPath = PATH + 'all_applied_applications_history.csv'
        
        if not os.path.exists(csvPath):
            return jsonify({"error": f"CSV file not found at {csvPath}"}), 404
            
        # Read current CSV content
        with open(csvPath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            fieldNames = reader.fieldnames
            found = False
            for row in reader:
                if row['Job ID'] == job_id:
                    row['Date Applied'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    found = True
                data.append(row)
        
        if not found:
            return jsonify({"error": f"Job ID {job_id} not found"}), 404

        with open(csvPath, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldNames)
            writer.writeheader()
            writer.writerows(data)
        
        return jsonify({"message": "Date Applied updated successfully"}), 200
    except Exception as e:
        print(f"Error updating applied date: {str(e)}")  # Debug log
        return jsonify({"error": str(e)}), 500

@app.route('/logs', methods=['GET'])
def get_logs():
    """Reads the last few lines of the log file and returns it."""
    try:
        log_path = 'logs/log.txt'
        if not os.path.exists(log_path):
            return "No logs found yet."
        
        with open(log_path, 'r', encoding='utf-8') as f:
            # Get last 100 lines for performance
            lines = f.readlines()
            return "".join(lines[-100:])
    except Exception as e:
        return f"Error reading logs: {str(e)}"

@app.route('/api/config', methods=['GET'])
def get_config():
    """Returns all configurations."""
    try:
        return jsonify(config_manager.get_all_configs())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/config', methods=['POST'])
def update_config():
    """Updates a specific configuration variable."""
    try:
        data = request.json
        filename = data.get('filename')  # e.g., 'search.py'
        key = data.get('key')
        value = data.get('value')
        
        if not all([filename, key, value is not None]):
            return jsonify({"error": "Missing filename, key, or value"}), 400
            
        success = config_manager.update_config_var(filename, key, value)
        if success:
            return jsonify({"message": "Configuration updated successfully."})
        else:
            return jsonify({"error": "Failed to update configuration."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/bot/status', methods=['GET'])
def get_bot_status():
    global bot_process
    if bot_process and bot_process.poll() is None:
        return jsonify({"status": "running", "pid": bot_process.pid})
    return jsonify({"status": "stopped"})

@app.route('/api/bot/start', methods=['POST'])
def start_bot():
    global bot_process
    if bot_process and bot_process.poll() is None:
        return jsonify({"error": "Bot is already running"}), 400
    
    try:
        # Start the bot using the venv python
        venv_python = os.path.join(os.getcwd(), "venv", "bin", "python3")
        if not os.path.exists(venv_python):
            venv_python = "python3"
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting bot with {venv_python} runAiBot.py...")
        
        # Add a separator to the log file
        with open("logs/log.txt", "a") as log_file:
            log_file.write(f"\n\n--- BOT STARTED AT {datetime.now()} ---\n\n")
            
        bot_process = subprocess.Popen(
            [venv_python, "runAiBot.py"],
            stdout=open("logs/log.txt", "a"),
            stderr=subprocess.STDOUT,
            preexec_fn=os.setsid # Create a process group to kill it cleanly
        )
        return jsonify({"message": "Bot started successfully", "pid": bot_process.pid})
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Error starting bot: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/bot/stop', methods=['POST'])
def stop_bot():
    global bot_process
    if not bot_process or bot_process.poll() is not None:
        return jsonify({"error": "Bot is not running"}), 400
    
    try:
        # Kill the entire process group
        os.killpg(os.getpgid(bot_process.pid), signal.SIGTERM)
        bot_process = None
        return jsonify({"message": "Bot stopped successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

##<