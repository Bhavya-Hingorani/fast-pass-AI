from flask import Flask, request
import os
import detectAPI as detect

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No file selected', 400
    
    if allowed_file(file.filename):
        # Save the file to disk, database, or cloud storage
        file.save(os.path.join('toBeRead', file.filename))
        return detect.inferModel('toBeRead/' + file.filename), 200
    else:
        return 'File type not allowed', 400
    
def allowed_file(filename):
    # Add your own file type checking logic here
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi', 'mov', 'mkv'}

if __name__ == '__main__':
    app.run(debug=True)
