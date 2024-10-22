from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import pandas as pd
from phone_processing import process_excel_file

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload and processed folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        file.save(file_path)
        output_path = process_excel_file(file_path)  # Process the uploaded Excel file

        # Extract the processed file name to return
        processed_filename = os.path.basename(output_path)
        
        return jsonify({'message': 'File processed successfully', 'file': processed_filename}), 200
    except Exception as e:
        print(f"Error processing file: {e}")  # Log the error to the console
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(PROCESSED_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        print(f"File not found at path: {file_path}") 
        return jsonify({'error': 'File not found'}), 404


@app.route('/preview/<filename>', methods=['GET'])
def preview_file(filename):
    file_path = os.path.join(PROCESSED_FOLDER, filename)
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        return df.head().to_json(orient='records')
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)


# The Excel file does not contain a 'Phone_Number' column.