from flask import Flask, send_from_directory, abort, render_template_string
import os

app = Flask(__name__)

# Specify the directory to serve files from
CDN_DIRECTORY = 'static'  # Change this to your desired directory

def safe_join(directory, path):
    # Join the directory and the requested path
    final_path = os.path.join(directory, path)
    
    # Ensure the final path is within the directory
    if os.path.commonprefix([os.path.realpath(final_path), os.path.realpath(directory)]) == os.path.realpath(directory):
        return final_path
    return None

@app.route('/', defaults={'filename': ''})
@app.route('/<path:filename>')
def serve_file(filename):
    try:
        # Safely join the directory and filename
        file_path = safe_join(CDN_DIRECTORY, filename)

        # If the file path is invalid, return 404
        if file_path is None:
            abort(404)  # File not found

        # If the path is a directory, list the directory contents
        if os.path.isdir(file_path):
            files = os.listdir(file_path)
            files_list = '<br>'.join([f'<a href="/{filename}/{file}">{file}</a>' for file in files])
            return render_template_string('<h1>{{ directory }}</h1><p>{{ files_list | safe }}</p>', directory=file_path, files_list=files_list)
        
        # If the file path is a valid file, serve the file
        if os.path.isfile(file_path):
            return send_from_directory(CDN_DIRECTORY, filename)

        # If none of the above conditions are met, return 404
        abort(404)
    except Exception as e:
        # Handle exceptions (e.g., file not found, security issues)
        abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
