from flask import Flask, send_from_directory, abort
import os

app = Flask(__name__)

# Specify the directory to serve files from
CDN_DIRECTORY = 'static'  # Change this to your desired directory

def safe_join(directory, path):
    # Join the directory and the requested path
    final_path = os.path.join(directory, path)
    
    # Ensure the final path is within the directory
    if os.path.commonprefix([final_path, directory]) == directory:
        return final_path
    return None
@app.route("/")
def route():
    return "Quantum is working!"
@app.route('/<path:filename>')
def serve_file(filename):
    try:
        # Safely join the directory and filename
        file_path = safe_join(CDN_DIRECTORY, filename)

        # Check if the file path is valid and the file exists
        if file_path is None or not os.path.isfile(file_path):
            abort(404)  # File not found

        # Serve the file from the specified directory
        return send_from_directory(CDN_DIRECTORY, filename)
    except Exception as e:
        # Handle exceptions (e.g., file not found, security issues)
        abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
