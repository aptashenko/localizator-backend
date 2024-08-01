import zipfile
import json
import re
def is_zip(file):
    return file.filename.endswith('.zip') or file.content_type == 'application/zip'

def is_json(file):
    return file.filename.endswith('.json') or file.content_type == 'application/json'

def count_symbols(array):
    combined_text = ' '.join(array)
    cleaned_text = re.sub(r'\{[^}]*\}', '', combined_text)
    letter_count = sum(c.isalpha() for c in cleaned_text)

    return letter_count

def print_strings(items, texts):
    if isinstance(items, str):
        texts.append(items)
    elif isinstance(items, dict):
        for sub_item in items.values():
            print_strings(sub_item, texts)
    elif isinstance(items, list):
        for sub_item in items:
            print_strings(sub_item, texts)


def process_zip(file_path):
    all_files = []
    symbols_length = 0

    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            if file_info.filename.startswith('__MACOSX') or file_info.filename.startswith('.'):
                continue

            if file_info.filename.endswith('index.json'):
                try:
                    with zip_ref.open(file_info.filename) as json_file:
                        data = json_file.read().decode('utf-8')
                        file_name_parts = file_info.filename.split('/')
                        index = file_name_parts.index('index.json') if 'index.json' in file_name_parts else -1
                        content = json.loads(data)
                        obj = {
                            'name': file_name_parts[index - 1],
                            'content': content
                        }
                        all_texts = []
                        print_strings(content, all_texts)
                        obj['texts'] = all_texts
                        all_files.append(obj)
                        symbols_length += count_symbols(all_texts)

                except (UnicodeDecodeError, json.JSONDecodeError) as e:
                    print(f"Ошибка при обработке файла {file_info.filename}: {e}")

    return {'files': all_files, 'count': symbols_length}
