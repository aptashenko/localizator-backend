import re
import json
from app import create_app
from app.services import process_zip, is_zip, is_json, count_symbols, print_strings
from app.openai_client import openai_client
from flask import request, Response, jsonify

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
                all_texts = []
                symbols = 0
                data = json.loads(file_content)
                print_strings(data, all_texts)
                symbols = count_symbols(all_texts)
                return Response(json.dumps({'data': {'files': data, 'count': symbols}}), status=200, mimetype='application/json')
            except json.JSONDecodeError:
                return Response(json.dumps({'error': 'Invalid JSON format'}), status=400, mimetype='application/json')

        if is_zip(file):
            data = process_zip(file)
            return Response(json.dumps({'data': data}), status=200, mimetype='application/json')

    except Exception as e:
        return Response(f'Error: {str(e)}', status=500)

@app.route('/translate', methods=['POST'])
def translate():
    user_text = request.json.get('user_text')
    target_language = request.json.get('target_language')
    
    # user_text validation
    if not user_text: 
        return Response('Error: Missing user_text', status=400)
        
    if len(user_text) > 12000:
        return Response('Error: text field is too large', status=400)
        
    try:
        json.dumps(user_text)
    except (TypeError, json.JSONDecodeError):
        return Response('Error: user_text is not a valid JSON string', status=400)

    # target_language validation
    if not isinstance(target_language, str) or not target_language.strip():
        return Response('Error: Invalid or missing target_language', status=400)

    # if validation passed
    try:
        response = openai_client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = [
                {
                    "role": "system",
                    "content": f"You are a professional translator tasked with translating website content for use in a Vue.js i18n library. Translate only JSON values text into {target_language}, maintaining the style, format, and meaning. DO NOT translate JSON keys, variables, or any HTML code. DO NOT format the response as Markdown Provide only the translated JSON WITH UNCHANGED STRUCTURE, without any extra explanations."
                },
                {
                    "role": "user", 
                    "content": json.dumps(user_text)
                }
            ]
        )
        translated_json = response.choices[0].message.content

        return Response(json.dumps(translated_json), status=200, mimetype='application/json')
    except Exception as e:
        return Response(f'Error: {str(e)}', status=500)


if __name__ == '__main__':
    app.run(port=5002)
