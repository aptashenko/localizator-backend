import os
import json
from app import create_app
from app.services import process_zip, is_zip, is_json
from flask import request, Response
app = create_app()

@app.route('/')
def index():
    return 'HELLO'

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return Response('No file part', status=400)

        file = request.files['file']

        if file.filename == '':
            return Response('No selected file', status=400)

        if not (is_zip(file) or is_json(file)):
            return Response(json.dumps({'error': 'Unsupported file type'}), status=400, mimetype='application/json')

        file_content = file.read()

        if is_json(file):
            try:
                data = json.loads(file_content)
                return Response(json.dumps({'data': data}), status=200, mimetype='application/json')
            except json.JSONDecodeError:
                return Response(json.dumps({'error': 'Invalid JSON format'}), status=400, mimetype='application/json')

        if is_zip(file):
            data = process_zip(file)
            return Response(json.dumps({'data': data}), status=200, mimetype='application/json')

    except Exception as e:
        return Response(f'Error: {str(e)}', status=500)


if __name__ == '__main__':
    app.run(port=5002)


