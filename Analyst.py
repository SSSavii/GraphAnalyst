import pandas as pd
import re
import os
from openpyxl import load_workbook
from openpyxl.workbook import Workbook

# Считываем данные из файла и сохраняем в словарь
def read_data_from_file(filename):
    glyph_data = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(': ')
            unicode = parts[0]
            glyphs = parts[1].split(',')
            glyph_data[unicode] = glyphs
    return glyph_data

# Функция для подсчёта графем
def count_glyphs(glyph_data):
    glyph_count = {}
    for glyphs in glyph_data.values():
        for glyph in glyphs:
            glyph_count[glyph] = glyph_count.get(glyph, 0) + 1
    result_list = [{"Графемы": k, "Кол-во": v} for k, v in glyph_count.items()]
    return result_list

# Функция для поиска символов с повторяющимися графемами
def find_repeated_glyphs(glyph_data):
    repeated_glyphs = []
    for unicode, glyphs in glyph_data.items():
        for glyph in set(glyphs):
            count = glyphs.count(glyph)
            if count > 1:
                repeated_glyphs.append({"Графема": glyph, "Unicode": unicode, "Кол-во": count})
    return repeated_glyphs

# Функция для поиска всех повторяющихся паттернов графем
def find_all_repeated_patterns(glyph_data):
    glyph_pairs = {}
    for unicode, glyphs in glyph_data.items():
        seen_pairs = set()
        for i in range(len(glyphs)):
            for j in range(i + 1, len(glyphs)):
                glyph_pair = tuple(sorted((glyphs[i], glyphs[j])))
                if glyph_pair not in seen_pairs:
                    seen_pairs.add(glyph_pair)
                    if glyph_pair in glyph_pairs:
                        glyph_pairs[glyph_pair].add(unicode)
                    else:
                        glyph_pairs[glyph_pair] = {unicode}
    repeated_patterns = [{"Пара": pair, "Unicodes": list(unicodes)} for pair, unicodes in glyph_pairs.items() if len(unicodes) > 1]
    return repeated_patterns

def count_glyphs_in_uni(glyph_data):
    count_dict = {}
    for glyphs in glyph_data.values():
        glyph_count = len(glyphs)
        count_dict[glyph_count] = count_dict.get(glyph_count, 0) + 1
    result_list = [{"Кол-во графем": k, "Кол-во иероглифов": v} for k, v in count_dict.items()]
    return result_list

def find_same_glyph_sets(glyph_data):
    same_glyph_sets = {}
    for unicode, glyphs in glyph_data.items():
        sorted_glyphs = tuple(sorted(glyphs))
        if sorted_glyphs in same_glyph_sets:
            same_glyph_sets[sorted_glyphs].append(unicode)
        else:
            same_glyph_sets[sorted_glyphs] = [unicode]
    result_list = [{"Набор графем": glyphs, "Unicodes": unicodes} for glyphs, unicodes in same_glyph_sets.items() if len(unicodes) >= 2]
    return result_list

# Новые названия листов
analysisFunctionNames = {
    'count_glyphs': 'Кол-во графем',
    'find_repeated_glyphs': 'Повторяющиеся графемы',
    'find_all_repeated_patterns': 'Часто используемые пары графем',
    'count_glyphs_in_uni': 'Длины иероглифов',
    'find_same_glyph_sets': 'Одинаковые наборы графем',
    'glyph_combinations_analysis': 'Анализ комбинаций графем'
}

# Функция для вывода в Excel с новыми названиями листов
def output_to_excel(data_dict, filename='output.xlsx'):
    try:
        with pd.ExcelWriter(filename, engine='openpyxl', mode='a' if os.path.exists(filename) else 'w') as writer:
            for func_name, data in data_dict.items():
                sheet_name = analysisFunctionNames.get(func_name, func_name)
                if not isinstance(data, pd.DataFrame):
                    data = pd.DataFrame(data)
                data.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"Data successfully saved to '{filename}'.")
    except Exception as e:
        print(f"An error occurred while writing to the file '{filename}': {e}")

# Функция для конвертации данных в файле
def convert_data_in_file(filename):
    converted_data = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip().lower()
            # Check if the line contains glyphs (Chinese, Japanese, Korean, etc.)
            if re.match(r'^[\u4e00-\u9fff]+$', line):
                # Convert glyphs to Unicode without 'U+' prefix and in lowercase
                unicode_line = ' '.join([f'{ord(glyph):04x}' for glyph in line])
                converted_data.append(unicode_line)
            # Check if the line contains Unicode representations without 'U+' prefix
            elif re.match(r'^([a-f0-9]{4,5}\s?)+$', line):
                # Convert Unicode to glyphs
                unicodes = line.split()
                glyphs_line = ''.join([chr(int(unicode_code, 16)) for unicode_code in unicodes])
                converted_data.append(glyphs_line)
            else:
                # If the format is not recognized, keep the original line
                converted_data.append(line)
    output_path = os.path.join('downloads', os.path.basename(filename))
    with open(output_path, 'w', encoding='utf-8') as output_file:
        for line in converted_data:
            output_file.write(line + '\n')

# Функция для анализа комбинаций графем
def glyph_combinations_analysis(glyph_data):
    glyph_combinations = {}

    # Собираем информацию о комбинациях графем
    for unicode, glyphs in glyph_data.items():
        for i, glyph in enumerate(glyphs):
            if glyph not in glyph_combinations:
                glyph_combinations[glyph] = {}
            for other_glyph in glyphs[:i] + glyphs[i+1:]:
                glyph_combinations[glyph][other_glyph] = glyph_combinations[glyph].get(other_glyph, 0) + 1

    # Подготавливаем данные для вывода в Excel
    data_for_excel = []
    for glyph, combinations in glyph_combinations.items():
        row = [glyph]
        combinations_str = ', '.join([f'{g}: {count}' for g, count in combinations.items()])
        row.append(combinations_str)
        data_for_excel.append(row)
    return data_for_excel

# Функция для запуска анализа с использованием конкретной функции анализа
def run_analysis(analysis_function):
    data_filename = "Data(моя).txt"
    excel_filename = 'output.xlsx'
    glyph_data = read_data_from_file(data_filename)
    result = analysis_function(glyph_data)
    output_to_excel({analysis_function.__name__: result}, excel_filename)