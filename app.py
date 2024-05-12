from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from Analyst import read_data_from_file, count_glyphs, find_repeated_glyphs, find_all_repeated_patterns, \
    count_glyphs_in_uni, find_same_glyph_sets, output_to_excel, glyph_combinations_analysis

UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
ALLOWED_EXTENSIONS = {'txt', 'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return jsonify({"success": "File uploaded successfully", "filename": file.filename}), 200
    else:
        return jsonify({"error": "File is not allowed"}), 400


@app.route('/analyze/<function_name>', methods=['POST'])
def analyze(function_name):
    filename = request.json.get('filename')
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    results_file = os.path.join(DOWNLOAD_FOLDER, filename.rsplit('.', 1)[0] + '_results.xlsx')
    glyph_data = read_data_from_file(file_path)

    # Вызываем нужную функцию
    if function_name == 'count_glyphs':
        analysis_result = count_glyphs(glyph_data)
    elif function_name == 'find_repeated_glyphs':
        analysis_result = find_repeated_glyphs(glyph_data)
    elif function_name == 'find_all_repeated_patterns':
        analysis_result = find_all_repeated_patterns(glyph_data)
    elif function_name == 'count_glyphs_in_uni':
        analysis_result = count_glyphs_in_uni(glyph_data)
    elif function_name == 'find_same_glyph_sets':
        analysis_result = find_same_glyph_sets(glyph_data)
    elif function_name == 'glyph_combinations_analysis':
        analysis_result = glyph_combinations_analysis(glyph_data)
    else:
        return jsonify({"error": "Function does not exist"}), 404

    output_to_excel(analysis_result, results_file)

    return jsonify({"success": "Analysis complete", "results_file": results_file})


@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)


@app.route('/favicon.ico')
def favicon():
    return '', 204


if __name__ == "__main__":
    app.run(debug=True)