from flask import Flask, request, jsonify, abort, send_file
from functools import wraps
import os

app = Flask(__name__)

# Directory to store uploaded files
UPLOAD_FOLDER = './https_server/mem'
DOWNLOAD_FOLDER = './https_server/mem/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

USERNAME = "admin"
PASSWORD = "password"

def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

# Decorator to require authentication
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return None
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    return 'File Upload Server'

# Endpoint to handle file uploads
@app.route('/upload', methods=['POST'])
@requires_auth
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    try:
        # Save the uploaded file to the local directory
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        return jsonify({'message': f'File {file.filename} uploaded successfully!'}), 200
    
    except Exception as e:
        return jsonify({'message': f'Failed to upload file: {str(e)}'}), 500


@app.route('/download/<filename>', methods=['GET'])
@requires_auth
def download_file(filename):
    try:
        # Check if the file exists
        file_path =os.path.join(DOWNLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file("../https_server/mem/"+filename, as_attachment=True)
        else:
            abort(404, description=f"File {filename} not found")
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True, port=5000)
