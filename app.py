import os
import threading
import time
from flask import Flask, render_template, request, jsonify, send_from_directory, after_this_request
from openpyxl.workbook import Workbook
from Analyst import (read_data_from_file, count_glyphs, find_repeated_glyphs, find_all_repeated_patterns,
                     count_glyphs_in_uni, find_same_glyph_sets, output_to_excel, glyph_combinations_analysis,
                     convert_data_in_file)
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'csv'}

base_path = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(base_path, UPLOAD_FOLDER)
app.config['DOWNLOAD_FOLDER'] = os.path.join(base_path, DOWNLOAD_FOLDER)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "Нет части файла"}), 400
    file = request.files['file']
    if file and allowed_file(file.filename):
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({"success": True, "filename": filename}), 200
    else:
        return jsonify({"error": "Тип файла не допускается"}), 400

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    filename = data.get('filename')
    function_name = data.get('function_name')

    if not filename or not function_name:
        return jsonify({'error': 'Необходимые параметры отсутствуют'}), 400

    upload_dir = app.config['UPLOAD_FOLDER']
    download_dir = app.config['DOWNLOAD_FOLDER']

    safe_filename = secure_filename(filename)
    file_path = os.path.join(upload_dir, safe_filename)
    results_filename = safe_filename.rsplit('.', 1)[0] + '_results.xlsx'  # Имя итогового файла
    results_file_path = os.path.join(download_dir, results_filename)

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    if not os.path.exists(file_path):
        return jsonify({'error': 'Файл не найден'}), 404

        # Считываем данные для анализа
    glyph_data = read_data_from_file(file_path)

    analysis_functions = {
        'count_glyphs': count_glyphs,
        'find_repeated_glyphs': find_repeated_glyphs,
        'find_all_repeated_patterns': find_all_repeated_patterns,
        'count_glyphs_in_uni': count_glyphs_in_uni,
        'find_same_glyph_sets': find_same_glyph_sets,
        'glyph_combinations_analysis': glyph_combinations_analysis,
        # Добавьте другие функции анализа, если необходимо
    }

    if function_name in analysis_functions:
        analysis_result = analysis_functions[function_name](glyph_data)
        if not os.path.exists(results_file_path):
            wb = Workbook()
            wb.save(results_file_path)
        output_to_excel({function_name: analysis_result}, results_file_path)

        return jsonify(
            {"success": True, "message": f"Анализ '{function_name}' завершен", "results_file": results_filename}
        )
    else:
        return jsonify({'error': 'Указанная функция анализа не существует'}), 404


@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    download_folder = app.config['DOWNLOAD_FOLDER']
    file_path = os.path.join(download_folder, filename)

    @after_this_request
    def remove_file(response):
        def attempt_delete(path, max_attempts=5, wait_seconds=1):
            """ Пытается удалить файл с несколькими попытками и задержками """
            for _ in range(max_attempts):
                try:
                    os.remove(path)
                    print(f"Файл {path} успешно удален.")
                    return
                except OSError as e:
                    print(f"Ошибка при удалении файла {path}: {e}")
                    time.sleep(wait_seconds)
            print(f"Не удалось удалить файл {path} после {max_attempts} попыток.")

        threading.Thread(target=attempt_delete, args=(file_path,)).start()
        return response

    try:
        return send_from_directory(download_folder, filename, as_attachment=True)
    except FileNotFoundError:
        print(f"Файл {filename} не найден в {download_folder}")  # Для отладки
        return jsonify({'error': 'Файл не найден'}), 404


@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({"error": "Нет части файла"}), 400
    file = request.files['file']
    if file and allowed_file(file.filename):
        # Сохраняем полученный файл в папке 'uploads'
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Вызываем функцию конвертации
        convert_data_in_file(file_path, app.config['DOWNLOAD_FOLDER'])

        # Файл сохранен в папке 'downloads' с тем же именем
        return jsonify({"success": True, "filename": filename}), 200
    else:
        return jsonify({"error": "Тип файла не допускается"}), 400


@app.route('/favicon.ico')
def favicon():
    return '', 204


if __name__ == "__main__":
    app.run(debug=True)